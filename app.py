import cherrypy


class Root():

    @cherrypy.expose
    @cherrypy.tools.mako(filename="base.mako")
    def default(self, *args, **kwargs):
        return

