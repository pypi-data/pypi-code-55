import os
import re
import datetime as dt
import pandas as pd
# import ntpath


def checkdirexists(dirname):
    if not os.path.isdir(dirname):
        try:
            os.mkdir(dirname)
            print("Successfully created the directory {} ".format(dirname))
        except OSError:
            print("Creation of the directory {} failed".format(dirname))
            os.system('pause')
    else:
        print("Directory {} exists".format(dirname))


def checklegendexists(dirname):
    legendexists = os.path.isfile(os.path.join(dirname, "legend.txt"))
    if not legendexists:
        try:
            legend = open(os.path.join(dirname, "legend.txt"), 'w')
            # include all exercises - update as required.
            L = ['PistolSquats:PS\n', 'Benchpress:BP\n', 'Pushups:PU\n', 'Planks:PL\n',
                 'Jogging/Running:Rn\n', 'Pullups:Pu\n', 'Situps:Su\n', 'Crunches:Cr\n',
                 'BicepCurlAlternating:BCA\n', 'BicepCurlSimultaneous:BCS\n', 'LateralShoulderRaise:LRS\n',
                 'Squats:SQ\n', 'Grippers:Gr\n', 'SteelbowGroinSqueeze:SBG\n', 'BullworkerLatissimusDorsi:BullLD\n']
            L.sort()
            legend.writelines(L)
            legend.close()
            print("Successfully created the file {} ".format(os.path.join(dirname, "legend.txt")))
        except Exception as ex:
            print("Creation of file legend.txt failed; error {}".format(str(ex)))
    else:
        print('legend.txt exists')


def checkconfigexists(dirname, currentdir, ext):
    defaultsexists = os.path.isfile(os.path.join(dirname, "config.txt"))
    if not defaultsexists:
        try:
            defaults = open(os.path.join(dirname, "config.txt"), 'w')
            L = ['Logging_Resolution=Day\n',
                 'Logging_to_File=None\n',
                 f'Default_Directory={currentdir}\n',
                 f'Logging_Extension={ext}\n',
                 'Cache_Period=Forever\n'  # Default cache period of 30 days --> call a cache check thru 'log' function
                 'Favourite_Folder=None\n'
                 'BodyHealth_File=None\n'
                 'BodyHealth_Directory=None\n']
            defaults.writelines(L)
            defaults.close()
            print("Successfully created the file {} ".format(os.path.join(dirname, "config.txt")))
            print('Initialised logging resolution as "Day".')
            print(f'Initialised directory path: {currentdir}. ')
            print(f'Initialised default extension as "{ext}".')
            print('Initialised default cache period as "Forever".')
        except Exception as ex:
            print("Creation of file config.txt failed; error {}".format(str(ex)))
    else:
        print('config.txt exists')


def checkbodyhealthpersonalinfoexists(dirname, personalNAME):
    bodyinfoexists = os.path.isfile(os.path.join(dirname, "BodyHealthPersonalInfo.txt"))
    if not bodyinfoexists:
        try:
            bodyinfo = open(os.path.join(dirname, "BodyHealthPersonalInfo.txt"), 'w')
            L = [f'Name:{personalNAME}\n', 'Gender:Unfilled\n', 'DateOfBirth:Unfilled\n']
            L.sort()
            bodyinfo.writelines(L)
            bodyinfo.close()
            print("Successfully created the file {} ".format(os.path.join(dirname, "BodyHealthPersonalInfo.txt")))
        except Exception as ex:
            print("Creation of file BodyHealthPersonalInfo.txt failed; error {}".format(str(ex)))
    else:
        print('BodyHealthPersonalInfo.txt exists')


def createnewfile(selectedfilename, fileextension, dirname, ancillarydir):
    print(f'{selectedfilename}{fileextension} does not exist. Creating and selecting file...')
    if fileextension == '.txt':
        createdfile = open(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}"),
                           'w')
        createdfile.close()
    elif fileextension == '.csv':
        csvcolumns = ['Time', 'Exercise', 'Repetitions', 'Weight(kilograms)', 'Duration', 'DoneBy', 'AdditionalNotes',
                      'CreatedByComputer']
        csvfile = pd.DataFrame(columns=csvcolumns)
        csvfile.to_csv(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}"))

    file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
    fileoverwrite = file1.readlines()
    file1.close()
    fileoverwrite[1] = f'Logging_to_File={selectedfilename}\n'
    with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
        selectedfile.writelines(fileoverwrite)
    print(f'{selectedfilename}{fileextension} created and selected')


