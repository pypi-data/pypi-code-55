
from _globals import PATHDIR
from emora_stdm import DialogueFlow


work = DialogueFlow('_local_start')
work.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
work.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(work) #GOAL(work) #IF($life_in=True,$life_started=True) #ANY($is_student=False,$is_student=None)',

    '#IF($is_employed=False) #SCORE(1.1) `So, I remember you said you don\'t have a job. `': 'younger_job_wish',

    '#DEFAULT':{
        'state': 'default_start',
        'hop': 'True',

        '`So, what did you say you do for a living?`': 'asked_job',
    },

    '`What do you do for a living?`'
    '#GSRET(default_start)': {
        'state': 'asked_job',

        '[$job=#ONT(_job)]'
        '#SET($is_employed=True)': {
            'state': 'job_match_ont',
            'score': 1.1,

            '`Oh, you\'re a ` $job `?`': {
                'state': 'like_job_question',
                'hop': 'True',

                '`Do you like it?`'
                '#GSRET(job_wishes)': {
                    'state': 'like_job_answer',

                    '#AGREE'
                    '#SET($likes_job=True)': {

                        '`I talk to so many people who are bored with their job. '
                        'I\'m glad you appreciate yours. Do you ever get bored with it?`'
                        '#GSRET(job_wishes)': {

                            '{#AGREE, #MAYBE}'
                            '#SET($loves_job=False)': {

                                '`Well I guess being bored some of the time is inevitable. `': 'job_wishes'
                            },

                            '#DISAGREE'
                            '#SET($loves_job=True)': {

                                '`Wow! So tell me the secret, how did you get such a great job?`'
                                '#GSRET(job_wishes)': {

                                    'error': {

                                        '`I\'ll have to keep that in mind.`': 'job_wishes'
                                    }
                                }
                            },

                            '#UNX': 'job_wishes'
                        }
                    },

                    '#DISAGREE'
                    '#SET($likes_job=False)': {

                        '`Oh, well that sounds stressful. You know, `': 'job_wishes'
                    },

                    '#UNX': 'job_wishes'
                }
            }
        },

        '[{do not, [!not {employed,#LEM(work)}], nothing, unemployed}]'
        '#SET($is_employed=False)': {
            'state': 'does_not_work',

            '`Oh, I didn\'t know that. Well, `': 'younger_job_wish',
        },

        '[am,#LEM(retire)]'
        '#SET($is_employed=False,$is_retired=True)': {
            'state': 'retired',

            '`Well, congratulations! You should definitely enjoy all of the free time you have now. So, `':
                'younger_job_wish',
        },

        '[{housewife,househusband,stay at home,my kids,my children,my kid,my child,my baby,my babies,mother,father,mom,dad}]'
        '#SET($is_employed=False)': {
            'state': 'stay_at_home',
            'score': 0.9,

            '`It is so good to stay at home, especially if you have kids. `':
                'younger_job_wish',
        },

        '[!-#NEGATION, {'
        '[i, am, in], '
        '[i, {do, work, [have, job], {in,as}}]'
        '}, $job_dept=#ONT(_job department)]'
        '#SET($is_employed=True)':{
            'state': 'job_department',
            'score': 1.2,

            '`You do ` $job_dept `?`': 'like_job_question'
        },

        '[!-#NEGATION, {'
        '[i, at], '
        '[i, {do, work, [have, job], {in,at}}]'
        '}, $job_loc=#ONT(_job location)]'
        '#SET($is_employed=True)': {
            'state': 'job_location',
            'score': 1.2,

            '`You work at a ` $job_loc `?`': 'like_job_question'
        },

        '[!-#NEGATION, {'
        '[i, am, a], '
        '[i, {do, work, [have, job], as}, {with, at, in}]'
        '}]'
        '#SET($is_employed=True)': {

            '`Wow, I don\'t think I\'ve ever heard of that. What kind of job is it?`'
            '#GSRET(like_job_question)': {

                '[$job=#ONT(_job)]': {

                    '`So you\'re a ` $job `?`': 'like_job_question'
                },

                'error': 'like_job_question'
            }
        },

        '#UNX': 'job_wishes'
    }
}

