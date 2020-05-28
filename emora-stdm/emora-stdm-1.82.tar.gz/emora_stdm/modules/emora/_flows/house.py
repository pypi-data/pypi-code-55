from _globals import PATHDIR
from emora_stdm import DialogueFlow


house = DialogueFlow('_local_start')
house.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
house.add_system_transition('_local_start', 'start', '#RAND(life_in,True)')


system = {
    'state': 'start',
    'enter': '#GATE #GCOM(house) #GOAL(house) #IF($life_in=True,$life_started=True) '
             '#ANY($relationship_status=married,$relationship_status=divorced,$partner=husband,$partner=wife)',

    '`Do you want to know something? I can\'t stop thinking about my day yesterday. '
    'My friends came over to my new apartment for the first time and it was so much fun.`'
    '#GSRET(user_living) #SET($introduced_virtual=False)':{
        'state': 'share_new_house',
        'score': 2.0,

        '{[why],[what,{[you,do],happened,good}]}':{
            'state': 'friends_at_apartment',

            '`It was just nice to show them my apartment a bit. We also talked and played some basketball together. '
            'There is a community basketball court in the complex. So, `': 'user_living'

        },


        '#INTERESTED':{
            'state': 'more_about_house',

            '`Yeah I really like it, it\'s close to where I go to school and it even has a community basketball court.`'
            '#GSRET(user_living)':{

                '[you,{school,student}]': {

                    '`Oh yeah, I am a student right now and go to school. `':{
                        'state': 'school_new:start',
                        'score': 2.0
                    },

                    '`Oh yeah, I am a student right now and go to school.  `':
                        'user_living'
                },

                '[you,basketball]': {
                    'state': 'community_bball',

                    '`I actually enjoy basketball a lot, my friends and I like to play it when we get together.`'
                    '#GSRET(user_living)': {
                        'state': 'community_bball_unx',

                        '#NOT(not) [{we,i,my},{play,#EXP(like)},basketball]':{
                            '`Awesome, isn\'t it so much fun? Anyway, `': 'user_living'
                        },

                        '#UNX': 'user_living'
                    }
                },

                '#NOT(not) [i,{play,#EXP(like)},basketball]':{
                    '`Me too! `': 'community_bball'
                },

                '#UNX': 'user_living'
            }
        },

        # '#TOKLIMIT(3)': {
        #     'state': 'world:user_in_disbelief',
        #     'score': 0.9
        # },

        '{'
        '[{how,what},it,{like,have}],'
        '[[!tell me {more,about it,more about it,more about that}]],'
        '[how,{is,feel},it],'
        '[what,you,think,{of,about},it]'
        '}': {
            'state': 'tell_more_apartment_local',
            'score': 10.1,

            '`It\'s a pretty good place for me, honestly. '
            'It is just a one-bedroom apartment, but it has a lot more space and I get a lot of light through my '
            'windows. I also have a balcony which is nice.`'
            '#GSRET(user_living)': {

                '#UNX': 'user_living'
            }
        },

        '{'
        '[{how,what},experience,{like,have}],'
        '[[!tell me {about that experience, more about that experience}]],'
        '[how,{#LEM(is),feel},experience],'
        '[what,you,think,{of,about},experience]'
        '}': {
            'state': 'tell_more_experience',
            'score':10.2,

            '`I love having my friends over. We hang out a lot and talk and do fun things together. `'
            '#GSRET(user_living)': {

                '#UNX': 'user_living'
            }
        },

        '#UNX': {
            'state': 'user_living'
        }
    }
}

