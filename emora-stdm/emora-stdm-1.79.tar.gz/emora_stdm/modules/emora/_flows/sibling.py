
from _globals import PATHDIR
from emora_stdm import DialogueFlow


family = DialogueFlow('_local_start')
family.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
family.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'family.json'))
family.add_system_transition('_local_start', 'start', '')

siblings = {
    'state': 'siblings',
    'enter': '#GATE #GCOM(family) #GOAL(family)',

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
        '#SET($gets_along_with_sibling=True)': {

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

    '`So you said you live with your` $sibling=#I($lives_with, #U(brothers, sisters)) ` right? '
    'Do you guys get along?`': 'sibling',
}

exit = {
    'state': 'exit',

    '`Well I think it\'s great you get along with your ` $sibling `. So, `'
    '#IF($gets_along_with_sibling=True) #GCOM(family) #GRET': 'SYSTEM:root',

    '`Well anyway, I\'m sure your ` $sibling ` loves you even if you guys aren\'t best friends. So, `'
    '#IF($gets_along_with_sibling=False) #GCOM(family) #GRET': 'SYSTEM:root',

    '#GCOM(family) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

family.load_transitions(siblings)
family.load_transitions(exit)
family.load_global_nlu(user)


if __name__ == '__main__':
    family.run(debugging=True)