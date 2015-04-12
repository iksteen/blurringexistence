Title: nginx and StartSSL
Date: 2010-07-21 21:45
Author: nospam@example.com (Ingmar Steen)
Tags: nginx
Slug: nginx-and-startssl

If you get a (free) SSL certificate and key
from [StartSSL](http://www.startssl.com) it might not be obvious how to
install use them properly in nginx. nginx doesn't automatically chain
certificates like f.e. Apache does so you'll have to do that yourself.

First, use the StartSSL website to create an
SSL key and certificate and transfer them to your
server. Then execute the following steps (if you use a class 2
certificate replace class1 by class2 in the instructions below):

-   Decrypt the private key using the password you entered when you
    created your key:

    `openssl rsa -in ssl.key -out /etc/nginx/conf/ssl.key`


-   Protect your key from prying eyes:

    `chmod 600 /etc/nginx/conf/ssl.key`

-   Fetch StartSSL's root CA and class 1 intermediate server CA
    certificates:

    `wget http://www.startssl.com/certs/ca.pem`

    `wget http://www.startssl.com/certs/sub.class1.server.ca.pem`

-   Create a unified certificate from your certificate and the CA
    certificates:

    `cat ssl.crt sub.class1.server.ca.pem ca.pem > /etc/nginx/conf/ssl-unified.crt`

-   Configure your nginx server to use the new key and certificate (in
    the global settings or a `server` section):

    `ssl on;`

    `ssl_certificate /etc/nginx/conf/ssl-unified.crt;`

    `ssl_certificate_key /etc/nginx/conf/ssl.key;`

-   Tell nginx to reload its configuration:

    `killall -HUP nginx`

And you're done!
