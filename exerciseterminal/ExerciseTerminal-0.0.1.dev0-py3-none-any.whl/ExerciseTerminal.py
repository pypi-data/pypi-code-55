import os
import datetime as dt
import pandas as pd
from exerciseterminal import CreateRequiredFiles
import click
import getpass
import re
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


def validate_timeddmmyyyyhhmm(ctx, param, value):
    try:
        ddmmyyyy_HHMM = re.compile('^\d{8}-\d{4}$')
        HHMM = re.compile('^\d{4}$')
        if value == "now":
            return value
        elif ddmmyyyy_HHMM.match(value):
            timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', value)
            if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                    timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                    timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                    timeerror.group(5)) > 59:
                raise ValueError(value)
            else:
                return value
        elif HHMM.match(value):
            timeerror = re.match('^(\d\d)(\d\d)$', value)
            if int(timeerror.group(1)) > 23 or int(timeerror.group(2)) > 59:
                raise ValueError(value)
            else:
                return value
    except (ValueError, AttributeError):
        raise click.BadParameter(f'Log time specified was not in the correct format. Specify time as either \n'
                                '(1) "now" - time of logging set to time command received. \n'
                                '(2) "ddmmyyyy-HHMM" - time of logging set to specified time. \n'
                                '(3) HHMM - time of logging set to specified time with date set to today.')


@click.command()
@click.option('-l', '--log-time', callback=validate_timeddmmyyyyhhmm, default='now', help= 'Log at specified time: '
                                         '(1) "now" - time of logging set to time command received. '
                                         '(2) "ddmmyyyy-HHMM" - time of logging set to specified time. '
                                         '(3) HHMM - time of logging set to specified time with date set to today. ', required=True, type=str)
