#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ingmar Steen'
SITENAME = u'Blurring Existence'
SITESUBTITLE = u'Things are getting weirder at the speed of light...'
SITEURL = ''
THEME = 'themes/blurry'

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = u'en'

PLUGINS = ['pelican_albums']
ARTICLE_EXCLUDES = ['images']

MD_EXTENSIONS = [
    'codehilite(css_class=highlight, guess_lang=False, linenums=False)',
    'extra',
]

TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (
    (
        'Projects',
        (
            ('pwnypack', 'https://github.com/edibledinos/pwnypack'),
            ('pelican-albums', 'https://github.com/iksteen/pelican-albums'),
            ('automatron', 'https://github.com/automatron'),
        ),
    ),
    (
        '(Web)hosting providers',
        (
            ('BASIC Networks', 'http://basicnetworks.net/'),
            ('Network Solutions', 'http://www.networksolutions.com/'),
            ('Soleus', 'http://soleus.nu/'),
            ('TransIP', 'http://transip.nl/'),
        ),
    ),
    (
        'Software',
        (
            ('nginx', 'http://nginx.org/'),
            ('Pelican', 'http://blog.getpelican.com/'),
        ),
    ),
    (
        'More me',
        (
            ('Google+', 'http://gplus.to/iksteen'),
            ('LinkedIn', 'http://nl.linkedin.com/in/iksteen'),
            ('Twitter', 'http://twitter.com/iksteen/'),
            ('GitHub', 'http://github.com/iksteen/'),
            ('Certified Edible Dinosaurs', 'http://ced.pwned.systems'),
        ),
    ),
)

DEFAULT_PAGINATION = 10

RELATIVE_URLS = True

THUMBNAIL_DEFAULT_SIZE = '192x192'
