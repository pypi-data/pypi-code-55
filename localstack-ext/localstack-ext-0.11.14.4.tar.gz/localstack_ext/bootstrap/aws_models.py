from localstack.utils.aws import aws_models
NLCKm=super
NLCKR=None
NLCKH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NLCKm(LambdaLayer,self).__init__(arn)
  self.cwd=NLCKR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,NLCKH,env=NLCKR):
  NLCKm(RDSDatabase,self).__init__(NLCKH,env=env)
 def name(self):
  return self.NLCKH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