def loaddestinationfile(dirname, ancillarydir):
    print(f'Logging directory selected: {dirname}')
    defaults = open(os.path.join(ancillarydir, "config.txt"), 'r').readlines()
    destinationfile = defaults[1].strip('\n').split('=')[1]
    fileextension = defaults[3].strip('\n').split('=')[1]  # get file extension
    print(f'File extension chosen is "{fileextension}"; any file created/selected must have the stated extension.')
    if not os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{destinationfile}{fileextension}")):
        print('No logging file selected. Files in MainLogFile folder of selected directory: \n')
        selecteddir = os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], 'ExerciseTerminalLogFiles', 'ExerciseLogs')
        files = [f for f in os.listdir(selecteddir) if os.path.isfile(os.path.join(selecteddir, f))]
        print('\n'.join(files))

        selectedfilename = input(f'\nSelect your file; this file must have the file extension "{fileextension}". \n'
                                 'To select a file, type in its name WITHOUT THE EXTENSION. If file does not exists, '
                                 'or if the extensions do not match, a new file will be created with the file extension'
                                 f'{fileextension}.'
                                 '(it is recommended to name the file after the person whose activities are logged):'
                                 '\n\n')
        if selectedfilename and os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}")):
            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            file1.close()
            fileoverwrite[1] = f'Logging_to_File={selectedfilename}\n'
            with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
                selectedfile.writelines(fileoverwrite)
            print(f'{selectedfilename}{fileextension} selected. ')
        elif selectedfilename and not os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}")):
            print(f'{selectedfilename}{fileextension} does not exist. Creating and selecting file...')
            if fileextension == '.txt':
                createdfile = open(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}"), 'w')
                createdfile.close()
            elif fileextension == '.csv':
                csvcolumns = ['Time', 'Exercise', 'Repetitions', 'Weight(kilograms)', 'Duration', 'DoneBy', 'AdditionalNotes', 'CreatedByComputer']
                csvfile = pd.DataFrame(columns=csvcolumns)
                csvfile.to_csv(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}"))

            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[1] = f'Logging_to_File={selectedfilename}\n'
            with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
                selectedfile.writelines(fileoverwrite)
            print(f'{selectedfilename}{fileextension} created and selected')
        elif not selectedfilename:
            print('No input. Please try again.')
    else:
        if os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{destinationfile}{fileextension}")):
            print(f'Logging file selected: {destinationfile}{fileextension}')
        else:
            print('Selected logging file does not exist. ')
            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[1] = f'Logging_to_File=None\n'
            selectedfile = open(os.path.join(ancillarydir, "config.txt"), 'w+')
            selectedfile.writelines(fileoverwrite)
            selectedfile.close()
            loaddestinationfile(dirname, ancillarydir)  # after overwriting default logging file, call loaddestination again.


