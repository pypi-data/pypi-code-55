from _globals import PATHDIR
from emora_stdm import DialogueFlow
from emora_stdm.state_transition_dialogue_manager.natex_common import CommonNatexMacro


baby = DialogueFlow('_local_start')

baby.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
baby.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(baby) #GOAL(baby) #IF($life_in=True,$life_started=True)'
             '#ANY($relationship_status=married,$relationship_status=divorced,$partner=husband,$partner=wife)',

    '#DEFAULT `Wait, did you say you have kids?`': 'ask_user_kids',

    '`Do you have any kids?`'
    '#GATE': {
        'state': 'ask_user_kids',

        '[! -#NEGATION [#EXTR(children, child)]]': {
            'state': 'like_being_parent_q',
            'score': 1.1,
        },

        '{#AGREE,[i do #NOT(not)]}'
        '#SET($has_kids=True)':{
            'state': 'ask_user_kids_age',
            'score': 0.9,

            '`Oh, how old are they?`'
            '#GATE': {
                'state': 'asked_kids_age',

                '#EXTR(children, child)':{

                     '`You sound like you have your hands full. `': 'like_being_parent_q'
                },

                '[$child_age=#ONT(_number)]':{

                    '`You sound like you have your hands full with a ` $child_age ` year old.`': 'like_being_parent_q'
                },
            },

            '#DEFAULT `So, how old are your kids?`': 'asked_kids_age'
        },

        '[{#DISAGREE,i do not}]'
        '#SET($has_kids=False)':{

            '`Me neither. Thinking about having kids myself just sounds weird, '
            'I am still learning so much myself that I don\'t think I\'m ready to '
            'take care of someone like that.`':
                'want_kids_q'
        },

        '[{pregnant,expecting,on the way,due}]':{
            'state': 'pregnant',

            '`Oh, you guys are expecting a baby soon? Well, congratulations, that is very exciting!`'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        },

        '#UNX':{

            '`Thinking about having kids myself just sounds weird, '
            'I am still learning so much myself that I don\'t think I\'m ready to '
            'take care of a kid.`'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        }
    }
}

want_kids = {
    'state': 'want_kids_q',

    '#DEFAULT `So, are you planning to have kids in the future?`': 'want_kids',

    '`Do you think you want kids at some point?`'
    '#GATE': {
        'state': 'want_kids',

        '{#AGREE,[i do -not],[!-#NEGATION [{i,we},#LEM(want,wish,hope,dream,try)]]}'
        '#SET($wants_kids=True)': {
            'state': 'want_kids_y',

            '`That makes sense. You sound like you will be a great parent!`'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        },

        '{#DISAGREE,[i do not],[#NEGATION,{i,we},#LEM(want,wish,hope,dream,try)]}'
        '#SET($wants_kids=False)': {
            'state': 'want_kids_n',

            '`That\'s totally respectable. I hope you don\'t feel pressured by anyone to have kids, you know what '
            'is best for you!`'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        },

        '#UNX': {
            'state': 'want_kids_unx',

            '`Gotcha. I hope everything goes exactly as you hope it will. `': 'exit'
        },
    }
}

parent_question = {
    'state': 'like_being_parent_q',

    '#DEFAULT `Hmm, I don\'t think I heard you. How do you like being a parent?`': 'like_being_parent',

    '`How do you like being a parent?`'
    '#GATE': {
        'state': 'like_being_parent',

        '{[#NOT(not),{like,love,enjoy},{it,parenting,parent,raising,caring,care}],[! -#NEGATION [#ONT(_positive adj)]]}':{
            'state': 'like_being_parent_y',
            'score': 1.1,

            '`Oh, I am so glad you find it so rewarding. `' : 'proud_q'
        },

        '{'
        '[#NEGATION,{like,love,enjoy},{it,parenting,parent,raising,caring,care}],'
        '[#NEGATION, #ONT(_positive adj)],'
        '[!-#NEGATIO [{challenge,challenging,difficult,tough,stressful}]]'
        '}': {
            'state': 'like_being_parent_n',

            '`It definitely is one of the hardest things to do, raising another person into an adult. Even though '
            'it sounds like you have encountered some challenges, I am sure you are doing a great job! `'
            '#GSRET(proud_q)': {

                '#UNX': 'proud_q'
            }
        },

        '[{#IDK,hard to say}]':{
            'state': 'like_being_parent_idk',

            '`It definitely is one of the hardest things to do, raising another person into an adult, so I understand '
            'your uncertainty. But it also can be super rewarding, based on what I have heard. '
            'No matter what, I am sure you are doing a great job! `'
            '#GSRET(proud_q)': {

                '#UNX': 'proud_q'
            }
        },

        '#UNX':{
            'state': 'like_being_parent_unx',

            '`It definitely is one of the hardest things to do, raising another person into an adult. But it also '
            'can be super rewarding, based on what I have heard. No matter what, I am sure you are doing a great job! `'
            '#GSRET(proud_q)': {

                '#UNX': 'proud_q'
            }
        }
    }

}

proud = {
    'state': 'proud_q',

    '#DEFAULT `Wait, so what has been your proudest parenting moment so far?`': 'proud',

    '`What has been your proudest moment as a parent so far?`'
    '#GATE': {
        'state': 'proud',

        '[{#IDK,[not {pick,choose,select,decide} one]}]': {
            'state': 'proud_idk',

            '`I get it. It\'s a tough question to pick just one answer to. `': 'close_to_q'
        },

        '[{nothing,none,not have one,[not,a,thing],[not,proud],[i am not]}]':{
            'state': 'not_proud',

            '`I see. I\'m sorry to hear that. Would you say you are close to your kids?`': 'close_to_q'
        },

        'error': {
            'state': 'proud_unx',

            '`That sounds pretty awesome. I know that is one thing my friend is hoping for, she just had a '
            'new baby and has been thinking a lot about being a parent. `'
            '#GSRET(close_to)': {
                'state': 'share_friend_baby',

                '#UNX': 'close_to_q'
            }
        }
    }
}

