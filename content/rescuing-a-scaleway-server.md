Title: Rescuing a Scaleway server
Date: 2017-05-27 17:55
Tags: technical
Slug: rescuing-a-scaleway-server

I recently ran across a problem where one of the Scaleway servers I rent no longer booted because it could not mount `/dev/nbd1` after a reboot:

[![Give root password for maintenance]({thumbnail:192x}scaleway/giveroot.png)]({image}scaleway/giveroot.png)

The canonical solution to problems like these in the age of the cloud is to delete the machine and to provision a new one. But, as this particular server wasn't provisioned automatically, I wanted to save its configuration and data. Unfortunately though, I never set a root password so I could not use the console to log in.

To get the machine to boot again, I decided to use Scaleway's rescue boot image. However, this was not as trivial as I thought it would be. Here is the process I went through:

I first noted the boot script the server was currently used it and then changed it to the rescue variant (the actual name might change over time):

[![Selected rescue image]({thumbnail:192x}scaleway/rescue.png)]({image}scaleway/rescue.png)

I then rebooted the server using the Off button at the top of the settings screen and choosing the Hard Reboot option. After the server has booted, I was greeted by a login prompt:

[![Rescue image booting]({thumbnail:192x}scaleway/login.png)]({image}scaleway/login.png)

I was now able to use ssh to connect to the rescue console (*51.1.1.1* being the fictional public IP address of my server):

```text
macbook:~ user$ ssh -o StrictHostKeyChecking=no root@51.1.1.1
root@scw01:~# mount /dev/nbd0 /mnt
mount: /dev/nbd0: can't read superblock
```

This was not what I expected. The reason I got this error is because the rescue image doesn't boot with the network block devices attached.

It appeared that the required `nbd-client` tool wasn't installed, so I installed it myself using *apt-get*:

```text
root@scw01:~# nbd-client
-bash: nbd-client: command not found
root@scw01:~# apt-get update
...
Fetched 15.5 MB in 10s (1,482 kB/s)
Reading package lists... Done
root@scw01:~# apt-get install nbd-client
...
```

Going back to the server settings page, I noted the IP address and port of the `nbd0` volume:

[![Volumes / network block devices]({thumbnail:192x}scaleway/volumes.png)]({image}scaleway/volumes.png)

I now had everything I needed to attach and mount the image myself:

```text
root@scw01:~# nbd-client 10.6.1.1 4100 /dev/nbd0
root@scw01:~# mount /dev/nbd0 /mnt
root@scw01:~# ls /mnt
bin  boot  dev  etc  home  initrd.img  lib  lib64  lost+found  media
mnt  proc  root  run  sbin  srv  sys  tmp  usr  var  vmlinuz
```

Success! I could finally fix whatever was broken to get my server booting again. Not really relevant to this item, but I more or less had to do [this](https://github.com/scaleway/image-archlinux/issues/31).

When I was finished, I changed the boot script back to what it was. I then unmounted and detached the network block device and rebooted the machine and all was well again:

```text
root@scw01:~# umount /mnt
root@scw01:~# nbd-client -d /dev/nbd0
disconnect, sock, done
root@scw01:~# reboot
```

Conclusion: The rescue image is a viable method to recover an instance (or its data). And while I can understand that Scaleway doesn't automatically attach the network block devices in rescue mode, it would have been nice if they included `nbd-client` on the rescue image and documented the procedure.
