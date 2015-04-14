Title: Samsung X125 linux kernel module
Date: 2011-02-10 19:29
Author: Ingmar Steen
Tags: linux, samsung x125

After installing Arch Linux on my new Samsung X125 laptop I noticed that
there were quite a few knobs I couldn't turn when using just the drivers
that come with the linux kernel. Most notably, I couldn't toggle the
'hardware' wireless kill switch (it's actually just a BIOS setting, but
disabling Wifi this way does seem
to conserve some of the power the little battery holds) or change the
performance mode (aka 'silent mode').

I did however stumble upon the
[easy-slow-down-manager](http://code.google.com/p/easy-slow-down-manager/)
driver. It's not part of the kernel and doesn't use the regular
facilities for controlling the wifi kill switch ('rfkill') but instead
uses some /proc entries.

Seeing how similar it was to the samsung-laptop platform driver already
available in the linux kernel I decided to adapt that to suit my
purposes. It wasn't that hard really. I contacted Greg Kroah-Hartman
(maintainer of the samsung-laptop driver) and asked him what I needed to
do to get the X125 support merged into the kernel. He told me that if I
was able to extend the existing driver to support the other BIOS flavor,
he'd merge it.

So I did just that. The code has trickled upwards to linux-next and
should be part of 2.6.39.
[[link]](http://git.kernel.org/?p=linux/kernel/git/next/linux-next.git;a=history;f=drivers/staging/samsung-laptop/samsung-laptop.c;h=51ec6216b1ea46b3a93801fb04595b60c5fa12f2;hb=HEAD)

The driver currently implements the following functionality:

-   rfkill using the native linux rfkill infrastructure.
-   backlight control (brightness and power toggle) using the native
    linux backlight infrastructure.
-   retrieve/change the performance level ('silent', 'normal' or
    'overclock') through a knob in
    /sys/devices/platform/samsung/performance\_level.

I'll see if I can also implement the manipulating the maximum charge
level of the battery, the 'Chargeable USB' functionality and maybe even
Samsung's fastboot functionality.

It was great fun to do some kernel hacking again :-)

It's been quite a while (I once implemented  ISA-PNP for the OPL3SA2
and gamepad drivers, that never got merged though).

Now, the beauty is that this kernel module will not only work for my
Samsung X125, but also for various other Samsung netbooks like the
Samsung NC-10, NP-Q45, X360, R518, N150, N210, N220, R530, R730, NF110,
NF120, NF130 and quite possibly others. If the driver can't match your
Samsung laptop, you can use the force=1 module parameter ('modprobe
samsung-laptop force=1') to skip the DMI check
and probe the BIOS directly. Don't forget to
contact Greg if it does work so he can add the hardware IDs to the
driver.
