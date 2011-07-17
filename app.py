import cherrypy
import urllib
import urllib2
import json
import oauth2 as oauth



class Root():


    # Our whole application is private: nobody can see anything of it unless he's authorized
    _cp_config = {'tools.authorize.on': True}


    def call_ws(self, query):
        request = urllib2.Request('http://apis.live.net/V4.1/cid-000000004C05390D/%s' % query)
        request.add_header('Accept', 'application/json')
        request.add_header('Content-type', 'application/json')
        request.add_header('Authorization', 'WRAP access_token=EwC4ARAnAAAUWkziSC7RbDJKS1VkhugDegv7L0eAAP0lu9B1bwj13NfZaKQC9BdbRLo9GVlXqu4+oviMdRnsZWtXjyjJIcvZnSC+wnbWC6FDg/sulnEVKGxmVnJ82Wp3LWPgmhWxKXXjzIowUWcNOsnjJw6ViFz+VhkGXTSqEhR70geSDLk+bUtF8QU7frnucGY0YBXa3Te7Q2azO6mHA2YAAAhql8T8oPTYSggBp3vPVZa68D1Q+CqwsKQXw1KNGtnFl/BQ4KvQW27aX5hgpABlAvXgjO9GakBWH617eUJsiKgflhBaNV59tE3CHzY622Hsp/jBWvbz6i7diDT7quMjbWP+iv/IroB7Qh+zbWyTkEBMwYFeiDLlJ8orIEBajHesRkqGjvgFJZ2LXpa+yHj5BJwFmFmbQdu14IaEWxF1+7tYtBCxNYC+wesRyUPIjzrLABAUgHyzJRG+CmKKGC2G4V3wzXQc3ab5R9TWUJGgVLSgty+36dEbgisu3Z7MEYOC9L/xOaIhYZRqdT153Jb6WpAHdTuQW/5q4TmzZpG/ECk3dQu4ERYI5ja2QyOVHytSGdvhAAA=')
        response = urllib2.urlopen(request)
        body = response.read()
        return json.loads(body)


    @cherrypy.expose
    def callback(self, code):
          print 'Got a call back code: %r' % code
          # We've got a code, we're ready to exchange it to a true access token
          params = {
              'client_id': '000000004C05390D',
              'redirect_uri': '%s/callback' % cherrypy.request.base,
              'client_secret': 'fiMIb91LhBu9T5LPk4hPd2QaqKXLTY4a',
              'code': code,
              'grant_type': 'authorization_code'
              }
          url = 'https://oauth.live.com/token'
          post_data = urllib.urlencode(params)
          request = urllib2.Request(url, post_data)
          response = urllib2.urlopen(request)
          body = response.read()
          creds = json.loads(body)
          print 'Access token exahnged to: %r' % creds
          # Save the current credentials to the session
          for (k, v) in creds.items():
              cherrypy.session[k] = v
          raise cherrypy.HTTPRedirect('/home')


    @cherrypy.expose
    @cherrypy.tools.mako(filename="login.mako")
    def login(self):
        return {}


    @cherrypy.expose
    @cherrypy.tools.mako(filename="home.mako")
    def home(self):
        return {}


