import numpy as np

def insertKptsFromXcrysden(kpfFile, updateFile):
    """
    Generates a new *.in file entitled updateFile(minus.in)_update.in 
    by incorporating the k-points listed in kpfFile 
    (real form of k-point coordinates)

    Parameters
    ----------
    kpfFile : str
        DESCRIPTION. Filename, including extension, of the XCRYSDEN *.kpf file 
        containing the points you want to add
    updateFile : TYPE
        DESCRIPTION. Filename, including extension, of the *.in file that you 
        want to update/replace k-points of. This should leave other blocks alone.

    Returns
    -------
    None.

    """
    read=False
    kpts=[]
    with open(kpfFile, "r") as f:
        for l in f.readlines():
            if read==True and len(l)>10:
                L=l.strip().split()[0:3]
                L=' '.join(L)+" 10\n"
                kpts.append(L)
            
            if l[0:2]=='Re':
                read=True
            if l[0]=='#':
                read=False
    lines=[]
    lenKPts=len(kpts)
    cnt=0
    cntEnd=0                
    with open(updateFile, "r") as f:
        lines=f.readlines()
        
        L=len(lines)
        
        while cnt<L and lines[cnt][0:3].upper() != 'K_P':
            cnt +=1
        cntEnd=cnt+1
        while cntEnd<L and len(lines[cntEnd].strip())>0 and lines[cntEnd].strip()[0].isdigit():
            cntEnd+=1
         
    kpstr=['K_POINTS crystal_b\n',
           str(lenKPts)+"\n"]
    #delete Kpoints and other lines between cnt and cntEnd
    del lines[cnt:cntEnd]
    kpstr.extend(kpts)
    
    for k in range(len(kpstr)):
        lines.insert(cnt+k, kpstr[k])
    #find end of K_points block
    ln=updateFile.split('.')
    L=len(ln)
    sr=''.join(ln[0:L-1])+'_update.'+ln[L-1]
    outF=open(sr, 'w', newline='\n')
    outF.writelines(lines)
    outF.close()
