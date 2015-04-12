Title: A new layout
Date: 2015-04-14 22:30
Author: Ingmar Steen
Tags: meta, webdesign
Slug: a-new-layout

As you might have noticed, the layout of blurringexistence.net has changed quite a bit. I also switched out s9y for
Pelican which generates static html instead of having to host a server side dynamic CMS. I really don't like doing
maintenance on CMS systems (a couple of my websites went black after CMSMadeSimple decided to drop Postgres support, it
never "just works"). As an added bonus, there's no server side scripting so there's nothing to exploit.

In the process of switching to Pelican, I've created a plug-in to easily create albums from groups of images and to
generate thumbnails on the fly: [pelican-albums](https://github.com/iksteen/pelican-albums/).

I've also created a set of scripts to easily deploy multiple Pelican sites on a single server based on GitHub
webhooks. It automatically creates a virtual environment for each site, installs the requirements and builds the site
according to the publishing configuration. I'll document this in a later post, it's pretty nifty for multi-user Pelican
installs: Each user can just push to the GitHub repository and the changes will be automatically published.

The way the new layout works was heavily inspired by a remake I did for the website of
[Certified Edible Dinosaurs](http://ced.pwned.systems/). It's a responsive design where the sidebar collapses based on
CSS media queries. A small jQuery based javascript then allows you to unfold and fold the sidebar. The way the sidebar
expands differs whether the screen is in portrait or landscape mode.

Speaking of sidebars, since the site now pre-generated, things like a twitter stream need to be implemented using
javascript. I've chosen [jQuery Lifestream](http://christianv.github.io/jquery-lifestream/) because it provides a very
simple API, requires no server-side components and is easily themeable.

Now... With all this marvellous technology in place, all I need is something to write about.