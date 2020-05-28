# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from autograd import make_jvp, jacobian as autograd_jac
import autograd.numpy as np
from noload.optimization.specifications import Spec
from noload.optimization.iterationHandler import Iterations

'''Used to store results'''
class Results:
    objectives  = []  #valeurs des objectifs
    eq_cstr     = []  #valeurs des contraintes d'équalité
    ineq_cstr   = []  #valeurs des contraintes d'inégalités
    def __init__(self, results, shape, spec:Spec, jac):
        from noload.optimization.Tools import unflatten
        results = unflatten(results, shape)
        self.jac = jac
        t1 = len(spec.objectives)
        t2 = len(spec.eq_cstr)
        t3 = len(spec.ineq_cstr)
        self.objectives = np.array(results[:t1])
        sh = np.shape(self.objectives)
        if (t1 == 1) and len(sh) > 1 and sh[0]==1:
            self.objectives = self.objectives[0]
        if t2 != 0:
            self.eq_cstr = np.array(results[t1:t1 + t2])
            sh = np.shape(self.eq_cstr)
            if (t2 == 1) and len(sh) > 1 and sh[0] == 1:
                self.eq_cstr = self.eq_cstr[0]
        if t3!=0:
            self.ineq_cstr = np.array(results[-t3:])
            sh = np.shape(self.ineq_cstr)
            if (t3 == 1) and len(sh) > 1 and sh[0] == 1:
                self.ineq_cstr = self.ineq_cstr[0]

        # if t2 != 0:
        #     self.eq_cstr    = self.normalizeEq(results[t1:t1+t2], spec.eq_cstr_val)
        # if t3 != 0:
        #     self.ineq_cstr  = self.normalizeIneq(results[-t3:], spec.ineq_cstr_bnd)

    def normalizeEq(self, values, limits):
        ''' on se ramène entre à 1 '''
        # if limits!=0:
        #     results = (values.T  / limits).T
        # else:
        results = values
        for i in range(len(limits)):
            if limits[i] != 0:
                results[i] = values[i] / limits[i]
        return results
    def normalizeIneq(self, values, bounds):
        ''' on se ramène entre [0,1] '''
        min = np.array([bnd[0] for bnd in bounds])  #TODO gérer des variables plus complexes comme des vecteurs d'inconnus
        max = np.array([bnd[1] for bnd in bounds])
        # min = bounds[0]
        # max = bounds[1]
        if (self.jac):
            results = values
        else:
            results = ((values.T - min).T).T    #TODO gerer les None
        results = (results.T / (abs(max-min))).T
        return results

class Wrapper:
    model  = None
    p      = None
    spec : Spec  = None
    resultsHandler = None
    constraints = []
    xold   = None
    xold_g = None
    results_val : Results = None #valeurs des objectifs et contraintes
    results_grad : Results = None #gradients des objectifs et contraintes
    rawResults   = None #valeurs des sorties du model
    resultsShape = None #forme du vecteur de sortie (mise à plat des résultats pour autograd)

    def __init__(self, model : 'function to compute',
                 specifications : Spec ,
                 parameters : 'a List of inputs that are not optimized' = [],
                 resultsHandler : "for real time plotting for instance" = None):
        self.model = model
        self.p = parameters
        self.spec = specifications
        # permet de sauvegarder les résultats au fur et à mesure (optionnel)
        if resultsHandler==True:
            self.resultsHandler = Iterations(specifications.iNames, specifications.oNames)
