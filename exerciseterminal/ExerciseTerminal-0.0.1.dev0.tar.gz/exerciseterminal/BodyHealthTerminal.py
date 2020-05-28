import os
import datetime as dt
import pandas as pd
import exerciseterminal.CreateRequiredFiles
import click
import re
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


def validate_timeddmmyyyyhhmmbh(ctx, param, value):
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
@click.option('-l', '--log-time', callback=validate_timeddmmyyyyhhmmbh, default='now', help= 'Log at specified time: '
                                         '(1) "now" - time of logging set to time command received. '
                                         '(2) "ddmmyyyy-HHMM" - time of logging set to specified time. '
                                         '(3) HHMM - time of logging set to specified time with date set to today. ', required=True, type=str)
def logH(log_time):
    # height and weight should be asked for within the function so that formatting requirements can be imposed.
    timenow = dt.datetime.now().strftime("%d%m%Y-%H%M")
    print('Logging command received at {}'.format(timenow))
    try:
        config = open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
            'r').readlines()
        # check cache
        currentdir = checkandclearcache()
        bodyhealthfile = config[6].strip('\n').split('=')[1]
        personalbodyhealthdir = config[7].strip('\n').split('=')[1]
        try:
            personalinformation = open(os.path.join(personalbodyhealthdir, "BodyHealthPersonalInfo.txt"),
                                       'r').readlines()
            DOB = personalinformation[0].strip('\n').split(':')[1]
            Gender = personalinformation[1].strip('\n').split(':')[1]
            Name = personalinformation[2].strip('\n').split(':')[1]
        except Exception as ex:
            print(f'Error: {str(ex)}. Call "initdir" to create a folder.')
            return
    except FileNotFoundError as ex:
        raise Exception(f'Error: {str(ex)}; call "initdir" to initialise directories first. ')

    if os.path.isfile(os.path.join(personalbodyhealthdir, f'{bodyhealthfile}.csv')):
        # print(f'logging to {os.path.join(personalbodyhealthdir, f"{bodyhealthfile}.csv")}')
        pass
    else:
        raise FileNotFoundError('Error: call "inithealth" to initialise logging file.')

    if Gender == 'Unfilled' or DOB == 'Unfilled':
        raise Exception('Gender or Age unfilled. Call "inithealth" before running this function. ')

    try:
        existinglogs = pd.read_csv(os.path.join(personalbodyhealthdir, f"{bodyhealthfile}.csv"))
    except FileNotFoundError as ex:
        print(f'Error (file not found): file not found; try calling the "initdir" function first: {str(ex)}')
    except NameError as ex:
        print(f'Error (name error): directory name not found; try calling the "initdir" function first: {str(ex)}')
    except PermissionError as ex:
        print(f'Error (permission error): please close the file if it is currently open and try again: {str(ex)}.')

    # time
    ddmmyyyy_HHMM = re.compile('^\d{8}-\d{4}$')
    HHMM = re.compile('^\d{4}$')
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

    # Age
    agecalculator = re.match('^(\d\d)(\d\d)(\d{4})$', DOB)
    datetoday = re.match('^(\d\d)(\d\d)(\d{4})$', dt.datetime.now().strftime('%d%m%Y'))
    if datetoday.group(2) > agecalculator.group(2) or (datetoday.group(2) == agecalculator.group(2) and datetoday.group(1) >= agecalculator.group(1)):
        Age = int(datetoday.group(3)) - int(agecalculator.group(3))
    elif datetoday.group(2) < agecalculator.group(2) or (datetoday.group(2) == agecalculator.group(2) and datetoday.group(1) < agecalculator.group(1)):
        Age = int(datetoday.group(3)) - int(agecalculator.group(3)) - 1

    if existinglogs.empty:
        # Weight
        bodyweight = click.prompt('Specify body weight (integer or decimal number in kilos)', type=float)
        if float(bodyweight) >= 0:
            pass
        else:
            raise Exception('Error: number must be greater than 0.')

        # height
        height = click.prompt('Specify body height (decimal number in metres)', type=float)
        if float(height) >= 0:
            pass
        else:
            raise Exception('Error: number must be greater than 0.')

        waistcircumf = click.prompt('Specify waist circumference (decimal number in metres)', type=float)  # use a tape measure

        BMI = bodyweight/(height**2)  # A BMI ≥30 is considered obese
        if Gender == 'M':
            RFM = 64 - (20 * (height/waistcircumf))
        elif Gender == 'F':
            RFM = 76 - (20 * (height / waistcircumf))

        logcolumns = ['ltime', 'Name', 'Gender', 'Age', 'Weight(kilograms)', 'Height(metres)', 'Waist-Circumference(metres)', 'BMI', 'RFM']
        csvlog = pd.DataFrame(columns=logcolumns)
        csvlog.loc[0] = time, Name, Gender, Age, bodyweight, height, waistcircumf, BMI, RFM
        existinglogs = existinglogs.append(csvlog.iloc[0])
        existinglogs.drop(existinglogs.columns[0], axis=1, inplace=True)
        existinglogs.to_csv(os.path.join(personalbodyhealthdir, f"{bodyhealthfile}.csv"))
        print(f"logging successful: \n\n{csvlog}")
    else:
        bodyweight = existinglogs['Weight(kilograms)'].iloc[-1]
        height = existinglogs['Height(metres)'].iloc[-1]
        waistcircumf = existinglogs['Waist-Circumference(metres)'].iloc[-1]

        # Weight
        bodyweightM = click.prompt('Specify body weight (integer or decimal number in kilos)', type=float, default=bodyweight)
        if float(bodyweightM) >= 0:
            pass
        else:
            raise Exception('Error: number must be greater than 0.')

        # height
        heightM = click.prompt('Specify body height (decimal number in metres)', type=float, default=height)
        if float(heightM) >= 0:
            pass
        else:
            raise Exception('Error: number must be greater than 0.')

        waistcircumfM = click.prompt('Specify waist circumference (decimal number in metres)', type=float, default=waistcircumf)  # use a tape measure

        BMI = bodyweightM/(heightM**2)  # A BMI ≥30 is considered obese
        if Gender == 'M':
            RFM = 64 - (20 * (heightM/waistcircumfM))
        elif Gender == 'F':
            RFM = 76 - (20 * (heightM / waistcircumfM))

        logcolumns = ['ltime', 'Name', 'Gender', 'Age', 'Weight(kilograms)', 'Height(metres)', 'Waist-Circumference(metres)', 'BMI', 'RFM']
        csvlog = pd.DataFrame(columns=logcolumns)
        csvlog.loc[0] = time, Name, Gender, Age, bodyweightM, heightM, waistcircumfM, BMI, RFM
        existinglogs = existinglogs.append(csvlog.iloc[0])
        existinglogs.drop(existinglogs.columns[0], axis=1, inplace=True)
        existinglogs.to_csv(os.path.join(personalbodyhealthdir, f"{bodyhealthfile}.csv"))
        print(f"logging successful: \n\n{csvlog}")