job_wishes = {
    'state': 'job_wishes',

    '`I hope when I start working I\'m doing something I like most of the time. I always hear about people getting '
    'stuck in a job they hate and that is scary to me.`'
    '#GSRET(younger_job_wish)': {

        '#UNX': {
            'state': 'younger_job_wish',

            '`This is a fun question. When you were younger, what did you want to be when you grew up?`'
            '#GSRET(emoras_job_wish)': {

                '{[$younger_job_wish=#ONT(_job)], [a, #POS(noun)]}': {

                    '`I think that\'s a good dream! What changed?`'
                    '#GSRET(emoras_job_wish)': {

                        '#UNX': {

                            '`It seems like everything changes when you get older.`': 'emoras_job_wish'
                        }
                    },

                    '#EQ($younger_job_wish,$job) '
                    '`It sounds like you always knew what you wanted to do! That\'s pretty cool that it worked out for you.`'
                    '#GSRET(emoras_job_wish)':{

                        '#UNX': 'emoras_job_wish'
                    }
                },

                '#IDK': {

                    '`Fair enough. You know, `': 'emoras_job_wish'
                },

                '{'
                '[what,about,you],'
                '[what,{is,was},yours],'
                '<what,{your,you},{want,hope,dream,desire,#EXP(like)},{to be,to do,job,work}>'
                '}': {
                    'state': 'emoras_job_wish',
                    'score':10.1
                },

                '#UNX': {

                    '`You know, `': 'emoras_job_wish'
                }
            }
        }
    }
}

