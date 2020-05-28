from setuptools import setup, find_packages

setup(
    name='ExerciseTerminal',
    version='0.0.1dev',
    # py_modules=['ExerciseTerminal', 'BodyHealthTerminal', 'CreateRequiredFiles'],
    packages=['exerciseterminal'],
    install_requires=[
        'Click',
        'pandas==1.0.3',
        'datetime',
    ],

    author='Tan Yann Xu',
    author_email='leejohn723@gmail.com',
    description='A lightweight CLI application for logging exercise and body information for easy statistical analysis; created using Click.',
    long_description='ExerciseTerminal is a CLI application that aims for ease of recording the timings of daily exercise regimes. Current functionality includes easy exporting to .csv files for further analysis.',
    keywords='exercise health healthy living',
    url='https://github.com/ckrat67/ExerciseTerminal',
    classifiers=[        
    	"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],

    entry_points='''
        [console_scripts]
        ex=exerciseterminal.ExerciseTerminal:log
        initdir=exerciseterminal.ExerciseTerminal:initialisefiledirectories
        dellog=exerciseterminal.ExerciseTerminal:deletelog
        modlog=exerciseterminal.ExerciseTerminal:modifylog
        createex=exerciseterminal.ExerciseTerminal:createnewexercise
        chknm=exerciseterminal.ExerciseTerminal:check_exnameexercise
        chkac=exerciseterminal.ExerciseTerminal:check_acronym
        setdir=exerciseterminal.ExerciseTerminal:changedefaultdir
        setlogfile=exerciseterminal.ExerciseTerminal:changeloggingfile
        delex=exerciseterminal.ExerciseTerminal:deleteexercise
        setreso=exerciseterminal.ExerciseTerminal:changereso
        setcp=exerciseterminal.ExerciseTerminal:changeCP
        setext=exerciseterminal.ExerciseTerminal:changeEXT
        querylog=exerciseterminal.ExerciseTerminal:showlog
        alllogs=exerciseterminal.ExerciseTerminal:queryalllogs
        sortlog=exerciseterminal.ExerciseTerminal:sortlogfile
        sortleg=exerciseterminal.ExerciseTerminal:sortlegend
        etconfig=exerciseterminal.ExerciseTerminal:printconfig
        inithealth=exerciseterminal.BodyHealthTerminal:initialisehealth
        logh=exerciseterminal.BodyHealthTerminal:logH
        bhinfo=exerciseterminal.BodyHealthTerminal:printbhconfig
        alllogsbh=exerciseterminal.BodyHealthTerminal:queryalllogsBH
        querylogbh=exerciseterminal.BodyHealthTerminal:showlogbh
        dellogbh=exerciseterminal.BodyHealthTerminal:deletelogbh
        modlogbh=exerciseterminal.BodyHealthTerminal:modifylogbh
        sortlogbh=exerciseterminal.BodyHealthTerminal:sortlogfilebh
        
    ''',
)