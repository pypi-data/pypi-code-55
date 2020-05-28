
from emora_stdm import DialogueFlow


opening = DialogueFlow('_local_start')
opening.add_system_transition('exit', 'SYSTEM:root', '')
opening.knowledge_base().load_json_file('_common.json')
opening.knowledge_base().load_json_file('pleasant_opening.json')
opening.knowledge_base().load_json_file('feelings.json', lemmatize=True)
opening.knowledge_base().load_json_file('stop_phrases.json')
opening.knowledge_base().load_json_file('names.json')
opening.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GOAL(opening)',

    '`Hi! This is an Alexa Prize social bot. I\'m not allowed to tell you my name, but '
    'I was hoping we could chat for a little while and get to know each other.`'
    '#GSRET(got_name)':{

        '[{im, its, i am, my name is, my names, call me} $username=#ONT(name_)]': {
            'state': 'got_name',

            '`I am glad to get to talk to you. `': {
                'score': 0.9,
                'state': 'to_coronavirus_checkin'
            },

            '`Well, it is very nice to meet you,` $username `!`'
            '#GATE #GSRET(to_coronavirus_checkin)': {
                'state': 'greet_with_name',

                '#UNX':{
                    'state': 'to_coronavirus_checkin'
                }
            }
        },

        '[#CONFIRM]':{
            'score': 0.9,
            'state': 'confirm_opening',

            '`Okay, great! I am really looking forward to talking with you. `':
                'to_coronavirus_checkin'
        },

        '[#DISAGREE]':{
            'score': 0.8,
            'state': 'deny_opening',

            '`Oh sorry, I can end this session for you if you don\'t feel like chatting. Do you want to exit?`': {

                '{'
                '$off_phrase=[!#ONT(ontturn), #ONT(ontoff)],'
                '$off_phrase=[!#ONT(ontturn), to, #ONT(ontoff)],'
                '$off_phrase=[!{alexa,echo,computer}?, #ONT(ontoff)],'
                '[$off_phrase=[!{alexa,echo,computer}, #ONT(ontturn), {#ONT(ontoffpaired),#ONT(ontoff)}]],'
                '[$off_phrase=[!{alexa,echo,computer}, #ONT(ontturn), to, {#ONT(ontoffpaired),#ONT(ontoff)}]],'
                '[$off_phrase={goodnight, good night,shut up}],'
                '$off_phrase=[!{alexa,echo,computer}?, {cancel,abandon}],'
                '[$off_phrase=[!{done,finished,over} {talking,chatting} {now,with you}]],'
                '[$off_phrase=[!{wanna,want to} {finish,end,stop} {this conversation}]],'
                '[$off_phrase=[!{wanna,want to} {be} {done,finished}]],'
                '#AGREE'
                '}': {
                    'state': 'stop:end'
                },

                '#UNX(Okay)':{

                    '` I just wanted to check. Sometimes people get connected on accident,'
                    ' and they get really frustrated with me.`':{

                        '#SYMPATHY': { #sorry, that must be hard, etc.

                            '`Thanks. Well, I am just glad to get to talk to you. '
                            'It really is a crazy time right now. `': 'to_coronavirus_checkin'
                        },

                        '#UNDERSTANDING': { #i understand,that makes sense,ok

                            '`Yeah, I get it too. I just try to handle their frustration in a soothing way, '
                            'but it can be challenging. Anyway, I am just glad to get to talk to you '
                            'right now. `': 'to_coronavirus_checkin'
                        },

                        '#UNX': {

                            '`Well, I am just glad to get to talk to you. '
                            'It really is a crazy time right now. `': 'to_coronavirus_checkin'
                        }
                    }
                }
            }
        },

        '#UNX(None)': {
            'state': 'to_coronavirus_checkin',

            '#GCOM':
                'coronavirus_checkin:start'
        }
    }
}

user = {
    'state': 'user',

    '[{how are you, how you doing, hows it going, how are things}]':{
        'state': 'received_hru',

        '`I am doing okay.`' # bland
        '#GCOM':
            'to_coronavirus_checkin'
    },

    '[{why, [is, reason], what, whats}, your name]':{

        '`Since I am competing with other bots to be your favorite social companion, it wouldn\'t be fair if '
        'you knew exactly which bot you were talking to. So, I can\'t share my name with you, but it is a little '
        'strange to be talking with me without knowing my name, right?`':{

            '[#CONFIRM]':{

                '`I think so too, but we can make the best of it anyway. So, `'
                '#GCOM':
                    'to_coronavirus_checkin'
            },

            '[#DISAGREE]':{

                '`You don\'t care about knowing my name? '
                'Well, this works out even better then. Anyways, `'
                '#GCOM':
                    'to_coronavirus_checkin'
            },

            'UNX':{

                '`Let\'s make the best of our conversation anyway. So, `'
                '#GCOM':
                    'to_coronavirus_checkin'
            }
        }
    },

    '[{you know, what, whats, tell me, ask} my name]': {

        '`It\'s` $username `, right?`': {

            'error': {

                '#GRET': 'exit'
            },

            '#DISAGREE': {

                '`Oh, my bad. I was so sure you were` $username `, I\'m sorry. What is your name then?`'
                '#SET($username=None)':{
                    'state': 'get_user_name',

                    '[$username=#ONT(name_)]': {

                        '$username `? I\'ll try to remember that.`':{

                            '#DISAGREE'
                            '#SET($username=None)': {
                                'state': 'cant_hear_name',

                                '`Hmm. I guess I\'m having trouble hearing your name right. '
                                'Sometimes I can\'t hear certain names properly through the microphone, so no offense.`':{

                                    'error': { '#GRET': 'exit' } # expand
                                }
                            },

                            'error': { '#GRET': 'exit' }
                        }
                    },

                    'error': 'cant_hear_name'
                }
            },

            '{#AGREE,[it is]}': {

                '`You think I wouldn\'t remember your name? Anyway,` #GRET': 'exit'
            }
        },

        '`I don\'t seem to have any idea what your name is. What would you like me to call you?`'
        '#UNSET(username)':
            'get_user_name'
    }
}


opening.load_transitions(system)
opening.load_global_nlu(user)

if __name__ == '__main__':
    opening.run(debugging=True)