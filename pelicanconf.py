#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ingmar Steen'
SITENAME = u'Blurring Existence'
SITESUBTITLE = u'Things are getting weirder at the speed of light...'
SITEURL = ''
TIMEZONE = 'Europe/Amsterdam'
DEFAULT_LANG = u'en'

STATIC_PATHS = [u'images', u'downloads']

RELATIVE_URLS = True
PATH = 'content'
FILENAME_METADATA = '(?P<slug>.*)'
THEME = 'themes/blurry'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican_albums', 'summary', 'tag_cloud']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
            'linenums': False,
        },
        'markdown.extensions.extra': {},
    },
}

DEFAULT_PAGINATION = 10
TYPOGRIFY = True
THUMBNAIL_OUTPUT_FORMAT = 'PNG'
THUMBNAIL_DEFAULT_SIZE = '192x192'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (
    (
        'Projects:',
        (
            ('automatron', 'https://github.com/automatron'),
            ('aws-request-signer', 'https://github.com/iksteen/aws-request-signer'),
            ('component-injector', 'https://github.com/iksteen/component-injector'),
            ('pelican-albums', 'https://github.com/iksteen/pelican-albums'),
            ('pelicide', 'https://github.com/iksteen/pelicide'),
            ('pwnypack', 'https://github.com/edibledinos/pwnypack'),
        ),
    ),
    (
        'Other sites:',
        (
            ('<span class="fa fa-twitter"></span> Twitter', 'http://twitter.com/iksteen/'),
            ('<span class="fa fa-github"></span> GitHub', 'http://github.com/iksteen/'),
            ('<span class="fa fa-linkedin"></span> LinkedIn', 'http://nl.linkedin.com/in/iksteen'),
            ('<span class="fa fa-play-circle-o"></span> Certified Edible Dinosaurs', 'http://ced.pwned.systems'),
        ),
    ),
)
