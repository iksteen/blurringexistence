Title: PHP's max_post_size
Date: 2010-10-27 10:04
Author: Ingmar Steen
Tags: photography, zenphoto
Slug: phps-max_post_size

When trying to set up a Zenphoto gallery on blurringexistence.net I
needed to upload a rather large zip archive (1.4GB) containing quite a
few 6MP photo's to Zenphoto. Obviously, PHP
wasn't configured to accept such large POST
requests and rejected the request.

So I increased the `post_max_size` and `upload_max_filesize` to
something that suited the large file. Uploading the file seemed to work
now. Except that it didn't do anything with the file I uploaded which I
guessed was because the processing of the zip archive took too long and
was aborted.

After that however, the entire Zenphoto instance refused to work
properly. Maybe something broke while processing the file? Since the
Zenphoto instance was nearly empty anyway, I tried to reinstall it.
Which worked up to the point of entering the MySQL settings and
credentials. They just wouldn't stick and return a very non-descriptive
message (something along the lines of 'query error', I don't remember
the exact message). PHP still worked, the
serendipity instance still seemed to work. No strange errors or warnings
any of my log files.

After a bit of debugging, the reason everything broke was that the PHP
variable `$_POST` was always empty. I figured
that something that fundamental shouldn't break by itself so it was
probably something I did which led me to removing the `post_max_size`
and `upload_max_filesize` options and everything started working again.

There are several warnings in the PHP
documentation about `post_max_size`: If PHP is
compiled with `memory_limit` support, `memory_limit` should be larger
than `post_max_size` and the one I broke:

> <span class="caps">PHP</span> allows shortcuts for bit values,
> including K (kilo), M (mega) and G (giga). <span
> class="caps">PHP</span> will do the conversions automatically if you
> use any of these. Be careful not to exceed the 32 bit signed integer
> limit (if you're using 32bit versions) as it will cause your script to
> fail.

Another couple of hours wasted because I didn't RTFM :-/
