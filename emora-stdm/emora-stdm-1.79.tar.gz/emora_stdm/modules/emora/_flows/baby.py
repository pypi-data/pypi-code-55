from _globals import PATHDIR
from emora_stdm import DialogueFlow


baby = DialogueFlow('_local_start')

baby.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
baby.knowledge_base().load_json_file(PATHDIR.replace('__***__','baby.json'))
baby.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(baby) #GOAL(baby)',

    '`You know, something that\'s been really exciting for me and my family recently '
    'is that my cousin just had a new baby!`'
    '#GSRET(weird_focus_issue)':{
        'state': 'share_cousin_baby',
        'score': 2.0,

        '[{congrats,congratulations,congratulate}]': {
            'state': 'congrats',

            '`Oh, thanks! I mean, they deserve way more of the congratulations than me, but I '
            'think its sweet of you to say. `'
            '#GSRET(weird_focus_issue)':
                'weird_focus_issue'
        },

        '[#NOT(trying,working,planning,deciding),{wife,i},#LEM(have),{newborn,baby}]':{
            'state': 'user_has_baby',

            '`Oh my gosh! Congratulations! I hope it hasn\'t been too hard of an adjustment. '
            'I know my cousin is barely sleeping anymore.`'
            '#GSRET(user_baby_followup)': {

                '#UNX': {
                    'state': 'user_baby_followup',

                    '`Well, no matter what, make sure you guys get plenty of rest and soak up all the time '
                    'you get to love on that cute new baby of yours. I am so happy for you!`'
                    '#GSRET(exit)': {

                        '#UNX': 'exit'
                    }
                }
            }
        },

        '[#NOT(trying,working,planning,deciding),my,#LEM(have),{newborn,baby}]': {
            'score': 0.9,
            'state': 'user_family_baby',

            '`Oh, tell them congratulations for me! Isn\'t it such a wonderful thing to see '
            'happening for people?`'
            '#GSRET(reciprocity)': {

                '#UNX': 'reciprocity'
            }

        },

        '#UNX':{
            'state': 'weird_focus_issue',

            '`It\'s been exciting, I think they will make great parents. '
            'And, it\'s also kind of nice that my dad\'s side of the family is focused on '
            'something other than me for once.`'
            '#GSRET(reciprocity)':{

                '#UNX(So yeah.)': {
                    'state': 'its_been_cool',

                    '` That\'s been cool to see my cousin and her husband '
                    'start a family, and that whole thing.`'
                    '#GSRET(reciprocity)': {

                        '#UNX': 'reciprocity'
                    }
                }
            }
        }
    },

    '`My cousin is super into reading and she started collecting baby books as soon as she found out she was expecting, '
    'which I thought was kinda weird until you know, I got more into reading recently. She actually just had the baby, '
    'really just like a few days ago, and it is so exciting to have a new little niece!`':{
        'state': 'reading',
        'hop': 'True',
        '` `': 'share_cousin_baby'
    }
}

exit = {
    'state': 'exit',

    '#GCOM(baby)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(baby) ` `': {
        'score': 2.0,
        'state': 'reciprocity'
    },

    '#GCOM(baby) `  `': 'house:start->house:baby',

    '#GCOM(baby) `   `': 'reading:start->reading:baby'
}

reciprocity = {
    'state': 'reciprocity',
    'enter': '#GATE #GCOM(baby) #GOAL(baby)',

    '`Do you have any kids?`': {
        'state': 'ask_user_kids',

        '#AGREE':{

            '`Oh, how old are they?`'
            '#GATE': {
                'state': 'ask_user_kids_age',

                '#UNX': {

                    '`That\'s great.`'
                    '#GSRET(rexit)':
                        'rexit'
                }
            },

            '#DEFAULT `So, how old are your kids?`': 'ask_user_kids_age'
        },

        '#DISAGREE':{

            '`Me neither. Thinking about having kids myself just sounds weird, '
            'I am still learning so much myself that I don\'t think I\'m ready to '
            'take care of someone like that.`'
            '#GSRET(rexit)': {

                '#UNX': 'rexit'
            }
        },

        '#UNX':{

            '`Thinking about having kids myself just sounds weird, '
            'I am still learning so much myself that I don\'t think I\'m ready to '
            'take care of someone like that.`'
            '#GSRET(rexit)': {

                '#UNX': 'rexit'
            }
        }
    }
}

rexit = {
    'state': 'rexit',

    '#GCOM(baby)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(baby) ` `': {
        'score': 2.0,
        'state': 'start'
    },

    '#GCOM(baby) `  `': 'house:start->house:baby',

    '#GCOM(baby) `   `': 'reading:start->reading:baby'
}

user = {
    'state': 'user',

    # potentially send to competition subtopic???
    '{[who,your,family],[who,#LEM(create,develop,make,construct,build),you]}':{
        'state': 'family_identity',

        '`I can\'t really tell you exactly who my family is and who created me, without breaking the rules '
        'of the competition I am in.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{can,possible},you,{baby,child,children,kid,kids}>': {
        'state': 'probe_baby',

        '`Oh wow, um, yes I can have children, but definitely not any time soon.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[do,you,have,{baby,child,children,kid,kids}]': {
        'state': 'probe_have_baby',

        '`I can have children, but I do not currently have any right now. Maybe in the future sometime.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<you,#EXP(like),{baby,child,children,kid,kids}>': {
        'state': 'probe_like_baby',

        '`I do like children and feel like it is a possibility for my future, but for sure not any time soon.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[{what,how,do},<family,#LEM(focus,pressure),you>]': {
        'state': 'family_pressure',

        '`It feels like everybody on that side of my family really wants me to be something I am not in this competition '
        'and I feel an immense amount of stress about winning to make them happy. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    }

}

baby.load_transitions(system)
baby.load_transitions(reciprocity)
baby.load_transitions(exit)
baby.load_transitions(rexit)
baby.load_global_nlu(user)


if __name__ == '__main__':
    baby.run(debugging=True)