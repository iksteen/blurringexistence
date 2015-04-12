Title: Sound on Samsung X125 using Linux
Date: 2011-11-01 21:09
Author: Ingmar Steen
Tags: linux, samsung x125
Slug: sound-on-samsung-x125-using-linux

Finally got around to fixing sound on my Samsung X125 when using Linux.
Text-book basics apparently, add the following to
`/etc/modprobe.d/alsa.conf` (or create that if it doesn't exist):

    options snd-hda-intel model=laptop

And don't forget to set the volume of the 'Speaker' channel.
