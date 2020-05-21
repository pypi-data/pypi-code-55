from localstack.utils.aws import aws_models
dGWIb=super
dGWIK=None
dGWIq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dGWIb(LambdaLayer,self).__init__(arn)
  self.cwd=dGWIK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,dGWIq,env=dGWIK):
  dGWIb(RDSDatabase,self).__init__(dGWIq,env=env)
 def name(self):
  return self.dGWIq.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
