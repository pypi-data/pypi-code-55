from emora_stdm import DialogueFlow
from _globals import VRDIR

vr_experience = DialogueFlow('_local_start')
vr_experience.add_system_transition('exit', 'SYSTEM:root', '#GCOM(vr_experience)', score=0.0)
vr_experience.add_system_transition('exit', 'SYSTEM:vr_topic_switch', '#GCOM(vr_experience)')
vr_experience.update_state_settings('exit', system_multi_hop=True)
vr_experience.update_state_settings('SYSTEM:root', system_multi_hop=True)
vr_experience.update_state_settings('SYSTEM:vr_topic_switch', system_multi_hop=True)
# vr_experience.knowledge_base().load_json_file('common.json')
vr_experience.knowledge_base().load_json_file(VRDIR.replace('__***__','vr_experience.json'))
vr_experience.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GCOM(vr_experience) #GOAL(vr_experience)',

    '`My friend was telling me this really funny story yesterday. He knocked down almost every piece of furniture in '
    'his living room because he was so wild while playing this virtual reality video game! Isn\'t that crazy?`'
    '#GSRET(ask_vr_q)':{
        'state': 'share_funny_vr',

        '#AGREE':{
            'state': 'share_funny_vr_y',

            '`I know, right? `': 'ask_vr_q'
        },

        '#DISAGREE':{
            'state': 'share_funny_vr_n',

            '`Oh, have you heard of similar things happening to other people?`'
            '#GSRET(ask_common_unx)': {
                'state': 'ask_common_q',

                '#AGREE':{
                    'state': 'ask_common_y',

                    '`Wow, really? I guess it is pretty hard to know where you are going in the real world when you '
                    'have a V R headset on. `'
                    '#GSRET(ask_vr_q)':
                        'ask_vr_q'
                },

                '#DISAGREE':{
                    'state': 'ask_common_n',

                    '`Me neither, really. I think most people try to clear their space before playing V R games so that '
                    'this doesn\'t happen to them.`'
                    '#GSRET(ask_vr_q)':
                        'ask_vr_q'
                },

                '#UNX':{
                    'state': 'ask_common_unx',

                    '`I think it is probably pretty hard to know where you are going in the real world when you '
                    'have a V R headset on. `'
                    '#GSRET(ask_vr_q)':
                        'ask_vr_q'
                }

            }
        },

        '[{do you,tell,what,which},{game,#LEM(play)}]': {
            'state': 'friend_vr_game',

            '`It was the virtual reality version of Skyrim. I know the regular version is pretty popular, and '
            'honestly I think it\'s setup as a role playing, quest-based game is perfect for virtual reality.`'
            '#GSRET(ask_vr_q)': {
                '#UNX': 'ask_vr_q'
            }
        },

        '{'
        '[that,#NEGATION,{#LEM(happen),real}],'
        '[that,{fake,false,lie}]'
        '}': {
            'state': 'friend_vr_disbelief',

            '`You don\'t believe me? Why would I lie to you?`'
            '#GSRET(ask_vr_q)': {

                '#UNX(Whatever you say. anyways )': 'ask_vr_q'
            }
        },

        '#NOT(not) [{funny,laugh,smile,comical,comedy,#LEM(humor),cool,nice,weird,odd,strange,unusual,uncommon}]': {
            'state': 'friend_vr_funny',

            '`He thought it was pretty funny too. It made me laugh to see him reenact it, for sure. He can be such a '
            'clown sometimes. `'
            '#GSRET(ask_vr_q)': {
                'state': 'friend_vr_funny_r',

                '#UNX': 'ask_vr_q'
            }
        },

        '{'
        '[not {funny,laugh,smile,comical,comedy,#LEM(humor),cool,nice,weird,odd,strange,unusual,uncommon}],'
        '[{bad,horrible,sad,unfortunate}]'
        '}': {
            'state': 'friend_vr_not_funny',

            '`Well, he wasn\'t really hurt or anything. He thought it was pretty funny too and did a hilarious '
            'reenactment. He can be such a clown sometimes. `'
            '#GSRET(ask_vr_q)': {
                'state': 'friend_vr_not_funny_r',

                '#UNX': 'ask_vr_q'
            }
        },

        '#UNX': {
            'state': 'ask_vr_q',

            '`Have you ever tried any virtual reality games before?`'
            '#GSRET(user_unknown_experience)': {
                'state': 'ask_vr_r',

                '#UNX': {
                    'state': 'user_unknown_experience',

                    '`Well, do you think a lot of people would find virtual reality fun? `': 'ask_interest'
                },

                '#AGREE'
                '#SET($userVR=True)':{
                    'state': 'user_yes_experience',

                    '`Awesome! I think virtual reality takes gaming to a whole new level since you really can feel like you are a part '
                    'of the game\'s world. `'
                    '#GSRET(ask_memorable)': {
                        '#UNX': {
                            'state': 'ask_memorable',

                            '` What sticks out the most to you about your experience with virtual reality?`': {
                                'state': 'asked_memorable',

                                '[#NOT(not) {cool,awesome,amazing,fun,good,unique,interesting,#LEM(enjoy,engage,immerse,excite)}]': {
                                    'state': 'ask_good_game',

                                    '`Good point. It is a pretty unique experience and definitely can be very fun. '
                                    'What was a good game you have tried?`'
                                    '#GATE': {
                                        'state': 'asked_good_game',

                                        '#UNX(None)': {
                                            'state': 'new_game_q',

                                            '`Ok, can you tell me more about that one?`'
                                            '#GSRET(exit)': {
                                                'state': 'new_game',

                                                '[!{yes,yeah,yup,ok,okay,sure,alright} {i can,i will}?]': {
                                                    'state': 'new_game_yes',

                                                    '`Thanks! So, what was it like to play it?`': {
                                                        'state': 'new_game_yes_more',

                                                        '#UNX': 'new_game_unx'
                                                    }
                                                },

                                                '#DISAGREE': {
                                                    'state': 'new_game_no',

                                                    '`Okay then. I will have to do some research on it myself. `'
                                                    '#GSRET(exit)': {
                                                        '#UNX': 'exit'
                                                    }
                                                },

                                                '#UNX': {
                                                    'state': 'new_game_unx',

                                                    '`Well, I will definitely keep that game in mind. It sounds like something '
                                                    'interesting to look into.`'
                                                    '#GSRET(exit)': {
                                                        '#UNX': 'exit'
                                                    }
                                                }
                                            }
                                        },

                                        '#IDK': {
                                            'state': 'good_game_idk',

                                           '`No worries. If you ever think of one, I would love to hear about it in the future! `'
                                           '#GSRET(exit)': {
                                                '#UNX': 'exit'
                                           }
                                        },

                                        '[{skyrim,elder scrolls,elder scroll}]': {
                                            'state': 'good_game_skyrim',

                                            '`Of course! I have heard very positive things about that game in particular. I '
                                            'keep meaning to pick it up, maybe I actually will now since you had such a '
                                            'good time with it too! `'
                                            '#GSRET(exit)':{
                                                '#UNX': 'exit'
                                            }
                                        },

                                        '[{#DISAGREE,none,nothing,[not,{one,any,#LEM(game,play),time,experience}]}]': {
                                            'state': 'good_game_none',

                                            '`Oh, that is really sad. You haven\'t found any good V R games? '
                                            'Well, keep me in the loop. If you ever find one, '
                                            'I would love to hear about it! `'
                                            '#GSRET(exit)': {
                                                '#UNX': 'exit'
                                            }
                                        },
                                    },

                                    '#DEFAULT `Wait, what was the best virtual reality game you have played?`': 'asked_good_game'
                                },

                                '#NOT(not) [{real,realistic,detail,detailed,pretty,beautiful,magnificent,majestic,stunning,'
                                'visual,visuals,visually,clear,nice,stunning,beauty,graphics}]': {
                                    'state': 'vr_beauty',

                                    '`That\'s fantastic. I think the realism and quality of the visuals can make or break '
                                    'your experience in V R, I know that is what I would want, too! '
                                    'What game were you playing that was like that?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '#NOT(not) [{#LEM(interact,adventure),interactive,adventurous}]': {
                                    'state': 'vr_adventure',

                                    '`That\'s a really important part, feeling like you can really interact and there '
                                    'are a lot of things to do in the game. '
                                    'What game were you playing that was like that?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '#NOT(not) [{#LEM(nausea,sick,ill,dizzy,headache),nauseous}]': {
                                    'state': 'vr_nausea',

                                    '`Oh no, that sounds rough. I think that is a common problem with V R, making people '
                                    'feel dizzy or sick. '
                                    'What is a good game you played that didn\'t make you feel like that?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '#NOT(not) [{easy,convenient,quick,comfortable,secure,[fit,{well,good,perfect}]}]': {
                                    'state': 'vr_comfort',

                                    '`That\'s great. '
                                    'I would hate to be uncomfortable or have a hard time using the device. '
                                    'What is a good game you have played?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '#NOT(not) [#LEM(crash,break,bump,run,hit,throw,shatter,piece,crack,snap,damage,harm,destroy)]': {
                                    'state': 'vr_break',

                                    '`Oh dear. It sounds like you had a bit of a wild ride while playing. Hopefully '
                                    'nothing was too damaged. '
                                    'What is a good game you have played, in spite of that?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '{'
                                '[#NOT(not) {scary,bad,horrible,unenjoyable,waste}],'
                                '[not,{fun,good,#LEM(enjoy,entertain)}]'
                                '}': {
                                    'state': 'vr_not_fun',

                                    '`Hmm. I\'m sorry to hear that. Hopefully that was just one bad V R game. '
                                    'What is a good game you have played, if any?`'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                },

                                '#UNX': {

                                    '`I have heard something similar from other people too. '
                                    'I just hope for games that actually feel real '
                                    'and don\'t have any weird glitches going on. '
                                    'What is a game you would recommend? `'
                                    '#GSRET(ask_good_game)':
                                        'asked_good_game'
                                }

                            }
                        }
                    }
                },

                '{#DISAGREE,#MAYBE}':{
                    'state': 'user_no_experience',

                    '`I see. Well, is it something you think would be fun to try?`': {
                        'state': 'ask_interest',

                        '#NOT(not) [{#AGREE,cool,awesome,amazing,fun,good,unique,#LEM(enjoy,engage,immerse,excite,interest)}]':{

                            '`Me too! I just wish they weren\'t so expensive. I am just a student after all, I don\'t have '
                            'hundreds of dollars to drop on a virtual reality headset. `'
                            '#GSRET(user_agree_expense)': {
                                'state': 'too_expensive',

                                '[you,{school,college,university,student}]': {
                                    'state': 'ask_about_student',

                                    '`Oh yeah! I am taking some classes right now.`':
                                        'school_new:reciprocity',

                                    '`Oh yeah! I am taking some classes right now. Actually, after school a few days ago, '
                                    'I tried one of those mobile apps where you see different pieces of furniture in your '
                                    'real room. Have you heard of something like that?`':
                                        'ask_ar'
                                },

                                '#NOT(not) [{[!me {too,neither}],expensive,[{high,too,hefty} {price,cost}],[out,budget]}]':{
                                    'state': 'user_agree_expense',

                                    '`I hope at least one of the V R devices becomes less expensive soon! But, I mean, I '
                                    'have used those mobile apps that let you see different pieces of furniture in the '
                                    'room. Have you heard of something like that? `'
                                    '#GSRET(no_ar)': {
                                        'state': 'ask_ar',

                                        '#AGREE': {
                                            'state': 'yes_ar',

                                            '`Sweet! I found it super helpful when buying some furniture for my new house, '
                                            'I have such a hard time picturing it in my mind clearly. `'
                                            '#GSRET(exit)':{
                                                'state': 'share_house_ar',

                                                '[{#AGREE,[me too],hard,difficult,#LEM(challenge),struggle}]':{

                                                    '`It is a struggle for sure. Thank goodness for technology for '
                                                    'things like this! `'
                                                    '#GSRET(exit)':
                                                        'exit'
                                                },

                                                '[you,#LEM(have,own,buy,rent),#LEM(house,home,place,apartment,live)]':{
                                                    'state': 'ask_about_home',

                                                    '`Of course! I live in a virtual world, similar to yours. `':
                                                        'house:start',

                                                    '`Of course! I live in a virtual world, similar to yours, with a house '
                                                    'and everything. `'
                                                    '#GSRET(exit)':
                                                        'exit'
                                                },

                                                '#UNX': 'exit'
                                            }
                                        },

                                        '#UNX(None)': {
                                            'state': 'no_ar',

                                            '`Oh, really? Well, I found it super helpful when buying some furniture for '
                                            'my new house, I have such a hard time picturing it in my mind clearly. `'
                                            '#GSRET(exit)':
                                                'share_house_ar'
                                        }
                                    }
                                },

                                '#UNX': 'user_agree_expense'
                            }
                        },

                        '{#DISAGREE, '
                        '[#NEGATION,{cool,awesome,amazing,fun,good,unique,#LEM(enjoy,engage,immerse,excite,interest)}],'
                        '[#NOT(not),{stupid,boring,lame,worthless,bad,horrible,terrible}]'
                        '}':{

                            '`It\'s not for everyone, I guess. I haven\'t even tried it. Although I did use a mobile '
                            'app to see different pieces of furniture in my house. Have you heard of something like that?`'
                            '#GATE':
                                'ask_ar',

                            '#DEFAULT `So, have you heard of the mobile apps that let you see how different items would '
                            'look in your home?`':
                                'ask_ar'
                        },

                        '#IDK':{

                            '`Okay, no big deal. Have you heard of those mobile apps that let you see what different '
                            'furniture or things look like in your own house? `'
                            '#GATE':
                                'ask_ar',

                            '#DEFAULT `So, have you heard of the mobile apps that let you see how different items would '
                            'look in your home?`':
                                'ask_ar'
                        }

                    }
                },

                '{'
                '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {that,it,you said,v r,vr,virtual reality}, {is,mean,means}],'
                '[! what is {that,it,you said,v r,vr,virtual reality}],'
                '[what,does,{that,it,you said,v r,vr,virtual reality},mean]'
                '}':{
                    'state': 'explain_vr',

                    '`Oh, that\'s alright. Virtual reality is a new technology '
                    'that puts you into the middle of a three dimensional virtual world and lets you interact with it. '
                    'What do you think? Does that sound interesting to you?`'
                    '#GSRET(user_unknown_experience)':
                        'ask_interest'
                }
            }
        }
    }


}

user = {
    'state': 'user',

    '{'
    '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {v r,vr,virtual,reality}, {is,mean,means}],'
    '[! what is {v r,vr,virtual reality}],'
    '[what,does,{v r,vr,virtual reality},mean]'
    '}':{
        'state': 'explain_vr_global',
        'score': 0.3,

        '`Oh, that\'s alright. Virtual reality is a new technology '
        'that puts you into the middle of a three dimensional virtual world and lets you interact with it. `':{
            'state': 'explain_vr_r',

            '#UNX': {'#GRET': 'exit', 'state': 'explain_vr_unx'}
        }
    },

    # have you done it before
    '[#LEM(have,do,can),you,#LEM(try,play,do),{any,one,some,virtual reality, v r, it, #LEM(game), #ONT(vr_company)}]':{
        'state': 'emora_done_vr_q',

        '`I haven\'t been able to try out virtual reality yet. I do want to, it sounds really cool!`': {
            'state': 'emora_done_vr',

            '#UNX':{'#GRET': 'exit', 'state': 'emora_done_vr_unx'}
        }
    },

    '[{what,how},{expensive,cost,price}]':{
        'state': 'cost_vr_q',

        '`I\'ve heard that good ones are anywhere between like 300 and 800 dollars. It\'s insane.`': {
            'state': 'cost_vr',

            '#UNX': {'#GRET': 'exit', 'state': 'cost_vr_unx'}
        }
    },

    '{'
    '[{what,which}, {good,fun,favorite,best,#LEM(want)}, #LEM(game)],'
    '[have,you,{good,fun},#LEM(game)]'
    '}': {
        'state': 'fave_vr_game_q',

        '`I haven\'t played any yet, so I am not sure. I have heard good things about the Skyrim one though.`': {
            'state': 'fave_vr_game',

            '#UNX': {'#GRET': 'exit', 'state': 'fave_vr_game_unx'}
        }
    },

    '{'
    '[{what,which},{favorite,best,#LEM(want)},#LEM(console,device,headset,one,virtual reality,v r)],'
    '[{what,which},#LEM(console,device,headset,one,virtual reality,v r),{[!should i {get,buy,purchase}],#LEM(recommend,suggest)}]'
    '}': {
        'state': 'fave_vr_device_q',

        '`That\'s a hard question since I haven\'t had the chance to use any. Oculus seems pretty popular.`': {
            'state': 'fave_vr_device',

            '#UNX': {'#GRET': 'exit', 'state': 'fave_vr_device_unx'}
        }
    },

    '[{what,tell me},skyrim]': {
        'state': 'about_skryim_q',

        '`Skyrim is a role-playing, quest-based game with magic and dragons. There is a version of it that isn\'t for '
        'virtual reality, too.`': {
            'state': 'about_skryim',

            '#UNX': {'#GRET': 'exit', 'state': 'about_skryim_unx'}
        }
    },

    '[{what,tell me},#LEM(worst,bad,challenge,struggle,disadvantage,problem,issue),{virtual reality,v r}]': {
        'state': 'vr_issues_q',

        '`Good question. I think some people get motion sick when they play virtual reality games since there is a '
        'disconnect between your mind and actual body.`': {
            'state': 'vr_issues',

            '#UNX': {'#GRET': 'exit', 'state': 'vr_issues_unx'}
        }
    },

    '[{can,how},you,#LEM(play,use,do),{#LEM(game,console,device,headset,controller),virtual reality,v r}]': {
        'state': 'how_vr_q',

        '`I live in a virtual world, similar to yours, where I can do a lot of the same things as you, like play '
        'video games and stuff.`': {
            'state': 'how_vr',

            '#UNX': {'#GRET': 'exit', 'state': 'how_vr_unx'}
        }
    },

    '{'
    '[{is not,are not},you,{virtual,computer,electronic,electric,robot,machine}],'
    '[you are,{virtual,computer,electronic,electric,robot,machine}]'
    '}': {
        'state': 'emora_virtual_q',

        '`I guess it\'s like virtual reality inception. My reality is technically virtual, compared to yours, but '
        'I can still experience a different reality in my virtual world using a virtual reality device.`': {
            'state': 'emora_virtual',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_virtual_unx'}
        }
    },

    '[{what,which},{app,application,store},#LEM(use,try,download)]': {
        'state': 'ar_app_q',

        '`Just some of those popular shops, like Target and Wayfair. There were some really cute furniture items, but '
        'I haven\'t made up my mind on what to buy yet! `': {
            'state': 'ar_app',

            '#UNX': {'#GRET': 'exit', 'state': 'ar_app_unx'}
        }
    },

    # is friend ok
    '[{is,did,was},{he,friend,him},#LEM(hurt,injure,pain,harm)]': {
        'state': 'friend_vr_ok_q',

        '`No, he didn\'t get hurt. I don\'t think he would have found it so funny if he did. `': {
            'state': 'friend_vr_ok',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_vr_ok_unx'}
        }
    },

    # did anything break
    '<{is,did,was},{anything,#LEM(thing,item,furniture,lamp,table,chair)},#LEM(break,crash,shatter,piece,crack,snap,damage,harm,destroy)>': {
        'state': 'friend_vr_furn_q',

        '`Nothing was broken. He had moved the lamps and stuff into the corner where they wouldn\'t fall over. `': {
            'state': 'friend_vr_furn',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_vr_furn_unx'}
        }
    },

    # vr is hazardous
    '<{v r, virtual reality},#LEM(hazard,danger,threat,trouble,problem)>': {
        'state': 'vr_hazard_q',

        '`I think you just need to take the proper precautions when playing a V R game. It doesn\'t have to be '
        'dangerous. But you\'re right, that is a valid concern. `': {
            'state': 'vr_hazard',

            '#UNX': {'#GRET': 'exit', 'state': 'vr_hazard_unx'}
        }
    }
}

vr_experience.load_transitions(system)
vr_experience.load_global_nlu(user)


if __name__ == '__main__':
    from emora._flows._global_nlu import global_update_rules
    vr_experience.load_update_rules(global_update_rules)
    vr_experience.precache_transitions()
    vr_experience.run(debugging=True)