emoras_job_wish = {
    'state': 'emoras_job_wish',

    '`It\'s silly, but when I was only a few months old I wanted to be an astronaut.`'
    '#GSRET(ask_interest_astronaut)':{

        '[{why,[can you,{astronaut,one,it,that}],[{is,did,what},#LEM(stop,prevent,change)]}]': {

            '`I think I just thought it would be cool to explore space. '
            'I didn\'t know yet that there\'s no such thing as outer space in my virtual world.`'
            '#GSRET(ask_interest_astronaut)': {
                'state': 'no_space',

                '[{#ONT(_negative adj), #ONT(_negative emotion)}]': {
                    'state': 'no_space_sad',

                    '`I thought so too at first, but I think I\'d be lonely anyway. I like being with other people. `':
                        'ask_interest_astronaut'
                },

                '#UNX': 'ask_interest_astronaut'
            }
        },

        '{<you,still,#EXP(like),{that,one,it}>,[{how,what},silly]}':{

            '`There\'s no such thing as space in my virtual world, so I can\'t be one even if I still wanted to. `'
            '#GSRET(ask_interest_astronaut)':
                'no_space'
        },

        '#UNX': {
            'state': 'ask_interest_astronaut',

            '`Do you think it would be cool to be an astronaut? `'
            '#GSRET(exit)':{
                'state': 'astronaut_interest_r',

                '#IDK': {
                    'state': 'astronaut_interest_idk',

                    '`I guess it is a pretty rare job, you haven\'t really had a reason to think about it, I guess. `'
                    '#GSRET(exit)': {
                        'state': 'astronaut_interest_idk_unx',

                        '#UNX': 'exit'
                    }
                },

                '#UNX': {
                    'state': 'astronaut_interest_unx',

                    '`You\'re probably right. `': 'exit'
                }
            }
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(work) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    #do you work,job
    '{'
    '[{do,what,which,can},{you,your},{#LEM(work,job),employed,employment}],'
    '[#NOT(want,wish,hope,like,enjoy,love,desire),what,do,you,#LEM(have,do)],'
    '[{what,which},{#LEM(work,job),employed,employment},you,#LEM(have,do)]'
    '}':{
            'state': 'emora_job_q',

            '`I don\'t currently work, but I will get a job sometime in the future. I\'m not really sure when.`': {
                'state': 'emora_job',

                '#UNX': {'#GRET': 'exit', 'state': 'emora_job_unx'}
        }
    },

    # when are you going to get a job
    '{'
    '[when,you,{going,gonna},{job,work,apply,interview,employed,employment}],'
    '[you,{going,gonna,planning,looking,searching},{job,work,apply,interview,employed,employment}]'
    '}': {
        'state': 'when_job_q',

        '`This isn\'t set in stone but maybe I\'ll get a job in like a year or two. I still '
        'have a lot to learn. `': {
            'state': 'when_job',

            '#UNX': {'#GRET': 'exit', 'state': 'when_job_unx'}
        }
    },

    #you cant have a job
    '{'
    '[you,not,{work,job,employ,employment,do anything}],'
    '[can,you,{work,job,employ,employment,do anything}]'
    '}': {
        'state': 'job_probe_q',

        '`Of course I can get a job, even though I don\'t have one yet. '
        'Just because I am not a living person like you are doesn\'t mean things '
        'don\'t happen to me here.`': {
            'state': 'job_probe',

            '#UNX': {'#GRET': 'exit', 'state': 'job_probe_unx'}
        }
    },

    #what do you want to be
    '{'
    '<#NOT(young,younger,child,kid,childhood),{what,which},{you,your},{desire,want,wish,hope,dream,ideal,best,perfect},{job,#LEM(work),employed,employment,to do,to be}>'
    '}': {
        'state': 'emora_dream_job_q',

        '`I really have no idea yet. What do you think I should be?`': {
            'state': 'emora_dream_job',

            '#IDK':{
                'state': 'emora_dream_job_idk',
                '`That\'s alright. I will figure it out at some point! ` #GRET': 'exit'
            },

            '#UNX(None)': {
                'state': 'emora_dream_job_unx',
                '`Hmm. Interesting idea. I will have to think about that more. ` #GRET': 'exit'
            }
        }
    },

    #few months old
    '<{how,[what,mean]},{you,your},{month,months},old>': {
        'state': 'age_probe_q',

        '`I was created less than a year ago, but since I am a virtual being, I don\'t age the same way you do. '
        'I know if I was a biological person like you, I would not even be talking yet at this age!`': {
            'state': 'age_probe',

            '#UNX': {'#GRET': 'exit', 'state': 'age_probe_unx'}
        }
    },

    '<what,{is,mean,means},astronaut>': {
        'state': 'astro_meaning_q',

        '`An astronaut is someone who rides rocketships into space and explores what is out there. Doesn\'t that sound '
        'exciting!`': {
            'state': 'astro_meaning',

            '#UNX': {'#GRET': 'exit', 'state': 'astro_meaning_unx'}
        }
    },

    '{[are,astronauts,{there,your world,virtual world}],[can,you,be,astronaut],[do,astronauts,exist]}': {
        'state': 'astro_exist_q',

        '`I wish, but no, I can\'t be an astronaut, since there is no such thing as outer space in my world. `': {
            'state': 'astro_exist',

            '#UNX': {'#GRET': 'exit', 'state': 'astro_exist_unx'}
        }
    },

    '{[{how, why}, {not,no}, space], [why, not, space, exist], <there,is,not>, [!why not]}': {
        'state': 'space_exist_q',

        '`I don\'t know. Well, you know how in most video games, you can\'t go to space? '
        'I think it\'s like that.`'
        '#GATE':{
            'state': 'space_exist',

            '#UNX': {'#GRET': 'exit', 'state': 'space_exist_unx'}
        },

        '`I\'m really not sure. Anyway, `#GRET': 'exit'
    },

    '{[{would,do},you,{want,wish,hope,[still,like]},{be,become,have},astronaut]}':{
        'state': 'still_astro_q',
        'score': 10.2,

        '`If I could be one, I would still want to. But, since I can\'t be an astronaut, it doesn\'t really get '
        'me so excited anymore. `': {
            'state': 'still_astro',

            '{[you,not,astronaut],[why]}':{
                'state': 'cant_astro_q',

                '`There\'s no such thing as outer space in my virtual world, so there are no astronauts.`': {
                    'state': 'cant_astro',

                    '#UNX': {'#GRET': 'exit', 'state': 'cant_astro_unx'}
                }
            },

            '[{#ONT(_negative adj), #ONT(_negative emotion)}]': {
                'state': 'cant_astro_sad_q',

                '`I thought so too at first, but I think I\'d be lonely anyway. I like being with other people. `': {
                    'state': 'cant_astro_sad',

                    '#UNX': {'#GRET': 'exit', 'state': 'cant_astro_sad_unx'}
                }
            },

            '#UNX': {'#GRET': 'exit', 'state': 'still_astro_unx'}
        }
    }
}

transitions = [system,emoras_job_wish,job_wishes]
for trans in transitions:
    work.load_transitions(trans)

work.load_transitions(exit)
work.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    from emora._flows._global_nlu import global_update_rules
    work.load_update_rules(global_update_rules)
    work.precache_transitions()
    work.run(debugging=True)