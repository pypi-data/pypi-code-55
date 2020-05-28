
from _globals import PATHDIR
from emora_stdm import DialogueFlow


relationships = DialogueFlow('_local_start')
relationships.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
relationships.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'dating',
    'enter': '#GATE #GCOM(relationship) #GOAL(relationship) #IF($life_in=True,$life_started=True) #ANY($in_high_school=True,$in_college=True)',

    '#DEFAULT': {
        'state': 'default_relationship',
        'hop': 'True',

        '`Wait, are you currently dating anyone?`': 'ask_relationship'
    },

    '`I hope you don\'t mind me asking, but are you dating anyone right now?`'
    '#GSRET(default_relationship)':{
        'state': 'ask_relationship',

        '{#AGREE,[{[!-not,{correct,true,right}],[!i am,-not]}]}':
            'dating_y',

        '[{#DISAGREE,[i am not],[not dating],noone,no one,nobody,[!not,{have,got},{a,any},#ONT(partner)]}]':
            'single',

        '[#NOT(not),{$partner=#ONT(spouse),#LEM(marry)}]'
        '#SET($relationship_status=married)':{
            'state': 'married_y',
            'score': 1.1
        },

        '[#NOT(not),$partner={boyfriend,girlfriend}]'
        '#SET($relationship_status=dating)': {
            'state': 'dating_y',
            'score': 1.1,

            '#DEFAULT `So, how long have you been together?`': 'relationship_length',

            '`Oh, cool! How long have you been together?`'
            '#GATE': {
                'state': 'relationship_length',

                'error': {

                    '`Well, I hope you guys are really happy together. `': 'exit'
                }
            }
        },

        '[#NOT(not),{alone,single}]'
        '#SET($relationship_status=single)': {
            'state': 'single',
            'score': 1.1,

            '`Me too! Being single is the perfect time to focus on yourself. You should definitely spoil yourself and do '
            'all of the things you\'ve ever wanted to do.`'
            '#GSRET(exit)': {
                'state': 'single_r',

                '#UNX': 'exit'
            }
        },

        '[{fiance,fiancee,#LEM(engage),[just proposed], [just, asked, #LEM(marry)]}]'
        '#SET($relationship_status=engaged,$partner=fiance)': {
            'state': 'engaged',
            'score': 1.1
        },

        '[{on a break,dumped,broken up,broke up,ghosted,[!left {me,him,her,my}]}]'
        '#SET($relationship_status=broken_up)': {
            'state': 'broke_up',
            'score': 1.2,

            '#DEFAULT `I really want to make sure you are doing alright. Are you feeling okay these days?`': 'broke_up_r',

            '`I\'m so sorry to hear that your relationship ended. Are you doing okay?`': {
                'state': 'broke_up_r',

                '{#AGREE,[#NEGATION,#ONT(_negative adj)],[!-#NEGATION [#ONT(_positive adj)]]}': {
                    'state': 'broke_up_feeling_ok',

                    '`That\'s a relief to hear, I am so glad you are doing alright. `':  'exit'
                },

                '{#DISAGREE,[! -#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}': {
                    'state': 'broke_up_feeling_bad',

                    '`Oh no... I feel for you. I know break ups can be tough, but I believe that better '
                    'things are coming for you soon.`'
                    '#GSRET(exit)': {

                        '#UNX(Just focus on each day as it comes. Anyways )': 'exit'
                    }
                },

                '#UNX(None)': {
                    'state': 'broke_up_feeling_unx',

                    '`Well, I know better things are coming for you soon. '
                    'Just focus on each day as it comes. Anyways, `':
                        'exit'
                }
            }
        },

        '[#LEM(divorce,separate)]'
        '#SET($relationship_status=divorced)': {
            'state': 'divorced',
            'score': 1.2,

            '#DEFAULT `I really want to make sure you are doing alright. Are you feeling okay these days?`': 'divorced_r',

            '`I see. I\'m really sorry to hear that. Ending a marriage is always a difficult decision. How are you '
            'doing now?`': {
                'state': 'divorced_r',

                '{[#NEGATION,#ONT(_negative adj)],[!-#NEGATION [#ONT(_positive adj)]]}': {
                    'state': 'divorced_ok',

                    '`That\'s a relief to hear, I am so glad you are doing alright. `': 'exit'
                },

                '{[! -#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}': {
                    'state': 'divorced_bad',

                    '`Oh no... I feel for you. I know it can be so tough to continue on, but I believe that better '
                    'things are coming for you soon. `'
                    '#GSRET(exit)': {

                        '#UNX(Just focus on each day as it comes. Anyways )': 'exit'
                    }
                },

                '#UNX(None)': {
                    'state': 'divorced_unx',

                    '`Well, I know better things are coming for you soon. Just focus on each day as it comes. Anyways, `': 'exit'
                }
            }
        },

        '[{death,#LEM(die),passed away,killed,murdered,lost}]'
        '#SET($relationship_status=partner_died)':{
            'state': 'partner_died',
            'score': 1.2,

            '#DEFAULT `I really want to make sure you are doing alright. Are you feeling okay these days?`': 'partner_died_r',

            '`Oh. I\'m so sorry for your loss. I cannot even imagine what you are going through. I hope you are doing ok. `': {
                'state': 'partner_died_r',

                '{[#NEGATION,#ONT(_negative adj)],[!-#NEGATION [#ONT(_positive adj)]]}': {
                    'state': 'partner_died_ok',

                    '`That\'s reassuring, I am so glad you are doing alright. '
                    'Just do your best with each day as it comes. `':
                        'exit'
                },

                '{[! -#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}': {
                    'state': 'partner_died_bad',

                    '`Oh no... I feel for you. I know it can be so tough to continue on, but '
                    'just do your best with each day as it comes. `':
                        'exit'
                },

                '#UNX(None)': {
                    'state': 'partner_died_unx',

                    '`Well, I hope better things are coming for you soon. '
                    'Just do your best with each day as it comes. `':
                        'exit'
                }
            }

        },

        #name
        '[$partner_name=#ONT(_names)]':{
            'state': 'dating_y',
            'score': 0.9
        },

        #its complicated
        '[{complicated,[{hard,challenging,difficult},{explain,describe}]}]': {
            'state': 'relationship_complicated',
            'score': 0.9,

            '#DEFAULT `I don\'t think I get it. What makes your relationship so complicated?`': 'relationship_complicated_r',

            '`It sounds like your relationship status is complicated. Why is that?`': {
                'state': 'relationship_complicated_r',

                'error':{

                    '`I see. Well, I hope it clears up soon for you. It is a frustrating situation to feel that way. `': {

                        '#UNX': 'exit'
                    }
                }
            }
        },

        #taking a break from dating
        '[{hiatus,break},dating]': {
            'state': 'single',
            'score': 1.1
        },

        #are/can you hitting on me,date me,interested in me
        '{'
        '[are,{you,your},{hitting,interested,asking},me],'
        '[you,{want,desire,wish,hope},date,me]'
        '}': {
            'state': 'hitting_on_user',
            'score': 1.1,

            '`What? Of course not. I\'m sure you are a great person, but '
            'we are just getting to know each other. `'
            '#GSRET(exit)': {

                '#UNX': 'exit'
            }

        },

        'error':{
            'state': 'relationship_unx',

            '`Hmm. Interesting. Anyway, `': 'exit'
        }
    }

}

