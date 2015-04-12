Title: CSS3 fluff and clouds
Date: 2010-09-21 13:45
Author: Ingmar Steen
Tags: meta, photography, webdesign
Slug: css3-fluff-and-clouds
Thumbnail-Size: 128

Added some CSS3 fluff to pretty-up Blurring Existence, also changed the
horrible purple color scheme to blue. Works properly with Firefox 3.6
and Chrome. Internet Explorer 8 fails big time (no rgba color selector
for the transparent backgrounds), Internet Explorer 9 works a lot better
but seems to have a problem with the `background-size: cover` attribute:
a white bar appears on the right of the background image. CSS3 features
used: the `background-size` attribute to scale the background image and
`rgba` color selectors to make some panels semi-translucent.

<s>Now I just need to replace the header logo.</s> Ditched header logo
altogether.

I made the background picture when I was at Bospop 2010 (Weert, The
Netherlands) with Naomi. The aquarelle rainbow-like effect in the center
of that image was actually visible when looking at the sky while wearing
sunglasses. Which explains why the overall colors of the image are a bit
off and darkish: i was using my sunglasses as a filter for my camera.
It's actually part of a series of three pictures:

[![1]({thumbnail}clouds/dsc00230.jpg)]({image}clouds/dsc00230.jpg)
[![2]({thumbnail}clouds/dsc00231.jpg)]({image}clouds/dsc00231.jpg)
[![3]({thumbnail}clouds/dsc00232.jpg)]({image}clouds/dsc00232.jpg)

**Update**: I capitulated and switched to using PNGs with an alpha
channel as background images instead of using `rgba` color selectors.
