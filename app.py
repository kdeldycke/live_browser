from db import DB
import cherrypy
import urllib
import urllib2
import json
import os
import httplib2
#httplib2.debuglevel = 1
from httplib2 import Http
from urllib import urlencode



class Root(DB):
    """ This class contain our main application views and logic.
        It also holds the authentication process (TODO: move this parts in its own auth.py file).
    """

    # Our whole application is private: nobody can see anything of it unless he's authorized
    _cp_config = {'tools.authorize.on': True}


    @cherrypy.expose
    def default(self):
        raise cherrypy.HTTPRedirect('/home')


    @cherrypy.expose
    def callback(self, code):
          """ See documentation and reference there:
                * http://msdn.microsoft.com/en-us/library/hh243649.aspx
                * http://msdn.microsoft.com/en-us/library/hh243647.aspx
          """
          cherrypy.log('Got a callback code: %r' % code, 'INFO')
          # We've got a code, we're ready to exchange it to a true access token
          params = {
              'client_id': self.APP_CID,
              'redirect_uri': '%s/callback' % cherrypy.request.base,
              'client_secret': self.APP_SECRET,
              'code': code,
              'grant_type': 'authorization_code'
              }
          url = 'https://oauth.live.com/token'
          post_data = urllib.urlencode(params)
          request = urllib2.Request(url, post_data)
          response = urllib2.urlopen(request)
          body = response.read()
          creds = json.loads(body)
          cherrypy.log('Callback code exchanged to: %r' % creds, 'INFO')
          # Save the current credentials to the session
          for (k, v) in creds.items():
              cherrypy.session[k] = v
          raise cherrypy.HTTPRedirect('/home')


    @cherrypy.expose
    @cherrypy.tools.mako(filename="login.mako")
    def login(self):
        # Force session expiration each time we are redirected to the login screen.
        self.expire_session()
        # Build up the URL for authentication on Windows Live
        # List of scopes is available at: http://msdn.microsoft.com/en-us/library/hh243646.aspx
        SCOPES = ['wl.signin', 'wl.basic', 'wl.birthday', 'wl.work_profile', 'wl.emails', 'wl.postal_addresses', 'wl.phone_numbers']
        callback_url = '%s/callback' % cherrypy.request.base
        auth_url = "https://oauth.live.com/authorize?client_id=%s&scope=%s&response_type=code&redirect_uri=%s" % (self.APP_CID, '%20'.join(SCOPES), callback_url)
        return { 'auth_url': auth_url
               }


    @cherrypy.expose
    def logout(self):
        self.expire_session()
        raise cherrypy.HTTPRedirect('/login')


    def expire_session(self):
        """ Helper method to expire the current session
        """
        try:
            cherrypy.session.delete()
        except KeyError:
            pass
        cherrypy.lib.sessions.expire()


    @cherrypy.expose
    def home(self):
        raise cherrypy.HTTPRedirect('/profile/me')


    @cherrypy.expose
    @cherrypy.tools.mako(filename="profile.mako")
    def profile(self, user_id='me'):
        template_var = {}
        me = self.get_data('/me')
        template_var.update({'me': me})
        if user_id == 'me':
            user_id = me.get('id')
        template_var.update({'profile_info': self.get_data('/%s' % user_id)})
        template_var.update({'contacts': self.get_data('/%s/contacts' % user_id)})
        return template_var

