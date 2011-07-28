import cherrypy
import urllib
import urllib2
import json
import os
import pymongo
import httplib2
#httplib2.debuglevel = 1
from httplib2 import Http
from urllib import urlencode



class DB():
    """ This class contain all non-exposed internal database automation
    """

    # App ID and secret we got from the Windows Live Dev Center
    APP_CID = "000000004C05390D"
    APP_SECRET = "fiMIb91LhBu9T5LPk4hPd2QaqKXLTY4a"


    def get_db(self):
        DB_NAME = 'live_browser'
        connection = pymongo.Connection("localhost", 27017)
        if DB_NAME not in connection.database_names():
            cherrypy.log("There is no %r database in MongoDB." % DB_NAME, 'INFO')
        return connection[DB_NAME]

    db = property(get_db)


    def get_db_params_from_query(self, query):
        """ Transform the API request to parameters which will help us query our DB
        """
        # Map the query to our DB schema
        # Consider queries to be normalized here
        q_elements = query.split('/')[1:]
        # XXX Do not try to save for now query we haven't validated yet
        if len(q_elements) > 1 or q_elements[0] == 'me':
            cherrypy.log("Query schema had not been validated yet. Skip database persistency.", 'INFO')
            return None
        # Get the collection
        collection_name = 'user'
        # Get the query specification
        spec = {'id': q_elements[0]}
        return (collection_name, spec)


    def save_to_db(self, query, data):
        """ Save a request made to the Live API to the local persistent DB
        """
        cherrypy.log("Savin to the databaseg %r data associated with the %r query" % (query, data), 'INFO')
        db_params = self.get_db_params_from_query(query)
        if not db_params:
            return None
        (collection_name, spec) = db_params
        c = self.db[collection_name]
        doc = c.update(spec, data, upsert=True)
        return doc


    def get_data(self, query):
        """ This is the entry point for getting data, given a REST query.
            This method will then get data from the persisten DB layer or directly from the API.
        """
        # Normalize queries
        # TODO: Make this into a method if used elsewhere
        query = query.strip().lower()
        if not query.startswith('/'):
            query = '/%s' % query
        query = os.path.abspath(query)
        cherrypy.log('Data requested at: %s' % query, 'INFO')
        # Try to get data from the DB 
        data = self.get_data_from_db(query)
        # Else, get our data directly from the web service
        if not data:
            data = self.get_data_from_ws(query)
            # Save these data to the DB
            self.save_to_db(query, data)
        cherrypy.log('Data returned: %r' % data, 'INFO')
        return data


    def get_data_from_db(self, query):
        """ This method return data associated with the API query from the persistent DB layer.
        """
        # TODO: add an expiration data to the data we saved
        data = None
        db_params = self.get_db_params_from_query(query)
        if db_params:
            (collection_name, spec) = db_params
            c = self.db[collection_name]
            data = c.find_one(spec)
        return data



    def get_data_from_ws(self, query):
        """ This method perform a REST query to the Windows Live API.
        """
        API_URL = 'https://apis.live.net/v5.0'
        params = { 'access_token': cherrypy.session.get('access_token')
                 }
        headers = { 'Accept'         : 'application/json'
                  # Force identity else httplib2 default to deflate/gzip which raise the following exception with the python-httplib2 0.6.0-4 Debian Squeeze package:
                  #   error: Error -3 while decompressing data: incorrect header check
                  , 'Accept-Encoding': 'identity'
                  }
        query_url = full_url = '%s/%s' % (API_URL, query)
        cherrypy.log('Calling the web service at %s' % query_url, 'INFO')
        if params:
            full_url = '%s?%s' % (query_url, urlencode(params))
        h = Http()
        response, content = h.request(full_url, "GET", headers=headers)
        cherrypy.log('Web service returned: %r' % [response, content], 'INFO')
        data = json.loads(content)
        if type(data) is type({}):
            if 'data' in data:
                data = data['data']
#            elif 'error' in data:
#                # TODO: raise a proper exception ?
#                data = '%s - %s' % (data['error']['code'], data['error']['message'])
        return data