@click.command()
@click.argument('inithealth', default=1)
def initialisehealth(inithealth):
    if inithealth == 1:
        try:
            config = open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                'r').readlines()
            currentdir = config[2].strip('\n').split('=')[1]
            bodyhealthdir = os.path.join(currentdir, "ExerciseTerminalLogFiles", "BodyHealthLogs")
            bodyhealthfile = config[6].strip('\n').split('=')[1]
            personalbodyhealthdir = config[7].strip('\n').split('=')[1]

            if not os.path.isdir(personalbodyhealthdir):
                collectpersonalinfodirnames = []
                for root, dirs, files in os.walk(bodyhealthdir, topdown=True):
                    for dir in dirs:
                        collectpersonalinfodirnames.append(dir)
                if collectpersonalinfodirnames:
                    print('The following persons have an existing BodyHealth folder: \n')
                    for i in collectpersonalinfodirnames:
                        regexdirname = re.match('^(.*)PersonalInfo$', i).group(1)
                        print(regexdirname)
                    personalinfoname = input('Select name. \n')
                    personalbodyhealthdir = os.path.join(bodyhealthdir, f'{personalinfoname}PersonalInfo')
                else:
                    print('No folder found. call "initdir" to create or select a folder.')
                    return
            else:
                change = input(f'Current folder selected: {personalbodyhealthdir}. Would you like to change folders? \n[y/N]\n')
                if change == 'y':
                    collectpersonalinfodirnames = []
                    for root, dirs, files in os.walk(bodyhealthdir, topdown=True):
                        for dir in dirs:
                            collectpersonalinfodirnames.append(dir)
                    if collectpersonalinfodirnames:
                        print('The following persons have an existing BodyHealth folder: \n')
                        for i in collectpersonalinfodirnames:
                            regexdirname = re.match('^(.*)PersonalInfo$', i).group(1)
                            print(regexdirname)
                        personalinfoname = input('Select name. \n')
                        personalbodyhealthdir = os.path.join(bodyhealthdir, f'{personalinfoname}PersonalInfo')
                        # save to config
                        if not os.path.isdir(personalbodyhealthdir):
                            raise Exception('Error: no such file exists. Call "initdir" to create or select a folder.')
                    else:
                        print('No folder found. Call "initdir" to create or select a folder.')
                        return
                else:
                    pass

            if not os.path.isfile(os.path.join(personalbodyhealthdir, f'{bodyhealthfile}.csv')):
                CreateRequiredFiles.loadbodyhealthfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles'))
            else:
                changefile = input(
                    f'Current folder selected: {bodyhealthfile}.csv. Would you like to change files? \n[y/N]\n')
                if changefile == 'y':
                    CreateRequiredFiles.loadbodyhealthfile2(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles'))
                else:
                    pass

        except FileNotFoundError:
            raise FileNotFoundError(f'Error: file not found. Call "initdir" first.')

        personalinformation = open(os.path.join(personalbodyhealthdir, "BodyHealthPersonalInfo.txt"), 'r').readlines()
        DOB = personalinformation[0].strip('\n').split(':')[1]
        Gender = personalinformation[1].strip('\n').split(':')[1]
        if Gender == 'Unfilled' or DOB == 'Unfilled':
            # gender
            def validate_gender(value):
                try:
                    if value == 'M' or value == 'F':
                        return value
                    else:
                        raise ValueError(value)
                except ValueError:
                    raise click.BadParameter("Error: argument must be either 'M' or 'F'. ")
            Gender = click.prompt('Specify gender', value_proc=validate_gender, type=str)

            # DOB
            def validate_time(value):
                try:
                    timeerror = re.search('^(\d\d)(\d\d)(\d{4})$', value)
                    if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                            timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year:
                        raise ValueError(value)
                except (ValueError, AttributeError):
                    raise click.BadParameter("Invalid date input.", param=value)
                return value
            DOB = click.prompt('Please enter a valid date/time (format ddmmyyyy)', value_proc=validate_time,
                                 type=str)

            personalinformation[0] = f'DateOfBirth:{DOB}\n'
            personalinformation[1] = f'Gender:{Gender}\n'
            # dont change name
            with open(os.path.join(personalbodyhealthdir, "BodyHealthPersonalInfo.txt"), 'w+') as fd:
                fd.writelines(personalinformation)
            print(f'Personal info saved - DOB:{DOB}, Gender:{Gender}.')
        else:
            changeGenderDOB = input('Do you want to change date of birth and/or gender information? [y/N] ')
            if changeGenderDOB == 'y':
                # gender
                def validate_gender(value):
                    try:
                        if value == 'M' or value == 'F':
                            return value
                        else:
                            raise ValueError(value)
                    except ValueError:
                        raise click.BadParameter("Error: argument must be either 'M' or 'F'. ")

                Gender = click.prompt('Specify gender', value_proc=validate_gender, type=str)

                # DOB
                def validate_time(value):
                    try:
                        timeerror = re.search('^(\d\d)(\d\d)(\d{4})$', value)
                        if int(timeerror.group(1)) <= 0 or int(timeerror.group(1)) > 31 or int(
                                timeerror.group(2)) <= 0 or int(
                            timeerror.group(2)) > 12 or int(timeerror.group(3)) > dt.datetime.now().year:
                            raise ValueError(value)
                    except (ValueError, AttributeError):
                        raise click.BadParameter("Invalid date input.", param=value)
                    return value
                DOB = click.prompt('Please enter a valid date/time (format ddmmyyyy)', value_proc=validate_time,
                                   type=str)

                personalinformation[0] = f'DateOfBirth:{DOB}\n'
                personalinformation[1] = f'Gender:{Gender}\n'
                # dont change name
                with open(os.path.join(personalbodyhealthdir, "BodyHealthPersonalInfo.txt"), 'w+') as fd:
                    fd.writelines(personalinformation)
                print(f'Personal info saved - DOB:{DOB}, Gender:{Gender}.')
            else:
                return
    else:
        print('Error: function called with incorrect arguments')


@click.command()
@click.argument('all', default=1)
def queryalllogsBH(all):
    '''prints all logs of selected file in sorted form.'''
    if all == 1:
        # check cache
        checkandclearcache()

        pd.set_option('display.max_columns', None)  # print all columns
        pd.set_option('display.max_rows', None)  # print all rows
        try:
            logfile = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[7].strip(
                '\n').split('=')[1], f"{logfile}.csv")
            if os.path.isfile(logdir):
                log = pd.read_csv(logdir)
            else:
                raise Exception(f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        log.drop(log.columns[0], axis=1, inplace=True)
        if log.empty:
            print(f'No logs in file {logfile}.csv. ')
            return
        else:
            log['Time2'] = pd.to_datetime(log['ltime'], format='%d%m%Y-%H%M')
            log.sort_values(by=['Time2'], inplace=True)
            log.drop(log.columns[-1], axis=1, inplace=True)
            log.reset_index(drop=True, inplace=True)
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
@click.option('-d', '--querydate', prompt='Input date period to extract logs; format: \n'
                                          '(1)Day: ddmmyyyy_ddmmyyyy\n'
                                          '(2)12h, 6h, 3h: ddmmyyyy-HHMM_ddmmyyyy-HHMM\n', help='format: '
                                          '(1)Day: ddmmyyyy_ddmmyyyy'
                                          '(2)12h, 6h, 3h: ddmmyyyy-HHMM_ddmmyyyy-HHMM ')
def showlogbh(querydate):
    # check cache
    checkandclearcache()

    checkformatDAY = re.compile('^\d{8}[_]\d{8}$')
    checkformatOTHER = re.compile('^\d{8}[-]\d{4}[_]\d{8}[-]\d{4}$')
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
        startdate = querydate.split('_')[0]
        enddate = querydate.split('_')[1]
        pd.set_option('display.max_columns', None)  # print all columns
        pd.set_option('display.max_rows', None)  # print all rows
        try:
            logfile = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[7].strip(
                '\n').split('=')[1], f"{logfile}.csv")
            if os.path.isfile(logdir):
                log = pd.read_csv(logdir)
            else:
                raise Exception(
                    f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        log.drop(log.columns[0], axis=1, inplace=True)

        if log.empty:
            print(f'No logs in file {logfile}.csv. ')
            return
        else:
            log.sort_values(by=['ltime'], inplace=True)
            log['Time2'] = pd.to_datetime(log['ltime'], format='%d%m%Y-%H%M')
            mask = (log['Time2'] >= dt.datetime.strptime(startdate, '%d%m%Y')) & (
                        log['Time2'] <= dt.datetime.strptime(enddate, '%d%m%Y').replace(hour=23, minute=59))
            log = log.loc[mask]
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
        timeerror = re.search('^(\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)[_](\d\d)(\d\d)(\d{4})[-](\d\d)(\d\d)$',
                              querydate)
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
        startdate = querydate.split('_')[0]
        enddate = querydate.split('_')[1]
        pd.set_option('display.max_columns', None)  # print all columns
        pd.set_option('display.max_rows', None)  # print all rows
        try:
            logfile = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[7].strip(
                '\n').split('=')[1], f"{logfile}.csv")
            if os.path.isfile(logdir):
                log = pd.read_csv(logdir)
            else:
                raise Exception(
                    f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        log.drop(log.columns[0], axis=1, inplace=True)

        if log.empty:
            print(f'No logs in file {logfile}.csv. ')
            return
        else:
            log.sort_values(by=['ltime'], inplace=True)
            log['Time2'] = pd.to_datetime(log['ltime'], format='%d%m%Y-%H%M')
            mask = (log['Time2'] >= dt.datetime.strptime(startdate, '%d%m%Y-%H%M')) & (
                        log['Time2'] <= dt.datetime.strptime(enddate, '%d%m%Y-%H%M'))
            log = log.loc[mask]
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
                        '(1)Day: ddmmyyyy_ddmmyyyy\n'
                        '(2)12h, 6h, 3h: ddmmyyyy-HHMM_ddmmyyyy-HHMM\n')


