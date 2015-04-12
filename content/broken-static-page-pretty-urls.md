Title: Broken static page pretty urls
Date: 2011-04-22 08:27
Author: Ingmar Steen
Tags: meta, serendipity
Slug: broken-static-page-pretty-urls

Somehow the pretty URLs to static pages on this s9y install stopped
working (returning a 404) and I have no idea why.

It does work when I redirect the pretty URLs to the not-so-pretty URL,
but somehow it doesn't work if I let nginx rewrite it internally.

So I’m currently using this:  

    location / {
        index  index.php;
        rewrite ^(/pages/.*\.html)$ /index.php?$1 redirect;
        try_files $uri $uri/ /index.php?$uri;
    }

Could this be a bug in s9y's static page plugin where it doesn't parse
the passed URL correctly?