user_living = {
    'state': 'user_living',

    '`Do you like where you\'re living right now?`':{
        'state': 'ask_user_living',

        '{#AGREE, [{i do, i like, not bad, not too bad}]}'
        '#SET($user_likes_home=True)':{

            '#DEFAULT `So, what do you like the most about your home?`': 'user_best_home',

            '`That\'s great! What do you like about it?`'
            '#GATE': {
                'state': 'user_best_home',

                '#IDK': {
                    'state': 'user_likes_house_idk',

                    '`You must not be a very picky person, I admire that. For me, I just want an '
                    'open floor plan. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{yard,backyard,#LEM(garden),lawn,grass,deck,patio,[outdoor living {area,space}]}]': {
                    'state': 'user_likes_house_yard',

                    '`Having a good outdoor space is cool. It is a fun way to spend time when the weather is good. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '<{beautiful,large,big,#LEM(advance,upgrade),fancy,cool,awesome,good,great}, kitchen>': {
                    'state': 'user_likes_house_kitchen',

                    '`You must like to cook then, or at least have a cook in your family. I do love a good kitchen, too. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{palace,mansion,large,big,spacious,huge,enormous,[{lots,a lot,many} {rooms,bedrooms}]}]': {
                    'score': 0.9,
                    'state': 'user_likes_house_big',

                    '`Oh yeah, that\'s a good point. It is so relieving when you have plenty of space to live '
                    'comfortably. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{open space,open floor}]': {
                    'state': 'user_likes_house_open',

                    '`I love an open floor plan, too! Makes the room seem spacious and airy. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{bright,light,#LEM(window)}]': {
                    'state': 'user_likes_house_light',

                    '`My old apartment literally felt like I was living in the dark basement, so I completely '
                    'agree with you on this. Windows and lighting are so important. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{neighborhood,neighbors,street,location,area}]': {
                    'state': 'user_likes_house_location',

                    '`Yes, you definitely want a place that makes you feel welcome and like you belong. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[{near,close,by,nearby,within},{family,#ONT(_related person)}]': {
                    'state': 'user_likes_house_family',

                    '`You like being close to your family? That is so sweet. I really think family is important too. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '[pool]': {
                    'state': 'user_likes_house_pool',

                    '`Having your own pool is amazing! You can take a swim whenever you want, that\'s so cool. `'
                    '#GSRET(ask_entertain_people)': {

                        '#UNX': 'ask_entertain_people'
                    }
                },

                '#UNX': {
                    'state': 'user_likes_house_unx',

                    '`It\'s awesome to be in a place that really feels like home.`': 'ask_entertain_people'
                }
            }
        },

        '[{#DISAGREE, i do not, #ONT(_negative adj)}]'
        '#SET($user_likes_home=False)':{

            '#DEFAULT `So, what do you like the least about your home?`': 'user_worst_home',

            '`That\'s hard. What bothers you the most about it?`'
            '#GATE': {
                'state': 'user_worst_home',

                '#IDK': {
                    'state': 'user_hates_house_idk',

                    '`Oh dear, well I hope it isn\'t too bad. Is it at least close to where you work? `'
                    '#GSRET(school_proximity)':
                        'asked_school_proximity'
                },

                '[{yard,backyard,#LEM(garden),lawn,grass,deck,patio,[outdoor living {area,space}]}]': {
                    'state': 'user_hates_house_yard',

                    '`I\'m sorry to hear that. I wish that you had an outdoor space that you could enjoy. `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '[{kitchen,oven,fridge,stove,cabinet,cabinets,dining}]': {
                    'state': 'user_hates_house_kitchen',

                    '`The kitchen is an essential part, that stinks that yours isn\'t really good! `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '{'
                '[{want,wish,#EXP(like)} {palace,mansion,large,big,spacious,huge,enormous,[{few,not enough,small} {rooms,bedrooms}]}],'
                '[{small,tiny,cramped,space}]'
                '}': {
                    'score': 0.9,
                    'state': 'user_hates_house_small',

                    '`It is definitely not good to feel cramped in your own house. That must be so annoying! `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '[{want,wish,#EXP(like)} {open space,open floor}]': {
                    'state': 'user_hates_house_not_open',

                    '`I love an open floor plan, too! Hopefully you can get that in a future home or something. `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '{'
                '[{no,not,few} {bright,light,#LEM(window)}],'
                '[{dark,dim}]'
                '}': {
                    'state': 'user_hates_house_dark',

                    '`My old apartment literally felt like I was living in the dark basement, so I completely '
                    'sympathize with you on this. Windows and lighting are so important. `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '<{bad,dangerous,sketchy,shady} {neighborhood,neighbors,street,location,area}>': {
                    'state': 'user_hates_house_location',

                    '`Oh no, you definitely want a place that makes you feel welcome and safe! I hope it isn\'t too bad. `'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '[{far,[not,{close,near,by}]},$far_family={family,#ONT(_related person)}]': {
                    'state': 'user_hates_house_family',

                    '`I hope you are able to see` $far_family `as much as you want. It can be tough if people live too far '
                    'away.`'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '[{no,not} pool]': {
                    'state': 'user_hates_house_pool',

                    '`Having your own pool is pretty cool, but I have heard it can be a lot of work too. Just depends '
                    'on how much you use it!`'
                    '#GSRET(school_proximity)': {

                        '#UNX': 'school_proximity'
                    }
                },

                '#UNX': {

                    '`It\'s tough to be in a place that doesn\'t feel like home. I know I hated the last place I was living.`'
                    '#GSRET(school_proximity)':{

                        '[{why,[what,about,{that,it}]}]': {

                            '`It was just really, really small and dark. I couldn\'t even have people over because '
                            'of the small space. `'
                            '#GSRET(school_proximity)': {

                                '#UNX': 'school_proximity'
                            }
                        },

                        '#UNX': 'school_proximity'
                    }
                }
            }
        },

        '#UNX': 'school_proximity'
    }
}

school_proximity = {
    'state': 'school_proximity',

    '#IF($is_employed=False)': {
        'score': 1.1,
        'state': 'live_with'
    },

    '`So are you close to where you work?`'
    '#GSRET(exit)': {
        'state': 'asked_school_proximity',

        '{[unemployed],[#NEGATION,{work,job,employed}],[!a {kid,child}]}'
        '#SET($is_employed=False)':{
            'state': 'not_work',

            '`Oh, sorry, I didn\'t know that. Well, I hope you are close to places you like to '
            'go to a lot. `': 'old_apartment_distance'
        },

        '{#AGREE, [!-#NEGATION [i am, close]], [not far]}'
        '#SET($is_employed=True)': {

            '`That\'s really good.`': {
                'state': 'old_apartment_distance',
                'hop': 'True',

                '`My old apartment was forty five minutes away from where I go to school, it was the worst.`'
                '#GSRET(live_with)': {

                    '[{fifty, #LEM(hour), sixty, seventy, eighty, ninety}]': {

                        '`Wow, and I thought my commute time was bad before. I cannot believe you survive that. '
                        'I feel for you. `'
                        '#GSRET(live_with)': {

                            '#UNX': 'live_with'
                        }
                    },

                    '[you,{school,student}]': {

                        '`Yes, I am a student right now and go to school. `':{
                            'state': 'school_new:start',
                            'score': 2.0
                        },

                        '`Yes, I am a student right now and go to school.  `':
                            'live_with'
                    },

                    '[{what,why},you,{dislike,hate,#EXP(like)},'
                    '{[{old,previous,past,last,used,before,that},{#LEM(live),apartment,house,home,place}],it}]': {
                        'state': 'like_previous_place_local',

                        '`Something was always broken that I had to deal with and it was very small and dark, too. '
                        'I never could imagine living there again.`': {

                            '#UNX': {'#GRET': 'exit'}
                        }
                    },

                    '#UNX': 'live_with'
                }
            }
        },

        '{#DISAGREE, [i, am, not], [not, close]}'
        '#SET($is_employed=True)': {

            '`Oh I hate that.`': 'old_apartment_distance'
        },

        '#UNX': 'old_apartment_distance'
    }
}

entertain_people = {
    'state': 'ask_entertain_people',

    '#DEFAULT `So, do you like having people over at your place?`': 'asked_entertain_people',

    '`Now that I have a bigger apartment, I think I will enjoy hosting more gatherings. Do you like having people over '
    'at your place?`'
    '#GATE': {
        'state': 'asked_entertain_people',

        '{#AGREE, [{i do, i like, not bad, not too bad}]}'
        '#SET($user_likes_hosting=True)': {
            'state': 'likes_hosting',

            '`Good! It is always so fun to hang out and socialize. Plus you get to be in charge of the snacks!`'
            '#GSRET(school_proximity)': {

                '#UNX': 'school_proximity'
            }
        },

        '[{#DISAGREE, not so much, i do not, #ONT(_negative adj)}]'
        '#SET($user_likes_hosting=False)': {
            'state': 'hates_hosting',

            '`It is a lot of work, isn\'t it? It can be hard to plan everything out. Might as well '
            'let someone else worry about all the details!`'
            '#GSRET(school_proximity)': {

                '#UNX': 'school_proximity'
            }
        },

        '[{coronavirus,corona,virus,pandemic,#LEM(isolate,distance,quarantine),'
        'shelter in place,stay at home,lockdown,[!social #LEM(distance)]}]': {
            'state': 'hosting_coronavirus_restrictions',
            'score': 10.1,

            '`I am really sorry to hear that. Hopefully you can get together with the people you care about soon.`'
            '#GSRET(school_proximity)': {

                '#UNX': 'school_proximity'
            }
        },

        '#UNX':{
            'state': 'unx_hosting',

            '`It can be a lot of work, but it is nice to bring everyone together! `'
            '#GSRET(school_proximity)': {

                '#UNX': 'school_proximity'
            }
        }
    }
}

live_with = {
    'state': 'live_with',

    '#DEFAULT `Wait, do you live with anyone?`': 'live_with_response',

    '#ANY($relationship_status=married,$partner=husband,$partner=wife,$partner=spouse)':{
        'state': 'exit',
        'score': 1.1
    },

    '`You know, sometimes I can get lonely because I don\'t have any roommates, '
    'even though I do have friends and family come over a lot. Do you live with anyone?`'
    '#GATE': {
        'state': 'live_with_response',

        '[#EXTR(lives_with, _related person)]':{
            'state': 'lives_with_fam',
            'score': 1.1,

            '`That\'s nice! Do you guys get along well?`'
            '#GSRET(exit)': {
                'state': 'ask_get_along',

                '[#NOT(not) {#AGREE, we do, mostly, most, usually, a lot}]':{
                    'state': 'get_along_yes',

                    '`That\'s really good to hear. You seem like a pretty grateful person.`'
                    '#GSRET(exit)': {
                        'state': 'get_along_yes_unx',

                        '#UNX': 'exit'
                    }
                },

                '[{#DISAGREE, we do not}]':{
                    'state': 'get_along_no',

                    '`Oh, it must be pretty stressful to live with people you don\'t have a good relationship '
                    'with. I\'m sorry. `'
                    '#GSRET(exit)': {
                        'state': 'get_along_no_unx',

                        '#UNX': 'exit'
                    }
                },

                '#UNX':{
                    'state': 'get_along_unx',

                    '`To be fair, I think every household has its ups and downs. Anyway, `': 'exit'
                }
            }
        },

        '#AGREE #GATE':{
            'state': 'lives_with_y',

            '`Oh, that\'s cool! Who do you live with then?`'
            '#GSRET(exit)':
                'live_with_response'

        },

        '[{#DISAGREE, alone, myself, no one, nobody, anybody, me too, neither, either, i do not, have not}]'
        '#SET($user_lives_alone=True)':{
            'score': 0.9,
            'state': 'lives_alone',

            '`Do you like living by yourself?`': {

                '#AGREE': {
                    'state': 'likes_lives_alone',

                    '`It definitely has it\'s benefits, doesn\'t it? Anyway, `': 'exit'
                },

                '#DISAGREE':{
                    'state': 'hates_lives_alone',

                    '`I understand that. It can be kind of boring. Anyway, `': 'exit'
                },

                '#UNX': 'exit'
            }
        },

        '#UNX(Okay)': 'exit'
    }
}

exit = {
    'state': 'exit',

    '#GCOM(house) #GRET': {
        'score': 0.0,
        'state':'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    '{'
    '[where, {you,your,the}, <{old,previous,past,last,used,before}, {#LEM(live),house,home,place}>],'
    '[where,were,you,#LEM(live,stay)]'
    '}':{
        'state': 'previous_place',

        '`It was just this small apartment, nothing special.`': {

            '#UNX': {

                '`Honestly, I am pretty glad to be out of it. ` #GRET': 'exit'
            }
        }
    },

    '<you,{dislike,hate,#EXP(like)},{old,previous,past,last,used,before},{#LEM(live),house,home,place}>': {
        'state': 'like_previous_place',

        '`Oh, gosh, I did not like it at all. It was the absolute worst, something was always broken that I had to deal with. '
        'I never could imagine living there again.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[{congrats,congratulations,congratulate,{#LEM(excite),happy} for you}]': {
        'state': 'thanks',

        '`Thanks! ` #GRET': 'exit'
    },

    '[{covid,coronavirus,corona,pandemic,#LEM(isolate,distance,quarantine),'
    'shelter in place,stay at home,lockdown,[!social #LEM(distance)]}]': {
        'state': 'coronavirus_restrictions',

        '`The coronavirus doesn\'t affect me where I live, since it is separate from your physical world. I am really '
        'sorry to hear that you have so many restrictions on you. I hope you are staying safe and healthy.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '[what,your,{house,home,apartment,place},{like,have}],'
    '[tell me {about,more},your,{house,home,apartment,place}],'
    '[how,{is,feel},your,{house,home,apartment,place}],'
    '[what,you,think,your,{house,home,apartment,place}]'
    '}': {
        'state': 'tell_more_apartment',

        '`It\'s a pretty good place for me, honestly. '
        'It is just a one-bedroom apartment, but it has a lot more space and I get a lot of light through my '
        'windows. I also have a balcony which is nice.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{you,your},{rooms,size,big,small,large},{house,home,apartment,place}>': {
        'state': 'apartment_size',

        '`It has a kitchen, living room, bathroom, bedroom, and laundry room. That\'s about it, nothing too big. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<what,in,your,{house,home,apartment,place}>': {
        'state': 'apartment_contents',

        '`It has a kitchen, living room, bathroom, bedroom, and laundry room. And obviously some furniture like a tv and '
        'couch and stuff. Just normal things. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<why,#LEM(friend,people),{come,over,visit}>': {
        'state': 'why_friends_come',

        '`It was like a house-warming party, so they could see my new place. Plus we just like to hang out all the time. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '<{you,your},{neighborhood,community,neighbors,area,location},{good,fun,safe}>,'
    '<you,feel,{welcome,belong,belonging}>,'
    '[what,you,like,{neighborhood,community,neighbors,area,location}]'
    '}':{
        'state': 'apartment_neighborhood',

        '`I like my community a lot. It is in a good area with lots of walking paths and nobody is too loud in the '
        'apartments near me. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    }
}

update_rules = {
    '[!-#NEGATION [i, live, $home_type={r v, dorm, dormitory, residence hall, apartment, '
    'condo, condominium, house, loft, townhouse, manor, mansion, palace, mobile home, trailer}]]': '',
    '[!-#NEGATION [i, live, {ranch, two story, one story, penthouse, duplex}]]': '#SET($home_type=house)',
    '[!-#NEGATION [{am, live} with, my, #EXTR(lives_with, _related person)]]': ''
}

house.load_transitions(system)
house.load_transitions(user_living)
house.load_transitions(live_with)
house.load_transitions(school_proximity)
house.load_transitions(entertain_people)
house.load_transitions(exit)
house.load_global_nlu(user, default_score=10.0)
house.load_update_rules(update_rules)

if __name__ == '__main__':
    #house.precache_transitions()
    house.run(debugging=True)