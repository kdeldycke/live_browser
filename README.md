Live Browser
============

Live Browser is a web application which let you browse data provided by
Microsoft Live Messenger Connect API.

It is based on CherryPy and Mako.

This was tested on Kubuntu 11.04.


Test Accounts
-------------

Here is a list of account created for tests. I'm sure they violates Microsoft's
TOS but I need some real meat to play with the APIi.

Windows Live accounts:

<table>
  <tr>
    <th>Mail / Login</th>
    <th>Password</th>
  </tr>
  <tr>
    <td><code>rwzwiybgu3hibsr@jetable.org</code></td>
    <td><code>4ddc9a0df</code></td>
  </tr>
  <tr>
    <td><code>sg6abk6c3yqprfj@jetable.org</code></td>
    <td><code>9850a6dbf</code></td>
  </tr>
  <tr>
    <td><code>jz08gxgvffqrtfk@jetable.org</code></td>
    <td><code>253bb129e</code></td>
  </tr>
</table>

All these `@jetable.org` mails above are redirections to my true
`kevin@deldycke.com` mail address. They'll expire in a month from now.

If you need more fake accounts, then go to: https://signup.live.com


Windows Live API
----------------

I created an authorization token via the `rwzwiybgu3hibsr@jetable.org` account.
Here are the details:

  * Application name : `Live Browser`
  * Client ID        : `000000004C05390D`
  * Client secret    : `fiMIb91LhBu9T5LPk4hPd2QaqKXLTY4a`

To get new tokens, go to: https://manage.dev.live.com


Installation
------------

1. Install system dependencies using your favorite package manager. Here is the
   example for an Ubuntu machine:

        $ apt-get install python python-httplib2 python-pyopenssl mongodb-server

1. Initialize the buildout environment:

        $ python ./bootstrap.py --distribute

1. Run buildout itself:

        $ ./bin/buildout

1. Launch the app:

        $ ./bin/live_browser


TODO
----

  * Upgrade HTML5 Boilerplate to v2.0
  * Replace the "Awesome Button" by a Call-to-Action button (source:
  http://pixify.com/blog/increase-conversions-with-call-to-action-buttons/ )
  * Use Jquery UI transitions to fade and morph pages of the paginated list of
  properties available on each profile.
  * Add a simple profile search form based on email addresses.
  * Enhance the search form to let us add details criterion (age, name,
  employer, ...).
  * Add a crawler to automaticcaly get and save info we can get from an entered
  mail address.
  * Feed the crawler with something like
  http://www.tux-planet.fr/lulzsec-devoile-62-000-mots-de-passe/
  * When saving to MongoDB the data coming from the contact API, update the
  inverse reference of all contacts. Better yet: use MongoDB internal reference
  type to point to another contact (but I'm not sure I can point a reference to
  an object of the same collection).
  * The v4.1 Live API seems to offer a lots more informations about the contact
  list of each user. Use it to fetch the social graph.
  * Save the social network in a Neo4j database
  * Use Bulbflow: http://bulbflow.com
  * Draw the social network with the NetworkX library (see:
  http://networkx.lanl.gov/ )
  * Add OpenStreetMap integration.


HTML5 Boilerplate
-----------------

The HTML5 Boilerplate code included was generated on
http://html5boilerplate.com with the following parameters:

  * Conditional classes: All IE classes
  * Mobile: Handheld stylesheet
  * Javascript: jQuery minified
  * HTML5 enabler: Modernizr
  * Server config: None
  * Google analytics: Analytics snippet


Embedded external projects
--------------------------

This tool uses external softwares, scripts, libraries and artworks:

        HTML5 Boilerplate
        Copyright (c) 2010-2011, HTML5 Boilerplate project & contributors
        Components distributed under several license (MIT, BSD, GPL and Public Domain).
        Source: http://html5boilerplate.com

        jQuery Pagination plugin
        Copyright 2010-2011, birke@d-scribe.de
        Released under the GNU GPL v2 license.
        Source: https://github.com/gbirke/jquery_pagination

        Blueprint CSS framework 1.0.1
        Copyright 2007 - 2010 blueprintcss.org
        Released under a custom public license.
        Source: https://github.com/joshuaclayton/blueprint-css

        Buildout's bootstrap.py
        Copyright (c) 2006, Zope Corporation and Contributors
        Distributed under the Zope Public License, version 2.1 (ZPL).
        Source: http://svn.zope.org/repos/main/zc.buildout/trunk/bootstrap/bootstrap.py

