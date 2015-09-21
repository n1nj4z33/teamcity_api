# -*- coding: utf-8 -*-
'''
TeamcityUtils
'''
from teamcity_api.api import TeamcityAPI


class TeamcityUtils(TeamcityAPI):
    '''Class for additional utils for TeamcityAPI'''
    def __init__(self, url):
        TeamcityAPI.__init__(self, url)
        self.guestauth()

    def save_artifact(self, build_id, artifact):
        '''Save artifact file with chucked encoding'''
        response = self.get_artifact(build_id, artifact)
        assert response.status_code == 200
        with open(artifact, 'wb') as artifact_file:
            for chunk in response.iter_content(512 * 1024):
                artifact_file.write(chunk)