def loadbodyhealthfile(ancillarydir):
    # print(f'Logging directory selected: {dirname}')
    config = open(os.path.join(ancillarydir, "config.txt"), 'r').readlines()
    bodyhealthfile = config[6].strip('\n').split('=')[1]
    personalbodyhealthdir = config[7].strip('\n').split('=')[1]
    if not os.path.isfile(os.path.join(personalbodyhealthdir, f'{bodyhealthfile}.csv')):
        print(f'No BodyHealth logging file selected. Files in {personalbodyhealthdir} folder: \n')
        files = [f for f in os.listdir(personalbodyhealthdir) if f.endswith('.csv')]
        print('\n'.join(files))

        selectedfilename = input(f'\n\nSelect your file; '
                                 'to select a file, type in its name WITHOUT THE EXTENSION. If file does not exists, '
                                 'or if the extensions do not match, a new ".csv" file will be created with the '
                                 'input filename. '
                                 '(it is recommended to name the file after the person whose activities are logged):'
                                 '\n\n')
        if selectedfilename and os.path.isfile(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv")):
            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[6] = f'BodyHealth_File={selectedfilename}\n'
            with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
                selectedfile.writelines(fileoverwrite)
            print(f'{selectedfilename}.csv selected. ')
        elif selectedfilename and not os.path.isfile(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv")):
            print(f'{selectedfilename}.csv does not exist. Creating and selecting file...')
            csvcolumns = ['ltime', 'Name', 'Gender', 'Age', 'Weight(kilograms)', 'Height(metres)', 'Waist-Circumference(metres)', 'BMI', 'RFM']
            csvfile = pd.DataFrame(columns=csvcolumns)
            csvfile.to_csv(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv"))

            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[6] = f'BodyHealth_File={selectedfilename}\n'
            with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
                selectedfile.writelines(fileoverwrite)
            print(f'{selectedfilename}.csv selected. ')
        elif not selectedfilename:
            print('No input. Please try again.')
    else:
        if os.path.isfile(os.path.join(personalbodyhealthdir, f'{bodyhealthfile}.csv')):
            print(f'Logging file selected: {bodyhealthfile}.csv')
        else:
            print('Selected logging file does not exist. ')
            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[6] = f'BodyHealth_File=None\n'
            selectedfile = open(os.path.join(ancillarydir, "config.txt"), 'w+')
            selectedfile.writelines(fileoverwrite)
            selectedfile.close()
            loaddestinationfile(ancillarydir)  # after overwriting default logging file, call loaddestination again.


def loadbodyhealthfile2(ancillarydir):
    # print(f'Logging directory selected: {dirname}')
    config = open(os.path.join(ancillarydir, "config.txt"), 'r').readlines()
    # bodyhealthfile = config[6].strip('\n').split('=')[1]
    personalbodyhealthdir = config[7].strip('\n').split('=')[1]
    print(f'Files in {personalbodyhealthdir} folder: \n')
    files = [f for f in os.listdir(personalbodyhealthdir) if f.endswith('.csv')]
    print('\n'.join(files))

    selectedfilename = input(f'\n\nSelect your file; '
                             'to select a file, type in its name WITHOUT THE EXTENSION. If file does not exists, '
                             'or if the extensions do not match, a new ".csv" file will be created with the '
                             'input filename. '
                             '(it is recommended to name the file after the person whose activities are logged):'
                             '\n\n')
    if selectedfilename and os.path.isfile(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv")):
        file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
        fileoverwrite = file1.readlines()
        fileoverwrite[6] = f'BodyHealth_File={selectedfilename}\n'
        with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
            selectedfile.writelines(fileoverwrite)
        print(f'{selectedfilename}.csv selected. ')
    elif selectedfilename and not os.path.isfile(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv")):
        print(f'{selectedfilename}.csv does not exist. Creating and selecting file...')
        csvcolumns = ['ltime', 'Name', 'Gender', 'Age', 'Weight(kilograms)', 'Height(metres)', 'Waist-Circumference(metres)', 'BMI', 'RFM']
        csvfile = pd.DataFrame(columns=csvcolumns)
        csvfile.to_csv(os.path.join(personalbodyhealthdir, f"{selectedfilename}.csv"))

        file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
        fileoverwrite = file1.readlines()
        fileoverwrite[6] = f'BodyHealth_File={selectedfilename}\n'
        with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
            selectedfile.writelines(fileoverwrite)
        print(f'{selectedfilename}.csv selected. ')
    elif not selectedfilename:
        print('No input. Please try again.')


# call without decorator
def createnewexercise_nodecorator(exercisename, acronym):
    legend1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'r').readlines()
    findexercise = re.compile(exercisename)
    findacronym = re.compile(acronym)

    # check if exercise and acronym exists
    for i in legend1:
        if findexercise.match(i.split(':')[0]):
            print("Exercise already exists! Please try again. ")
            return
        else:
            pass

    for v in legend1:
        if findacronym.match(v.split(':')[1].strip('\n')):
            print("Acronym already exists! Please try again.")
        else:
            pass

    # amendfile
    amendingline = f'{exercisename}:{acronym}\n'
    legend2 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'a')
    legend2.write(amendingline)
    legend2.close()
    print('Exercise successfully added to legend.txt! ')

    # sort legend.txt
    sorting = input('Do you want to sort legend.txt alphabetically? y/n: ')
    if sorting == 'y':
        print('Sorting file alphabetically...')
        legend3 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'r')
        fileoverwrite = legend3.readlines()
        legend3.close()
        fileoverwrite.sort()
        overwrite = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
        overwrite.writelines(fileoverwrite)
        overwrite.close()
        print('File sorted.')
    else:
        pass

    return exercisename


# check cache and clear any files if required
def checkcache(cacheperiod, maindir):
    print('Checking if cache exists...')
    cachedir = os.path.join(maindir, "cache")
    checkdirexists(cachedir)
    for root, dirs, files in os.walk(cachedir, topdown=True):
        for file in files:
            if dt.datetime.now() - dt.datetime.utcfromtimestamp(os.path.getctime(os.path.join(cachedir, file))) > dt.timedelta(days=int(cacheperiod)):
                os.remove(os.path.join(cachedir, file))
            else:
                pass
    print('Cache cleared.')


def caching(filename, filecontents, fileextension, maindir):
    print('Checking if cache exists...')
    cachedir = os.path.join(maindir, "cache")
    checkdirexists(cachedir)
    print('Caching files...')
    if fileextension == '.txt':
        tocache = filecontents
        tocachex = open(os.path.join(cachedir, f'{filename}_{dt.datetime.now().strftime("%d%m%Y-%H%M%S")}.txt'), 'w')
        tocachex.writelines(tocache)
        tocachex.close()
        print('Cache complete.')
    elif fileextension == '.csv':
        tocache = filecontents
        tocache.to_csv(os.path.join(cachedir, f'{filename}_{dt.datetime.now().strftime("%d%m%Y-%H%M%S")}.csv'))