def vcRelaxTransfer(inFileHead, outputF):
    '''
    Applies the new lattice parameters and atom sites obtained from a vc-relax calculation to a new *.in file
    example: vcRelaxTransfer('Si-vcRelax', 'Si-vcRelax2.in')
    Caution: Not fully tested.

    Parameters
    ----------
    inFileHead : str
        DESCRIPTION. Head of pw.x input and output files used for vc-relax calculation ([HEAD].in and [HEAD].out). No extension included
    outputF : str
        DESCRIPTION. Name of the new pw.x input file that you want to create. MUST INCLUDE *.in EXTENSION!

    Returns
    -------
    None.

    '''
    inFileOut=inFileHead+'.out'
    inFileIn=inFileHead+'.in'
    inLines=[]
    startAtPos=0
    startcellParam=0
    endAtPos=0
    endcellParam=0
    celldmABC=False
    importantL=[]
    sysStart=0
    sysEnd=0
    with open(inFileIn, 'r') as f:
        inLines=f.readlines()
        k=0
        while k< len(inLines):
            L=inLines[k].strip()
            if L[0:2].upper()=='&S':
                sysStart=k
                while k<len(inLines) and L[0]!='/':
                    L=inLines[k].strip()
                    k=k+1
                sysEnd=k-1
            if len(L)>13:
                if inLines[k][0:8].upper()=='ATOMIC_P':
                    startAtPos=k+1
                    k=k+1
                    L=inLines[k].strip().split()
                    while k<len(inLines) and len(L)==4:
                        k=k+1
                        L=inLines[k].strip().split()
                    endAtPos=k
                if inLines[k][0:6].upper()=='CELL_P':
                    print('Old ' +inLines[k])
                    print(inLines[k+1])
                    print(inLines[k+2])
                    print(inLines[k+3])
                    startcellParam=k+1
                    endcellParam=k+4
                
            k=k+1
        if startcellParam==0:
            #go back and look for celldm statements
            celldmABC=True
            
            for k in range(sysStart, sysEnd):
                L=inLines[k].strip().split('=')
                if L[0][0:6]=='celldm':
                    importantL.append(k)
                    print(inLines[k])
                if len(L[0])==1:
                    importantL.append(k)
                    print(inLines[k])
                if L[0][0:3].lower()=='cos':
                    importantL.append(k)
                    print(inLines[k])
    
                    
    
                    
    #go into output file and pull out atomic positions and cell parameters
    
        
    pos=[]
    
    
    cellParam=[]
    cellNP=[]
    with open(inFileOut, "r") as f:
        outLines=f.readlines()
        k=0
    
        while k<len(outLines):
            L=outLines[k]
            if len(L)>10 and L[0:5]=='Begin':
                cellParam.append(outLines[k+4])
                print('New ' +outLines[k+4])
                cellParam.append(outLines[k+5])
                cellNP.append(outLines[k+5].split())
                print(outLines[k+5])
                cellParam.append(outLines[k+6])
                cellNP.append(outLines[k+6].split())
                print(outLines[k+6])
                cellParam.append(outLines[k+7])
                cellNP.append(outLines[k+7].split())
                print(outLines[k+7])
                k=k+7
            if len(L)>10 and L[0:4]=='ATOM':
                k=k+1
                L=outLines[k].strip().split()
                while len(L)==4:
                    pos.append(outLines[k])
                    k=k+1
                    L=outLines[k].strip().split()
                    
    
            k=k+1
    newCell=np.array(cellNP, float)
    #make updated data file
    out=inLines
    print('Exported lines')
    if celldmABC==False:
        out[startAtPos:endAtPos]=pos
        out[startcellParam:endcellParam]=cellParam
        print(pos)
        print(cellParam)
    
    elif len(importantL)>0:
        L=cellParam[0].strip().split('=')[1][0:-1]
        alat=float(L)
        
        for k in range (0, len(importantL)):
            oldLine=inLines[importantL[k]]
            oldLine=oldLine.strip().split('=')
            if oldLine[0][0:9]=='A':
                out[importantL[k]]=' A = '+str(newCell[0,0]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='B':
                out[importantL[k]]=' B = '+str(newCell[1,1]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='C':
                out[importantL[k]]=' C = '+str(newCell[2,2]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='cosAB':
                out[importantL[k]]=' cosAB = '+str(np.dot(newCell[0, :], newCell[1, :])/(np.linalg.norm(newCell[0, :])*np.linalg.norm(newCell[1, :])))+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='cosAC':
                out[importantL[k]]=' cosAC = '+str(np.dot(newCell[0, :], newCell[2, :])/(np.linalg.norm(newCell[0, :])*np.linalg.norm(newCell[2, :])))+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='cosBC':
                out[importantL[k]]=' cosBC = '+str(np.dot(newCell[2, :], newCell[1, :])/(np.linalg.norm(newCell[2, :])*np.linalg.norm(newCell[1, :])))+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(1)':
                out[importantL[k]]=' celldm(1)= '+str(newCell[0,0]*alat)+"\n"
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(2)':
                out[importantL[k]]=' celldm(2)= '+str(np.linalg.norm(newCell[1, :])/np.linalg.norm(newCell[0, :]))+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(3)':
                out[importantL[k]]=' celldm(3)= '+str(np.linalg.norm(newCell[2, :])/np.linalg.norm(newCell[0, :]))+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(4)':
                out[importantL[k]]=' celldm(4)= '+str(newCell[0,0]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(5)':
                out[importantL[k]]=' celldm(5)= '+str(newCell[0,0]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
            elif oldLine[0][0:9]=='celldm(6)':
                out[importantL[k]]=' celldm(6)= '+str(newCell[0,0]*alat)+"\n"
                print('Caution! This code has not been tested')
                print(out[importantL[k]])
    
    
    
    outF=open(outputF, 'w', newline='\n')
    outF.writelines(out)
    outF.close()
