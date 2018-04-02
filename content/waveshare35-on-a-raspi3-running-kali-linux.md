Title: Waveshare 3.5" RPi LCD on a Raspberry Pi 3 running Kali Linux
Date: 2017-05-07 21:53
Status: draft
Tags: technical
Slug: waveshare35-on-a-raspi3-running-kali-linux

So, you've ordered a Waveshare 3.5inch RPi LCD and connected it to your Raspberry Pi 3. With much anticipation you boot your Pi and ... nothing.

The backlight's on, the screen is completely white and no matter how hard you press the resistive touchscreen, it doesn't seem to do anything. Spoiler: The shield requires drivers to work properly. The supplier I bought my (knock off) Waveshare from recommends to use [this](http://www.spotpear.com/download/diver24-5/LCD-show-160823-touch.tar.gz) driver pack to get things working (extract it and run the `LCD35-show script`). And they did for me, once, on raspbian, until I updated it and it hasn't worked since then.

Now, I want use my Raspberry Pi for my work as an (offensive) security consultant so I prefer Kali over raspbian for my Pi. Let's see if we can get this display working on Kali! I'll write this in a journalling fashion instead of a step-by-step list of instructions so that if your environment doesn't match mine exactly, you can hopefully use the comments to find your own way.

### Chapter 1: Getting the framebuffer working

After some googling, I stumble upon [this fbtft issue on GitHub](https://github.com/notro/fbtft/issues/215). It contains some hints about how to get the framebuffer working without the Waveshare driver package:

    sudo modprobe flexfb width=320 height=480 regwidth=16 init=-1,0xb0,0x0,-1,0x11,-2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
    sudo modprobe fbtft_device debug=3 rotate=90 name=flexfb speed=16000000 gpios=reset:25,dc:24

So, I log in using SSH and run the commands:

    root@kali:~# modprobe flexfb width=320 height=480 regwidth=16 init=-1,0xb0,0x0,-1,0x11,-2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
    root@kali:~# modprobe fbtft_device debug=3 rotate=90 name=flexfb speed=16000000 gpios=reset:25,dc:24
    modprobe: ERROR: could not insert 'fbtft_device': Invalid argument

Not what I hoped for or expected. Check `dmesg` to see what happened:

```
[  179.918848] fbtft: module is from the staging directory, the quality is unknown, you have been warned.
[  179.933076] flexfb: module is from the staging directory, the quality is unknown, you have been warned.
[  240.091998] fbtft_device: module is from the staging directory, the quality is unknown, you have been warned.
[  240.104791] bcm2708_fb soc:fb: soc:fb id=-1 pdata? no
[  240.117178] fbtft_device: spi_busnum_to_master(0) returned NULL
[  240.128607] fbtft_device: failed to register SPI device
```

By default, Kali Linux doesn't enable the SPI device by default. Let's enable it and reboot:

    root@kali:~# mount /boot
    root@kali:~# echo dtparam=spi=on >> /boot/config.txt
    root@kali:~# reboot

After the Pi is booted, let's try again:

    root@kali:~# modprobe flexfb width=320  height=480  regwidth=16 init=-1,0xb0,0x0,-1,0x11,-2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
    root@kali:~# modprobe fbtft_device debug=3 rotate=90 name=flexfb speed=16000000 gpios=reset:25,dc:24

Success! No error message and the display turns black instead of white. Let's check `dmesg` again:

```
[   28.152788] fbtft: module is from the staging directory, the quality is unknown, you have been warned.
[   28.157026] flexfb: module is from the staging directory, the quality is unknown, you have been warned.
[   33.526594] fbtft_device: module is from the staging directory, the quality is unknown, you have been warned.
[   33.527837] spidev spi0.0: spidev spi0.0 500kHz 8 bits mode=0x00
[   33.527857] spidev spi0.1: spidev spi0.1 500kHz 8 bits mode=0x00
[   33.527896] bcm2708_fb soc:fb: soc:fb id=-1 pdata? no
[   33.527934] spidev spi0.0: Deleting spi0.0
[   33.529311] flexfb spi0.0: fbtft_request_gpios: 'reset' = GPIO25
[   33.529367] flexfb spi0.0: fbtft_request_gpios: 'dc' = GPIO24
[   33.529387] flexfb spi0.0: flexfb_verify_gpios_dc()
[   33.529404] flexfb spi0.0: fbtft_reset()
[   33.649472] flexfb spi0.0: init: write(0xB0) 0x00
[   33.649571] flexfb spi0.0: init: write(0x11)
[   33.649600] flexfb spi0.0: init: mdelay(250)
[   33.899657] flexfb spi0.0: init: write(0x3A) 0x55
[   33.899739] flexfb spi0.0: init: write(0xC2) 0x44
[   33.899787] flexfb spi0.0: init: write(0xC5) 0x00 0x00 0x00 0x00
[   33.899852] flexfb spi0.0: init: write(0xE0) 0x0F 0x1F 0x1C 0x0C 0x0F 0x08 0x48 0x98 0x37 0x0A 0x13 0x04 0x11 0x0D 0x00
[   33.899938] flexfb spi0.0: init: write(0xE1) 0x0F 0x32 0x2E 0x0B 0x0D 0x05 0x47 0x75 0x37 0x06 0x10 0x03 0x24 0x20 0x00
[   33.900023] flexfb spi0.0: init: write(0xE2) 0x0F 0x32 0x2E 0x0B 0x0D 0x05 0x47 0x75 0x37 0x06 0x10 0x03 0x24 0x20 0x00
[   33.900093] flexfb spi0.0: init: write(0x36) 0x28
[   33.900134] flexfb spi0.0: init: write(0x11)
[   33.900162] flexfb spi0.0: init: write(0x29)
[   34.161664] flexfb spi0.0: Display update: 1146 kB/s, fps=0
[   34.161687] flexfb spi0.0: fbtft_register_backlight(): led pin not set, exiting.
[   34.162120] graphics fb1: flexfb frame buffer, 480x320, 300 KiB video memory, 4 KiB DMA buffer memory, fps=20, spi0.0 at 16 MHz
[   34.162194] fbtft_device: GPIOS used by 'flexfb':
[   34.162205] fbtft_device: 'reset' = GPIO25
[   34.162215] fbtft_device: 'dc' = GPIO24
[   34.162232] spidev spi0.1: spidev spi0.1 500kHz 8 bits mode=0x00
[   34.162247] flexfb spi0.0: flexfb spi0.0 16000kHz 8 bits mode=0x00
```

Great, looks good. Now let's see if we can get a console working on the newly created framebuffer device /dev/fb1. We'll need the `con2fbmap` utility from the `fbset` package. Let's install that, map console 1 to the TFT screen and activate that console:

```
root@kali:~# apt install fbset
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  fbset
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 122 kB of archives.
After this operation, 236 kB of additional disk space will be used.
Get:1 http://ftp2.nluug.nl/os/Linux/distr/kali kali-rolling/main armhf fbset armhf 2.1-29 [122 kB]
Fetched 122 kB in 0s (229 kB/s)
Selecting previously unselected package fbset.
(Reading database ... 127134 files and directories currently installed.)
Preparing to unpack .../fbset_2.1-29_armhf.deb ...
Unpacking fbset (2.1-29) ...
Processing triggers for man-db (2.7.6.1-2) ...
Setting up fbset (2.1-29) ...
root@kali:~# con2fbmap 1 1
root@kali:~# chvt 1
```

You should now be able to see the final bits of the boot messages and a familiar login prompt on the screen.

### Making it permanent

Now let's make these changes permanent. Kali Linux is a modern linux variant that uses configuration files in `/etc/modprobe.d` to configure module options, blacklisting, etc. Configuration files in `/etc/modules-load.d` are used to auto-load modules.

Let's configure options for the `flexfb` and `fbtft_device` modules and configure them to load automatically:

```
root@kali:~# cat >/etc/modprobe.d/waveshare.conf <<EOF
options flexfb width=320 height=480 regwidth=16 init=-1,0xb0,0x0,-1,0x11,-2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
options fbtft_device debug=3 rotate=90 name=flexfb speed=16000000 gpios=reset:25,dc:24
EOF

root@kali:~# cat >/etc/modules-load.d/waveshare.conf <<EOF
flexfb
fbtft_device
EOF
```

Let's reboot and see if the modules load properly. They didn't for me.

```text
root@kali:~# dmesg
...
[    3.043378] fbtft_device: spi_busnum_to_master(0) returned NULL
[    3.043380] fbtft_device: failed to register SPI device
...
root@kali:~# lsmod
Module                  Size  Used by
ipt_MASQUERADE          1363  1
nf_nat_masquerade_ipv4     3123  1 ipt_MASQUERADE
iptable_nat             2320  1
nf_conntrack_ipv4       8890  1
nf_defrag_ipv4          1824  1 nf_conntrack_ipv4
nf_nat_ipv4             6071  1 iptable_nat
nf_nat                 18854  2 nf_nat_masquerade_ipv4,nf_nat_ipv4
nf_conntrack          104800  4 nf_conntrack_ipv4,nf_nat_masquerade_ipv4,nf_nat_ipv4,nf_nat
evdev                  12423  2
brcmfmac              222720  0
brcmutil                9092  1 brcmfmac
cfg80211              543027  1 brcmfmac
spidev                  7373  0
rfkill                 20851  3 cfg80211
bcm2835_gpiomem         3940  0
spi_bcm2835             7596  0
uio_pdrv_genirq         3923  0
uio                    10204  1 uio_pdrv_genirq
fixed                   3285  0
flexfb                 14308  0
fbtft                  34966  1 flexfb
syscopyarea             3225  1 fbtft
sysfillrect             3826  1 fbtft
sysimgblt               2480  1 fbtft
fb_sys_fops             1741  1 fbtft
ip_tables              13161  1 iptable_nat
x_tables               20578  2 ip_tables,ipt_MASQUERADE
ipv6                  406279  36
```

What happens is that the `fbtft_device` driver is loaded before the SPI driver (`spi_bcm2835`) is loaded. We can prevent that from happening by adding a _softdep_ to the modprobe config file and reboot once more:

```
root@kali:~# echo "softdep fbtft_device pre: spi_bcm2835" >> /etc/modprobe.d/waveshare.conf
root@kali:~# reboot
```

And the screen turns black after reboot.

A black screen is nice, but we can do more. Let's redirect the console to the `fb1` device at boot time. We do this by changing the kernel commandline by adding the `fbcon=map:1` option. Make sure to adjust the commandline to the existing content of your `/boot/cmdline.txt` file.

```
root@kali:~# mount /boot
root@kali:~# cat >/boot/cmdline.txt <<EOF
dwc_otg.fiq_fix_enable=2 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait rootflags=noload net.ifnames=0 fbcon=map:1
EOF
root@kali:~# reboot
```

You'll see the boot messages scrolling and finally the screen turns black with a blinking cursor. The screen blanks because the display manager is started which runs on the VT7 console which is backed by the `fb0` device which drives the HDMI output. If you connect using SSH and run `chvt 1` again, you'll get see the login prompt.

### X11

By default, when _xorg_ starts, it will use the `fbdev` driver which defaults to using the device on `/dev/fb0`. We can change this by creating a config file to override the default and restarting the display manager:

```
root@kali:~# cat >/usr/share/X11/xorg.conf.d/99-fbdev.conf <<EOF
Section "Device"
  Identifier "waveshare"
  Driver "fbdev"
  Option "fbdev" "/dev/fb1"
EndSection
EOF
root@kali:~# systemctl restart display-manager
```

You should now be greeted by the login manager. If you have a USB keyboard and mouse connected, you can even log in. Let's enable auto-login for the root user (it's Kali linux.. all the good bits require root).

```
root@kali:~# sed -i '/^#autologin-user=/c\autologin-user=root' /etc/lightdm/lightdm.conf
root@kali:~# sed -i '/^#autologin-user-timeout=/c\autologin-user-timeout=0' /etc/lightdm/lightdm.conf
```

Almost there. However, by default `pam` will deny the root user to auto login using lightdm. Let's change that as well:

```
root@kali:~# sed -i '/^auth \+required pam_succeed_if.so user != root quiet_success/d' /etc/pam.d/lightdm-autologin
```

### Touchscreen

- enable ads overlay
- outdated xinput information
- axis mirroring

### Performance tuning

```
fbtft dma
flexfb speed=320000000
```

### TL;DR

```
mount /boot

echo dtparam=spi=on >> /boot/config.txt

cat >/boot/cmdline.txt <<EOF
dwc_otg.fiq_fix_enable=2 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait rootflags=noload net.ifnames=0 fbcon=map:1
EOF

cat >/etc/modprobe.d/waveshare.conf <<EOF
options flexfb width=320 height=480 regwidth=16 init=-1,0xb0,0x0,-1,0x11,-2,250,-1,0x3A,0x55,-1,0xC2,0x44,-1,0xC5,0x00,0x00,0x00,0x00,-1,0xE0,0x0F,0x1F,0x1C,0x0C,0x0F,0x08,0x48,0x98,0x37,0x0A,0x13,0x04,0x11,0x0D,0x00,-1,0xE1,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0xE2,0x0F,0x32,0x2E,0x0B,0x0D,0x05,0x47,0x75,0x37,0x06,0x10,0x03,0x24,0x20,0x00,-1,0x36,0x28,-1,0x11,-1,0x29,-3
options fbtft dma
options fbtft_device debug=3 rotate=90 name=flexfb speed=32000000 gpios=reset:25,dc:24
softdep fbtft_device pre: spi_bcm2835
EOF

cat >/etc/modules-load.d/waveshare.conf <<EOF
flexfb
fbtft_device
EOF

cat >/usr/share/X11/xorg.conf.d/99-fbdev.conf <<EOF
Section "Device"
  Identifier "waveshare"
  Driver "fbdev"
  Option "fbdev" "/dev/fb1"
EndSection
EOF

sed -i '/^#autologin-user=/c\autologin-user=root' /etc/lightdm/lightdm.conf
sed -i '/^#autologin-user-timeout=/c\autologin-user-timeout=0' /etc/lightdm/lightdm.conf
sed -i '/^auth \+required pam_succeed_if.so user != root quiet_success/d' /etc/pam.d/lightdm-autologin

reboot
```
