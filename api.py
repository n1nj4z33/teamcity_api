# -*- coding: utf-8 -*-
'''
A python wrapper for the Teamcity 9.x REST API
For more information see https://confluence.jetbrains.com/
'''
import requests
from requests.utils import urlparse
import logging

def prepare_logger():
    '''Prepare module logger'''
    inner_logger = logging.getLogger(__name__)
    inner_logger.setLevel(logging.DEBUG)
    chanel = logging.StreamHandler()
    chanel.setLevel(logging.DEBUG)
    inner_logger.addHandler(chanel)
    return inner_logger

LOGGER = prepare_logger()

class TeamcityAPI(object):
    '''Class for communication with teamcity'''
    def __init__(self, url):
        self.base_url = urlparse(url).netloc
        self.url = 'http://%s' % self.base_url
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def prepare_url(self, url):
        '''Prepare url from methods url. Returns String'''
        return '/'.join((self.url, url))

    def send_request(self, url=None, method=None, headers=None, data=None, auth=None):
        '''Send request and logging the response. Returns Response Object'''
        url = self.prepare_url(url)
        LOGGER.info('Request url: %s', url)
        LOGGER.info('Request data: %s', data)
        response = self.session.request(method=method,
                                        url=url,
                                        headers=headers,
                                        data=data,
                                        auth=auth,
                                        verify=False)
        LOGGER.info('Response code: %s', response.status_code)
        LOGGER.info('Response text: %s', response.text)
        return response

    def httpauth(self, username, password):
        '''HTTP authorization'''
        auth = requests.auth.HTTPBasicAuth(username,
                                           password)
        url = self.prepare_url('httpAuth/')
        return self.session.post(url=url,
                                 auth=auth)

    def guestauth(self):
        '''Guest authorization'''
        url = self.prepare_url('guestAuth/')
        return self.session.post(url=url)

    def get_version(self):
        '''Get api version'''
        url = 'app/rest/version'
        headers = {'Accept': 'text/plain'}
        return self.send_request(url=url,
                                 method='GET',
                                 headers=headers)

    def get_users(self):
        '''Get all users'''
        url = 'app/rest/users'
        return self.send_request(url=url,
                                 method='GET')

    def get_projects(self):
        '''Get all projects'''
        url = 'app/rest/projects'
        return self.send_request(url=url,
                                 method='GET')

    def get_project(self, project_id):
        '''Get project by project_id'''
        url = 'app/rest/projects/id:%s' % project_id
        return self.send_request(url=url,
                                 method='GET')

    def get_build_types(self):
        '''Get all buildTypes'''
        url = 'app/rest/buildTypes'
        return self.send_request(url=url,
                                 method='GET')

    def get_build_type(self, build_type_id):
        '''Get buildType by build_id'''
        url = 'app/rest/buildTypes/id:%s' % build_type_id
        return self.send_request(url=url,
                                 method='GET')

    def get_builds(self):
        '''Get all builds'''
        url = 'app/rest/builds'
        return self.send_request(url=url,
                                 method='GET')

    def get_build(self, build_id):
        '''Get build by build_id'''
        url = 'app/rest/builds/%s' % build_id
        return self.send_request(url=url,
                                 method='GET')

    def get_tag(self, build_id):
        '''Get tags of build by build_id'''
        url = 'app/rest/builds/id:%s/tags' % build_id
        return self.send_request(url=url,
                                 method='GET')

    def get_artifact(self, build_id, artifact):
        '''Get artifact by build_id and artifact name'''
        url = self.prepare_url('app/rest/builds/id:%s/artifacts/content/%s' %
                               (build_id, artifact))
        return self.session.get(url=url,
                                stream=True)
