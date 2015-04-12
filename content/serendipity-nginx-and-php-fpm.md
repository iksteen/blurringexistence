Title: Serendipity, nginx and php-fpm
Date: 2010-07-27 07:37
Author: Ingmar Steen
Tags: meta, nginx, serendipity
Slug: serendipity-nginx-and-php-fpm

Arch Linux (the linux distribution I use) updated PHP to 5.3.3
yesterday and added the php-fpm package
so I decided to switch to using that instead of a hacked up spawn-fcgi
and my own process launcher (Servitor).

I didn't have to change anything in the nginx configuration file, but
here's the php-fpm configuration recipe:  

    [blurringexistence_net]
    listen = /srv/http/fastcgi/blurringexistence_net-php.sock
    listen.owner = http
    listen.group = http
    listen.mode = 0600
    user = blurringexistence_net
    group = blurringexistence_net
    pm = dynamic
    pm.max_children = 50
    pm.start_servers = 5
    pm.min_spare_servers = 2
    pm.max_spare_servers = 35
    pm.max_requests = 500
    chdir = /srv/http/vhosts/blurringexistence_net/public_html/
    php_flag[output_buffering] = off
    php_admin_value[open_basedir] = /srv/http/:/home/:/tmp/:/usr/share/pear/:/usr/bin/
    php_admin_value[post_max_size] = 32M
    php_admin_value[upload_max_filesize] = 32M

I also moved the php.ini changes into the php-fpm configuration file as
I found no way to tell php-fpm to load a different php.ini file for a
specific instance but that's a probably a good thing as it decreases
maintenance efforts when the ini file changes after an update of php.

Now all that’s left is setting up php-fpm's chroot feature and / or
getting rid of /usr/bin/ in open\_basedir.
