Title: Introducing Pelicide
Date: 2015-04-28 22:37
Tags: pelicide, pelican, python
Slug: introducing-pelicide

Recently, I've been working on a new project. It's called Pelicide and it's an IDE for sites built with the [Pelican Static Site Generator](http://getpelican.com). It consists of a web service which is written in python and uses the twisted framework which serves the main web interface, an RPC service and the built site. The RPC service spawns a small runner (optionally using a different python interpreter than the one used to run pelicide) which is basically a wrapper around Pelican.

The user interface is written in javascript using the [w2ui](http://w2ui.com) JavaScript UI library and it uses a quite a few other libraries: requirejs, the es6-promise polyfill and jQuery + some plugins.

Anyway, I suck at introductions so I've prepared an [**interactive demo**](http://blurringexistence.net/pelicide-demo) of the user interface. It's not fully functional but you should be able to get an idea of what Pelicide attempts to provide.

Pelicide has not been officially released yet but feel free to take a look at the source code. It's over on [GitHub](https://github.com/iksteen/pelicide).

Also, here's a screenshot of the user interface (click on it for a larger version):

[![Pelicide demo screenshot]({thumbnail:384x@100}pelicide/pelicide-demo.png)]({image}pelicide/pelicide-demo.png)
