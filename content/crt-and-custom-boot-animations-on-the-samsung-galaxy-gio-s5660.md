Title: CRT and custom boot animations on the Samsung Galaxy Gio S5660
Date: 2011-08-07 13:53
Author: Ingmar Steen
Tags: samsung gio

### Disclaimer:

_Following this procedure may result in your phone not starting up or
working properly any more. Usually, you can recover it using ODIN. I
cannot be held responsible for what happens to your device. By following
these instructions, you agree to take full responsibility._

### Introduction

Here's what I did to enable the infamous Gingerbread CRT and custom
boot animations on my Samsung Galaxy Gio S5660. This procedure is based
on various hints and posts by other people on various forums.

These instructions are based on a rooted S5660XXKQ6 rom (Android 2.3.4),
it should work on any rooted Android 2.3.3 rom for the Gio though.

-   You can download the S5660XXKQ6 rom over at
    [SamFirmware](http://www.samfirmware.com) (free registration
    required), follow the instructions on how to use ODIN to flash the rom.
-   To root this rom (or any stock Gingerbread rom for the Samsung Gio),
    follow these instruction on the [XDA developers
    forum](http://forum.xda-developers.com/showthread.php?t=1111414).

### Requirements

1.  I use the EStrongs File Explorer in root explorer mode with / and
    /system mounted as read-write (check the ES File Explorer settings).
    If you prefer using Root Explorer or adb, feel free to do so.
2.  Install Samsung KIES so you have the necessary drivers to access your
    phone's SD card when you connect it.
3.  Get yourself a decent archiver like 7-zip, jZip or PowerArchiver.
4.  Download and unpack
    [apktool](http://code.google.com/p/android-apktool/). You;ll need
    `apktool-install-windows-r04-brut1.tar.bz2` and
    `apktool1.4.1.tar.bz2` (latest version while writing this guide,
    newer versions should also work), extract both of them to a new
    directory. Note that apktool depends on the Java Runtime
    Environment.
5.  A 320x480 `bootanimation.zip` file on your SD card. You can find a
    couple of them
    [here](http://forum.xda-developers.com/showthread.php?t=905538)
    (these were made by Dysgenic).

### CRT animation

This is the hardest part of this guide, I’ll try to describe it as
clearly as I can. Also, these instructions are based on using a Windows
7 host.

1.  Start ES File Explorer and navigate to `/system`, locate the
    `build.prop` file and open it in the ES File Explorer editor.
2.  Remove the line that reads `debug.sf.hw=1`.
3.  Save and close.
4.  Use ES File Explorer to copy `/system/framework/framework-res.apk`
    to your SD card.
5.  Connect your phone to your PC and enable <span
    class="caps">USB</span> storage.
6.  Copy the `framework-res.apk` file from the SD card to the folder
    where you extracted apktool.
7.  Open a command prompts (`cmd.exe`) and change to the directory where
    you extracted apktool using the `cd` command.
8.  Extract `framework-res.apk`: `apktool d framework-res.apk`
9.  Open the file `framework-res/res/values/bools.xml` in your favorite
    text editor and change the line
    `<bool name="config_animateScreenLights">true</bool>` to
    `<bool name="config_animateScreenLights">false</bool>`.
10. Go back to the command prompt and rebuild the apk file:
    `apktool b framework-res framework-res-crt.apk`.
11. Now open both `framework-res.apk` and `framework-res-crt.apk` in
    your archiver and copy `resources.arsc` from the newly created apk
    file to the original apk file. **Make sure the file doesn't get
    compressed (use the 'Store' compression method)!**
12. Copy the `framework-res.apk` file back to your SD card.
13. Safely remove the SD card from Windows and disable USB storage on
    your phone.
14. Use ES File Explorer to copy `framework-res.apk` from the SD card
    back to the `/system/framework` folder.
15. Reboot your phone. You'll notice the boot animation disappeared and
    is now a completely white screen which is where part 2 of this guide
    comes in.

### Custom boot animation

1.  Start ES File Explorer and navigate to `/system/bin`.
2.  Delete or rename `samsungani`.
3.  Rename `bootanimation` to `samsungani`.
4.  Copy the 320×480 `bootanimation.zip` from your SD card to
    `/system/media`.
5.  Reboot your phone. You should now see your new boot animation.

### Questions and comments

If you have any questions or comments feel free to leave a comment
below.