@click.command()
@click.argument('modify', default=1)
def deletelogbh(modify):
    if modify == 1:
        try:
            config = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()
            logfile = config[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(config[7].strip('\n').split('=')[1], f"{logfile}.csv")
            # check cache
            maindir = checkandclearcache()
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        prompt = input(f'Are you sure you want to modify the selected log file "{logdir}"? [y/N]: ')
        if prompt == 'y':
            if os.path.isfile(logdir):
                log = pd.read_csv(logdir)
            else:
                raise Exception(
                    f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
            # fill nan with 'NA' string
            log.fillna('NA', inplace=True)
            modifydatetime = input('Input date and time of the log to delete (format "ddmmyyyy-HHMM") or '
                                   'input "prev" to delete previously made log: ')
            if modifydatetime == 'prev':
                try:
                    prompt2 = input(f"Delete following log? \n\n{log.iloc[-1]}\n [y/N]: ")
                    if prompt2 == 'y':
                        # first cache the file
                        CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                        # then continue with deleting file
                        log.drop(log.tail(1).index, inplace=True)  # drop last 1 row
                        log.drop(log.columns[0], axis=1, inplace=True)
                        log.to_csv(logdir)
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
                if log.loc[log['ltime'] == modifydatetime].empty:
                    print('No log found. Please try again. ')
                    return
                else:
                    if len(log.loc[log['ltime'] == modifydatetime]) == 1:
                        log.drop(log.columns[0], axis=1, inplace=True)
                        prompt3 = input(f"Delete following log? \n{log.loc[log['ltime'] == modifydatetime]}\n [y/N]: ")
                        if prompt3 == 'y':
                            # first cache the file
                            CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                            # then continue with deleting file
                            log.drop(log.loc[log['ltime'] == modifydatetime].index, inplace=True)
                            log.reset_index(drop=True, inplace=True)
                            # log.drop(log.columns[0], axis=1, inplace=True)
                            log.to_csv(logdir)
                            print('Log deleted. check file now.')
                        else:
                            print('Aborted process!')
                    else:
                        print(f'Multiple logs with log time {modifydatetime} found: ')
                        log.drop(log.columns[0], axis=1, inplace=True)
                        todelete = log.loc[log['ltime'] == modifydatetime].copy()
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
                            prompt4 = input(
                                f"Delete following log? \n{todelete.iloc[chooselog]}\n [y/N]: ")
                            if prompt4 == 'y':
                                # first cache the file
                                CreateRequiredFiles.caching((logfile+'BH'), log, '.csv', maindir)
                                # then continue with deleting file
                                log.drop(log.loc[log['ltime'] == modifydatetime].iloc[chooselog].name, inplace=True)
                                log.reset_index(drop=True, inplace=True)
                                log.to_csv(logdir)
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
def modifylogbh(mod):
    if mod == 1:
        try:
            logfile = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[7].strip(
                '\n').split('=')[1], f"{logfile}.csv")
            # check cache
            maindir = checkandclearcache()
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        modifydatetime = input('Input date and time of the log to modify (format "ddmmyyyy-HHMM") or '
                               'input "prev" to modify previously made log: ')
        if os.path.isfile(logdir):
            log = pd.read_csv(logdir)
        else:
            raise Exception(
                f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
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
                    CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                    # then continue with modifying file

                    time = log['ltime'].iloc[-1]
                    name = log['Name'].iloc[-1]
                    gender = log['Gender'].iloc[-1]
                    age = log['Age'].iloc[-1]
                    weight = log['Weight(kilograms)'].iloc[-1]
                    height = log['Height(metres)'].iloc[-1]
                    waistcircumf = log['Waist-Circumference(metres)'].iloc[-1]

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
                    timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)',
                                         value_proc=validate_time, type=str, default=time)

                    # name
                    def validate_name(value):
                        try:
                            if '_' in value:
                                raise ValueError(value)
                            else:
                                return value
                        except ValueError:
                            raise click.BadParameter("Error: cannot have '_' in name. ")
                    nameM = click.prompt('Specify name', value_proc=validate_name, type=str, default=name)

                    # gender
                    def validate_gender(value):
                        try:
                            if value == 'M' or value == 'F':
                                return value
                            else:
                                raise ValueError(value)
                        except ValueError:
                            raise click.BadParameter("Error: argument must be either 'M' or 'F'. ")
                    genderM = click.prompt('Specify gender', value_proc=validate_gender, type=str, default=gender)

                    # age
                    def validate_age(value):
                        try:
                            if age < 0:
                                raise ValueError(value)
                            else:
                                return value
                        except ValueError:
                            raise click.BadParameter("Error: age cannot be negative. ")
                    ageM = click.prompt('Specify age (in years)', value_proc=validate_age, type=int, default=age)

                    # weight
                    def validate_weightbh(value):
                        try:
                            if float(value) < 0:
                                raise ValueError(value)
                        except (ValueError, AttributeError):
                            raise click.BadParameter("Weight cannot be negative or string", param=value)
                        return value
                    weightM = click.prompt('Specify body weight (integer or decimal number in kilos)',
                                           value_proc=validate_weightbh, type=float, default=weight)

                    # height
                    def validate_heightbh(value):
                        try:
                            if float(value) < 0:
                                raise ValueError(value)
                        except (ValueError, AttributeError):
                            raise click.BadParameter("Height cannot be negative or string", param=value)
                        return value
                    heightM = click.prompt('Specify height (integer or decimal number in metres)',
                                           value_proc=validate_heightbh, type=float, default=height)

                    # waistcircumf
                    def validate_waistcircumfbh(value):
                        try:
                            if float(value) < 0:
                                raise ValueError(value)
                        except (ValueError, AttributeError):
                            raise click.BadParameter("Waist Circumference cannot be negative or string", param=value)
                        return value
                    waistcircumfM = click.prompt('Specify waist circumference (integer or decimal number in metres)',
                                           value_proc=validate_waistcircumfbh, type=float, default=waistcircumf)

                    BMI = float(weightM) / (float(heightM) ** 2)  # A BMI ≥30 is considered obese
                    if genderM == 'M':
                        RFM = 64 - (20 * (float(heightM) / float(waistcircumfM)))
                    elif genderM == 'F':
                        RFM = 76 - (20 * (float(heightM) / float(waistcircumfM)))

                    log.iloc[-1] = timeM, nameM, genderM, ageM, weightM, heightM, waistcircumfM, BMI, RFM
                    log.to_csv(logdir)
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
            elif log.loc[log['ltime'] == modifydatetime].empty:
                print('No log found for that time. Please try again. ')
                return
            else:
                if len(log.loc[log['ltime'] == modifydatetime]) == 1:
                    if click.confirm(f'Do you want to Modify following log? \n\n{log.loc[log["ltime"] == modifydatetime]}\n', abort=True):
                        # first cache the file
                        CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                        # then continue with modifying file
                        time = log.loc[log['ltime'] == modifydatetime]['ltime'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        name = log.loc[log['ltime'] == modifydatetime]['Name'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        gender = log.loc[log['ltime'] == modifydatetime]['Gender'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        age = log.loc[log['ltime'] == modifydatetime]['Age'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        weight = log.loc[log['ltime'] == modifydatetime]['Weight(kilograms)'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        height = log.loc[log['ltime'] == modifydatetime]['Height(metres)'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        waistcircumf = log.loc[log['ltime'] == modifydatetime]['Waist-Circumference(metres)'][log.loc[log['ltime'] == modifydatetime]['ltime'].index[0]]
                        chooselog = 0

                else:  # if multiple logs at same time
                    print(f'Multiple logs with log time {modifydatetime} found: ')
                    # log.drop(log.columns[0], axis=1, inplace=True)
                    tomodify = log.loc[log['ltime'] == modifydatetime].copy()
                    tomodify.reset_index(drop=True, inplace=True)
                    print(tomodify)
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
                                f'Do you want to Modify following log? \n\n{tomodify.iloc[chooselog]}\n',
                                abort=True):
                            # first cache the file
                            CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                            # then continue with modifying file
                            time = tomodify['ltime'][tomodify.index[chooselog]]
                            name = tomodify['Name'][tomodify.index[chooselog]]
                            gender = tomodify['Gender'][tomodify.index[chooselog]]
                            age = tomodify['Age'][tomodify.index[chooselog]]
                            weight = tomodify['Weight(kilograms)'][tomodify.index[chooselog]]
                            height = tomodify['Height(metres)'][tomodify.index[chooselog]]
                            waistcircumf = tomodify['Waist-Circumference(metres)'][tomodify.index[chooselog]]

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
                timeM = click.prompt('Please enter a valid date/time (format ddmmyyyy-HHMM)',
                                     value_proc=validate_time, type=str, default=time)

                # name
                def validate_name(value):
                    try:
                        if '_' in value:
                            raise ValueError(value)
                        else:
                            return value
                    except ValueError:
                        raise click.BadParameter("Error: cannot have '_' in name. ")
                nameM = click.prompt('Specify name', value_proc=validate_name, type=str, default=name)

                # gender
                def validate_gender(value):
                    try:
                        if value == 'M' or value == 'F':
                            return value
                        else:
                            raise ValueError(value)
                    except ValueError:
                        raise click.BadParameter("Error: argument must be either 'M' or 'F'. ")
                genderM = click.prompt('Specify gender', value_proc=validate_gender, type=str, default=gender)

                # age
                def validate_age(value):
                    try:
                        if age < 0:
                            raise ValueError(value)
                        else:
                            return value
                    except ValueError:
                        raise click.BadParameter("Error: age cannot be negative. ")
                ageM = click.prompt('Specify age (in years)', value_proc=validate_age, type=int, default=age)

                # weight
                def validate_weightbh(value):
                    try:
                        if float(value) < 0:
                            raise ValueError(value)
                    except (ValueError, AttributeError):
                        raise click.BadParameter("Weight cannot be negative or string", param=value)
                    return value
                weightM = click.prompt('Specify body weight (integer or decimal number in kilos)',
                                       value_proc=validate_weightbh, type=float, default=weight)

                # height
                def validate_heightbh(value):
                    try:
                        if float(value) < 0:
                            raise ValueError(value)
                    except (ValueError, AttributeError):
                        raise click.BadParameter("Height cannot be negative or string", param=value)
                    return value
                heightM = click.prompt('Specify height (integer or decimal number in metres)',
                                       value_proc=validate_heightbh, type=float, default=height)

                # waistcircumf
                def validate_waistcircumfbh(value):
                    try:
                        if float(value) < 0:
                            raise ValueError(value)
                    except (ValueError, AttributeError):
                        raise click.BadParameter("Waist Circumference cannot be negative or string", param=value)
                    return value
                waistcircumfM = click.prompt('Specify waist circumference (integer or decimal number in metres)',
                                       value_proc=validate_waistcircumfbh, type=float, default=waistcircumf)

                BMI = float(weightM) / (float(heightM) ** 2)  # A BMI ≥30 is considered obese
                if genderM == 'M':
                    RFM = 64 - (20 * (float(heightM) / float(waistcircumfM)))
                elif genderM == 'F':
                    RFM = 76 - (20 * (float(heightM) / float(waistcircumfM)))

                logname = log.loc[log["ltime"] == modifydatetime].iloc[chooselog].name
                log.loc[logname] = timeM, nameM, genderM, ageM, weightM, heightM, waistcircumfM, BMI, RFM
                log.to_csv(logdir)
                print(f'log modified: \n\n{log.loc[logname]}\n')

    else:
        raise Exception('Error: function called with incorrect arguments. Please try again. ')


@click.command()
@click.argument('show', default=1)
def printbhconfig(show):
    if show == 1:
        # checkcache
        checkandclearcache()

        config = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"),
                            'r').readlines()
        # filename = config[6].strip("\n").split("=")[1]
        filedir = config[7].strip('\n').split('=')[1]
        bhinfofile = open(os.path.join(f'{filedir}', 'BodyHealthPersonalInfo.txt'), 'r').readlines()
        bhinfofile[0] = ' ' + bhinfofile[0]
        print('\n')
        print(*bhinfofile)
    else:
        return


@click.command()
@click.argument('sort', default=1)
def sortlogfilebh(sort):
    if sort == 1:
        try:
            logfile = open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[6].strip(
                '\n').split('=')[1]
            logdir = os.path.join(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'AncillaryFiles', "config.txt"), 'r').readlines()[7].strip(
                '\n').split('=')[1], f"{logfile}.csv")
            # checkcache
            maindir = checkandclearcache()
        except FileNotFoundError as ex:
            raise FileNotFoundError("Error: Call 'initdir' first. ")
        prompt = input(f'Sort log file "{logdir}" by date and time? [y/N]: ')
        if prompt == 'y':
            if os.path.isfile(logdir):
                log = pd.read_csv(logdir)
                log.drop(log.columns[0], axis=1, inplace=True)
            else:
                raise Exception(f'Error: file {logdir} does not exist. Call "initdir" and then "inithealth" if you have not done so yet.')
            print(f'Sorting file "{logdir}"...')
            if log.empty:
                print(f'No logs in file {logfile}.csv. ')
                return
            else:
                # first cache the file
                CreateRequiredFiles.caching((logfile + 'BH'), log, '.csv', maindir)
                # then continue with deleting file
                log.fillna('NA', inplace=True)  # fill na with "NA"
                log['Time2'] = pd.to_datetime(log['ltime'], format='%d%m%Y-%H%M')
                log.sort_values(by=['Time2'], inplace=True)
                log.drop(log.columns[-1], axis=1, inplace=True)
                # log.sort_values(by=['ltime'], inplace=True)
                log.reset_index(drop=True, inplace=True)
                log.to_csv(logdir)
                print('File sorted.')
        else:
            print('Aborted process!')
            return
    else:
        raise Exception('Error: function called with incorrect argument.')


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