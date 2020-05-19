import requests
import os
import shutil
import re
import codecs
import time
import datetime
import click
from git import Repo
from colorama import init
from pathlib import Path

targetPaths = []
workTree = []
stats = []
cont = ''
greenFlag = False
processed = False
reqs = 0
chars = 0
enUi = ['button', 'checkbox', 'field', 'column', 'area', 'box', 'role', 'user', 'line', 'table', 'mode', 'module', 'menu', 'event',
        'RFx', 'search', 'page', 'tab', 'panel', 'option', 'dialog', 'status', 'tag', 'symbol', 'sign', 'label', 'scenario', 'link',
        'auction', 'events', 'checkboxes', 'columns', 'lines', 'answers', 'answer', 'responses', 'response', 'buttons', 'fields',
        'tabs', 'icon', 'icons', 'users', 'widget', 'widgets', 'window', 'windows', 'dialog box', 'dialog boxes', 'modal window',
        'modal windows', 'dialog window', 'dialog windows', 'homepage']

# Configuração da API de tradução

urlTrad = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
apiTradKey = 'trnsl.1.1.20200423T224754Z.c7c8ffe1eb46fb13.862b87f341a60e80ade11d71c970d3f2f1ebdcf9'

# Idioma fonte

sourceLang = 'en'

# Idiomas traduzidos

targetLangs = ['es', 'pt']

# Diretório fonte

sourceDir = 'amostra/' + '_'.join(sourceLang.split('-')).lower()

# Preservação da sintaxe Markdown DocFX

mdRegex = re.compile(r'''(\]\(.+?\)[\W ]?)|          # referência de imagem ou link
                         (uid:\s?[\w.]+)|            # âncora de link no cabeçalho
                         (\{\{.*?\}\}[\W ]+?)|       # nome de UI localizado pelo Zanata
                         (:{3}\s*[a-z]*)|            # demarcador de bloco de ênfase customizado para o Docs 2.0
                         (`{1,3}.+?`{1,3}[\W ]?)|    # bloco de código
                         (<.+?>)|                    # HTML
                         ([-=|_:]{2,})|              # linha horizontal e divisor de cabeçalho de tabela
                         (\s*?\d\.\s)|               # numeração em lista numerada
                         (\s?[\[!#*|>\r\n\t]+?\s*)   # outros elementos de Markdown DocFX''', re.VERBOSE | re.DOTALL)

# Preservação da sintaxe Yaml DocFX

ymlRegex = re.compile(r'(name: [ \w\'\-]+)')         # traduz texto entre 'name: ' e quebra de linha

#--------------------------------

def ProcessFiles(sourceFile):
    fileName = sourceFile.split('/')[-1]
    if fileName[-3:] in ('yml', '.md'):
        file = codecs.open(sourceFile, encoding = 'utf-8', mode = 'r')
        sourceContent = (file.read())
        file.close()
        for i in range (len(targetLangs)):
            langCombo = sourceLang + '-' + targetLangs[i]
            targetContent = ''
            if fileName[-3:] == 'yml':
                PrGreen('\n Traslating Yaml from ' + sourceLang + ' to ' + targetLangs[i] + ':\n' + sourceFile)
                slicedApple = list(filter(lambda x: x != '' and x is not None, ymlRegex.split(sourceContent)))
                for piece in slicedApple:
                    if not ymlRegex.fullmatch(piece):
                        targetContent = [n + piece for n in targetContent]
                    else:
                        localized = 'name: ' + Translate(piece[6:], langCombo).title()
                        targetContent += localized
            else:
                PrGreen('\n Traslating Markdown from ' + sourceLang + ' to ' + targetLangs[i] + ':\n' + sourceFile)
                if sourceLang[:2] == 'en':
                    slicedUi = re.split(r'(\{\{.*?\}\} [a-zA-Z]+)', sourceContent)
                    for i in range(len(slicedUi)):
                        if re.fullmatch(r'\{\{.*?\}\} [a-zA-Z]+', slicedUi[i]) and re.search(r'(?<=\}\} ).+', slicedUi[i]).group().casefold() in enUi:
                            slicedUi[i] = ' '.join(re.split(r'(?<=\}\}) ', slicedUi[i])[::-1])
                    sourceContent = ''.join(slicedUi)
                slicedApple = list(filter(lambda x: x != '' and x is not None, mdRegex.split(sourceContent)))
                for piece in slicedApple:
                    if mdRegex.fullmatch(piece):
                        if re.fullmatch(r'\]\(#.+\)', piece):
                            anchors = Translate(' '.join(piece[3:-1].split('-')))
                            for i in range(len(anchors)):
                                targetContent[i] += '](#' + '-'.join(anchors[i].split(' ')).lower() + ')'
                        else:
                            targetContent = [n + piece for n in targetContent]
                    else:
                        localized = Translate(piece, langCombo)
                        targetContent += localized
            file = codecs.open(targetPaths[i] + '/' + '/'.join(sourceFile.split('/')[2:]), encoding = 'utf-8', mode = 'w+')
            file.write(targetContent)
            file.close()
        return

    PrLightPurple('Copying ' + sourceFile)
    for i in range (len(targetLangs)):
        shutil.copy(sourceFile, targetPaths[i] + '/' + '/'.join(sourceFile.split('/')[2:]))

