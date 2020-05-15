import requests
import yaml
import os
import pandas as pd
import numpy as np
import json as json
from askdata.askdata_client import Agent
import uuid
from datetime import datetime

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)


class Entity:
    def __init__(self, Agent):
        self.agentId = Agent.agentId
        self.workspaceId = Agent.workspaceId
        self.username = Agent.username
        self.language = Agent.language
        self.token = Agent.token
        self.env = Agent.env
        self.regex_list = []


        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self.token
        }

        if self.env == 'dev':
            self.base_url_entity = url_list['BASE_URL_MANGER_DEV']
        if self.env == 'qa':
            self.base_url_entity = url_list['BASE_URL_MANGER_QA']
        if self.env == 'prod':
            self.base_url_entity = url_list['BASE_URL_MANGER_PROD']

    def GetEntities(self):
        # https://smartmanager.askdata.com/types/GROUPAMA_QA/entity/menu

        # to test
        authentication_url = self.base_url_entity + '/types/' + self.workspaceId + '/entity/menu'
        r = requests.get(url=authentication_url, headers=self.headers, verify=False)
        r.raise_for_status()
        df_entities = pd.DataFrame(r.json())
        return df_entities

    def GetEntityValues(self, entity_code):
        #https://smartmanager.askdata.com//data/GROUPAMA_QA/entity/AGENZIA?_page=0&_limit=50&filter=%257B%257D
        # to test
        authentication_url = self.base_url_entity + '//data/' + self.workspaceId + '/entity/' + entity_code
        r = requests.get(url=authentication_url, headers=self.headers, verify=False)
        r.raise_for_status()
        df_values = pd.DataFrame(r.json())
        return df_values

    def SetEntity(self):
        pass

    def SetEntityValues(self):
        pass

    def SynModifier(self,regex):
        #self.regex_list.append()
        pass

    def PushSynonyms(self):
        #https://smartmanager.askdata.com/data/GROUPAMA_QA/entity/AGENZIA
        pass
