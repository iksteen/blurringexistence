Title: Serendipity and nginx
Date: 2010-07-21 09:34
Author: Ingmar Steen
Tags: meta, nginx, serendipity

I use nginx as my primary webserver for applications hosted on
TheGraveyard.org, mainly because it's simple to configure and use,
lightweight and fast (or maybe because I just don't trust server
applications that just work ;-) ). Most applications are pretty easy
to install once you get the hang of
it, but for future reference I'll share how I got serendipity working
using nginx.

I created a user 'blurringexistence\_net' on the webserver as whom the
PHP scripts will run and set up
[Servitor](http://projects.thegraveyard.org/projects/show/servitor) to
spawn an fcgi'd version of php:

*/etc/servitor/services/fastcgi-php-blurringexistence.net*:  

    #! /bin/sh
    exec /usr/bin/spawn-fcgi -n -u blurringexistence_net -g blurringexistence_net -d /srv/http/vhosts/blurringexistence_net/public_html -s /srv/http/fastcgi/blurringexistence_net-php.sock -M 0600 -U http -G http -- /usr/bin/php-cgi -c /srv/http/vhosts/blurringexistence_net/etc/php

To tune php to serendipity's needs, I copied `/etc/php/php.ini` to
`/srv/http/vhosts/blurringexistence_net/etc/php/php.ini` (see the `-c`
parameter for the `php-cgi` command in the Servitor launch script),
changed ownership to `blurringexistence_net:blurringexistence_net` and
changed the `post_max_size` and `upload_max_filesize` options to `32M`.
Also made sure `open_basedir` contains the directory where the
ImageMagick binaries are installed. Next, I created a database user and
database on the PostgreSQL server for serendipity to use.

Here's the nginx configuration I use for which also facilitates
serendipity's pretty urls (adapted from serendipity's .htaccess file)
and SSL on port 444:

    server {    
        listen       80;    
        listen       444 default ssl;    
        server_name  blurringexistence.net www.blurringexistence.net;    
        ssl_certificate      /etc/nginx/certs/blurringexistence.net.crt;    
        ssl_certificate_key  /etc/nginx/certs/blurringexistence.net.key;    
        ssl_session_timeout  5m;    
        ssl_protocols        SSLv3 TLSv1;    
        ssl_ciphers          HIGH:!ADH:!MD5;    
        ssl_prefer_server_ciphers   on;    
        error_page   404 = /index.php;    
        error_page   500 502 503 504  /50x.html;    
        client_max_body_size 32m;    
        rewrite      ^/serendipity_admin.php$ serendipity_admin.php last;    
        rewrite      ^/((archives/([0-9]+)\-[0-9a-z\.\_!\;,\+\-\%]+\.html)/?)$ index.php?/$1 last;    
        rewrite      ^/(authors/([0-9]+)\-[0-9a-z\.\_!\;,\+\-\%]+)$ index.php?/$1 last;    
        rewrite      ^/(feeds/categories/([0-9\;]+)\-[0-9a-z\.\_!\;,\+\-\%]+\.rss)$ index.php?/$1 last;    
        rewrite      ^/(feeds/authors/([0-9]+)\-[0-9a-z\.\_!\;,\+\-\%]+\.rss)$ index.php?/$1 last;    
        rewrite      ^/(categories/([0-9\;]+)\-[0-9a-z\.\_!\;,\+\-\%]+)$ index.php?/$1 last;    
        rewrite      ^/archives([/A-Za-z0-9]+)\.html$ index.php?url=/archives/$1.html last;    
        rewrite      ^/([0-9]+)\-][0-9a-z\-]*\.html$ index.php?url=$1-article.html last;    
        rewrite      ^/feeds/(.*)$ index.php?url=/feeds/$1 last;    
        rewrite      ^/unsubscribe/(.*)/([0-9]+)$ index.php?url=/unsubscribe/$1/$2 last;    
        rewrite      ^/approve/(.)/(.)/([0-9]+)$ index.php?url=approve/$1/$2/$3 last;    
        rewrite      ^/delete/(.)/(.)/([0-9]+)$ index.php?url=delete/$1/$2/$3 last;    
        rewrite      ^/(admin|entries)(/.+)?$ index.php?url=admin/ last;    
        rewrite      ^/archive/? index.php?url=/archive last;    
        rewrite      ^/(index|atom[0-9]*|rss|b2rss|b2rdf).(rss|rdf|rss2|xml)$ rss.php?file=$1&ext=$2;    
        rewrite      ^/(plugin|plugin)/(.*)$ index.php?url=$1/$2 last;    
        rewrite      ^/search/(.*)$ index.php?url=/search/$1 last;    
        rewrite      ^/comments/(.*)$ index.php?url=/comments/$1 last;    
        rewrite      ^/(serendipity\.css|serendipity_admin\.css)$ index.php?url=/$1 last;    
        rewrite      ^/index\.(html?|php.+)$ index.php?url=index.html last;    
        rewrite      ^/htmlarea/(.*)$ htmlarea/$1 last;    
        rewrite      ^/(.*\.html?)$ index.php?url=/$1 last;    
        location = /50x.html {        
            root   html;    
        }    
        location / {        
            root   /srv/http/vhosts/blurringexistence_net/public_html;        
            index  index.php;    
        }
        location ~ \.php$ {        
            root           /srv/http/vhosts/blurringexistence_net/public_html;        
            fastcgi_connect_timeout 60;        
            fastcgi_send_timeout 180;        
            fastcgi_read_timeout 180;        
            fastcgi_buffer_size 128k;        
            fastcgi_buffers 4 256k;        
            fastcgi_busy_buffers_size 256k;        
            fastcgi_temp_file_write_size 256k;        
            fastcgi_intercept_errors on;        
            fastcgi_pass   unix:/srv/http/fastcgi/blurringexistence_net-php.sock;        
            fastcgi_index  index.php;        
            fastcgi_param  SCRIPT_FILENAME  /srv/http/vhosts/blurringexistence_net/public_html$fastcgi_script_name;        
            set $https off;        
            if ($scheme = https) {            
                set $https on;        
            }        
            fastcgi_param  HTTPS  $https;        
            include        fastcgi_params;    
        }    
        location ~ /\.ht {        
            deny  all;    
        }    
        location ~ (\.tpl\.php|\.tpl|\.sql|\.inc\.php|\.db)$ {        
            deny   all;    
        }
    }

After that I installed serendipity without much trouble.

Suggestions and comments are welcome! Just leave a comment.

**Note:** This currently uses a home-brewn solution to run PHP scripts through
FastCGI based on lighttpd's spawn-fcgi. Sometime soon I'll hopefully get
around to changing that to use [PHP-FPM](http://php-fpm.org/).