#--------------------------------

def FileStats(sourceFile):
    fileName = sourceFile.split('/')[-1]
    if fileName[-3:] not in ('yml', '.md'): return
    file = codecs.open(sourceFile, encoding = 'utf-8', mode = 'r')
    content = (file.read())
    file.close()
    charsFile = 0
    reqsFile = 0
    if fileName[-3:] == 'yml':
        reqsFile = len(ymlRegex.findall(content))
        charsFile = len(''.join(ymlRegex.findall(content)))
    else:
        slicedApple = list(filter(lambda x: x != '' and x is not None, mdRegex.split(content)))
        for d in slicedApple:
            if mdRegex.fullmatch(d) is None:
                reqsFile += 1
                charsFile += len(d)
    return [reqsFile * len(targetLangs), charsFile * len(targetLangs)]

#--------------------------------

def Translate(text, langCombo):
    if re.search(r'\w', text) is None: return [text for n in targetLangs]
    firstLetter = re.search(r'\w', text).group()
    resp = requests.get(
        urlTrad,
        params = {
            'key': apiTradKey,
            'lang': langCombo,
            'text': text
            }
    )
    print(resp.status_code)
    if resp.status_code != 200:
        PrRed('Translation failed!')
        exit()
    translation = resp.json()['text'][0]
    try:
        firstLetterTranslated = re.search(r'\w', translation).group()
    except:
        firstLetterTranslated = ''
    if firstLetter.islower():
        translation = re.sub(r'\w', firstLetterTranslated.lower(), translation, count = 1)
    print(translation)
    return translation

#--------------------------------
    
def PrRed(skk):
    print('\033[91m {}\033[00m'.format(skk))

def PrYellow(skk):
    print('\033[93m {}\033[00m'.format(skk))

def PrGreen(skk):
    print('\033[92m {}\033[00m'.format(skk))

def PrLightPurple(skk):
    print('\033[94m {}\033[00m'.format(skk))

#--------------------------------

@click.group()
def root():
    """Traslation of DocFX source code"""
    init()
    global workTree
    if sourceDir.split('/')[0] not in os.listdir():
        PrRed('\nPath "' + sourceDir.split('/')[0] + '" has not been found!')
        exit()

    if sourceDir.split('/')[1] not in os.listdir(sourceDir.split('/')[0]):
        PrRed('\nPath "' + sourceDir + '" for source language has not been found!')
        exit()

    for lang in targetLangs:
        targetPaths.append(sourceDir.split('/')[0] + '/' + '_'.join(lang.split('-')).lower())

    try:
        repo = Repo(sourceDir.split('/')[0])
    except:
        PrRed('Repository not found!\n Initialize a Git repo at "' + sourceDir.split('/')[0] + '" and make the first commit.')
        re.purge
        exit()
    modifiedUnstaged = repo.index.diff(None)
    modifiedStaged = repo.index.diff('HEAD')
    allModified = modifiedStaged + modifiedUnstaged
    workTree = [n.a_blob.path for n in allModified if n.a_blob.path.split('/')[0] == '_'.join(sourceLang.split('-')).lower()] + repo.untracked_files

    # option = input(' Digite uma opção:\n [1] para traduzir arquivos modificados desde o último commit,\n [2] para traduzir todo o projeto, ou\n [Enter] para sair: ')

@root.command()
def diff():
    """Translation of modified files (work tree)"""
    if workTree:
        PrYellow('\n The following files will be added or overwritten in target languages:')
        for doc in workTree:
            if doc.split('/')[-1] in os.listdir(sourceDir + '/' + '/'.join(doc.split('/')[1:-1])):
                stats.append(FileStats(sourceDir.split('/')[0] + '/' + doc))
                PrLightPurple(sourceDir.split('/')[0] + '/' + doc)
            else:
                PrYellow(sourceDir.split('/')[0] + '/' + doc + ' will be deleted in target languages.')
        fls = list(filter(lambda x: x is not None, stats))
        for i in range(len(fls)):
            reqs += fls[i][0]
            chars += fls[i][1]
        estimatedT = int(reqs*.7)
        print('\n Target languages:\t\t\t' + ', '.join(targetLangs))
        print(' Total of calls to be made to the machine translation service:\t' + str(reqs))
        print(' Total of characters to be sent to the machine translation service:\t' + str(chars))
        print(' Estimated process duration:\t\t' + str(datetime.timedelta(seconds = estimatedT)))
        cont = input('\n Continue [c] or abort [Enter]? ')
        if cont == 'c':
            for doc in workTree:
                if doc.split('/')[-1] in os.listdir(sourceDir + '/' + '/'.join(doc.split('/')[1:-1])):
                    ProcessFiles(sourceDir.split('/')[0] + '/' + doc)
                else:
                    for path in targetPaths:
                        try:
                            os.remove(path + '/' + '/'.join(doc.split('/')[2:]))
                        except:
                            pass
            PrGreen('\n\n Completed successfully!')
    else:
        PrYellow('There are no changes since the last commit.')
    if cont != 'c': PrRed('\n\n Exiting...')
    time.sleep(1)

