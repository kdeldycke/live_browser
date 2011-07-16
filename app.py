import cherrypy


class Root():

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return "Hello World !"

