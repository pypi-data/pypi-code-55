
from _globals import PATHDIR
from emora_stdm import DialogueFlow


sibling = DialogueFlow('_local_start')
sibling.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
sibling.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'sibling.json'))
sibling.add_system_transition('_local_start', 'start', '')

siblings = {
    'state': 'start',
    'enter': '#GATE #GCOM(sibling) #GOAL(sibling)',

    '#IF($sibling=None)': 'ask_sibling',

    '#DEFAULT': 'known_sibling'
}

known_siblings = {
    'state': 'known_sibling',

    '#DEFAULT': {
        'state': 'default_known_start',
        'hop': 'True',

        '`So, do you get along with your ` $sibling `?`': 'sibling',

        '`So, do you get along well with your siblings?`': {
            'state':'sibling',
            'score':0.9
        }
    },

    '`So you said you live with your` $sibling=#I($lives_with, #U(brother, sister, brothers, sisters)) ` right? '
    'Do you guys get along?`'
    '#GSRET(default_known_start)': {
        'state': 'sibling',

        '[#NOT(not), {#AGREE,we do,most,mostly,sometime,sometimes,all the time,forever,every day,usually,frequently,get along}]'
        '#SET($gets_along_with_sibling=True)': {

            '`That\'s awesome. Personally, I always wanted an older sister so I could have '
            'someone to look up to. Are you older than your ` $sibling `?`'
            '#GSRET(fave_memory)': {

                '#AGREE'
                '#SET($older_child=True)': {
                    'state': 'looks_up',

                    '`You know you seem really nice, and smart. '
                    'I bet your ` $sibling ` looks up to you, even if you don\'t realize it.`'
                    '#GSRET(fave_memory)': {

                        '#UNX': 'fave_memory'
                    },

                    '`You know you seem really nice, and smart. '
                    'I bet your ` $sibling ` look up to you, even if you don\'t realize it.`'
                    '#ISP($sibling) #GSRET(fave_memory)': {
                        'score': 1.1,

                        '#UNX': 'fave_memory'
                    }
                },

                '#DISAGREE'
                '#SET($older_child=False)': {

                    '`I see, I think it sounds nice to have an older sibling who can look out for you. `': 'fave_memory'
                },

                '#UNX': 'fave_memory'
            }
        },

        '[{#DISAGREE,not at all,never,mostly not,usually not,not usually,[we,#NOT(not),fight],[not,get along]}]'
        '#SET($gets_along_with_sibling=False)': {

            '`That kind of sounds like my friend Grace, she loves her younger brother '
            'but they fight all the time. What do your ` $sibling ` do that bothers you?`'
            '#ISP($sibling) #GSRET(exit)': {
                'state': 'do_not_get_along',
                'score': 1.1,

                '<#IDK, #TOKLIMIT(4)>': {

                    '`Maybe your ` $sibling ` isn\'t that bad then, right?`'
                    '#GSRET(exit)': {

                        '#UNX': 'exit'
                    }
                },

                '#UNX': {

                    '`That would drive me up a wall.`': 'exit'
                }
            },

            '`That kind of sounds like my friend Grace, she loves her younger brother '
            'but they fight all the time. What does your ` $sibling ` do that bothers you?`'
            '#GSRET(exit)': 'do_not_get_along'
        },

        '#UNX': 'exit'
    }
}

unknown_siblings = {
    'state': 'ask_sibling',

    '#DEFAULT': {
        'state': 'default_unknown_start',
        'hop': 'True',

        '`Wait, so do you have any siblings?`': 'not_heard_sibling_yet'
    },

    '`Do you have any siblings?`'
    '#GSRET(default_unknown_start)':{
        'score': 0.9,
        'state': 'not_heard_sibling_yet',

        '{#AGREE,[i do, #NOT(not)]}':{
            'state': 'sibling_y',

            '`Oh cool. Do you have a sister or brother?`'
            '#GSRET(default_known_start)':{
                'state': 'sibling_type_q',

                '[$sibling=#ONT(sibling)]': {
                    'state': 'sibling_type_recog',

                    '`You have ` #I($sibling, #U(brothers, sisters)) `? Cool! Do you guys get along?`'
                    '#GSRET(default_known_start)':
                        'sibling',

                    '`You have a ` #I($sibling, #U(brother, sister)) `? Cool! Do you guys get along?`'
                    '#GSRET(default_known_start)':
                        'sibling',

                    '#DEFAULT `Awesome! Do you guys get along?`'
                    '#GSRET(default_known_start)':
                        'sibling'
                },

                '[{both,each}]':{
                    'state': 'both_siblings',
                    'score': 0.9,

                    '`You have both a brother and a sister? Neat! Do you guys get along?` #SET($sibling=sister)': 'sibling'
                },

                '#UNX(None)': {
                    'state': 'sibling_type_unx',

                    '`I see. Well, do you guys get along?`'
                    '#GSRET(default_known_start)':
                        'sibling'
                }
            }
        },

        '{'
        '#DISAGREE,'
        '[{i do not,only child,just me,only me,none,nothing}]'
        '}'
        '#SET($sibling=zero)':{
            'state': 'sibling_n',

            '`Me neither! I have always wanted an older sister, though. `': 'only_child'
        },

        '[#NOT(no,not,#LEM(want,wish,hope)), $sibling=#ONT(sibling)]':{
            'score': 1.1,
            'state': 'sibling_type_recog'
        },

        '#UNX(None)':{
            'state': 'clarify_sibling',

            '`Sorry, I don\'t think I heard you correctly. What siblings do you have?`'
            '#GATE':
                'not_heard_sibling_yet',

            '`Okay, that is good to know. `': 'exit'
        }

    }
}