def log(log_time):
    try:
        dirname = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1]
        logfilename = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[1].strip('\n').split('=')[1]
        fileextension = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[3].strip('\n').split('=')[1]
    except FileNotFoundError as ex:
        raise Exception(f'Error: {str(ex)}; call "initdir" to initialise directories first. ')

    if not os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}{fileextension}")):
        print('No file name set. You should call  "initdir" (recommended) or "setlogfile" to update the selected '
              'filename. ')
        return

    username = getpass.getuser()
    if '_' in username:
        username = '-'.join(username.split('_'))  # remove all underscores from username.
    print('User {} creating log...'.format(username))
    timenow = dt.datetime.now().strftime("%d%m%Y-%H%M")
    print('Logging command received at {}'.format(timenow))

    # check cache
    checkandclearcache()

    dividerstart = '[START]'
    dividerend = '[END]\n'
    ddmmyyyy_HHMM = re.compile('^\d{8}-\d{4}$')
    HHMM = re.compile('^\d{4}$')

    # rewrite config file - directory&logfile; get saved extension for file-handling
    configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
    configupdate[1] = f'Logging_to_File={logfilename}\n'
    configupdate[2] = f'Default_Directory={dirname}\n'
    # fileextension = configupdate[3].strip('\n').split('=')[1]  # get extension for filehandling
    configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
    configupdatex.writelines(configupdate)
    configupdatex.close()

    # time
    if log_time == "now":
        time = timenow
    elif ddmmyyyy_HHMM.match(log_time):
        time = log_time
    elif HHMM.match(log_time):
        time = f'{timenow.split("-")[0]}-{log_time}'
    else:
        raise Exception('log time specified was not in the correct format. Specify time as either \n'
                        '(1) "now" - time of logging set to time command received. \n'
                        '(2) "ddmmyyyy-HHMM" - time of logging set to specified time. \n'
                        '(3) HHMM - time of logging set to specified time with date set to today.')

    if fileextension == '.txt':
        # logfilename is log file name
        # fileextension is extension
        loadlog = open(os.path.join(
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}.txt"), 'r').readlines()
        if loadlog:
            h, ii, j, k, l, m = loadlog[-1].split('_')
            exercise = ii.split(':')[1]
            reps = j.split(':')[1].split('/')[0]
            weight = j.split(':')[1].split('/')[1]
            duration = j.split(':')[1].split('/')[2]
            doneby = k.split(':')[1]

            # find exercise acronym
            legend = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                'r').readlines()
            acronym = 0
            regexname = re.compile(f'^{exercise}$')
            for i in legend:
                if regexname.match(i.split(':')[0]):
                    acronym = i.strip("\n").split(":")[1]
                    break
            if acronym == 0:
                raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                'Please check legend and manually correct the log file. ')
            # exercise
            exerciseM = click.prompt('Specify exercise in acronym form', type=str, default=acronym)
            findexercise = re.compile(f'^{exerciseM}$')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                          'r').readlines()
            for i in legend:
                if findexercise.match(i.strip('\n').split(':')[1]):
                    selectedexercise: str = i.split(':')[0]
                    break
            try:
                selectedexercise  # error used to show exercise not found
            except UnboundLocalError:
                exercisenotfound = input('Error: acronym does not match any exercise compiled in "legend.txt". '
                                         f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                if exercisenotfound == 'y':
                    newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                    newacronym = exerciseM
                    selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename, newacronym)
                    # createnewexercise()
                else:
                    return

            # repetitions
            def validate_repetitions(value):
                try:
                    if int(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int,
                                        default=reps)

            # weight
            def validate_weight(value):
                try:
                    if float(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    if value in ('NA', 'na', 'Na', 'na'):
                        pass
                    else:
                        raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight,
                                   type=float, default=weight)

            # duration
            def validate_duration(value):
                try:
                    prog = re.compile(
                        '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                    if prog.match(value):
                        return value
                    else:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), "
                                             "m-minute(s), s-second(s); or input 'NA' for none", param=value)
                    return value
            durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str, default=duration)

            # doneby
            def validate_doneby(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            donebyM = click.prompt('Who was the exercise done by', value_proc=validate_doneby, type=str,
                                   default=doneby)

            # notes
            def validate_notes(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            additionalnotesM = click.prompt('Type additional notes',
                                            value_proc=validate_notes, type=str, default='NA')

        else:  # for new file, if loadlog is empty
            # exercise
            exerciseM = click.prompt('Specify exercise in acronym form', type=str)
            findexercise = re.compile(f'^{exerciseM}$')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                          'r').readlines()
            for i in legend:
                if findexercise.match(i.strip('\n').split(':')[1]):
                    selectedexercise: str = i.split(':')[0]
                    break
            try:
                selectedexercise  # error used to show exercise not found
            except UnboundLocalError:
                exercisenotfound = input('Error: acronym does not match any exercise compiled in "legend.txt". '
                                         f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                if exercisenotfound == 'y':
                    newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                    newacronym = exerciseM
                    selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename, newacronym)
                    # createnewexercise()
                else:
                    return

            # repetitions
            def validate_repetitions(value):
                try:
                    if int(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int)

            # weight
            def validate_weight(value):
                try:
                    if float(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    if value in ('NA', 'na', 'Na', 'na'):
                        pass
                    else:
                        raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight,
                                   type=float)

            # duration
            def validate_duration(value):
                try:
                    prog = re.compile(
                        '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                    if prog.match(value):
                        return value
                    else:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), "
                                             "m-minute(s), s-second(s); or input 'NA' for none", param=value)
                    return value
            durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str)

            # doneby
            def validate_doneby(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            donebyM = click.prompt('Who was the exercise done by', value_proc=validate_doneby, type=str)

            # notes
            def validate_notes(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            additionalnotesM = click.prompt('Type additional notes',
                                            value_proc=validate_notes, type=str, default='NA')

    elif fileextension == '.csv':
        loadlog = pd.read_csv(os.path.join(open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip(
            '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}.csv"))
        # fill nan with 'NA' string
        loadlog.fillna('NA', inplace=True)
        # loadlog.drop(csvlogging.columns[0], axis=1, inplace=True)
        if loadlog.empty:
            # exercise
            exerciseM = click.prompt('Specify exercise in acronym form', type=str)
            findexercise = re.compile(f'^{exerciseM}$')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                          'r').readlines()
            for i in legend:
                if findexercise.match(i.strip('\n').split(':')[1]):
                    selectedexercise: str = i.split(':')[0]
                    break
            try:
                selectedexercise  # error used to show exercise not found
            except UnboundLocalError:
                exercisenotfound = input('Error: acronym does not match any exercise compiled in "legend.txt". '
                                         f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                if exercisenotfound == 'y':
                    newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                    newacronym = exerciseM
                    selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename, newacronym)
                    # createnewexercise()
                else:
                    return

            # repetitions
            def validate_repetitions(value):
                try:
                    if int(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int)

            # weight
            def validate_weight(value):
                try:
                    if float(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    if value in ('NA', 'na', 'Na', 'na'):
                        pass
                    else:
                        raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight,
                                   type=float)

            # duration
            def validate_duration(value):
                try:
                    prog = re.compile(
                        '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                    if prog.match(value):
                        return value
                    else:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), "
                                             "m-minute(s), s-second(s); or input 'NA' for none", param=value)
                    return value
            durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str)

            # doneby
            def validate_doneby(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            donebyM = click.prompt('Who was the exercise done by', value_proc=validate_doneby, type=str)

            # notes
            def validate_notes(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            additionalnotesM = click.prompt('Type additional notes',
                                            value_proc=validate_notes, type=str, default='NA')

        else:
            exercise = loadlog['Exercise'].iloc[-1]
            reps = loadlog['Repetitions'].iloc[-1]
            weight = loadlog['Weight(kilograms)'].iloc[-1]
            duration = loadlog['Duration'].iloc[-1]
            doneby = loadlog['DoneBy'].iloc[-1]

            # find exercise acronym
            legend = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                'r').readlines()
            acronym = 0
            regexname = re.compile(f'^{exercise}$')
            for i in legend:
                if regexname.match(i.split(':')[0]):
                    acronym = i.strip("\n").split(":")[1]
                    break
            if acronym == 0:
                raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                'Please check legend and manually correct the log file. ')

            # exercise
            exerciseM = click.prompt('Specify exercise in acronym form', type=str, default=acronym)
            findexercise = re.compile(f'^{exerciseM}$')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                          'r').readlines()
            for i in legend:
                if findexercise.match(i.strip('\n').split(':')[1]):
                    selectedexercise: str = i.split(':')[0]
                    break
            try:
                selectedexercise  # error used to show exercise not found
            except UnboundLocalError:
                exercisenotfound = input('Error: acronym does not match any exercise compiled in "legend.txt". '
                                         f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                if exercisenotfound == 'y':
                    newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                    newacronym = exerciseM
                    selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename, newacronym)
                    # createnewexercise()
                else:
                    return

            # repetitions
            def validate_repetitions(value):
                try:
                    if int(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int,
                                        default=reps)

            # weight
            def validate_weight(value):
                try:
                    if float(value) < 0:
                        raise ValueError(value)
                except ValueError:
                    if value in ('NA', 'na', 'Na', 'na'):
                        pass
                    else:
                        raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                return value
            weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight,
                                   type=float, default=weight)

            # duration
            def validate_duration(value):
                try:
                    prog = re.compile(
                        '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                    if prog.match(value):
                        return value
                    else:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter(
                        "Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), m-minute(s), s-second(s); or input 'NA' for none",
                        param=value)
                    return value
            durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str,
                                     default=duration)

            # doneby
            def validate_doneby(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            donebyM = click.prompt('Who was the exercise done by', value_proc=validate_doneby, type=str,
                                   default=doneby)

            # notes
            def validate_notes(value):
                try:
                    if '_' in value:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Cannot have '_' in string", param=value)
                return value
            additionalnotesM = click.prompt('Type additional notes',
                                            value_proc=validate_notes, type=str, default='NA')
    else:
        raise Exception('Error: file extension not found in config.txt. Call "initdir".')

    if fileextension == '.txt':
        logcreation = f'{dividerstart}' \
                      f'Time:{time}_' \
                      f'Exercise:{selectedexercise}_' \
                      f'Repetitions/Weight(kilograms)/Duration:{repetitionsM}/{weightM}/{durationM}_' \
                      f'DoneBy:{donebyM}_' \
                      f'AdditionalNotes:{additionalnotesM}_' \
                      f'CreatedByComputer:{username}' \
                      f'{dividerend}'
        try:
            with open(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}.txt"), 'a') as logging:
                logging.write(logcreation)
            print(f"logging successful: \n\n{logcreation}")
        except FileNotFoundError as ex:
            print(f'Error, file not found; try calling the "initdir" function first: {str(ex)}')
        except NameError as ex:
            print(f'Error, directory name not found; try calling the "initdir" function first: {str(ex)}')
    elif fileextension == '.csv':
        logcolumns = ['Time', 'Exercise', 'Repetitions', 'Weight(kilograms)', 'Duration', 'DoneBy', 'AdditionalNotes', 'CreatedByComputer']
        csvlog = pd.DataFrame(columns=logcolumns)
        csvlog.loc[0] = time, selectedexercise, repetitionsM, weightM, durationM, donebyM, additionalnotesM, username
        try:
            csvlogging = pd.read_csv(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}.csv"))
            csvlogging = csvlogging.append(csvlog.iloc[0])
            csvlogging.drop(csvlogging.columns[0], axis=1, inplace=True)
            # csvlogging.reset_index()
            csvlogging.to_csv(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfilename}.csv"))
            print(f"logging successful: \n\n{csvlog}")
        except FileNotFoundError as ex:
            print(f'Error (file not found): file not found; try calling the "initdir" function first: {str(ex)}')
        except NameError as ex:
            print(f'Error (name error): directory name not found; try calling the "initdir" function first: {str(ex)}')
        except PermissionError as ex:
            print(f'Error (permission error): please close the file if it is currently open and try again: {str(ex)}.')


@click.command()
@click.argument('modify', default=1)
def deletelog(modify):
    if modify == 1:
        # check cache
        maindir = checkandclearcache()

        logfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[1].strip('\n').split('=')[1]
        logextension = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[3].strip('\n').split('=')[1]
        prompt = input(f'Are you sure you want to modify the selected log file "{logfile}{logextension}"? [y/N]: ')
        if logextension == '.txt':
            if prompt == 'y':
                log = open(os.path.join(
                    open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
                modifydatetime = input('Input date and time of the log to delete (format "ddmmyyyy-HHMM") or '
                                       'input "prev" to delete previously made log: ')
                if modifydatetime == 'prev':
                    try:
                        prompt2 = input(f"Delete following log? \n\n{log[-1]}\n [y/N]: ")
                        if prompt2 == 'y':
                            # first cache the file
                            CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                            # then continue with deleting file
                            log = log[:-1]
                            overwrite = open(os.path.join(open(os.path.join(os.path.dirname(
                                os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split(
                                '=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                            overwrite.writelines(log)
                            overwrite.close()
                            print('Log deleted. check file now.')
                        else:
                            print('Aborted process!')
                    except IndexError as ex:
                        print(f'Error: log file empty. IndexError raised: {str(ex)} ')
                else:
                    # check if queried time input is valid --> raise exception for invalid input!
                    timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', modifydatetime)
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59:
                        raise Exception('Error: incorrect date given. Please check date and try again. ')
                    else:
                        pass

                    # this part deals with multiple logs at same timing.
                    placeholder = []
                    for i in range(len(log)):
                        if modifydatetime == log[i].split('_')[0].split(':')[1]:
                            placeholder.append(i)
                    if not placeholder:
                        print('No log found. Please try again. ')
                        return
                    else:
                        if len(placeholder) == 1:
                            prompt3 = input(f"Delete following log? \n{log[placeholder[0]]}\n [y/N]: ")
                            if prompt3 == 'y':
                                # first cache the file
                                CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                # then continue with deleting file
                                log.pop(placeholder[0])
                                overwrite = open(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                                overwrite.writelines(log)
                                overwrite.close()
                                print('Log deleted. check file now.')
                            else:
                                print('Aborted process!')
                        else:
                            print(f'Multiple logs with log time {modifydatetime} found: ')
                            for i in range(len(placeholder)):
                                print(log[placeholder[i]])
                            try:
                                chooselog = int(input('Select index of log to be deleted (ie, input "0" for first '
                                                      'log by order of printing, "1" for second... etc.): '))
                            except ValueError:
                                print("Invalid input. Please type integer number reflecting the position of the "
                                      "intended log by order of printing.")
                                return
                            try:
                                prompt4 = input(f"Delete following log? \n{log[placeholder[chooselog]]}\n [y/N]: ")
                                if prompt4 == 'y':
                                    # first cache the file
                                    CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                    # then continue with deleting file
                                    log.pop(placeholder[chooselog])
                                    overwrite = open(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                                    overwrite.writelines(log)
                                    overwrite.close()
                                    print('Log deleted. check file now.')
                                else:
                                    print('Aborted process!')
                            except IndexError:
                                print("Invalid input. Number out of range. ")
                                return
            else:
                print('Aborted process!')

        elif logextension == '.csv':
            if prompt == 'y':
                log = pd.read_csv(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                # fill nan with 'NA' string
                log.fillna('NA', inplace=True)
                modifydatetime = input('Input date and time of the log to delete (format "ddmmyyyy-HHMM") or '
                                       'input "prev" to delete previously made log: ')
                if modifydatetime == 'prev':
                    try:
                        prompt2 = input(f"Delete following log? \n\n{log.iloc[-1]}\n [y/N]: ")
                        if prompt2 == 'y':
                            # first cache the file
                            log.drop(log.columns[0], axis=1, inplace=True)
                            CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                            # then continue with deleting file
                            log.drop(log.tail(1).index, inplace=True)  # drop last 1 row
                            log.to_csv(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                            print('Log deleted. check file now.')
                        else:
                            print('Aborted process!')
                    except IndexError as ex:
                        print(f'Error: log file empty. IndexError raised: {str(ex)} ')
                else:
                    # check if queried time input is valid --> raise exception for invalid input!
                    timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', modifydatetime)
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59:
                        raise Exception('Error: incorrect date given. Please check date and try again. ')
                    else:
                        pass
                    if log.loc[log['Time'] == modifydatetime].empty:
                        print('No log found. Please try again. ')
                        return
                    else:
                        if len(log.loc[log['Time'] == modifydatetime]) == 1:
                            log.drop(log.columns[0], axis=1, inplace=True)
                            prompt3 = input(f"Delete following log? \n{log.loc[log['Time'] == modifydatetime]}\n [y/N]: ")
                            if prompt3 == 'y':
                                # first cache the file
                                CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                # then continue with deleting file
                                log.drop(log.loc[log['Time'] == modifydatetime].index, inplace=True)
                                log.to_csv(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                                print('Log deleted. check file now.')
                            else:
                                print('Aborted process!')
                        else:
                            print(f'Multiple logs with log time {modifydatetime} found: ')
                            log.drop(log.columns[0], axis=1, inplace=True)
                            todelete = log.loc[log['Time'] == modifydatetime].copy()
                            todelete.reset_index(drop=True, inplace=True)
                            print(todelete)
                            try:
                                chooselog = int(input('Select index of log to be deleted (ie, input "0" for first '
                                                      'log by order of printing, "1" for second... etc. - '
                                                      'index is printed as above): '))
                            except ValueError:
                                print("Invalid input. Please type integer number reflecting the position of the "
                                      "intended log by order of printing.")
                                return
                            try:
                                prompt4 = input(f"Delete following log? \n{todelete.iloc[chooselog]}\n [y/N]: ")
                                if prompt4 == 'y':
                                    # first cache the file
                                    CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                    # then continue with deleting file
                                    log.drop(log.loc[log['Time'] == modifydatetime].iloc[chooselog].name, inplace=True)
                                    log.reset_index(drop=True, inplace=True)
                                    log.to_csv(os.path.join(open(
                                        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles',
                                                     "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1],
                                                            "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                                    print('Log deleted. check file now.')
                                else:
                                    print('Aborted process!')
                            except IndexError:
                                print("Invalid input. Number out of range. ")
            else:
                print('Aborted process!')
    else:
        raise Exception('Error: function called with incorrect arguments. Please try again. ')


@click.command()
@click.argument('mod', default=1)
def modifylog(mod):
    if mod == 1:
        # check cache
        maindir = checkandclearcache()
        logfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[1].strip('\n').split('=')[1]
        logextension = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[3].strip('\n').split('=')[1]
        modifydatetime = input('Input date and time of the log to modify (format "ddmmyyyy-HHMM") or '
                               'input "prev" to modify previously made log: ')
        if logextension == '.txt':
            log = open(os.path.join(
                open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                     'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
            if modifydatetime == 'prev':
                try:
                    if click.confirm(f'Do you want to Modify following log? \n\n{log[-1]}\n', abort=True):
                        # first cache the file
                        CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                        # then continue with modifying file
                        # split log up into constituents
                        h, ii, j, k, l, m = log[-1].split('_')
                        time = h.split(':')[1]
                        exercise = ii.split(':')[1]
                        repetitions = j.split(':')[1].split('/')[0]
                        weight = j.split(':')[1].split('/')[1]
                        duration = j.split(':')[1].split('/')[2]
                        doneby = k.split(':')[1]
                        additionalnotes = l.split(':')[1]
                        createdbycomputer = re.search('(.*)[[]\w{3}[]]', m.split(':')[1]).group(1)

                        dividerstart = '[START]'
                        dividerend = '[END]\n'

                        # time
                        def validate_time(value):
                            try:
                                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', value)
                                if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                                        timeerror.group(2)) <= 0 or int(
                                        timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                                        timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(
                                        timeerror.group(5)) < 0 or int(
                                        timeerror.group(5)) > 59:
                                    raise ValueError(value)
                            except (ValueError, AttributeError):
                                raise click.BadParameter("Invalid date input.", param=value)
                            return value
                        timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)', value_proc=validate_time, type=str, default=time)

                        ### find exercise acronym
                        legend = open(
                            os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                            'r').readlines()
                        acronym = 0
                        regexname = re.compile(f'^{exercise}$')
                        for i in legend:
                            if regexname.match(i.split(':')[0]):
                                acronym = i.strip("\n").split(":")[1]
                                break
                        if acronym == 0:
                            raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                            'Please check legend and manually correct the log file. ')
                        # prompt exercise
                        exerciseM = click.prompt(f'Exercise name "{exercise}" has acronym "{acronym}". \nPlease enter exercise acronym', type=str, default=acronym)

                        findexercise = re.compile(f'^{exerciseM}$')
                        legend = open(
                            os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                            'r').readlines()
                        for i in legend:
                            if findexercise.match(i.strip('\n').split(':')[1]):
                                selectedexercise: str = i.split(':')[0]
                                break
                        try:
                            selectedexercise  # error used to show exercise notfound
                        except UnboundLocalError:
                            exercisenotfound = input(
                                'Error: acronym does not match any exercise compiled in "legend.txt". '
                                f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                            if exercisenotfound == 'y':
                                newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                                newacronym = exerciseM
                                selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename,
                                                                                                     newacronym)
                            else:
                                return

                        #repetitions
                        def validate_repetitions(value):
                            try:
                                if int(value) < 0:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                            return value
                        repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int, default=repetitions)

                        #weight
                        def validate_weight(value):
                            try:
                                if float(value) < 0:
                                    raise ValueError(value)
                            except ValueError:
                                if value in ('NA', 'na', 'Na', 'na'):
                                    pass
                                else:
                                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                            return value
                        weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight, type=float, default=weight)

                        #duration
                        def validate_duration(value):
                            try:
                                prog = re.compile(
                                    '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                                if prog.match(value):
                                    return value
                                else:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), m-minute(s), s-second(s); or input 'NA' for none", param=value)
                                return value
                        durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str, default=duration)

                        #notes
                        def validate_notes(value):
                            try:
                                if '_' in value:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Cannot have '_' in string", param=value)
                            return value
                        additionalnotesM = click.prompt('Any additional notes', value_proc=validate_notes, type=str, default=additionalnotes)

                        #doneby and createdbycomputer(CBC)
                        def validate_donebyCBC(value):
                            try:
                                if '_' in value:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Cannot have '_' in string", param=value)
                            return value
                        donebyM = click.prompt('Who was the exercise done by', value_proc=validate_donebyCBC, type=str, default=doneby)
                        createdbycomputerM = click.prompt('Created by computer', value_proc=validate_donebyCBC, type=str, default=createdbycomputer)

                        logcreation = f'{dividerstart}' \
                                      f'Time:{timeM}_' \
                                      f'Exercise:{selectedexercise}_' \
                                      f'Repetitions/Weight(kilograms)/Duration:{repetitionsM}/{weightM}/{durationM}_' \
                                      f'DoneBy:{donebyM}_' \
                                      f'AdditionalNotes:{additionalnotesM}_' \
                                      f'CreatedByComputer:{createdbycomputerM}' \
                                      f'{dividerend}'

                        log[-1] = logcreation
                        overwrite = open(os.path.join(open(os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip(
                            '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                        overwrite.writelines(log)
                        overwrite.close()
                        print(f'log modified: \n\n{logcreation}\n')
                except IndexError as ex:
                    print(f'Error: log file empty. IndexError raised: {str(ex)} ')
                    return

            else:
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', modifydatetime)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59:
                        raise Exception('Error: invalid date format. Please check date input and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')

                # this part deals with multiple logs at same timing.
                placeholder = []
                for i in range(len(log)):
                    if modifydatetime == log[i].split('_')[0].split(':')[1]:
                        placeholder.append(i)
                if not placeholder:
                    print('No log found. Please try again. ')
                    return
                else:
                    if len(placeholder) == 1:
                        if click.confirm(f'Do you want to Modify following log? \n\n{log[placeholder[0]]}\n', abort=True):
                            # first cache the file
                            CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                            # then continue with modifying file
                            h, ii, j, k, l, m = log[placeholder[0]].split('_')
                            time = h.split(':')[1]
                            exercise = ii.split(':')[1]
                            repetitions = j.split(':')[1].split('/')[0]
                            weight = j.split(':')[1].split('/')[1]
                            duration = j.split(':')[1].split('/')[2]
                            doneby = k.split(':')[1]
                            additionalnotes = l.split(':')[1]
                            createdbycomputer = re.search('(.*)[[]\w{3}[]]', m.split(':')[1]).group(1)
                            chooselog = 0  # for logcreation

                    else:
                        print(f'Multiple logs with log time {modifydatetime} found: ')
                        for i in range(len(placeholder)):
                            print(log[placeholder[i]])
                        try:
                            chooselog = int(input('Select index of log to be modified (ie, input "0" for first '
                                                  'log by order of printing, "1" for second... etc.): '))
                        except ValueError:
                            print("Invalid input. Please type integer number reflecting the position of the "
                                  "intended log by order of printing.")
                            return
                        try:
                            if click.confirm(f'Do you want to Modify following log? \n\n{log[placeholder[chooselog]]}\n',
                                             abort=True):
                                # first cache the file
                                CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                # then continue with modifying file
                                h, ii, j, k, l, m = log[placeholder[chooselog]].split('_')
                                time = h.split(':')[1]
                                exercise = ii.split(':')[1]
                                repetitions = j.split(':')[1].split('/')[0]
                                weight = j.split(':')[1].split('/')[1]
                                duration = j.split(':')[1].split('/')[2]
                                doneby = k.split(':')[1]
                                additionalnotes = l.split(':')[1]
                                createdbycomputer = re.search('(.*)[[]\w{3}[]]', m.split(':')[1]).group(1)

                        except IndexError:
                            print("Invalid input. Number out of range. ")
                            return

                    dividerstart = '[START]'
                    dividerend = '[END]\n'

                    # time
                    def validate_time(value):
                        try:
                            timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', value)
                            if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                                    timeerror.group(2)) <= 0 or int(
                                    timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                                    timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(
                                    timeerror.group(5)) < 0 or int(
                                    timeerror.group(5)) > 59:
                                raise ValueError(value)
                        except (ValueError, AttributeError):
                            raise click.BadParameter("Invalid date input.", param=value)
                        return value

                    timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)', value_proc=validate_time, type=str, default=time)

                    ### find exercise acronym
                    legend = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                        'r').readlines()
                    acronym = 0
                    regexname = re.compile(f'^{exercise}$')
                    for i in legend:
                        if regexname.match(i.split(':')[0]):
                            acronym = i.strip("\n").split(":")[1]
                            break
                    if acronym == 0:
                        raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                        'Please check legend and manually correct the log file. ')
                    # prompt exercise
                    exerciseM = click.prompt(f'Exercise name "{exercise}" has acronym "{acronym}". \nPlease enter exercise acronym', type=str, default=acronym)

                    findexercise = re.compile(f'^{exerciseM}$')
                    legend = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                        'r').readlines()
                    for i in legend:
                        if findexercise.match(i.strip('\n').split(':')[1]):
                            selectedexercise: str = i.split(':')[0]
                            break
                    try:
                        selectedexercise  # error used to show exercise notfound
                    except UnboundLocalError:
                        exercisenotfound = input(
                            'Error: acronym does not match any exercise compiled in "legend.txt". '
                            f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                        if exercisenotfound == 'y':
                            newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                            newacronym = exerciseM
                            selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename,
                                                                                                 newacronym)
                        else:
                            return

                    #repetitions
                    def validate_repetitions(value):
                        try:
                            if int(value) < 0:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                        return value
                    repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int, default=repetitions)

                    #weight
                    def validate_weight(value):
                        try:
                            if float(value) < 0:
                                raise ValueError(value)
                        except ValueError:
                            if value in ('NA', 'na', 'Na', 'na'):
                                pass
                            else:
                                raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                        return value
                    weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight, type=float, default=weight)

                    #duration
                    def validate_duration(value):
                        try:
                            prog = re.compile(
                                '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                            if prog.match(value):
                                return value
                            else:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), m-minute(s), s-second(s); or input 'NA' for none", param=value)
                            # return value
                    durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str, default=duration)

                    #notes
                    def validate_notes(value):
                        try:
                            if '_' in value:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Cannot have '_' in string", param=value)
                        return value
                    additionalnotesM = click.prompt('Any additional notes', value_proc=validate_notes, type=str, default=additionalnotes)

                    #doneby and createdbycomputer(CBC)
                    def validate_donebyCBC(value):
                        try:
                            if '_' in value:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Cannot have '_' in string", param=value)
                        return value
                    donebyM = click.prompt('Who was the exercise done by', value_proc=validate_donebyCBC, type=str, default=doneby)
                    createdbycomputerM = click.prompt('Created by computer', value_proc=validate_donebyCBC, type=str, default=createdbycomputer)

                    logcreation = f'{dividerstart}' \
                                  f'Time:{timeM}_' \
                                  f'Exercise:{selectedexercise}_' \
                                  f'Repetitions/Weight(kilograms)/Duration:{repetitionsM}/{weightM}/{durationM}_' \
                                  f'DoneBy:{donebyM}_' \
                                  f'AdditionalNotes:{additionalnotesM}_' \
                                  f'CreatedByComputer:{createdbycomputerM}' \
                                  f'{dividerend}'

                    log[placeholder[chooselog]] = logcreation
                    overwrite = open(os.path.join(
                        open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles',
                                          "config.txt"),
                             'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                    overwrite.writelines(log)
                    overwrite.close()
                    print(f'log modified: \n\n{logcreation}\n')

        elif logextension == '.csv':
            log = pd.read_csv(os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip(
                '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
            # fill nan with 'NA' string
            log.fillna('NA', inplace=True)
            log.drop(log.columns[0], axis=1, inplace=True)
            pd.set_option('display.max_columns', None)  # print all columns
            pd.set_option('display.max_rows', None)  # print all rows
            if modifydatetime == 'prev':
                if log.empty:
                    print('Error: log file empty.')
                    return
                else:  # if log is NOT empty
                    if click.confirm(f'Do you want to Modify following log? \n\n{log.iloc[-1]}\n', abort=True):
                        # first cache the file
                        CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                        # then continue with modifying file
                        time = log['Time'].iloc[-1]
                        exercise = log['Exercise'].iloc[-1]
                        repetitions = log['Repetitions'].iloc[-1]
                        weight = log['Weight(kilograms)'].iloc[-1]
                        duration = log['Duration'].iloc[-1]
                        doneby = log['DoneBy'].iloc[-1]
                        additionalnotes = log['AdditionalNotes'].iloc[-1]
                        createdbycomputer = log['CreatedByComputer'].iloc[-1]

                        # time
                        def validate_time(value):
                            try:
                                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', value)
                                if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                                        timeerror.group(2)) <= 0 or int(
                                        timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                                        timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(
                                        timeerror.group(5)) < 0 or int(
                                        timeerror.group(5)) > 59:
                                    raise ValueError(value)
                            except (ValueError, AttributeError):
                                raise click.BadParameter("Invalid date input.", param=value)
                            return value

                        timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)', value_proc=validate_time, type=str, default=time)

                        #notes
                        def validate_notes(value):
                            try:
                                if '_' in value:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Cannot have '_' in string", param=value)
                            return value
                        additionalnotesM = click.prompt('Any additional notes', value_proc=validate_notes, type=str, default=additionalnotes)

                        ### find exercise acronym
                        legend = open(
                            os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                            'r').readlines()
                        acronym = 0
                        regexname = re.compile(f'^{exercise}$')
                        for i in legend:
                            if regexname.match(i.split(':')[0]):
                                acronym = i.strip("\n").split(":")[1]
                                break
                        if acronym == 0:
                            raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                            'Please check legend and manually correct the log file. ')
                        # prompt exercise
                        exerciseM = click.prompt(f'Exercise name "{exercise}" has acronym "{acronym}". \nPlease enter exercise acronym', type=str, default=acronym)

                        findexercise = re.compile(f'^{exerciseM}$')
                        legend = open(
                            os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                            'r').readlines()
                        for i in legend:
                            if findexercise.match(i.strip('\n').split(':')[1]):
                                selectedexercise: str = i.split(':')[0]
                                break
                        try:
                            selectedexercise  # error used to show exercise notfound
                        except UnboundLocalError:
                            exercisenotfound = input(
                                'Error: acronym does not match any exercise compiled in "legend.txt". '
                                f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                            if exercisenotfound == 'y':
                                newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                                newacronym = exerciseM
                                selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename,
                                                                                                     newacronym)
                            else:
                                return

                        #repetitions
                        def validate_repetitions(value):
                            try:
                                if int(value) < 0:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                            return value
                        repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int, default=repetitions)

                        #weight
                        def validate_weight(value):
                            try:
                                if float(value) < 0:
                                    raise ValueError(value)
                            except ValueError:
                                if value in ('NA', 'na', 'Na', 'na'):
                                    pass
                                else:
                                    raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                            return value
                        weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight, type=float, default=weight)

                        #duration
                        def validate_duration(value):
                            try:
                                prog = re.compile(
                                    '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                                if prog.match(value):
                                    return value
                                else:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), m-minute(s), s-second(s); or input 'NA' for none", param=value)
                                # return value
                        durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str, default=duration)

                        # doneby and createdbycomputer(CBC)
                        def validate_donebyCBC(value):
                            try:
                                if '_' in value:
                                    raise ValueError(value)
                            except ValueError:
                                raise click.BadParameter("Cannot have '_' in string", param=value)
                            return value
                        donebyM = click.prompt('Who was the exercise done by', value_proc=validate_donebyCBC, type=str, default=doneby)
                        createdbycomputerM = click.prompt('Created by computer', value_proc=validate_donebyCBC, type=str, default=createdbycomputer)

                        log.iloc[-1] = timeM, selectedexercise, repetitionsM, weightM, durationM, donebyM, additionalnotesM, createdbycomputerM
                        log.to_csv(os.path.join(
                            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles',
                                              "config.txt"),
                                 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                        print(f'log modified: \n\n{log.iloc[-1]}\n')
            else:
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', modifydatetime)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59:
                        raise Exception('Error: invalid date format. Please check date input and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')
                if log.empty:
                    print('Error: log file empty.')
                    return
                elif log.loc[log['Time'] == modifydatetime].empty:
                    print('No log found. Please try again. ')
                    return
                else:
                    if len(log.loc[log['Time'] == modifydatetime]) == 1:
                        if click.confirm(f'Do you want to Modify following log? \n\n{log.loc[log["Time"] == modifydatetime]}\n', abort=True):
                            # first cache the file
                            CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                            # then continue with modifying file
                            time = log.loc[log['Time'] == modifydatetime]['Time'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            exercise = log.loc[log['Time'] == modifydatetime]['Exercise'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            repetitions = log.loc[log['Time'] == modifydatetime]['Repetitions'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            weight = log.loc[log['Time'] == modifydatetime]['Weight(kilograms)'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            duration = log.loc[log['Time'] == modifydatetime]['Duration'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            doneby = log.loc[log['Time'] == modifydatetime]['DoneBy'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            additionalnotes = log.loc[log['Time'] == modifydatetime]['AdditionalNotes'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            createdbycomputer = log.loc[log['Time'] == modifydatetime]['CreatedByComputer'][log.loc[log['Time'] == modifydatetime]['Time'].index[0]]
                            chooselog = 0

                    else:  # if multiple logs at same time
                        print(f'Multiple logs with log time {modifydatetime} found: ')
                        # log.drop(log.columns[0], axis=1, inplace=True)
                        todelete = log.loc[log['Time'] == modifydatetime].copy()
                        todelete.reset_index(drop=True, inplace=True)
                        print(todelete)
                        try:
                            chooselog = int(input('Select index of log to be modified (ie, input "0" for first '
                                                  'log by order of printing, "1" for second... etc. - '
                                                  'index is printed as above): '))
                        except ValueError:
                            print("Invalid input. Please type integer number reflecting the position of the "
                                  "intended log by order of printing.")
                            return
                        try:
                            if click.confirm(
                                    f'Do you want to Modify following log? \n\n{todelete.iloc[chooselog]}\n',
                                    abort=True):
                                # first cache the file
                                CreateRequiredFiles.caching(logfile, log, logextension, maindir)
                                # then continue with modifying file
                                time = todelete['Time'][todelete.index[chooselog]]
                                exercise = todelete['Exercise'][todelete.index[chooselog]]
                                repetitions = todelete['Repetitions'][todelete.index[chooselog]]
                                weight = todelete['Weight(kilograms)'][todelete.index[chooselog]]
                                duration = todelete['Duration'][todelete.index[chooselog]]
                                doneby = todelete['DoneBy'][todelete.index[chooselog]]
                                additionalnotes = todelete['AdditionalNotes'][todelete.index[chooselog]]
                                createdbycomputer = todelete['CreatedByComputer'][todelete.index[chooselog]]

                        except IndexError:
                            print("Invalid input. Number out of range. ")

                    # time
                    def validate_time(value):
                        try:
                            timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', value)
                            if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                                    timeerror.group(2)) <= 0 or int(
                                    timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                                    timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(
                                    timeerror.group(5)) < 0 or int(
                                    timeerror.group(5)) > 59:
                                raise ValueError(value)
                        except (ValueError, AttributeError):
                            raise click.BadParameter("Invalid date input.", param=value)
                        return value

                    timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)', value_proc=validate_time, type=str, default=time)

                    # notes
                    def validate_notes(value):
                        try:
                            if '_' in value:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Cannot have '_' in string", param=value)
                        return value
                    additionalnotesM = click.prompt('Any additional notes', value_proc=validate_notes, type=str, default=additionalnotes)

                    ### find exercise acronym
                    legend = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                        'r').readlines()
                    acronym = 0
                    regexname = re.compile(f'^{exercise}$')
                    for i in legend:
                        if regexname.match(i.split(':')[0]):
                            acronym = i.strip("\n").split(":")[1]
                            break
                    if acronym == 0:
                        raise Exception('Error in logs: exercise is not mapped to any acronym. \n'
                                        'Please check legend and manually correct the log file. ')
                    # prompt exercise
                    exerciseM = click.prompt(f'Exercise name "{exercise}" has acronym "{acronym}". \nPlease enter exercise acronym', type=str, default=acronym)

                    findexercise = re.compile(f'^{exerciseM}$')
                    legend = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                        'r').readlines()
                    for i in legend:
                        if findexercise.match(i.strip('\n').split(':')[1]):
                            selectedexercise: str = i.split(':')[0]
                            break
                    try:
                        selectedexercise  # error used to show exercise notfound
                    except UnboundLocalError:
                        exercisenotfound = input(
                            'Error: acronym does not match any exercise compiled in "legend.txt". '
                            f'Do you want to create a new exercise (acronym "{exerciseM}")? [y/N]:  ')
                        if exercisenotfound == 'y':
                            newexercisename = input('What is the name of the exercise to be added to legend.txt? ')
                            newacronym = exerciseM
                            selectedexercise = CreateRequiredFiles.createnewexercise_nodecorator(newexercisename,
                                                                                                 newacronym)
                        else:
                            return

                    # repetitions
                    def validate_repetitions(value):
                        try:
                            if int(value) < 0:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                        return value
                    repetitionsM = click.prompt('Please enter no. of repetitions', value_proc=validate_repetitions, type=int, default=repetitions)

                    # weight
                    def validate_weight(value):
                        try:
                            if float(value) < 0:
                                raise ValueError(value)
                        except ValueError:
                            if value in ('NA', 'na', 'Na', 'na'):
                                pass
                            else:
                                raise click.BadParameter("Repetitions cannot be negative or string", param=value)
                        return value
                    weightM = click.prompt('Please enter weight used for exercise (kilograms)', value_proc=validate_weight, type=float, default=weight)

                    # duration
                    def validate_duration(value):
                        try:
                            prog = re.compile(
                                '^\d{1,2}[s]$|^\d{1,2}[m]$|^\d*[h]$|^\d{1,2}[m]\d{1,2}[s]$|^\d*[h]\d{1,2}[m]\d{1,2}[s]$|^[N][A]$|^[n][a]$|^[N][a]$|^[n][A]$')
                            if prog.match(value):
                                return value
                            else:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Duration specified in wrong format: format is 'XX*hXXmXXs' where h-hour(s), m-minute(s), s-second(s); or input 'NA' for none", param=value)
                            return value
                    durationM = click.prompt('Please enter duration of exercise', value_proc=validate_duration, type=str, default=duration)

                    # doneby and createdbycomputer(CBC)
                    def validate_donebyCBC(value):
                        try:
                            if '_' in value:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Cannot have '_' in string", param=value)
                        return value
                    donebyM = click.prompt('Who was the exercise done by', value_proc=validate_donebyCBC, type=str, default=doneby)
                    createdbycomputerM = click.prompt('Created by computer', value_proc=validate_donebyCBC, type=str, default=createdbycomputer)

                    logname = log.loc[log["Time"] == modifydatetime].iloc[chooselog].name
                    log.loc[logname] = timeM, selectedexercise, repetitionsM, weightM, durationM, donebyM, additionalnotesM, createdbycomputerM
                    log.to_csv(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                    print(f'log modified: \n\n{log.loc[logname]}\n')

    else:
        raise Exception('Error: function called with incorrect arguments. Please try again. ')


# make sure that initdir shows a list of files in ExerciseTerminalLogFiles for easy selection. DONE
@click.command()
@click.argument('init', default=1)
def initialisefiledirectories(init):
    if init == 1:
        try:
            config = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
            favouritefoldername = config[5].strip('\n').split('=')[1]
            if favouritefoldername == 'None':
                favouritefoldername = os.path.expanduser('~/Documents')
                initialising = input('Would you like to initialise the main log directory to the default path '
                                     f'{favouritefoldername}? [y/N]: ')
            else:
                initialising = input('Would you like to initialise the main log directory to the default path '
                                     f'{favouritefoldername}? [y/N]: ')
        except FileNotFoundError:
            favouritefoldername = os.path.expanduser('~/Documents')
            initialising = input('Would you like to initialise the main log directory to the default path '
                                 f'{favouritefoldername}? [y/N]: ')
        if initialising == 'y':
            print('Initialising to default file path: ')
            currentdir = favouritefoldername
            print(currentdir)
        elif initialising == 'N':
            currentdir = input('Input the full directory path: ')
            currentdir = os.path.join(currentdir)
            print(f'Checking if {currentdir} exists...')
            if os.path.isdir(currentdir):
                print(f'Saving directory path {currentdir} to default... ')
            else:
                print(f'{currentdir} does not exist. Please try again. ')
                return
        else:
            print('Incorrect input. Please try again. Input must be strictly "y" or "N".')
            return

        extension = int(input('What file extension would you like to save your log as?\n'
                              '(1) .csv\n'
                              '(2) .txt\n'
                              '[1/2]: '))
        if extension == 1 or extension == 2:
            if extension == 1:
                ext = '.csv'
            elif extension == 2:
                ext = '.txt'
        else:
            raise Exception('Incorrect input. Input must be 1 or 2. Please try again.')

        ancillarydir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles")
        CreateRequiredFiles.checkdirexists(ancillarydir)
        CreateRequiredFiles.checklegendexists(ancillarydir)
        CreateRequiredFiles.checkconfigexists(ancillarydir, currentdir, ext)

        maindir = os.path.join(currentdir, "ExerciseTerminalLogFiles")
        CreateRequiredFiles.checkdirexists(maindir)
        # a checkcachefolderexists function already exists -- use checkdirexists
        cachedir = os.path.join(maindir, "cache")
        CreateRequiredFiles.checkdirexists(cachedir)
        exercisedir = os.path.join(maindir, "ExerciseLogs")
        CreateRequiredFiles.checkdirexists(exercisedir)
        bodyhealthdir = os.path.join(maindir, "BodyHealthLogs")
        CreateRequiredFiles.checkdirexists(bodyhealthdir)

        # select personal folder
        collectpersonalinfodirnames = []
        for root, dirs, files in os.walk(bodyhealthdir, topdown=True):
            for dir in dirs:
                collectpersonalinfodirnames.append(dir)

        if collectpersonalinfodirnames:
            print('The following persons have an existing BodyHealth folder: \n\n')
            for i in collectpersonalinfodirnames:
                regexdirname = re.match('^(.*)PersonalInfo$', i).group(1)
                print(regexdirname)
        else:
            print('No existing BodyHealth folder...')
        personalinfoname = input("\nSelect an existing folder, or input a new name; "
                                 "this will be used to name the file in which personal information like DOB, height and weight "
                                 "will be kept. \nYou may name this otherwise if you wish: \n")
        personalbodyhealthdir = os.path.join(bodyhealthdir, f'{personalinfoname}PersonalInfo')
        CreateRequiredFiles.checkdirexists(personalbodyhealthdir)
        CreateRequiredFiles.checkbodyhealthpersonalinfoexists(personalbodyhealthdir, personalinfoname)

        try:
            configupdate = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                'r').readlines()
            configupdate[0] = 'Logging_Resolution=Day\n'
            configupdate[1] = f'Logging_to_File=None\n'
            configupdate[2] = f'Default_Directory={currentdir}\n'
            configupdate[3] = f'Logging_Extension={ext}\n'
            configupdate[4] = 'Cache_Period=Forever\n'
            # configupdate[5] = 'Favourite_Folder=None\n'  # dont change this!
            configupdate[6] = 'BodyHealth_File=None\n'
            configupdate[7] = f'BodyHealth_Directory={personalbodyhealthdir}\n'  # calling initdir allows one to change this
            configupdatex = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
            configupdatex.writelines(configupdate)
            configupdatex.close()
        except IndexError:
            configupdate = []
            configupdate = ['Logging_Resolution=Day\n',
                            f'Logging_to_File=None\n',
                            f'Default_Directory={currentdir}\n',
                            f'Logging_Extension={ext}\n',
                            'Cache_Period=Forever\n',
                            'Favourite_Folder=None\n',
                            'BodyHealth_File=None\n',
                            f'BodyHealth_Directory={personalbodyhealthdir}\n']  # calling initdir allows one to change this
            configupdatex = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
            configupdatex.writelines(configupdate)
            configupdatex.close()

        print('config.txt file restored to default. ')
        print('Initialising main log file....')
        CreateRequiredFiles.loaddestinationfile(currentdir, ancillarydir)
        currentfavfolder = configupdate[5].strip("\n").split("=")[1]
        loadfavfolder = input(f'\nYour current favourite folder is {currentfavfolder}. '
                              'Do you want to save a new favourite folder to default (this will be the default '
                              'initialisation folder on subsequent calls of "initdir")? [y/N] \n' )
        if loadfavfolder == 'y':
            favfoldername = input('Input full directory path: ')
            if os.path.isdir(os.path.join(favfoldername)):
                configupdate2 = open(
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                    'r').readlines()
                configupdate2[5] = f'Favourite_Folder={os.path.join(favfoldername)}\n'
                configupdatex2 = open(
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
                configupdatex2.writelines(configupdate2)
                configupdatex2.close()
                print(f'Saved {favfoldername} as favourite folder')
            else:
                raise Exception('Error: directory does not exist. ')
        else:
            return
    else:
        print('Files not initialised. To initialise, call default value 1.')


@click.command()
@click.argument('directory', type=click.Path(exists=True), required=True)
def changedefaultdir(directory):
    """Changes the config file to match the custom directory; remember to change the logging file as well"""
    prompt = input(f'Change directory to: {click.format_filename(directory)}? \n[y/N]: ')
    if prompt == 'y':
        # check cache
        checkandclearcache()

        print(f'Changing directory to: {click.format_filename(directory)}')
        #update config file - directory
        configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
        configupdate[1] = f'Logging_to_File=None\n'
        configupdate[2] = f'Default_Directory={directory}\n'
        # configupdate[3] = f'Logging_Extension={ext}\n'
        # configupdate[4] = 'Cache_Period=Forever\n'
        # configupdate[5] = 'Favourite_Folder=None\n'  # dont change this!
        configupdate[6] = 'BodyHealth_File=None\n'
        configupdate[7] = f'BodyHealth_Directory=None\n'  # calling initdir allows one to change this
        configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
        configupdatex.writelines(configupdate)
        configupdatex.close()
        print('Process completed. Call "setlogfile" to select log file. ')
    else:
        return


@click.command()
@click.argument('logfile', default=1)
def changeloggingfile(logfile):
    """Changes the config file to match the custom logfile; remember to change the directory as well"""
    if logfile == 1:
        # check cache
        checkandclearcache()
        # load file paths and config
        dirname = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1]
        ancillarydir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles")
        defaults = open(os.path.join(ancillarydir, "config.txt"), 'r').readlines()
        fileextension = defaults[3].strip('\n').split('=')[1]  # get file extension

        print(f'File extension chosen is "{fileextension}"; any file created/selected must have the stated extension.')
        print('Files in ExerciseTerminalLogFiles folder of selected directory: \n')

        selecteddir = os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], 'ExerciseTerminalLogFiles', 'ExerciseLogs')
        files = [f for f in os.listdir(selecteddir) if os.path.isfile(os.path.join(selecteddir, f))]
        print('\n'.join(files))
        selectedfilename = input(f'\nSelect your logging file; this file must have the file extension "{fileextension}". \n'
                                 'To select a file, type in its name WITHOUT THE EXTENSION. \n')
        if selectedfilename and os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}")):
            file1 = open(os.path.join(ancillarydir, "config.txt"), 'r')
            fileoverwrite = file1.readlines()
            fileoverwrite[1] = f'Logging_to_File={selectedfilename}\n'
            fileoverwrite[6] = 'BodyHealth_File=None\n'
            with open(os.path.join(ancillarydir, "config.txt"), 'w+') as selectedfile:
                selectedfile.writelines(fileoverwrite)
            print(f'{selectedfilename}{fileextension} selected. ')
        elif selectedfilename and not os.path.isfile(os.path.join(dirname, "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{selectedfilename}{fileextension}")):
            createnewfile = input(f'{selectedfilename}{fileextension} does not exist. '
                                  f'Create new file with name "{selectedfilename}{fileextension}"? [y/N]\n')
            if createnewfile == 'y':
                CreateRequiredFiles.createnewfile(selectedfilename, fileextension, dirname, ancillarydir)
            else:
                return
        elif not selectedfilename:
            print('No input. Please try again.')
        else:
            return


@click.command()
@click.argument('reso', type=str, required=True)
def changereso(reso):
    """Changes the "Logging_to_File" parameter to the desired resolution;
    only 4 supported; (1)"Day", (2)"12h", (3)"6h", (4)"3h\""""
    if reso in ('Day', '12h', '6h', '3h'):
        prompt = input(f'Change resolution to: {reso}? \n[y/N]: ')
        if prompt == 'y':
            # check cache
            checkandclearcache()

            print(f'Changing resolution to: {reso}')
            # update config file - directory
            configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
            configupdate[0] = f'Logging_Resolution={reso}\n'
            configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
            configupdatex.writelines(configupdate)
            configupdatex.close()
            print('Process completed. Any "querylog" calls will reflect the new resolution. ')
        else:
            print('Aborted process! ')
            return
    else:
        raise Exception('Error: function only supports "Day", "12h", "6h" and "3h" resolutions. Please try again. ')


@click.command()
@click.argument('cp', type=str, required=True)
def changeCP(cp):
    """Changes the "Cache_Period" parameter to the desired number of "Days";
    after this time elapses, as soon as the relevant function is called, the cache file will be deleted"""
    # do not clear cache in case user wants to preserve cache (which is why it is being changed in the first place)
    try:
        if int(cp) >= 1:
            prompt = input(f'Change cache period to: "{cp}Day(s)"? \n[y/N]: ')
            if prompt == 'y':
                print(f'Changing cache period to: "{cp}Day(s)"')
                #update config file - directory
                configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
                configupdate[4] = f'Cache_Period={cp}Day(s)\n'
                configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
                configupdatex.writelines(configupdate)
                configupdatex.close()
                print('Process completed. ')
            else:
                print('Aborted process! ')
                return
        else:
            raise Exception('Error: function only supports positive integer number of days, or string "F". '
                            'Please try again. ')
    except ValueError:
        if cp == 'F':
            prompt2 = input(f'Change cache period to: "Forever"? \n[y/N]: ')
            if prompt2 == 'y':
                print(f'Changing cache period to: "Forever"')
                #update config file - directory
                configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
                configupdate[4] = f'Cache_Period=Forever\n'
                configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
                configupdatex.writelines(configupdate)
                configupdatex.close()
                print('Process completed. ')
            else:
                print('Aborted process! ')
                return
        else:
            raise Exception('Error: function only supports positive integer number of days, or string "F". '
                            'Please try again. ')

@click.command()
@click.argument('extension', type=str, required=True)
def changeEXT(extension):
    """Changes the "Logging_Extension" parameter either (1)".txt" or (2)".csv\""""
    if extension in ('.txt', '.csv'):
        prompt = input(f'Change logging extension to: {extension}? \n[y/N]: ')
        if prompt == 'y':
            # check cache
            checkandclearcache()

            print(f'Changing resolution to: {extension}')
            # update config file - directory
            configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
            configupdate[1] = 'Logging_to_File=None\n'
            configupdate[3] = f'Logging_Extension={extension}\n'
            configupdatex = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'w+')
            configupdatex.writelines(configupdate)
            configupdatex.close()
            print('Process completed. Logging file set to none. Set logging file with "setlogfile" before continuing.')
        else:
            print('Aborted process! ')
            return
    else:
        raise Exception('Error: function only supports ".txt" and ".csv" file extensions. Please try again. ')


@click.command()
@click.option('-c', '--exercisename', prompt='What is the full name of your new exercise?', help='Recommended to use DASH in place of whitespaces if exercise-name so requires.'
                                                                                                'Ensure exercise name is not duplicate. ')
@click.option('-a', '--acronym', prompt='What is the acronym of your new exercise?', help='Ensure acronym is not duplicate. ')
def createnewexercise(exercisename, acronym):
    # check cache
    checkandclearcache()

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
        if findacronym.match(v.strip('\n').split(':')[1]):
            print("Acronym already exists! Please try again.")
            createnewexercise()
        else:
            pass

    # amendfile
    amendingline = f'{exercisename}:{acronym}\n'
    legend2 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'a')
    legend2.write(amendingline)
    legend2.close()
    print('Exercise successfully added to legend.txt! ')

    # sort legend.txt
    sorting = input('Do you want to sort legend.txt alphabetically? [y/N]: ')
    if sorting == 'y':
        print('Sorting file alphabetically...')
        legend3 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'r').readlines()
        legend3.sort()
        overwrite = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
        overwrite.writelines(legend3)
        overwrite.close()
        print('File sorted.')
    else:
        pass

    return exercisename

# delete exercise by acronym
@click.command()
@click.option('-d', '--deleteex', prompt='Type acronym (case-sensitive) of exercise you wish to delete; "CTRL+C" to abort', help='This function deletes an exercise referenced by its acronym from legend.txt.')
def deleteexercise(deleteex):
    # check cache
    checkandclearcache()

    legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                  'r').readlines()
    exercisematcher = re.compile(f'^{deleteex}$')
    flag = False
    for i in legend:
        if exercisematcher.match(i.strip('\n').split(':')[1]):
            flag = not flag
            if click.confirm(f'Acronym "{deleteex}" is matched to the exercise "{i.split(":")[0]}". Delete?\n'
                             f'Bear in mind that deleting exercises may cause '
                             f'issues with exporting or modifying files, '
                             f'if previous logs record the deleted exercise.\n', abort=True):
                if click.confirm('Backup folder?\n'):
                    # backup legend
                    backupfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", f"legendbackup_{dt.datetime.now().strftime('%d%m%Y-%H%M%S')}.txt"), 'w')
                    backupfile.writelines(legend)
                    backupfile.close()

                    legend.remove(i)
                    overwrite = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
                    overwrite.writelines(legend)
                    overwrite.close()
                    print(f'{i}Deleted successfully.')
                else:
                    legend.remove(i)
                    overwrite = open(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
                    overwrite.writelines(legend)
                    overwrite.close()
                    print(f'{i}Deleted successfully.')
        else:
            pass
    if flag == False:
        print('Exercise does not exist for that acronym.')
    return

# find out the full exercise name from the acronym.
@click.command()
@click.option('-nm', '--check-name', prompt='What is the exercise acronym (case-sensitive)?', help='You must have the case-sensitive exercise acronym to utilise this function.')
def check_exnameexercise(check_name):
    # check cache
    checkandclearcache()

    legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                  'r').readlines()
    regexacronym = re.compile(f'^{check_name}$')
    flag = False
    for i in legend:
        if regexacronym.match(i.strip('\n').split(':')[1]):
            flag = not flag
            print(f'Acronym "{check_name}" is matched to the exercise "{i.split(":")[0]}"')
        else:
            pass
    if flag == False:
        print('Exercise does not exist for that acronym.')
    return


# find out the exercise acronym from the full exercise name.
@click.command()
@click.option('-ac', '--check-acr', prompt='What is the full exercise name (case-sensitive)?', help='You must have the full and case-sensitive exercise name to utilise this function.')
def check_acronym(check_acr):
    # check cache
    checkandclearcache()

    legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"),
                  'r').readlines()
    regexname = re.compile(f'^{check_acr}$')
    flag = False
    for i in legend:
        if regexname.match(i.split(':')[0]):
            flag = not flag
            print('Exercise name "{}" has acronym "{}"'.format(check_acr, i.strip("\n").split(":")[1]))
        else:
            pass
    if flag == False:
        print('Acronym does not exist for that exercise.')
    return


@click.command()
@click.option('-d', '--querydate', prompt='Input date period to extract logs; format: \n'
                                          '(1) ddmmyyyy_ddmmyyyy\n'
                                          '(2) ddmmyyyy-HHMM_ddmmyyyy-HHMM\n', help='format: '
                                          '(1) ddmmyyyy_ddmmyyyy'
                                          '(2) ddmmyyyy-HHMM_ddmmyyyy-HHMM ')
def showlog(querydate):
    # check cache
    checkandclearcache()
    config = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                  'r').readlines()
    resolution = config[0].strip('\n').split('=')[1]
    fileextension = config[3].strip('\n').split('=')[1]  # get extension for filehandling
    logfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                   'r').readlines()[1].strip('\n').split('=')[1]
    checkformatDAY = re.compile('^\d{8}[_]\d{8}$')
    checkformatOTHER = re.compile('^\d{8}[-]\d{4}[_]\d{8}[-]\d{4}$')
    if fileextension == '.txt':
        logcompiler = []
        # check resolution, then continue to collect logs from log file
        if resolution in ('Day', '12h', '6h', '3h'):
            if checkformatDAY.match(querydate):
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[_](\d\d)(\d\d)(\d{4})$', querydate)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) <= 0 or int(timeerror.group(4)) > 31 or int(timeerror.group(5)) <= 0 or int(
                            timeerror.group(5)) > 12 or int(timeerror.group(6)) > dt.datetime.now().year:
                        raise Exception('Error: incorrect date given. Please check date and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')

                # continue to collect logs
                print(f'Querying "{resolution}" resolution')
                startdate = querydate.split('_')[0]
                enddate = querydate.split('_')[1]
                log = open(os.path.join(
                    open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
                for i in log:
                    if i == 'n':
                        print('A blank line in the log file has been detected. Please delete this manually. ')
                        return
                    else:
                        if dt.datetime.strptime(startdate, '%d%m%Y') <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M') <= dt.datetime.strptime(enddate, '%d%m%Y').replace(hour=23, minute=59):
                            if resolution == 'Day':
                                n = ['Day:1', i] # dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').strftime('%d%m%Y')
                                logcompiler.append(n)
                            elif resolution == '12h':
                                if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                    period = '12h:1'
                                else:
                                    period = '12h:2'
                                n = [period, i]
                                logcompiler.append(n)
                            elif resolution == '6h':
                                if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                                    period = '6h:1'
                                elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                    period = '6h:2'
                                elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                                    period = '6h:3'
                                else:
                                    period = '6h:4'
                                n = [period, i]
                                logcompiler.append(n)
                            elif resolution == '3h':
                                if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 3:
                                    period = '3h:1'
                                elif 3 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                                    period = '3h:2'
                                elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 9:
                                    period = '3h:3'
                                elif 9 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                    period = '3h:4'
                                elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 15:
                                    period = '3h:5'
                                elif 15 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                                    period = '3h:6'
                                elif 18 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 21:
                                    period = '3h:7'
                                else:
                                    period = '3h:8'
                                n = [period, i]
                                logcompiler.append(n)
                        else:
                            pass

                if not logcompiler:
                    print('No logs for that time period. Please check date and try again. ')
                    return
                else:
                    print(f'Collected {len(logcompiler)} log file(s): \n')
                    logcompiler.sort(key=takeTimefromloglistoflist)
                    for line in logcompiler:
                        print(*line)
                intentexport = input('Do you want to export these logs to .csv? [y/N]: ')
                if intentexport == 'y':
                    exporttocsv(logcompiler)
                else:
                    return

            elif checkformatOTHER.match(querydate):
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)[_](\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', querydate)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59 or int(timeerror.group(6)) <= 0 or int(timeerror.group(6)) > 31 or int(
                            timeerror.group(7)) <= 0 or int(
                            timeerror.group(7)) > 12 or int(timeerror.group(8)) > dt.datetime.now().year or int(
                            timeerror.group(9)) < 0 or int(timeerror.group(9)) > 23 or int(timeerror.group(10)) < 0 or int(
                            timeerror.group(10)) > 59:
                        raise Exception('Error: invalid date format. Please check date input and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')

                # continue to collect logs
                print(f'Querying "{resolution}" resolution')
                startdate = querydate.split('_')[0]
                enddate = querydate.split('_')[1]
                log = open(os.path.join(
                    open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
                for i in log:
                    if dt.datetime.strptime(startdate, '%d%m%Y-%H%M') <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M') <= dt.datetime.strptime(enddate, '%d%m%Y-%H%M'):
                        if resolution == 'Day':
                            n = ['Day:1', i]
                            logcompiler.append(n)
                        elif resolution == '12h':
                            if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                period = '12h:1'
                            else:
                                period = '12h:2'
                            n = [period, i]
                            logcompiler.append(n)
                        elif resolution == '6h':
                            if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                                period = '6h:1'
                            elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                period = '6h:2'
                            elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                                period = '6h:3'
                            else:
                                period = '6h:4'
                            n = [period, i]
                            logcompiler.append(n)
                        elif resolution == '3h':
                            if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 3:
                                period = '3h:1'
                            elif 3 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                                period = '3h:2'
                            elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 9:
                                period = '3h:3'
                            elif 9 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                                period = '3h:4'
                            elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 15:
                                period = '3h:5'
                            elif 15 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                                period = '3h:6'
                            elif 18 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 21:
                                period = '3h:7'
                            else:
                                period = '3h:8'
                            n = [period, i]
                            logcompiler.append(n)
                    else:
                        pass

                if not logcompiler:
                    print('No logs for that time period. Please check date and try again. ')
                    return
                else:
                    print(f'Collected {len(logcompiler)} log file(s): \n')
                    logcompiler.sort(key=takeTimefromloglistoflist)
                    for line in logcompiler:
                        print(*line)

                intentexport = input('Do you want to export these logs to .csv? [y/N]: ')
                if intentexport == 'y':
                    exporttocsv(logcompiler)
                else:
                    return

            else:
                raise Exception('Error: incorrect input format for period; format should match: \n'
                                '(1) ddmmyyyy_ddmmyyyy\n'
                                '(2) ddmmyyyy-HHMM_ddmmyyyy-HHMM\n')
        else:
            raise Exception('Error: function only supports "Day", "12h", "6h" and "3h" resolutions. '
                            'Set the appropriate resolution through "setreso" and try again. ')

    elif fileextension == '.csv':
        if resolution in ('Day', '12h', '6h', '3h'):
            if checkformatDAY.match(querydate):
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[_](\d\d)(\d\d)(\d{4})$', querydate)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) <= 0 or int(timeerror.group(4)) > 31 or int(timeerror.group(5)) <= 0 or int(
                            timeerror.group(5)) > 12 or int(timeerror.group(6)) > dt.datetime.now().year:
                        raise Exception('Error: incorrect date given. Please check date and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')

                # continue to collect logs
                print(f'Querying "{resolution}" resolution')
                startdate = querydate.split('_')[0]
                enddate = querydate.split('_')[1]
                pd.set_option('display.max_columns', None)  # print all columns
                pd.set_option('display.max_rows', None)  # print all rows
                log = pd.read_csv(os.path.join(open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[
                                                   2].strip(
                    '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                log.drop(log.columns[0], axis=1, inplace=True)

                if log.empty:
                    print(f'No logs in file {logfile}.csv. ')
                    return
                else:
                    log.fillna('NA', inplace=True)
                    log['Time2'] = pd.to_datetime(log['Time'], format='%d%m%Y-%H%M')
                    log.sort_values(by=['Time2'], inplace=True)
                    mask = (log['Time2'] >= dt.datetime.strptime(startdate, '%d%m%Y')) & (log['Time2'] <= dt.datetime.strptime(enddate, '%d%m%Y').replace(hour=23, minute=59))
                    log = log.loc[mask]
                    if resolution == 'Day':
                        dayrows = [1] * len(log)
                        log.insert(0, "Period:Day", dayrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '12h':
                        # initialise list
                        twelvehourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                twelvehourrows.insert(i, '12h:1')
                            else:
                                twelvehourrows.insert(i, '12h:2')
                        log.insert(0, "Period:12h", twelvehourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '6h':
                        # initialise list
                        sixhourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                                sixhourrows.insert(i, '6h:1')
                            elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                sixhourrows.insert(i, '6h:2')
                            elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                                sixhourrows.insert(i, '6h:3')
                            else:
                                sixhourrows.insert(i, '6h:4')
                        log.insert(0, "Period:6h", sixhourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '3h':
                        # initialise list
                        threehourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 3:
                                threehourrows.insert(i, '3h:1')
                            elif 3 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                                threehourrows.insert(i, '3h:2')
                            elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 9:
                                threehourrows.insert(i, '3h:3')
                            elif 9 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                threehourrows.insert(i, '3h:4')
                            elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 15:
                                threehourrows.insert(i, '3h:5')
                            elif 15 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                                threehourrows.insert(i, '3h:6')
                            elif 18 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 21:
                                threehourrows.insert(i, '3h:7')
                            else:
                                threehourrows.insert(i, '3h:8')
                        log.insert(0, "Period:3h", threehourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)

                    # ask if want to save the queried logs to separate folder
                    intentexport = input('Do you want to save these logs to a separate .csv? [y/N]: ')
                    if intentexport == 'y':
                        destinationfolder = input('Input destination folder: ')
                        if os.path.isdir(destinationfolder):
                            filename = input('Input filename without extension: ')
                            destinationfolder = os.path.join(destinationfolder)
                            print(f"Saving to folder {destinationfolder}...")
                            log.to_csv(os.path.join(destinationfolder, f'{filename}.csv'))
                            print(f'Saving completed. Check {destinationfolder}. ')
                        else:
                            raise Exception('Error: folder does not exist. Please try again. ')
                    else:
                        return

            elif checkformatOTHER.match(querydate):
                # check if queried time input is valid --> raise exception for invalid input!
                timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)[_](\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$', querydate)
                try:
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year or int(
                            timeerror.group(4)) < 0 or int(timeerror.group(4)) > 23 or int(timeerror.group(5)) < 0 or int(
                            timeerror.group(5)) > 59 or int(timeerror.group(6)) <= 0 or int(timeerror.group(6)) > 31 or int(
                            timeerror.group(7)) <= 0 or int(
                            timeerror.group(7)) > 12 or int(timeerror.group(8)) > dt.datetime.now().year or int(
                            timeerror.group(9)) < 0 or int(timeerror.group(9)) > 23 or int(timeerror.group(10)) < 0 or int(
                            timeerror.group(10)) > 59:
                        raise Exception('Error: invalid date format. Please check date input and try again. ')
                except AttributeError:
                    raise Exception('Error: invalid date format. Please check date input and try again. ')

                # continue to collect logs
                print(f'Querying "{resolution}" resolution')
                startdate = querydate.split('_')[0]
                enddate = querydate.split('_')[1]

                pd.set_option('display.max_columns', None)  # print all columns
                pd.set_option('display.max_rows', None)  # print all rows
                log = pd.read_csv(os.path.join(open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[
                                                   2].strip(
                    '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                log.drop(log.columns[0], axis=1, inplace=True)

                if log.empty:
                    print(f'No logs in file {logfile}.csv. ')
                    return
                else:
                    log.fillna('NA', inplace=True)
                    log['Time2'] = pd.to_datetime(log['Time'], format='%d%m%Y-%H%M')
                    log.sort_values(by=['Time2'], inplace=True)
                    mask = (log['Time2'] >= dt.datetime.strptime(startdate, '%d%m%Y-%H%M')) & (log['Time2'] <= dt.datetime.strptime(enddate, '%d%m%Y-%H%M'))
                    log = log.loc[mask]
                    if resolution == 'Day':
                        dayrows = [1] * len(log)
                        log.insert(0, "Period:Day", dayrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '12h':
                        # initialise list
                        twelvehourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                twelvehourrows.insert(i, '12h:1')
                            else:
                                twelvehourrows.insert(i, '12h:2')
                        log.insert(0, "Period:12h", twelvehourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '6h':
                        # initialise list
                        sixhourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                                sixhourrows.insert(i, '6h:1')
                            elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                sixhourrows.insert(i, '6h:2')
                            elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                                sixhourrows.insert(i, '6h:3')
                            else:
                                sixhourrows.insert(i, '6h:4')
                        log.insert(0, "Period:6h", sixhourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)
                    elif resolution == '3h':
                        # initialise list
                        threehourrows = []
                        for i in range(len(log)):
                            if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 3:
                                threehourrows.insert(i, '3h:1')
                            elif 3 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                                threehourrows.insert(i, '3h:2')
                            elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 9:
                                threehourrows.insert(i, '3h:3')
                            elif 9 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                                threehourrows.insert(i, '3h:4')
                            elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 15:
                                threehourrows.insert(i, '3h:5')
                            elif 15 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                                threehourrows.insert(i, '3h:6')
                            elif 18 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 21:
                                threehourrows.insert(i, '3h:7')
                            else:
                                threehourrows.insert(i, '3h:8')
                        log.insert(0, "Period:3h", threehourrows)
                        log.reset_index(drop=True, inplace=True)
                        log.drop(log.columns[-1], axis=1, inplace=True)
                        print(log)

                    # ask if want to save the queried logs to separate folder
                    intentexport = input('Do you want to save these logs to a separate .csv? [y/N]: ')
                    if intentexport == 'y':
                        destinationfolder = input('Input destination folder: ')
                        if os.path.isdir(destinationfolder):
                            filename = input('Input filename without extension: ')
                            destinationfolder = os.path.join(destinationfolder)
                            print(f"Saving to folder {destinationfolder}...")
                            log.to_csv(os.path.join(destinationfolder, f'{filename}.csv'))
                            print(f'Saving completed. Check {destinationfolder}. ')
                        else:
                            raise Exception('Error: folder does not exist. Please try again. ')
                    else:
                        return
            else:
                raise Exception('Error: incorrect input format for period; format should match: \n'
                                '(1) ddmmyyyy_ddmmyyyy\n'
                                '(2) ddmmyyyy-HHMM_ddmmyyyy-HHMM\n')

        else:
            raise Exception('Error: function only supports "Day", "12h", "6h" and "3h" resolutions. '
                            'Set the appropriate resolution through "setreso" and try again. ')



@click.command()
@click.argument('all', default=1)
def queryalllogs(all):
    '''prints all logs of selected file in sorted form.'''
    if all == 1:
        # check cache
        checkandclearcache()

        config = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()
        resolution = config[0].strip('\n').split('=')[1]
        fileextension = config[3].strip('\n').split('=')[1]  # get extension for filehandling
        logfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[1].strip('\n').split('=')[1]
        if fileextension == '.txt':
            try:
                log = open(os.path.join(
                    open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
            except FileNotFoundError as ex:
                print("Error: file not found. Call 'initdir' first. ")
                return
            logcompiler = []
            for i in log:
                if i == '\n':
                    print('A blank line in the log file has been detected. Please delete this manually. ')
                    return
                else:
                    if resolution == 'Day':
                        n = ['Day:1', i]
                        logcompiler.append(n)
                    elif resolution == '12h':
                        if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                            period = '12h:1'
                        else:
                            period = '12h:2'
                        n = [period, i]
                        logcompiler.append(n)
                    elif resolution == '6h':
                        if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                            period = '6h:1'
                        elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                            period = '6h:2'
                        elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                            period = '6h:3'
                        else:
                            period = '6h:4'
                        n = [period, i]
                        logcompiler.append(n)
                    elif resolution == '3h':
                        if dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 3:
                            period = '3h:1'
                        elif 3 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 6:
                            period = '3h:2'
                        elif 6 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 9:
                            period = '3h:3'
                        elif 9 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 12:
                            period = '3h:4'
                        elif 12 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 15:
                            period = '3h:5'
                        elif 15 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 18:
                            period = '3h:6'
                        elif 18 <= dt.datetime.strptime(i.split('_')[0].split(':')[1], '%d%m%Y-%H%M').hour < 21:
                            period = '3h:7'
                        else:
                            period = '3h:8'
                        n = [period, i]
                        logcompiler.append(n)

            if not logcompiler:
                print(f'No logs in file {logfile}.txt. ')
                return
            else:
                print(f'Collected {len(logcompiler)} log file(s): \n')
                logcompiler.sort(key=takeTimefromloglistoflist)
                for line in logcompiler:
                    print(*line)

            # ask if want to export
            intentexport = input('Do you want to export these logs to .csv? [y/N]: ')
            if intentexport == 'y':
                exporttocsv(logcompiler)
            else:
                return

        elif fileextension == '.csv':
            pd.set_option('display.max_columns', None)  # print all columns
            pd.set_option('display.max_rows', None)  # print all rows
            try:
                log = pd.read_csv(os.path.join(open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip(
                    '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
            except FileNotFoundError as ex:
                print("Error: file not found. Call 'initdir' first. ")
                return
            log.drop(log.columns[0], axis=1, inplace=True)
            if log.empty:
                print(f'No logs in file {logfile}.csv. ')
                return
            else:
                log['Time2'] = pd.to_datetime(log['Time'], format='%d%m%Y-%H%M')
                log.sort_values(by=['Time2'], inplace=True)
                log.drop(log.columns[-1], axis=1, inplace=True)
                log.reset_index(drop=True, inplace=True)
                if resolution == 'Day':
                    dayrows = [1]*len(log)
                    log.insert(0, "Period:Day", dayrows)
                    log.fillna('NA', inplace=True)
                    print(log)
                elif resolution == '12h':
                    # initialise list
                    twelvehourrows = []
                    for i in range(len(log)):
                        if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                            twelvehourrows.insert(i, '12h:1')
                        else:
                            twelvehourrows.insert(i, '12h:2')
                    log.insert(0, "Period:12h", twelvehourrows)
                    log.fillna('NA', inplace=True)
                    print(log)
                elif resolution == '6h':
                    # initialise list
                    sixhourrows = []
                    for i in range(len(log)):
                        if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                            sixhourrows.insert(i, '6h:1')
                        elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                            sixhourrows.insert(i, '6h:2')
                        elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                            sixhourrows.insert(i, '6h:3')
                        else:
                            sixhourrows.insert(i, '6h:4')
                    log.insert(0, "Period:6h", sixhourrows)
                    log.fillna('NA', inplace=True)
                    print(log)
                elif resolution == '3h':
                    # initialise list
                    threehourrows = []
                    for i in range(len(log)):
                        if dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 3:
                            threehourrows.insert(i, '3h:1')
                        elif 3 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 6:
                            threehourrows.insert(i, '3h:2')
                        elif 6 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 9:
                            threehourrows.insert(i, '3h:3')
                        elif 9 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 12:
                            threehourrows.insert(i, '3h:4')
                        elif 12 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 15:
                            threehourrows.insert(i, '3h:5')
                        elif 15 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 18:
                            threehourrows.insert(i, '3h:6')
                        elif 18 <= dt.datetime.strptime(log.iloc[i].Time, '%d%m%Y-%H%M').hour < 21:
                            threehourrows.insert(i, '3h:7')
                        else:
                            threehourrows.insert(i, '3h:8')
                    log.insert(0, "Period:3h", threehourrows)
                    log.fillna('NA', inplace=True)
                    print(log)

            # ask if want to save the queried logs to separate folder
            intentexport = input('Do you want to save these logs to a separate .csv? [y/N]: ')
            if intentexport == 'y':
                destinationfolder = input('Input destination folder: ')
                if os.path.isdir(destinationfolder):
                    filename = input('Input filename without extension: ')
                    destinationfolder = os.path.join(destinationfolder)
                    print(f"Saving to folder {destinationfolder}...")
                    log.to_csv(os.path.join(destinationfolder, f'{filename}.csv'))
                    print(f'Saving completed. Check {destinationfolder}. ')
                else:
                    raise Exception('Error: folder does not exist. Please try again. ')
            else:
                return

@click.command()
@click.argument('sort', default=1)
def sortlogfile(sort):
    if sort == 1:
        # check cache
        checkandclearcache()

        config = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                         'r').readlines()
        fileextension = config[3].strip('\n').split('=')[1]  # get extension for filehandling
        logfile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
             'r').readlines()[1].strip('\n').split('=')[1]
        maindir = os.path.join(
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles")
        prompt = input(f'Sort log file "{logfile}{fileextension}" by date and time? [y/N]: ')
        if fileextension == '.txt':
            if prompt == 'y':
                print(f'Sorting file "{logfile}.txt"...')
                log = open(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'r').readlines()
                # first cache the file
                CreateRequiredFiles.caching(logfile, log, fileextension, maindir)
                # continue...
                log.sort(key=takeTimefromlog)
                overwrite = open(os.path.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.txt"), 'w+')
                overwrite.writelines(log)
                overwrite.close()
                print('File sorted.')
            else:
                print('Aborted process!')
                return
        elif fileextension == '.csv':
            if prompt == 'y':
                print(f'Sorting file "{logfile}.csv"...')
                log = pd.read_csv(os.path.join(open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[2].strip(
                    '\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                log.drop(log.columns[0], axis=1, inplace=True)
                if log.empty:
                    print(f'No logs in file {logfile}.csv. ')
                    return
                else:
                    # first cache the file
                    CreateRequiredFiles.caching(logfile, log, fileextension, maindir)
                    # continue...
                    log.fillna('NA', inplace=True)
                    log['Time2'] = pd.to_datetime(log['Time'], format='%d%m%Y-%H%M')
                    log.sort_values(by=['Time2'], inplace=True)
                    log.drop(log.columns[-1], axis=1, inplace=True)
                    log.reset_index(drop=True, inplace=True)
                    log.to_csv(os.path.join(
                        open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                             'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles", 'ExerciseLogs', f"{logfile}.csv"))
                    print('File sorted.')
            else:
                print('Aborted process!')
                return
    else:
        return


@click.command()
@click.argument('sort', default=1)
def sortlegend(sort):
    if sort == 1:
        # check cache
        checkandclearcache()

        prompt = input('Sort legend by alphabetical order: \n'
                       '(a) Full name of exercise \n'
                       '(b) Acronym of exercise \n'
                       '(c) Abort \n'
                       'a/b/c: ')
        if prompt == 'a':
            print('Sorting file alphabetically (Full name of exercise)...')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'r').readlines()
            legend.sort()
            overwrite = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
            overwrite.writelines(legend)
            overwrite.close()
            print('File sorted.')
        elif prompt == 'b':
            print('Sorting file alphabetically (Acronym of exercise)...')
            legend = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'r').readlines()
            legend.sort(key=takeAcronym)
            overwrite = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "AncillaryFiles", "legend.txt"), 'w+')
            overwrite.writelines(legend)
            overwrite.close()
            print('File sorted.')
        else:
            print("Aborted process!")
            return
    else:
        return


@click.command()
@click.argument('show', default=1)
def printconfig(show):
    # checkcache
    checkandclearcache()

    if show == 1:
        configupdate = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                            'r').readlines()
        configupdate[0] = ' ' + configupdate[0]
        print('\n')
        print(*configupdate)
    else:
        return



def exporttocsv(logcompiler):
    # check cache
    checkandclearcache()

    destinationfolder = input('Input destination folder: ')
    if os.path.isdir(destinationfolder):
        filename = input('Input filename without extension: ')
        destinationfolder = os.path.join(destinationfolder)
        print(f"Exporting to folder {destinationfolder}...")
        a, b, c, d, e, f = logcompiler[0][1].split('_')
        a_column = re.search('[[]\w{5}[]](\w*)', a.split(':')[0]).group(1)
        dataframecolumns = [f'Period:{logcompiler[0][0].split(":")[0]}', a_column, b.split(':')[0], c.split(':')[0].split('/')[0], c.split(':')[0].split('/')[1], c.split(':')[0].split('/')[2], d.split(':')[0], e.split(':')[0], f.split(':')[0]]
        exporterdataframe = pd.DataFrame(columns=dataframecolumns)
        for i in range(len(logcompiler)):
            g = logcompiler[i][0]
            h, ii, j, k, l, m = logcompiler[i][1].split('_')
            period = g.split(':')[1]
            time = h.split(':')[1]
            exercise = ii.split(':')[1]
            repetitions = j.split(':')[1].split('/')[0]
            weight = j.split(':')[1].split('/')[1]
            duration = j.split(':')[1].split('/')[2]
            doneby = k.split(':')[1]
            additionalnotes = l.split(':')[1]
            createdbycomputer = re.search('(.*)[[]\w{3}[]]', m.split(':')[1]).group(1)
            exporterdataframe.loc[i] = period, time, exercise, repetitions, weight, duration, doneby, additionalnotes, createdbycomputer
        exporterdataframe.to_csv(os.path.join(destinationfolder, f'{filename}.csv'))
        print(f'Exporting completed. Check {destinationfolder}. ')
    else:
        raise Exception('Error: folder does not exist. Please try again. ')


def takeAcronym(elem):
    return elem.strip('\n').split(':')[1]


def takeTimefromlog(elem):
    return dt.datetime.strptime(elem.split('_')[0].split(':')[1], '%d%m%Y-%H%M')


def takeTimefromloglistoflist(elem):
    return dt.datetime.strptime(elem[1].split('_')[0].split(':')[1], '%d%m%Y-%H%M')


def checkandclearcache():  # note: if need to use CreateRequiredFiles.caching() function, have to use maindir variable
    # check cache
    cacheperiod = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                       'r').readlines()[4].strip('\n').split('=')[1]
    maindir = os.path.join(
        open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
             'r').readlines()[2].strip('\n').split('=')[1], "ExerciseTerminalLogFiles")
    if cacheperiod == 'Forever':
        pass
    else:
        cacheperiod = ''.join([i for i in cacheperiod if i.isdigit()])  # strip string of digits
        CreateRequiredFiles.checkcache(cacheperiod, maindir)  # check if cache exists and clearcache if required
    return maindir


if __name__ == '__main__':
    initialisefiledirectories()