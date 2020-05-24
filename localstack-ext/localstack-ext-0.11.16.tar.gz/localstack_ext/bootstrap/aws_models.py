from localstack.utils.aws import aws_models
glDHy=super
glDHP=None
glDHn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  glDHy(LambdaLayer,self).__init__(arn)
  self.cwd=glDHP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,glDHn,env=glDHP):
  glDHy(RDSDatabase,self).__init__(glDHn,env=env)
 def name(self):
  return self.glDHn.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