close_to = {
    'state': 'close_to_q',

    '#DEFAULT `So, would you say you are close to your kids?`': 'close_to',

    '`Do you have a really close relationship with your kids?`'
    '#GATE': {
        'state': 'close_to',

        '#IDK': {
            'state': 'close_to_idk',

            '`I guess it can be hard to tell in your day-to-day living. I hope nothing too stressful has happened to '
            'make you unsure.`'
            '#GSRET(traditions_q)': {
                'state': 'stressed_relationship',

                '#UNX': 'traditions_q'
            }
        },

        '{#AGREE,[!{i,we} do -not],[! -#NEGATION [#ONT(_positive adj)]]}':{
            'state': 'close_to_y',

            '`I\'m so happy to hear that! I know sometimes being a parent means making some tough choices that your '
            'kids don\'t appreciate in the moment, but it sounds like you have a really good bond with them. `'
            '#GSRET(traditions_q)': {
                'state': 'good_relationship',

                '#UNX': 'traditions_q'
            }
        },

        '{#DISAGREE,[!{i,we} do not],[#NEGATION,#ONT(_positive adj)]}': {
            'state': 'close_to_n',

            '`That\'s tough. I know sometimes being a parent means making some tough choices that your '
            'kids don\'t appreciate in the moment, but I know they will come around. `'
            '#GSRET(traditions_q)': {
                'state': 'bad_relationship',

                '#UNX': 'traditions_q'
            }
        },

        '#UNX(Really?)':{
            'state': 'close_to_unx',

            '`I wasn\'t expecting that answer. I know being a parent has its ups and downs. `': 'traditions_q'
        }
    }
}

traditions = {
    'state': 'traditions_q',

    '#DEFAULT `Well, what is your favorite family tradition?`': 'traditions',

    '`Do you guys have any fun family traditions that you do every year?`': {
        'state': 'traditions',

        '<#TOKLIMIT(5),{#AGREE,[!{i,we} do -not]}>':{
            'state': 'traditions_y',
            'score':1.1,

            '`Oh, cool! What is your favorite yearly tradition?`'
            '#GSRET(exit)': {

                '#UNX': {

                    '`That sounds super fun. I\'ll have to share that with my friend, she has '
                    'already started planning out all of the fun family activities they want to do.`'
                    '#GSRET(exit)': {

                        '#UNX': 'exit'
                    }
                }
            }
        },

        '{#AGREE,[!{i,we} do -not]}': {
            'state': 'traditions_y',

            '`That sounds super fun. I\'ll have to share that with my friend, she has '
            'already started planning out all of the fun family activities they want to do.`'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        },

        '{#IDK, #DISAGREE,[!{i,we} do not]}': {
            'state': 'traditions_n',

            '`Not everyone does. It can be hard to keep traditions going as everyone grows up anyways. `'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }
        },

        'error': {
            'state': 'traditions_unx',

            '`Hmm. I\'m not sure what that is, but it sounds like a good fit for you guys. `': 'exit'
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(baby) #GRET': {
        'score': 0.0,
        'state':'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    '{'
    '[who,your,family],'
    '[who,#LEM(create,develop,make,construct,build),you],'
    '[{you,your},{have,got},{parent,parents,mom,dad,mother,father}]'
    '}':{
        'state': 'family_identity',

        '`I can\'t really tell you exactly who my family is and who created me, without breaking the rules '
        'of the competition I am in.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{can,possible},you,{baby,child,children,kid,kids}>': {
        'state': 'probe_baby',

        '`It is possible for me to have children, but definitely not any time soon.`': {

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

    '[what,<{name,names},{they,their,her,she,#LEM(baby,child,kid)}>]': {
        'state': 'friend_baby_name',

        '`I can tell you that they named her after my friend\'s mom, but they want to keep the name private. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{they,their,her,she,#LEM(baby,child,kid)},{boy,girl,female,male}>': {
        'state': 'friend_baby_gender',

        '`They had a baby girl. It\'s their first kid.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{they,their,friend,friends,she,her},{one,#LEM(baby,child,kid)},{first,second,other,more,older}>': {
        'state': 'friend_baby_first',

        '`The baby girl they just had is their first kid. They do want more in the future.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    }

}

children = '[$children={#LEM(son), #LEM(daughter)}]'
expecting = '[{expecting, {one, two, son, daughter, baby} on the way}, {we, i} pregnant] #SET($expecting_children=True)'
infant = '[$baby=#LEM(baby)]'
toddler = '[$toddler=#LEM(toddler)]'
teenager = '[$teen={#LEM(teenager), #LEM(teen)}] #SET($teenage_children=True)'
adult = '[{#LEM(adult), grown up, on their own, on her own, on his own, moved out}] #SET($adult_children=True)'
genders = '[$young_children={#LEM(boy), #LEM(girl)}]'
ages = '[[!{a, #LEM(is,turn)} $child_age=#ONT(_age)]]'
number = '[have $children_num=#ONT(_number)]'

rules = {
    children: '',
    expecting: '',
    infant: '',
    toddler: '',
    teenager: '',
    adult: '',
    genders: '',
    ages: '',
    number: ''
}

transitions = [system,want_kids,parent_question,proud,close_to,traditions]
for trans in transitions:
    baby.load_transitions(trans)

baby.load_transitions(exit)
baby.load_global_nlu(user, 10.0)
baby.load_update_rules(rules)

if __name__ == '__main__':
    baby.run(debugging=True)