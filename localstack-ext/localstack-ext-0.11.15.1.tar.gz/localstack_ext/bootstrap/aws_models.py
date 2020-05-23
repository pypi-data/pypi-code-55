from localstack.utils.aws import aws_models
UKoJn=super
UKoJl=None
UKoJI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UKoJn(LambdaLayer,self).__init__(arn)
  self.cwd=UKoJl
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,UKoJI,env=UKoJl):
  UKoJn(RDSDatabase,self).__init__(UKoJI,env=env)
 def name(self):
  return self.UKoJI.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