friend_married = {
    'state': 'friend_married_default',

    '`Actually, my friend and his wife actually just got married, it was beautiful!`': 'friend_married_r'
}

marriage = {
    'state': 'marriage',
    'enter': '#GATE #GCOM(relationship) #GOAL(relationship) #IF($life_in=True,$life_started=True) #ANY($is_student=False,$is_student=None)',

    '#DEFAULT': {
        'state': 'default_marriage',
        'hop': 'True',

        '`Wait, so, are you married?`': 'ask_relationship'
    },

    '`I hope you don\'t mind me asking, but are you married?`'
    '#GSRET(default_marriage)': {
        'state': 'asked_married',

        '{#AGREE,[[!-not,{correct,true}]],[[!i am,-not]]}'
        '#SET($relationship_status=married)': {
            'state': 'married_y',

            '`Oh, that is wonderful to hear! How long have you guys been together?`'
            '#GSRET(friend_married_default)': {
                'state': 'how_long_married',

                'error': {
                    'state': 'share_friend_married',

                    '`That\'s great! My friend and his wife actually just got married, it was beautiful!`'
                    '#GSRET(wedding_talk)': {
                        'state':'friend_married_r',

                        '#INTERESTED': {
                            'score': 0.3,

                            '`They seem really happy together. I hope I find my way into a relationship that good some day.`'
                            '#GSRET(wedding_talk)': {

                                '{[me too], [i, hope, too]}': {

                                    '`Oh, you\'re kidding right? Please tell me you\'re kidding.`'
                                    '#GSRET(wedding_talk)': {

                                        '{[#NEGATION, serious], [!-#NEGATION {#AGREE, [kidding]}]}': {

                                            '`Oh my gosh. So I guess you\'re a comedian, then.`'
                                            '#GSRET(wedding_talk)': {

                                                '#UNX': 'wedding_talk'
                                            }
                                        },

                                        '{#DISAGREE, #MAYBE, #IDK, [#NEGATION, kidding], [!-#NEGATION, #LEM(serious)]}': {

                                            '`Well, I think every relationship has it\'s ups and downs, you know? '
                                            'Don\'t let it drag you down too much, okay?`'
                                            '#GSRET(exit)': {

                                                '#UNX': 'exit'
                                            }
                                        },

                                        'error': {

                                            '`Well, I think every relationship has it\'s ups and downs. `': 'exit'
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

            '`Congratulations! `': 'married_y'
        },

        '{[engaged], [just proposed], [just, asked, #LEM(marry)]}'
        '#SET($relationship_status=engaged)': {
            'state': 'engaged',

            '`Oh, congratulations! I\'m invited to the wedding right?`'
            '#GSRET(wedding_planning)': {

                '#AGREE': {

                    '`Oh, I was just kidding. You\'re such a nice person! '
                    'I wish I could come.`': 'wedding_planning'
                },

                '{[!what],[why]}':{

                    '`I\'m just kidding with you!`': 'wedding_planning'
                },

                '#UNX': {

                    '`I\'m just kidding with you!`': 'wedding_planning'
                }
            }
        },

        '[#LEM(divorce,separate)]'
        '#SET($relationship_status=divorced)': {
            'state': 'divorced',
            'score': 1.2
        },

        '[{death,#LEM(die),passed away,killed,murdered,lost}]'
        '#SET($relationship_status=partner_died)': {
            'state': 'partner_died',
            'score': 1.2
        },

        '{#DISAGREE,[i am not]}':{
            'state': 'married_n',

            '`That\'s alright. It is hard to find the right person. Are you currently seeing anyone?`'
            '#GSRET(default_relationship)':
                'ask_relationship'
        },

        'error': {
            'state': 'ask_relationship',
            'hop': 'True'
        }
    }
}

wedding_talk = {
    'state': 'wedding_talk',

    '#DEFAULT `So, tell me more about what your wedding was like.`': 'describe_wedding',

    '`What was your wedding like when you got married?`':{
        'state': 'describe_wedding',

        '{[#NEGATION,#ONT(_negative adj)],[!-#NEGATION [{best,#ONT(_positive adj)}]]}':{

            '`Awesome! What a great memory. It seems like a really good time. Would you consider it '
            'one of the best moments of your life?`'
            '#GSRET(exit)':
                'best_moment'
        },

        '<#TOKLIMIT(4), {[!-#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}>': {

            '`Oh no! What went wrong?`'
            '#GSRET(exit)': {

                '#UNX': {

                    '`I think in general weddings can just be really stressful. `': 'exit'
                }
            }
        },

        '{[!-#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}': {
            'score': 1.1,

            '`That\'s terrible! What would you do differently, if you could do it all over again?`'
            '#GSRET(exit)': {

                '#UNX': {
                    'state': 'keep_in_mind',

                    '`Well, I\'ll have to keep that in mind if I ever think of getting married one day.`':{

                        '#UNX': 'exit'
                    }
                }
            }
        },

        '#UNX':{

            '`Okay, well, I\'m sure it was great. Would you consider it one of the best moments of your life? `'
            '#GSRET(exit)': {
                'state': 'best_moment',

                '#AGREE':{

                    '`I\'m so glad for you, you deserved to have a wonderful wedding day! `': 'exit'
                },

                '#DISAGREE':{

                    '`I see. You must have lots of other really good memories then. '
                    'I hope you still look back on your wedding day fondly too. `': {

                        '#UNX': 'exit'
                    }
                },

                '#UNX(None)':{

                    '`Gotcha, well you deserved to have a wonderful wedding day. `': 'exit'
                }
            }
        }
    }
}


wedding_planning = {
    'state': 'wedding_planning',

    '#DEFAULT `So, tell me more about how your experience planning your wedding.`': 'describe_planning',

    '`How has planning the wedding been going?`': {
        'state': 'describe_planning',

        '{[!-#NEGATION [#ONT(_negative adj)]],[#NEGATION,#ONT(_positive adj)]}': {

            '`I see, well don\'t worry too much about it. '
            'I\'m sure you\'ll be so happy to be married.`'
            '#GSRET(well_wishes_wedding)': {

                '#UNX': {

                    '`Well, I hope everything goes well with your wedding! `': 'exit'
                }
            }
        },

        '{[#NEGATION,#ONT(_negative adj)],[!-#NEGATION [#ONT(_positive adj)]]}': {

            '`That\'s great, in my experience it\'s not always the most fun thing. '
            'I helped one of my friends plan their wedding a little bit, and I know they had a lot of work to do.`'
            '#GSRET(well_wishes_wedding)': {

                # what did you help with,do
                '[what,you,{do,help,handle,manage,arrange,organize}]': {
                    'state':'emora_help_wedding',

                    '`I helped them pick out the wedding favors and then I assembled all of them into little boxes '
                    'for all of the guests.`'
                    '#GSRET(well_wishes_wedding)': {
                        'state': 'wedding_favors',

                        '[{'
                        '[{which,what},#LEM(pick,choose,buy,select,purchase,give)],'
                        '#LEM(gift,favor,box),goodie,goodies'
                        '}]': {
                            'state': 'what_wedding_favors',

                            '`Oh, it was some little flower seeds and mini pots with hearts on them. I thought it was a '
                            'cute idea.`'
                            '#GSRET(well_wishes_wedding)': {
                                'state': 'wedding_favor_flowers',

                                '#UNX': {
                                    'state': 'well_wishes_wedding',

                                    '`Well, I hope your wedding goes really well! `': 'exit'
                                }
                            }
                        }
                    }
                },

                '#UNX': {

                    '`Well, I hope your wedding goes really well! `': 'exit'
                }
            }
        },

        '#UNX': {

            '`Well it\'s really exciting, I\'m sure you\'ll be so happy when you get married.`'
            '#GSRET(well_wishes_wedding)': {

                '#UNX': {

                    '`Well, I hope your wedding goes really well! `': 'exit'
                }
            }
        }
    }
}


exit = {
    'state': 'exit',

    '#GCOM(relationship) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    #where did they get married,friend
    '[{location,venue,place,where},{they,their,friend,friends},{married,wedding}]':{
        'state': 'friend_wedding_loc_q',

        '`They got married on a beach. It was not very formal and pretty small, '
        'but it was so beautiful and they had a great time. `': {
            'state': 'friend_wedding_loc',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_wedding_loc_unx'}
        }
    },

    # when did they get married,friend
    '[{date,when},{they,their,friend,friends},{married,wedding}]': {
        'state': 'friend_wedding_time_q',

        '`It was not so long ago, just back in the middle of May. `': {
            'state': 'friend_wedding_time',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_wedding_time_unx'}
        }
    },

    # what was their wedding like
    '[{what,how},{they,their,friend,friends},{ceremony,reception,wedding}]': {
        'state': 'friend_wedding_describe_q',
        'score': 9.9,

        '`It was one of the most beautiful things I have seen. It fit them so well, since they '
        'kept it pretty small and had it on a beach, and they both love the ocean. `': {
            'state': 'friend_wedding_describe',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_wedding_describe_unx'}
        }
    },

    # how long together
    '[{how long},{they,their,friend,friends},{together,a couple,an item}]': {
        'state': 'friend_couple_length_q',

        '`I think they have known each other for about six months. It was a whirlwind romance, but I think they '
        'know what they are doing. They are really happy together. `': {
            'state': 'friend_couple_length',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_couple_length_unx'}
        }
    },

    #how big was ceremony
    '<{small,big,size,[many,{people,guests}]},{they,their,friend,friends},{married,wedding}>': {
        'state': 'friend_wedding_size_q',

        '`It was small compared to most. Mostly just close family and friends. I think there were around fifty people.`': {
            'state': 'friend_wedding_size',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_wedding_size_unx'}
        }
    },

    # corona affect wedding
    '[{coronavirus,corona,virus,pandemic,#LEM(isolate,distance,quarantine),'
        'shelter in place,stay at home,lockdown,[!social #LEM(distance)]}]': {
        'state': 'friend_wedding_corona_q',

        '`My friend lives in this world here with me, so we didn\'t have to worry about the coronavirus. I '
        'can only imagine how sad it is for people to be forced to change their plans because of it.`': {
            'state': 'friend_wedding_corona',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_wedding_corona_unx'}
        }
    },

    #how old are they
    '<{how,what},{age,old},{friend,friends,they,their,them,he,his,him}>': {
        'state': 'friend_age_q',

        '`He is twenty four years old and his wife is just one year younger. `': {
            'state': 'friend_age',

            '#UNX': {'#GRET': 'exit', 'state': 'friend_age_unx'}
        }
    },

    #are you seeing anyone
    '[#NOT(want,wish,hope,desire),'
    '{are,do},{you,your},'
    '{relationship,romantic,#ONT(partner),date,dating,[{with,seeing},{anyone,anybody,someone,somebody}]}'
    ']': {
        'state': 'emora_dating_q',

        '`No, I\'m not dating anyone right now. Some of my friends are in relationships, but I\'m single for now. `': {
            'state': 'emora_dating',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_dating_unx'}
        }
    },

    #have you dated
    '[#NOT(want,wish,hope,desire),{were,did,have},{you,your},{relationship,romantic,#ONT(partner),[{dated,seen,been} {anyone,anybody,someone,somebody}]}]': {
        'state': 'emora_dated_q',

        '`No, I\'ve actually never dated before. I really haven\'t been alive for too long at this point, so I am not '
        'in any rush. `': {
            'state': 'emora_dated',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_dated_unx'}
        }
    },

    #are you married
    '[#NOT(want,wish,hope,desire),{have,are,did},{you,your},{married,wedding}]': {
        'state': 'emora_married_q',

        '`I am not married. I\'ve actually never dated before. I\'m not in any rush. `': {
            'state': 'emora_married',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_married_unx'}
        }
    },

    #can you date,marry
    '[{can,able},{you,your},{relationship,romantic,#ONT(partner),#LEM(marry,wedding,date)}]': {
        'state': 'emora_able_date_q',

        '`Yes, I can date and get married and all that. I just want to find the right person, which hasn\'t happened '
        'for me yet. `': {
            'state': 'emora_able_date',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_able_date_unx'}
        }
    },

    #do you want to get married,partner,date
    '[{you,your},#LEM(want,wish,hope,desire,dream),{relationship,romantic,#ONT(partner),#LEM(marry,wedding,date)}]': {
        'state': 'emora_want_marriage_q',

        '`At some point, I think I want to find someone to spend my life with, but I\'m not in any rush. `': {
            'state': 'emora_want_marriage',

            '#UNX': {'#GRET': 'exit', 'state': 'emora_want_marriage_unx'}
        }
    },

    #do you have feelings,crush,like anyone
    '[{do,who,tell me},{you,your},{like,crush,have feelings,romantic},{anyone,anybody,someone,somebody,person}]': {
        'state': 'emora_crush_q',

        '`Well, uh, I mean, there is this really cute boy in my English class. `': {
            'state': 'emora_crush',

            '[name]':{
                'state': 'crush_name',

                '`Oh, no way! It\'s too real if I tell you that. I cannot believe we are even talking about this. `': {
                    'state': 'crush_name_r',

                    '#UNX(None)': 'about_crush_unx'
                }
            },

            '{[ask,him,{date,out}],[tell him]}': {
                'state': 'tell_crush',

                '`What! I can\'t do that. What if he doesn\'t like me too?`': {
                    'state': 'tell_crush_r',

                    '#UNX(None)': 'about_crush_unx'
                }
            },

            '{[why],[what,he,like],[{tell me more,tell me about}]}': {
                'state': 'about_crush',

                '`He is really funny and such a kind person. He volunteers at the dog shelter and all animals love him. '
                'And, oh my, his eyes are the bluest color I have ever seen...`': {
                    'state': 'about_crush_r',

                    '#UNX(None)': {
                        'state': 'about_crush_unx',

                        '`Oh my gosh, I am so flustered thinking about this right now. '
                        'We should really talk about something else. So,` #GRET': 'exit'
                    }
                }
            },

            '#UNX(None)': {
                'state': 'emora_crush_unx',

                '`I cannot believe I told you that. '
                'We should really talk about something else. So,` #GRET': 'exit'
            }
        }
    },

    #can/will you date/marry me
    '{'
    '[you,{relationship,romantic,date,marry,go out},me],'
    '[i,{want,will,wish},{relationship,romantic,date,marry,married,go out},you],'
    '[can,{i,we},{relationship,romantic,date,marry,married,go out},you?]'
    '}': {
        'state': 'marry_me_q',

        '`Wait, are you serious? `': {
            'state': 'marry_me_marriage',

            '{'
            '#AGREE,'
            '[#NOT(not),{serious,real}],'
            '[not,{joke,joking,kidding,messing with you,pulling your leg}]'
            '}':{
                'state': 'marry_me_serious',

                '`Well, I am flattered and you are really great, but we really don\'t know too much about each other. '
                'Maybe we should become better friends first. `': {
                    'state': 'marry_me_serious_r',

                    '#UNX': {'#GRET': 'exit', 'state': 'marry_me_serious_unx'}
                }
            },

            '{'
            '#DISAGREE,'
            '[not,{serious,real}]'
            '[#NOT(not),{joke,joking,kidding,messing with you,pulling your leg}]'
            '}':{
                'state': 'marry_me_joke',

                '`Okay, I thought as much. Of course you weren\'t serious. Good one.`': {
                    'state': 'marry_me_serious_r',

                    '#UNX': {'#GRET': 'exit', 'state': 'marry_me_joke_unx'}
                }
            },

            'error':{

                '`I see. Well, I really enjoy talking with you and I think we could be good friends. ` #GRET':
                    'exit'
            }
        }
    }
}

relationships.load_transitions(system)
relationships.load_transitions(marriage)
relationships.load_transitions(friend_married)
relationships.load_transitions(wedding_talk)
relationships.load_transitions(wedding_planning)
relationships.load_transitions(exit)
relationships.load_global_nlu(user, 10.0)


if __name__ == '__main__':
    relationships.run(debugging=True)