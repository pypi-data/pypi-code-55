"""
Written by Jan H. Jensen 2018, copied 04/2020
"""
from rdkit import Chem
from rdkit.Chem import AllChem

import random

from rdkit import rdBase
rdBase.DisableLog('rdApp.error')


def cut(mol):
    if not mol.HasSubstructMatch(Chem.MolFromSmarts('[*]-;!@[*]')): 
        return None
    bis = random.choice(mol.GetSubstructMatches(Chem.MolFromSmarts('[*]-;!@[*]')))  # single bond not in ring
    bs = [mol.GetBondBetweenAtoms(bis[0],bis[1]).GetIdx()]
  
    fragments_mol = Chem.FragmentOnBonds(mol,bs,addDummies=True,dummyLabels=[(1, 1)])
  
    try:
        fragments = Chem.GetMolFrags(fragments_mol,asMols=True)
        return fragments
    except:
        return None


def cut_ring(mol):
    for i in range(10):
        if random.random() < 0.5:
            if not mol.HasSubstructMatch(Chem.MolFromSmarts('[R]@[R]@[R]@[R]')): 
                return None
            bis = random.choice(mol.GetSubstructMatches(Chem.MolFromSmarts('[R]@[R]@[R]@[R]')))
            bis = ((bis[0],bis[1]),(bis[2],bis[3]),)
        else:
            if not mol.HasSubstructMatch(Chem.MolFromSmarts('[R]@[R;!D2]@[R]')): 
                return None
            bis = random.choice(mol.GetSubstructMatches(Chem.MolFromSmarts('[R]@[R;!D2]@[R]')))
            bis = ((bis[0],bis[1]),(bis[1],bis[2]),)

        bs = [mol.GetBondBetweenAtoms(x,y).GetIdx() for x,y in bis]
    
        fragments_mol = Chem.FragmentOnBonds(mol,bs,addDummies=True,dummyLabels=[(1, 1),(1,1)])
    
        try:
            fragments = Chem.GetMolFrags(fragments_mol,asMols=True)
        except:
            return None
    
        if len(fragments) == 2:
            return fragments
      
    return None


def ring_OK(mol):
    if not mol.HasSubstructMatch(Chem.MolFromSmarts('[R]')):
        return True
    
    ring_allene = mol.HasSubstructMatch(Chem.MolFromSmarts('[R]=[R]=[R]'))
    
    cycle_list = mol.GetRingInfo().AtomRings() 
    max_cycle_length = max([ len(j) for j in cycle_list ])
    macro_cycle = max_cycle_length > 6
    
    double_bond_in_small_ring = mol.HasSubstructMatch(Chem.MolFromSmarts('[r3,r4]=[r3,r4]'))
    
    return not ring_allene and not macro_cycle and not double_bond_in_small_ring


def mol_OK(mol):
    try:
        Chem.SanitizeMol(mol)
        test_mol = Chem.MolFromSmiles(Chem.MolToSmiles(mol))
        if test_mol is None:
            return None
        else:
            return True
        # target_size = size_stdev*np.random.randn() + average_size #parameters set in GA_mol
        # if mol.GetNumAtoms() > 5 and mol.GetNumAtoms() < target_size:
        #    return True
        # else:
        #    return False
    except:
        return False


def crossover_ring(parent_A,parent_B):
    ring_smarts = Chem.MolFromSmarts('[R]')
    if not parent_A.HasSubstructMatch(ring_smarts) and not parent_B.HasSubstructMatch(ring_smarts):
      return None
    
    rxn_smarts1 = ['[*:1]~[1*].[1*]~[*:2]>>[*:1]-[*:2]','[*:1]~[1*].[1*]~[*:2]>>[*:1]=[*:2]']
    rxn_smarts2 = ['([*:1]~[1*].[1*]~[*:2])>>[*:1]-[*:2]','([*:1]~[1*].[1*]~[*:2])>>[*:1]=[*:2]']
    for i in range(10):
        fragments_A = cut_ring(parent_A)
        fragments_B = cut_ring(parent_B)
        if fragments_A is None or fragments_B is None:
            return None
        
        new_mol_trial = []
        for rs in rxn_smarts1:
            rxn1 = AllChem.ReactionFromSmarts(rs)
            new_mol_trial = []
            for fa in fragments_A:
                for fb in fragments_B:
                    new_mol_trial.append(rxn1.RunReactants((fa,fb))[0]) 
    
        new_mols = []
        for rs in rxn_smarts2:
            rxn2 = AllChem.ReactionFromSmarts(rs)
            for m in new_mol_trial:
                m = m[0]
                if mol_OK(m):
                    new_mols += list(rxn2.RunReactants((m,)))
          
        new_mols2 = []
        for m in new_mols:
            m = m[0]
            if mol_OK(m) and ring_OK(m):
                new_mols2.append(m)
          
        if len(new_mols2) > 0:
            return random.choice(new_mols2)
      
    return None


def crossover_non_ring(parent_A,parent_B):
    for i in range(10):
        fragments_A = cut(parent_A)
        fragments_B = cut(parent_B)
        if fragments_A is None or fragments_B is None:
            return None
        rxn = AllChem.ReactionFromSmarts('[*:1]-[1*].[1*]-[*:2]>>[*:1]-[*:2]')
        new_mol_trial = []
        for fa in fragments_A:
            for fb in fragments_B:
                new_mol_trial.append(rxn.RunReactants((fa,fb))[0]) 
                                     
        new_mols = []
        for mol in new_mol_trial:
            mol = mol[0]
            if mol_OK(mol):
                new_mols.append(mol)
        
        if len(new_mols) > 0:
          return random.choice(new_mols)
        
    return None


def crossover(parent_A,parent_B):
    parent_smiles = [Chem.MolToSmiles(parent_A), Chem.MolToSmiles(parent_B)]
    try:
        Chem.Kekulize(parent_A, clearAromaticFlags=True)
        Chem.Kekulize(parent_B, clearAromaticFlags=True)
    except:
        pass
    for i in range(10):
        if random.random() <= 0.5:
            new_mol = crossover_non_ring(parent_A,parent_B)
            if new_mol is not None:
                new_smiles = Chem.MolToSmiles(new_mol)
            if new_mol is not None and new_smiles not in parent_smiles:
                return new_mol
    else:
        new_mol = crossover_ring(parent_A,parent_B)
        if new_mol is not None:
            new_smiles = Chem.MolToSmiles(new_mol)
        if new_mol is not None and new_smiles not in parent_smiles:
            return new_mol

    return None
