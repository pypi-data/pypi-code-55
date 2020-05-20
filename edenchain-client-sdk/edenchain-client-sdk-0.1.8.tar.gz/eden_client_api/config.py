"""
    Edenchain configuration related
"""
import os

class EdenConfig:
    def __init__(self):
        self.apis=[
            {
                'api_key': 'AIzaSyBmK_WZhv6DtrQU-kSjFcfQ3i8CFQ0o5RY',
                'api_end_point': 'https://api-ep.edenchain.io/api'
            }
        ]


    def getConfig(self, network):
        if len(self.apis) <= network or network < 0:
            return False,{}
            
        return True, self.apis[network] 
