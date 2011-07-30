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
import re



class WSException(Exception):
    """ This kind of exception are raised by the web service
    """
    def __init__(self, data):
        Exception.__init__(self, data['error']['message'])
        self.message = data['error']['message']
        self.code = data['error']['code']



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


    def normalize_query(self, query):
        """ Normalize the query for easy and consistent parsing
        """
        query = query.strip().lower()
        if not query.startswith('/'):
            query = '/%s' % query
        # TODO: translate the 'me' element here
        return os.path.abspath(query)


    def get_data(self, query):
        """ This is the entry point for getting data, given a REST query.
            This method will then get data from the persisten DB layer or directly from the API.
        """
        query = self.normalize_query(query)
        cherrypy.log('Data requested at %r' % query, 'INFO')
        # Try to get data from the DB 
        data = self.execute_db_query(query)
        cherrypy.log('Request to DB returned: %r' % data, 'INFO')
        # Else, get our data directly from the web service
        if not data:
            cherrypy.log("No data found in DB, let's call the web service.", 'INFO')
            try:
                data = self.execute_ws_query(query)
                cherrypy.log('Request to the web service returned: %r' % data, 'INFO')
                # Save these data to the DB
                self.save_to_db(query, data)
            except WSException, err:
                return err
        return data


    def execute_ws_query(self, query):
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
        query_url = full_url = '%s%s' % (API_URL, query)
        cherrypy.log('Calling the web service at %r' % query_url, 'INFO')
        if params:
            full_url = '%s?%s' % (query_url, urlencode(params))
        h = Http()
        response, content = h.request(full_url, "GET", headers=headers)
        cherrypy.log('Web service returned: %r' % [response, content], 'INFO')
        data = json.loads(content)
        if type(data) is type({}):
            if 'data' in data:
                data = data['data']
            elif 'error' in data:
                raise WSException(data)
        return data


    def execute_db_query(self, query):
        """ This method return data associated with the API query from the persistent DB layer.
        """
        # TODO: add an expiration data to the data we saved
        executor_name = self.query_dispatcher(query)
        executor_func = getattr(self, executor_name)
        return executor_func(query) or None


    def save_to_db(self, query, data):
        """ Save a request made to the Live API to the local persistent DB
            XXX Should we merge with the method above ?
        """
        cherrypy.log("Update database with %r" % data, 'INFO')
        executor_name = self.query_dispatcher(query, data)
        executor_func = getattr(self, executor_name)
        return executor_func(query, data)


    def query_dispatcher(self, query, data=None):
        """ Dispatch the web service request to a method that can directly speak to our DB
        """
        # While writing the regxep below, you can consider queries to be normalized (no double nor trailing slashes, no blanks before and after the query string and all lowercase)
        mapping = { 'user': r'^/[a-zA-Z0-9]+$'
                  , 'contacts': r'^/[a-zA-Z0-9]+/contacts$'
                  }
        for (executor_name, pattern) in mapping.items():
            if re.match(pattern, query):
                executor_type = 'get'
                if data is not None:
                    executor_type = 'save'
                return '%s_%s' % (executor_type, executor_name)
        cherrypy.log("Query %r can't be mapped to the database schema." % query, 'INFO')
        return None


    def get_user(self, query):
        q_elements = query.split('/')[1:]
        if q_elements[0] == 'me':
            return None
        return self.db['user'].find_one({'id': q_elements[0]})

    def save_user(self, query, data):
        q_elements = query.split('/')[1:]
        if q_elements[0] == 'me':
            return None
        return self.db['user'].update({'id': q_elements[0]}, data, upsert=True)


    def get_contacts(self, query):
        return None

    def save_contacts(self, query, data):
        q_elements = query.split('/')[1:]
        user_id = q_elements[0]

        # Here is the name of fields already defined on the user data collection
        foreign_fields = ['first_name', 'last_name', 'name', 'gender']

        new_contacts = []
        for contact in data:
            # Split contact data in two set: one for native data comming from the contact user profile, the rest being local data tied to the contact relationship
            contact_id = contact.get('user_id')
            contact_user_data = dict([(i, contact.pop(i)) for i in contact.keys() if i in foreign_fields])
            contact_user_data.update({'id': contact_id})
            # Save native contact data to another user profile
            self.save_user('/%s' % contact_id, contact_user_data)
            # Save the rest to the local contact property
            new_contacts.append(contact)

        # Merge the old contact list with the new one
        # Query below work but do not deduplicate contact list content
        #self.db['user'].update({'id': q_elements[0]}, {'$pushAll': {'contacts': [contact]}}, upsert=True)

        user = self.db.user.find_one({'id': user_id})
        old_contacts = user.get('contacts', [])
        # Here we consider the id property of each contact item to be unique
        user['contacts'] = dict([(c['id'], c) for c in (old_contacts + new_contacts)]).values()
        self.db.user.save(user)
           
        # TODO: use DBRef for contact list ?
        # Examples and stuff to read before updating:
        #    https://github.com/mongodb/mongo-python-driver/blob/cd47b2475c5fe567e98696e6bc5af3c402891d12/examples/auto_reference.py
        #    http://api.mongodb.org/python/1.7/api/pymongo/dbref.html
        #    http://www.mongodb.org/display/DOCS/Schema+Design
        #contact['user_id'] = self.db['user'].findOne({'id': contact_id})

