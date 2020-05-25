
from _globals import PATHDIR
from emora_stdm import DialogueFlow


sibling = DialogueFlow('_local_start')
sibling.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
sibling.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'sibling.json'))
sibling.add_system_transition('_local_start', 'start', '')

siblings = {
    'state': 'start',
    'enter': '#GATE #GCOM(sibling) #GOAL(sibling)',

    '`So you said you live with your` $sibling=#I($lives_with, #U(brothers, sisters)) ` right? '
    'Do you guys get along?`': 'sibling',

    '`So you said you live with your` $sibling=#I($lives_with, #U(brother, sister)) ` right? '
    'Do you guys get along?`': {
        'state': 'sibling',

        '#AGREE'
        '#SET($gets_along_with_sibling=True)': {

            '`That\'s awesome. Personally, I always wanted an older sister so I could have '
            'someone to look up to. Are you older than your ` $sibling `?`': {

                '#AGREE'
                '#SET($older_child=True)': {
                    'state': 'looks_up',

                    '`You know you seem really nice, and smart. '
                    'I bet your ` $sibling ` looks up to you, even if you don\'t realize it.`': {

                        '#UNX': 'fave_memory'
                    },

                    '`You know you seem really nice, and smart. '
                    'I bet your ` $sibling ` look up to you, even if you don\'t realize it.`'
                    '#ISP($sibling)': {
                        'score': 1.1,

                        '#UNX': 'fave_memory'
                    }
                },

                '#DISAGREE'
                '#SET($older_child=False)': {

                    '`I see, I think that\'s nice. `': {
                        'state': 'fave_memory',
                        'hop': 'True',

                        '`So tell me, what is the most fun you\'ve ever'
                        'had with your ` $sibling `?`': {

                            '<#AGREE #TOKLIMIT(2)>': {

                                '`Great, tell me!`': 'fave_memory'
                            },

                            '{<#IDK, #TOKLIMIT(4)>, #DISAGREE}': {

                                '`Well I\'m sure you have one but just can\'t think '
                                'of it right now.`': 'exit'
                            },

                            '#UNX': {

                                '`That\'s a good one.`': 'exit'
                            }
                        }
                    }
                },

                '#UNX': 'fave_memory'
            }
        },

        '#DISAGREE'
        '#SET($gets_along_with_sibling=False)': {

            '`That kind of sounds like my friend Grace, she loves her younger brother '
            'but they fight all the time. What does your ` $sibling ` do that bothers you?`': {

                '<#IDK, #TOKLIMIT(4)>': {

                    '`Maybe your ` $sibling ` isn\'t that bad then, right?`': {

                        '#UNX': 'exit'
                    }
                },

                '#UNX': {

                    '`That would drive me up a wall.`': 'exit'
                }
            }
        },

        '#UNX': 'exit'
    },

    #dont know sibling yet
    '`Do you have any siblings?`':{
        'score': 0.9,
        'state': 'not_heard_sibling_yet',

        '{#AGREE,[i do, #NOT(not)]}':{
            'state': 'sibling_y',

            '`Oh cool. Do you have a sister or brother?`':{
                'state': 'sibling_type_q',

                '[$sibling=#ONT(sibling)]': {
                    'state': 'sibling_type_recog',

                    '`You have ` #I($sibling, #U(brothers, sisters)) `? Awesome! Do you guys get along?`': 'sibling',

                    '`You have a ` #I($sibling, #U(brother, sister)) `? Awesome! Do you guys get along?`': 'sibling',

                    '#DEFAULT `Awesome! Do you guys get along?`': 'sibling'
                },

                '#UNX(None)': {
                    'state': 'sibling_type_unx',

                    '`I see. Well, do you guys get along?`': 'sibling'
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

only_child = {
    'state': 'only_child',

    '`Do you wish you had siblings?`':{

    }
}

exit = {
    'state': 'exit',

    '`Well I think it\'s great you get along with your ` $sibling `. So, `'
    '#IF($gets_along_with_sibling=True) #GCOM(sibling) #GRET': 'SYSTEM:root',

    '`Well anyway, I\'m sure your ` $sibling ` loves you even if you guys aren\'t best friends. So, `'
    '#IF($gets_along_with_sibling=False) #GCOM(sibling) #GRET': 'SYSTEM:root',

    '#GCOM(sibling) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

sibling.load_transitions(siblings)
sibling.load_transitions(only_child)
sibling.load_transitions(exit)
sibling.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    sibling.run(debugging=True)