#        elif resultsHandler != None:
#            self.resultsHandler = resultsHandler
        #else : no resultHandler => no iteration history

        self.init()

    def init(self):
        self.constraints=[]
        if len(self.spec.eq_cstr) != 0:
            self.constraints.append({'type': 'eq',
                 'fun' : self.eq_cstr_val,
                 'jac' : self.eq_cstr_grad})
        if len(self.spec.ineq_cstr) != 0:
            self.constraints.append({'type': 'ineq',
                 'fun' : self.ineq_cstr_val,
                 'jac' : self.ineq_cstr_grad})
        self.xold = None
        self.xold_g = None
        self.results_val = None
        self.results_grad = None
        self.rawResults = None

    ## 3 fonctions pour récupérer les VALEURS des objectifs et contraintes
    def f_val(self, x):
        if (not np.array_equal(self.xold,x)):
            self.results_val=Results(self.compute_model(x), self.resultsShape, self.spec, jac = False)
            self.xold=np.array(x, copy=True)
        return self.results_val.objectives

    def eq_cstr_val(self, x):
        if (not np.array_equal(self.xold,x)):
            self.results_val = Results(self.compute_model(x), self.resultsShape, self.spec, jac = False)
            self.xold=np.array(x, copy=True)
        #il faut bien se mettre en dehors du if car le calcul du model aura pu être fait dans une autre fonction.
        if (self.spec.eq_cstr_val!=[]):
            self.results_val.eq_cstr = self.results_val.eq_cstr - self.spec.eq_cstr_val  # -1
        return self.results_val.eq_cstr

    def ineq_cstr_val(self, x):
        if (not np.array_equal(self.xold,x)):
            res=self.compute_model(x)
            self.results_val = Results(res, self.resultsShape, self.spec, jac = False)
            self.xold=np.array(x, copy=True)
        if (self.spec.ineq_cstr_bnd!=[]):# and len(self.results_val.ineq_cstr)==len(self.spec.ineq_cstr)):
            constraints = self.results_val.ineq_cstr.copy()
            for i in range(len(self.spec.ineq_cstr_bnd)):
                inf = self.spec.ineq_cstr_bnd[i][0]
                sup = self.spec.ineq_cstr_bnd[i][1]
                if (inf!=None):
                    constraints[i] = self.results_val.ineq_cstr[i] - inf   # borne inf = 0 après normalisation
                    if (sup != None):   #on ajoute une contrainte
                        constraints = np.append(constraints, sup-self.results_val.ineq_cstr[i]  )  #sup = 1 si normalisé
                else:   #on suppose que sup est différent de None !
                    constraints[i] = sup - self.results_val.ineq_cstr[i]  #sup = 1 si normalisé

        return constraints

    ## 3 fonctions pour récupérer les GRADIENTS des objectifs et contraintes
    def f_grad(self, x):
        if (not np.array_equal(self.xold_g,x)):
            grad = autograd_jac(self.compute_model)(x)
            self.results_grad = Results(grad, self.resultsShape, self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        return self.results_grad.objectives
    # Autre methode de calcul du Jacobien, à utiliser si il la dimension en sortie est plus grande qu'en entrée
    def f_grad_using_make_jvp(self, x):
        if (not np.array_equal(self.xold_g, x)):
            a = np.array([1])
            basis = np.pad(a, [(0, len(x) - 1)], mode='constant')  # create first vector basis (1, 0, 0, ...)
            val_of_f, jac = (make_jvp(self.compute_model)(x))(basis)
            lines=len(jac)
            for i in range(1, len(x)):
                basis = np.roll(basis, 1)
                val_of_f, col_of_jacobian = (make_jvp(self.compute_model)(x))(basis)
                jac=np.append(jac, col_of_jacobian, axis = 0)
            jac =np.reshape(jac,(len(x),lines)).T
            self.results_grad = Results(jac, self.resultsShape, self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        return self.results_grad.objectives

    def eq_cstr_grad(self, x):
        if (not np.array_equal(self.xold_g,x)):
            self.results_grad = Results(autograd_jac(self.compute_model)(x), self.resultsShape, self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        return self.results_grad.eq_cstr

    def ineq_cstr_grad(self, x):
        if (not np.array_equal(self.xold_g,x)):
            self.results_grad = Results(autograd_jac(self.compute_model)(x), self.resultsShape, self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        # on duplique les contraintes d'inégalité qui on une borne supérieure:
        if (self.spec.ineq_cstr_bnd!=[]): #TODO cette contrainte ne fonctionne plus en vectoriel : and len(self.results_grad.ineq_cstr[:])==len(self.spec.ineq_cstr)):
            if len(np.shape(self.results_grad.ineq_cstr))==1:
                self.results_grad.ineq_cstr=np.array([self.results_grad.ineq_cstr])
            for i, cstr in enumerate(self.spec.ineq_cstr_bnd):
                inf = self.spec.ineq_cstr_bnd[i][0]
                sup = self.spec.ineq_cstr_bnd[i][1]
                #TODO NE FONCTIONNE PAS EN VECTORIEL !
                if (inf!=None):
                    # inf : on ne fait rien car la contrainte sur le gradiant est déjà bien définie.
                    if (sup != None):
                        self.results_grad.ineq_cstr = np.append(self.results_grad.ineq_cstr, [- self.results_grad.ineq_cstr[i][:]], axis = 0)
                else:   #contrainte d'infériorité (par défaut SLSQP : ctr>0)
                    self.results_grad.ineq_cstr[i][:] = - self.results_grad.ineq_cstr[i][:]

        return self.results_grad.ineq_cstr

    # fonction utilisée par minimize de scipy
    def f_val_grad(self, x):
        return (self.f_val(x), self.f_grad(x))

    # wrapper permettant d'être selectif sur les sorties du modèles, en particulier pour le calcul du Jacobien
    def compute_model(self, x):
        if len(self.spec.iNames)==1 and len(x)!=1:   #TODO, patch for 1 array variable, to do more general
            xList = dict(zip(self.spec.iNames, [x]))
        else:
            xList = dict(zip(self.spec.iNames, x))  #TODO, verifier que ça fonctionne pour une liste d'entrée scalaire et vectorielle (uniquement le premier élement du vecteur ?)
        if self.p != []:
            res = self.model(**xList, **self.p)
        else:
            res = self.model(**xList)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        out = [dico[vars] for vars in self.spec.oNames]     #TODO attraper une exception si la variable du cahier des charge n'appartient pas aux sorties du modèle
        #TODO l'agregation des sortie pose un pb pour les sortie vectorielle (par exemple pour l'optimi Leastsqare)
        # sauvegarde et tracé des résultats uniquement si appel à la fonction et non au gradient
        if (type(x[0]) != np.numpy_boxes.ArrayBox):
            self.rawResults = dico
            if (self.resultsHandler!=None):
                self.resultsHandler.updateData(x, out)
        from noload.optimization.Tools import flatten
        out, shape = flatten(out)
        self.resultsShape = shape
        return np.array(out)


    def solution(self):
        return self.resultsHandler.solutions[-1].iData.tolist()

    def getLastInputs(self):
        lastSol = self.resultsHandler.solutions[-1]
        if len(self.resultsHandler.iNames)==1:
            dico = {self.resultsHandler.iNames[0]: lastSol.iData.tolist()}
        else:
            dico = {self.resultsHandler.iNames[i]: lastSol.iData[i] for i in range(len(self.resultsHandler.iNames))}
        return dico
    def getLastOutputs(self):
        lastSol = self.resultsHandler.solutions[-1]
        dico = {self.resultsHandler.oNames[i]: lastSol.oData[i] for i in range(len(self.resultsHandler.oNames))}
        return dico

    def printResults(self):
        print(self.getLastInputs())
        print(self.getLastOutputs())

    def printAllResults(self):
        sols = self.resultsHandler.solutions
        for sol in sols:
            if len(self.resultsHandler.iNames)==1:
                dico = {self.resultsHandler.iNames[0]: sol.iData.tolist()}
            else:
                dico = {self.resultsHandler.iNames[i]: sol.iData[i] for i in range(len(self.resultsHandler.iNames))}
            print(dico)

    def plotResults(self):
        import noload.gui.plotIterations as pltIter
        pltIter.plotIO(self.resultsHandler)

    def plotNormalizedSolution(self):

        bnd=np.transpose(self.spec.bounds)
        sols = self.solution()
        x = list(range(0,len(sols)))
        #normalize :
        mean = (bnd[1]+bnd[0])/2
        init = self.spec.xinit
        solsN = (sols-init)/(bnd[1]-bnd[0])

        import matplotlib.pyplot as plt
        plt.bar(x, solsN)
        plt.show()

