from localstack.utils.aws import aws_models
yBoFt=super
yBoFb=None
yBoFY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yBoFt(LambdaLayer,self).__init__(arn)
  self.cwd=yBoFb
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,yBoFY,env=yBoFb):
  yBoFt(RDSDatabase,self).__init__(yBoFY,env=env)
 def name(self):
  return self.yBoFY.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