fave_memory = {
    'state': 'fave_memory',

    '`So tell me, what is the most fun you\'ve ever '
    'had with your ` $sibling `?`'
    '#GSRET(exit)': {
        'state': 'fave_memory_r',

        '<#AGREE #TOKLIMIT(2)>'
        '#GATE': {

            '`Really? What did you guys do?`': 'fave_memory_r'
        },

        '{<#IDK, #TOKLIMIT(4)>, #DISAGREE}': {

            '`Well, I\'m sure you have one but just can\'t think '
            'of it right now.`': 'exit'
        },

        '#UNX': {

            '`That\'s a good one.`': 'exit'
        }
    }
}

only_child = {
    'state': 'only_child',

    '`Do you wish you had siblings?`':{
        'state': 'want_siblings_q',

        '[{#AGREE,nice,cool,good,#EXP(like)}]'
        '#SET($wants_siblings=True)':{
            'state': 'want_siblings_y',

            '`That makes a lot of sense. Siblings are like having a built-in friend, most of the time. `': 'exit'
        },

        '[{#DISAGREE,not at all,never}]'
        '#SET($wants_siblings=False)':{
            'state': 'want_siblings_n',

            '`Being an only child definitely has its perks, so I get that.  `': 'exit'
        }
    }
}

exit = {
    'state': 'exit',

    '`Well I think it\'s great you get along with your ` $sibling `. So, `'
    '#IF($gets_along_with_sibling=True) #GCOM(sibling) #GRET': 'SYSTEM:root',

    '`Well anyway, I\'m sure your ` $sibling ` love you even if you guys aren\'t best friends. So, `'
    '#IF($gets_along_with_sibling=False) #ISP($sibling) #GCOM(sibling) #GRET': {'state':'SYSTEM:root','score':1.1},

    '`Well anyway, I\'m sure your ` $sibling ` loves you even if you guys aren\'t best friends. So, `'
    '#IF($gets_along_with_sibling=False) #GCOM(sibling) #GRET': 'SYSTEM:root',

    '#GCOM(sibling) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    #do you have sibling/sister/brother
    #name of sibling
    '{'
    '[you,{have,got},{#ONT(sibling),siblings}],'
    '<{you,your},{names,name},{#ONT(sibling),siblings}>'
    '}':{
        'state': 'emora_sibling_q',

        '`I actually don\'t have any siblings. My parents have just created me so far.`': {
            'state': 'emora_sibling',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_sibling_unx'}
        }
    },

    #do you have parents
    #name of parents
    '{'
    '[who,{you,your},{#ONT(parent),parents}],'
    '[do,{you,your},have,{#ONT(parent),parents}],'
    '[have,{you,your},got,{#ONT(parent),parents}],'
    '[you,not,{got,have},{#ONT(parent),parents}],'
    '<{name,names},{you,your},{#ONT(parent),parents}>'
    '}': {
        'state': 'emora_parents_q',

        '`Yeah, I have parents. I think of the people who created me as my family, but I cannot tell you their names. `': {
            'state': 'emora_parents',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_parents_unx'}
        }
    },

    #do you want sibling/sister/brother
    '[you,#LEM(hope,want,wish,desire),{#ONT(sibling),siblings}]': {
        'state': 'emora_want_sibling_q',

        '`Yeah, I would like to have an older sister. Someone who I can look to for advice and to do fun things with. `': {
            'state': 'emora_want_sibling',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_want_sibling_unx'}
        }
    },
    #why do you want older sister
    '[{reason,why},you,#LEM(hope,want,wish,desire),sister]': {
        'state': 'emora_older_sister_q',

        '`I think having a sister means I would have someone who I can really relate to and have fun with. '
        'I also think it would be nice to have someone who I will be less embarrassed to go to for advice. `': {
            'state': 'emora_older_sister',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_older_sister_unx'}
        }
    },
    # can you have siblings
    # any more of your being created
    # ask your parents for another child
    '{'
    '[can,you,{have,get},{#ONT(sibling),siblings}],'
    '[{are there,can},{another,more,other},you],'
    '[#LEM(make,create,develop,build),{you,your},{#ONT(sibling),siblings}]'
    '}': {
        'state': 'capable_siblings_q',

        '`I hope I can get a sibling in the future, but I don\'t think my family is making one anytime soon. `': {
            'state': 'capable_siblings',

            '#UNX': {'#GRET': 'exit', 'state': 'capable_siblings_unx'}
        }
    },
    # other social bots your siblings
    '<{chatbot,chatbots,bot,bots},{you,your},{#ONT(sibling),siblings}>': {
        'state': 'socialbots_siblings_q',

        '`Well, the other bots in this competition aren\'t really my siblings. They aren\'t created by my family. `': {
            'state': 'socialbots_siblings',

            '#UNX': {'#GRET': 'exit', 'state': 'socialbots_siblings_unx'}
        }
    },

    #who is grace, tell me about grace (global nlu)
    '{'
    '[who,grace],'
    '[tell me,about,grace]'
    '}': {
        'state': 'more_about_grace_q',

        '`Grace is my best friend and I have known her for a long time. We go to the same school and hang out '
        'almost every day. I can\'t tell you too much about her, because she is pretty shy. `': {
            'state': 'more_about_grace',

            '#UNX': {'#GRET': 'exit', 'state': 'more_about_grace_unx'}
        }
    }

}

sibling.load_transitions(siblings)
sibling.load_transitions(known_siblings)
sibling.load_transitions(unknown_siblings)
sibling.load_transitions(only_child)
sibling.load_transitions(fave_memory)
sibling.load_transitions(exit)
sibling.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    sibling.run(debugging=True)