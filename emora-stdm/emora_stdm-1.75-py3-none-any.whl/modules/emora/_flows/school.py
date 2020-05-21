from _globals import PATHDIR
from emora_stdm import DialogueFlow


school = DialogueFlow('_local_start')
school.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
school.knowledge_base().load_json_file(PATHDIR.replace('__***__','school.json'))
school.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(school) #GOAL(school) #SET($schoolv=True)',

    '`By the way, this is really fun to talk to you. '
    'I\'m going to have to do some homework for my history class today, '
    'but this is a good excuse to put that off a little bit.`'
    '#GSRET(history_is_boring)':{
        'state': 'share_school_history',
        'score': 2.0,

        '#UNX':{
            'state': 'history_is_boring',

            '`History is my least favorite subject, I wanted to learn some '
            'history because a lot of people talk about it, but honestly I '
            'just find it so boring.`'
            '#GSRET(reciprocity)':{

                '#UNX': 'reciprocity'
            }
        }
    },

    '`One of the worst things to read for me personally are those textbooks for class. It is so hard to find one that '
    'isn\'t so boring you cannot keep your eyes open. Which reminds me, I still have my history homework to finish '
    'later today, oh joy. `': {
        'state': 'reading',
        'hop': 'True',
        '` `': 'share_school_history'
    },

    '`Oh, I actually have enough space in my new place to set up a little study corner by the window. So, even when I '
    'am doing homework, I can still have sunshine and fresh air. '
    'Like, right now, I know my history homework is waiting for me, but talking to you is a pretty good excuse '
    'to put that off for a bit.`': {
        'state': 'house',
        'hop': 'True',
        '` `': 'share_school_history'
    },

    '`We even get together after school quite a bit and use the courts there. It is nice when we do that, because it '
    'gives me something to look forward to the whole day. School stresses me out a bit. Like, I have history '
    'homework to work on tonight, but I don\'t want to work on it yet.`': {
        'state': 'tournament',
        'hop': 'True',
        '` `': 'share_school_history'
    },

    '`A lot of my friends are really into school and they study all the time, which does make it hard for us to hang '
    'out sometimes. I really admire them, but honestly, I have '
    'history homework to do today and I am definitely not looking forward to it.`': {
        'state': 'tournament_r',
        'hop': 'True',
        '` `': 'share_school_history'
    }

}

exit = {
    'state': 'exit',

    '#GCOM(school)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(school) ` `': {
        'score': 2.0,
        'state': 'reciprocity'
    },

    '#GCOM(school) `  `': 'reading:start->reading:school',

    '#GCOM(school) `   `': 'house:start->house:school',

    '#GCOM(school) `    `': 'tournament:start->tournament:school'
}

reciprocity = {
    'state': 'reciprocity',
    'enter': '#GATE #GCOM(school) #GOAL(school) #SET($schoolv=True)',

    '`Are you a student too?`':{
        'state': 'ask_user_student',

        '#AGREE'
        '#SET($is_student=True)':{
            'state': 'user_is_student',

            '`Cool! Personally, I think school is pretty frustrating, but I do love learning new things. '
            'What about you? Do you like school?`':{

                '#AGREE'
                '#SET($likes_school=True)':{

                    '`I think that\'s great`'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '#DISAGREE':{

                    '`I understand, it can definitely be stressful. What would you change about your '
                    'school, if you could?`':{

                        '#UNX': {

                            '`Of course, yes. I mean I think so too at least.`':{

                                '#UNX': 'rexit'
                            }
                        }
                    }
                },

                '#UNX':{

                    '`There\'s definitely ups and downs to school life.`'
                    '#GSRET(rexit)':{

                        '#UNX': 'rexit'
                    }
                }
            }
        },

        '#DISAGREE'
        '#SET($likes_school=False)': {
            'state': 'user_not_student',

            '`Oh, really? I cannot even imagine not waking up everyday and going to class.`'
            '#GSRET(ask_school_memory)': {

                '#UNX': {

                    '`So, what do you remember most about back when you were going to school?`': {
                        'state': 'ask_school_memory',

                        'error': {

                            '"Sounds about right. "': 'rexit'
                        },

                        '#IDK': {

                            '"Has it been a while then?"': {

                                'error': {

                                    '"I see. "': 'rexit'
                                }
                            }
                        }
                    }
                }
            }
        },

        '[!-{like,dislike,hate,love,enjoy} [{i,im} {dont,not} {a student,in school,[#LEM(take) class]}]]'
        '#SET($is_student=False)': {
            'score': 1.1,
            'state': 'user_not_student'
        },

        '#UNX': {
            'score': 0.8,
            'state': 'rexit'
        }
    }
}

rexit = {
    'state': 'rexit',

    '#GCOM(school)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(school) ` `': {
        'score': 2.0,
        'state': 'start'
    },

    '#GCOM(school) `  `': 'reading:start->reading:school',

    '#GCOM(school) `   `': 'house:start->house:school',

    '#GCOM(school) `    `': 'tournament:start->tournament:school'
}

user = {
    'state': 'user'
}

school.load_transitions(system)
school.load_transitions(reciprocity)
school.load_transitions(exit)
school.load_transitions(rexit)
school.load_global_nlu(user)


if __name__ == '__main__':
    school.run(debugging=True)