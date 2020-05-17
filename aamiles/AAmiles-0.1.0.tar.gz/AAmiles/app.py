import getDataAA
import numpy as np
import os

def run():
    print('Scanner de millas AA iniciado...')

    data = getDataAA.get()

    pMiles = np.array(data.millas[0]) # clase promocional
    tMiles = np.array(data.millas[0]) # clase turista
    bMiles = np.array(data.millas[0]) # clase busines

    pMiles[pMiles == 'N/A'] = '-1'
    tMiles[tMiles == 'N/A'] = '-1'
    bMiles[bMiles == 'N/A'] = '-1'

    pMiles = pMiles.astype(np.float)
    tMiles = tMiles.astype(np.float)
    bMiles = bMiles.astype(np.float)

    # chequeo si existen las tablas anteriores. Sino uso las actuales y las guardo.
    if os.path.isfile('pMiles_old.npy'):
        pMiles_old = np.load('pMiles_old.npy')
    else:
        pMiles_old = pMiles
        np.save('pMiles_old.npy', pMiles)

    if os.path.isfile('tMiles_old.npy'):
        tMiles_old = np.load('tMiles_old.npy')
    else:
        tMiles_old = tMiles
        np.save('tMiles_old.npy', tMiles)

    if os.path.isfile('bMiles_old.npy'):
        bMiles_old = np.load('bMiles_old.npy')
    else:
        bMiles_old = bMiles
        np.save('bMiles_old.npy', bMiles)

    if bool((pMiles-pMiles_old).any()) or bool((tMiles-tMiles_old).any()) or bool((bMiles-bMiles_old).any()):
        print('\n¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡')
        print('Hay cambio en la tabla de Millas.')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        print('Reemplazar tabla anterior de millas? ')
        
        val = input('(S/N): ')
        if val == 'S' or val == 's':
            np.save('pMiles_old.npy', pMiles)
            np.save('tMiles_old.npy', tMiles)
            np.save('bMiles_old.npy', bMiles)
    else:
        print('No cambio en la tabla de Millas.')
        val = 'N'
    #print('Escanear nuevamente?')
    #val = input('(S/N): ')
    return val
    


