from localstack.utils.aws import aws_models
cCoxO=super
cCoxm=None
cCoxM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cCoxO(LambdaLayer,self).__init__(arn)
  self.cwd=cCoxm
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,cCoxM,env=cCoxm):
  cCoxO(RDSDatabase,self).__init__(cCoxM,env=env)
 def name(self):
  return self.cCoxM.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