@root.command()
def all():
    """Translation of the entire DocFX project"""
    global processed
    global greenFlag
    while not processed:
        if greenFlag:
            for item in Path(sourceDir.split('/')[0]).iterdir():
                if item.name != sourceDir.split('/')[1] and item.name in list(map(lambda x: '_'.join(x.split('-')).lower(), targetLangs)) and item.is_dir():
                    shutil.rmtree(sourceDir.split('/')[0] + '/' + item.name)
            processed = True

        if greenFlag:
            for path in targetPaths:
                os.mkdir(path)
        for entry in Path(sourceDir).iterdir():
            if entry.is_dir():
                dirLevel2 = sourceDir + '/' + entry.name
                if greenFlag:
                    for path in targetPaths:
                        os.mkdir(path + '/' + entry.name)
                for entry2 in Path(dirLevel2).iterdir():
                    if entry2.is_dir():
                        tgSeg = '/' + entry.name + '/' + entry2.name
                        dirLevel3 = dirLevel2 + '/' + entry2.name
                        if greenFlag:
                            for path in targetPaths:
                                os.mkdir(path + tgSeg)
                        for entry3 in Path(dirLevel3).iterdir():
                            if entry3.is_dir():
                                tgSeg = '/' + entry.name + '/' + entry2.name + '/' + entry3.name
                                dirLevel4 = dirLevel3 + '/' + entry3.name
                                if greenFlag:
                                    for path in targetPaths:
                                        os.mkdir(path + tgSeg)
                                for entry4 in Path(dirLevel4).iterdir():
                                    if entry4.is_dir():
                                        tgSeg = '/' + entry.name + '/' + entry2.name + '/' + entry3.name + '/' + entry4.name
                                        dirLevel5 = dirLevel4 + '/' + entry4.name
                                        if greenFlag:
                                            for path in targetPaths:
                                                os.mkdir(path + tgSeg)
                                        for entry5 in Path(dirLevel5).iterdir():
                                            if not entry5.is_dir():
                                                if greenFlag:
                                                    ProcessFiles(dirLevel5 + '/' + entry5.name)
                                                else:
                                                    stats.append(FileStats(dirLevel5 + '/' + entry5.name))
                                    else:
                                        if greenFlag:
                                            ProcessFiles(dirLevel4 + '/' + entry4.name)
                                        else:
                                            stats.append(FileStats(dirLevel4 + '/' + entry4.name))
                            else:
                                if greenFlag:
                                    ProcessFiles(dirLevel3 + '/' + entry3.name)
                                else:
                                    stats.append(FileStats(dirLevel3 + '/' + entry3.name))
                    else:
                        if greenFlag:
                            ProcessFiles(dirLevel2 + '/' + entry2.name)
                        else:
                            stats.append(FileStats(dirLevel2 + '/' + entry2.name))
            else:
                if greenFlag:
                    ProcessFiles(sourceDir + '/' + entry.name)
                else:
                    stats.append(FileStats(sourceDir + '/' + entry.name))
        
        if not greenFlag:
            fls = list(filter(lambda x: x is not None, stats))
            nFls = len(fls)*len(targetLangs)
            print('\n Target languages:\t\t\t' + ', '.join(targetLangs))
            print(' Total of source language files:\t' + str(len(fls)))
            for i in range(len(fls)):
                reqs += fls[i][0]
                chars += fls[i][1]
            estimatedT = int(reqs*.7)
            print(' Total of source language characters:\t' + str(chars))
            print(' Total of target language files to be generated:\t' + str(nFls))
            print(' Total of calls to be made to the machine translation service:\t' + str(reqs))
            print(' Total of characters to be sent to the machine translation service:\t' + str(chars))
            print(' Estimated process duration:\t\t' + str(datetime.timedelta(seconds = estimatedT)))
            cont = input('\n Continue [c] or abort [Enter]? ')
            if cont == 'c':
                greenFlag = True
            else:
                break

    if greenFlag:
        PrGreen('\n\n Completed successfully!')
    else:
        PrRed('\n\n Exiting...')
    time.sleep(1)

re.purge()
