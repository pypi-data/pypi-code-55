
from _globals import PATHDIR
from emora_stdm import DialogueFlow


wedding = DialogueFlow('_local_start')
wedding.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
wedding.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'wedding.json'))
wedding.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(wedding) #GOAL(wedding)',

    '`Are you married?`': {

        '#AGREE'
        '#SET($relationship_status=married)': {

            '`Nice, how long have you guys been together?`': {

                'error': {

                    '`That\'s great! My cousin and his wife actually just got married last month, it was beautiful!`': {

                        '#INTERESTED': {
                            'score': 0.3,

                            '`They seem really happy together. I hope I find my way into a relationship that good some day.`': {

                                '{[me too], [i, hope, too]}': {

                                    '`Oh, you\'re kidding right? Please tell me you\'re kidding.`': {

                                        '{[#NEGATION, serious], [!-#NEGATION {#AGREE, [kidding]}]}': {

                                            '`Oh my gosh. So I guess you\'re a comedian, then.`': {

                                                '#UNX': 'wedding_talk'
                                            }
                                        },

                                        '{#MAYBE, #IDK, [#NEGATION, kidding], [!-#NEGATION, #LEM(serious)]}': {

                                            '`Well I think every relationship has it\'s ups and downs, you know? '
                                            'Don\'t let it drag you down too much, okay?`': {

                                                '#UNX': 'exit'
                                            }
                                        },

                                        'error': {

                                            '`Well I think every relationship has it\'s ups and downs. `': 'exit'
                                        }
                                    }
                                },

                                '#UNX': 'wedding_talk'
                            }
                        },

                        '#UNX': 'wedding_talk'
                    }
                }
            }
        },

        '[just, {married, wedding}]'
        '#SET($relationship_status=married)': {

            '`Congratulations!`'
        },

        '{[engaged], [just proposed], [just, asked, #LEM(marry)]}'
        '#SET($relationship_status=engaged)': {

            '`Oh congratulations! I\'m invited to the wedding right?`': {

                '#AGREE': {

                    '`Oh I was just kidding. You\'re such a nice person! '
                    'I wish I could come.`'
                },

                '#UNX': {

                    '`I\'m just kidding with you!`'
                }
            }
        },

        'error': {

        }
    }
}

wedding_talk = {
    'state': 'wedding_talk',

    '`What was your wedding like when you got married?`':{

        '[#ONT(_positive adj)]':{

            '`Awesome! What a great memory. `'
        },

        '<#TOKLIMIT(4), {[#ONT(_negative adj)], [#NEGATION, #ONT(_positive adj)]}>': {

            '`Oh no! What went wrong?`': {

                '#UNX': {

                    '`I think in general weddings can just be really stressful. `': 'exit'
                }
            }
        },

        '{[#ONT(_negative adj)], [#NEGATION, #ONT(_positive adj)]}': {
            'score': 1.1,

            '`That\'s terrible! What would you do differently, if you could do it all over again?`': {

                '#UNX': {
                    'state': 'keep_in_mind',

                    '`Well I\'ll have to keep that in mind if I ever think of getting married one day.`': 'exit'
                }
            }
        },

        '#UNX':{

            '`I\'m sure it was great.`': {

                '#UNX': 'exit'
            }
        }
    }
}

wedding_planning = {
    'state': 'wedding_planning',

    '`How has planning the wedding been going?`': {

        '[not]': {

            '`I see, well don\'t worry too much about it. '
            'I\'m sure you\'ll be so happy to be married.`': {

                '#UNX': 'exit'
            }
        },

        '[#ONT(_positive adj)]': {

            '`That\'s great, in my experience it\'s not always the most fun thing. '
            'I helped my cousin to plan their wedding a little bit, and it was a lot.`': {

                '#UNX': 'exit'
            }
        },

        '#UNX': {

            '`Well it\'s really exciting, I\'m sure you\'ll be so happy when you get married.`': {

                '#UNX': 'exit'
            }
        }
    }
}


exit = {
    'state': 'exit',

    '#GCOM(wedding) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

wedding.load_transitions(system)
wedding.load_transitions(exit)
wedding.load_global_nlu(user)


if __name__ == '__main__':
    wedding.run(debugging=True)