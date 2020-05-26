from .helpers import (Client, Coaching, Learning, Campaign, 
    Calibration, Evaluation, Scorecard, Team, User, Role, Integration, 
    Interaction)

class Playvox:
    def __init__(self, pv_subdomain, uid, key):
        self.client = Client(pv_subdomain, uid, key)
        self.coaching = Coaching(self.client)
        self.learning = Learning(self.client)
        self.campaign = Campaign(self.client)
        self.calibration = Calibration(self.client)
        self.evaluation = Evaluation(self.client)
        self.scorecard = Scorecard(self.client)
        self.team = Team(self.client)
        self.user = User(self.client)
        self.role = Role(self.client)
        self.integration = Integration(self.client)
        self.interaction = Interaction(self.client)
    
    def __repr__(self):
        return '<Playvox API Wrapper for {}>'.format(self.client.pv_subdomain)

