'''
Created on Apr 22, 2020

@author: ballance
'''
from pssparser.model.expr_id import ExprId

class PoolBindStmt(object):
    
    def __init__(self, pool : ExprId):
        self.pool = pool
        self.bindlist = []
        
    def accept(self, v):
        v.visit_pool_bind_stmt(self)