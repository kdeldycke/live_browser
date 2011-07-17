import cherrypy
import urllib2
import json



class Root():


    @cherrypy.expose
    @cherrypy.tools.mako(filename="base.mako")
    def default(self, *args, **kwargs):
        return { 'content': repr(self.call_ws('Contacts/AllContacts'))
               }


    def call_ws(self, query):
        request = urllib2.Request('http://apis.live.net/V4.1/cid-000000004C05390D/%s' % query)
        request.add_header('Accept', 'application/json')
        request.add_header('Content-type', 'application/json')
        request.add_header('Authorization', 'WRAP access_token=EwC4ARAnAAAUWkziSC7RbDJKS1VkhugDegv7L0eAAP0lu9B1bwj13NfZaKQC9BdbRLo9GVlXqu4+oviMdRnsZWtXjyjJIcvZnSC+wnbWC6FDg/sulnEVKGxmVnJ82Wp3LWPgmhWxKXXjzIowUWcNOsnjJw6ViFz+VhkGXTSqEhR70geSDLk+bUtF8QU7frnucGY0YBXa3Te7Q2azO6mHA2YAAAhql8T8oPTYSggBp3vPVZa68D1Q+CqwsKQXw1KNGtnFl/BQ4KvQW27aX5hgpABlAvXgjO9GakBWH617eUJsiKgflhBaNV59tE3CHzY622Hsp/jBWvbz6i7diDT7quMjbWP+iv/IroB7Qh+zbWyTkEBMwYFeiDLlJ8orIEBajHesRkqGjvgFJZ2LXpa+yHj5BJwFmFmbQdu14IaEWxF1+7tYtBCxNYC+wesRyUPIjzrLABAUgHyzJRG+CmKKGC2G4V3wzXQc3ab5R9TWUJGgVLSgty+36dEbgisu3Z7MEYOC9L/xOaIhYZRqdT153Jb6WpAHdTuQW/5q4TmzZpG/ECk3dQu4ERYI5ja2QyOVHytSGdvhAAA=')
        response = urllib2.urlopen(request)
        body = response.read()
        return json.loads(body)


    @cherrypy.expose
    def get_token(self):
        params = {
            'redirect_uri': 'http://vps.deldycke.com:8081/callback',
            'response_type': 'code',
            'scope': 'SCOPES',
            'client_id': '4B26CC835745365D'
          }
        return "getting token...."


    @cherrypy.expose
    def callback(self, code):
        print 'Got a call back code: %r' % code
