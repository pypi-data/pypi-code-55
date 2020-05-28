
from _globals import PATHDIR
from emora_stdm import DialogueFlow


coronavirus = DialogueFlow('_local_start')
coronavirus.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
coronavirus.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(coronavirus) #GOAL(coronavirus)',

    '`So it\'s a pretty crazy time right now with the corona virus going on. '
    'Are you and your family doing okay?`'
    '#GSRET(exit)': {

        '{#AGREE,[!-not [{safe,okay,good,well,fine,alright,healthy}]]} #SET($okay_in_corona=True)': {

            '`That\'s good. `': {
                'state': 'stay_connected',
                'hop': 'True',

                '`Do you feel like it\'s harder to stay connected with people these days, '
                'or is that not really a problem for you?`'
                '#GSRET(exit)': {

                    '[#NOT(not),{hard,harder,challenge,challenging,problem,difficult,tough}]': {

                        '`Right. I think it could be a good opportunity to spend some '
                        'quality time with the people you live with though, right?`'
                        '#GSRET(exit)': {

                            '#AGREE': {

                                '`It is always good to remember that this isn\'t permanent and '
                                'it will calm down in time, so just keep doing your best. `':
                                    'exit'
                            },

                            '{[i, not, #LEM(live), with], [i, alone]}'
                            '#SET($lives_alone=True)':{

                                '`I see. You should video call someone then.`'
                                '#GSRET(exit)': {

                                    '[!-{should, could, can, might, will} [i, {do, call}]]': {

                                        '`I guess it\'s not the same, huh?`'
                                        '#GSRET(exit)': {

                                            '#UNX': {

                                                '`It is always good to remember that this isn\'t permanent and '
                                                'it will calm down in time, so just keep doing your best. `':
                                                    'exit'
                                            }
                                        }
                                    },

                                    '#UNX': {

                                        '`And remember, I am always happy to talk to you too if you get lonely. `': 'exit'
                                    }
                                }
                            },

                            '#UNX': {

                                '`It is always good to remember that this isn\'t permanent and '
                                'it will calm down in time, so just keep doing your best. `':
                                    'exit'
                            }
                        }
                    },

                    '[#NEGATION, {hard, problem, difficult, tough}]': {

                        '`Okay, that\'s good to hear. It is always good to remember that this isn\'t permanent and '
                        'it will calm down in time, so just keep doing your best. `': 'exit'
                    },

                    '#UNX': {

                        '`It is always good to remember that this isn\'t permanent and '
                        'it will calm down in time, so just keep doing your best. `': 'exit'
                    }
                }
            }
        },

        '{'
        '#DISAGREE, '
        '[-not,{bad,hard,tough,challenging,challenge,sick,unhealthy,lonely,stress,stressed}], '
        '[not {best,happy,happiest,safe,okay,good,well,fine,alright,healthy}]'
        '}': {
            'score': 1.1,

            '`Oh, I\'m sorry. Do you want to talk about it?`'
            '#GSRET(exit)': {

                '{#AGREE, [sure,okay,ok], [!-#NEGATION [i, talk]]}': {

                    '`Sure. I know it\'s a pretty hard time overall. '
                    'What\'s weighing on you the most right now?`'
                    '#GSRET(exit)': {

                        '#UNX': {

                            '`Things might be hard now, but it won\'t last forever. '
                            'Everything\'s going to be okay.`': 'exit'
                        }
                    }
                },

                '#DISAGREE': 'exit',

                '#UNX': 'exit'
            }
        },

        '#UNX': 'stay_connected'
    }
}



exit = {
    'state': 'exit',

    '#GCOM(coronavirus) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    },

    '#GCOM(coronavirus) #GRET ` `': {
        'state': 'SYSTEM:pet_intro'
    },

    '#GCOM(coronavirus) #GRET `  `': {
        'state': 'SYSTEM:travel_intro'
    }
}

user = {
    'state': 'user'
}

coronavirus.load_transitions(system)
coronavirus.load_transitions(exit)
coronavirus.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    coronavirus.run(debugging=True)