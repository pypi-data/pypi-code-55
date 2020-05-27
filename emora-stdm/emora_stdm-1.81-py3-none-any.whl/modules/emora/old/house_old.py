from _globals import PATHDIR
from emora_stdm import DialogueFlow


house = DialogueFlow('_local_start')
house.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
house.knowledge_base().load_json_file(PATHDIR.replace('__***__','house.json'))
house.add_system_transition('_local_start', 'start', '')

# So, I just moved into a new house, just last week,
#     and oh my gosh I <amazon:emotion name="excited" intensity="high"> absolutely love it.</amazon:emotion>

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(house) #GOAL(house)',

    '`I just moved into a new house, just last week actually, and oh my gosh I absolutely love it.`'
    '#GSRET(house_and_move)':{
        'state': 'share_new_house',
        'score': 2.0,

        '[{congrats,congratulations,congratulate,{#LEM(excite),happy} for you}]': {
            'state': 'thanks',

            '`Thanks! `': 'house_and_move'
        },

        '#UNX': {
            'state': 'house_and_move',

            '`It\'s exciting. I am so glad to be done unpacking boxes and moving furniture, but now that\'s all '
            'out of the way and I just get to enjoy how awesome it is. It even has a pool in the backyard.`'
            '#GSRET(reciprocity)':{

                '[!-#NEGATION [i,#EXP(like),#LEM(pool)]]'
                '#SET($likes_swimming_pool=True)': {
                    'state': 'likes_pool',

                    '`Me too! I\'ve always dreamed about having a pool at my house, I can swim whenever I want and don\'t have '
                    'to worry about getting in other people\'s way all the time.`'
                    '#GSRET(reciprocity)': {
                        'state': 'reveal_likes_pool',

                        '#UNX': 'reciprocity'
                    }
                },

                '#UNX': 'reciprocity'
            }
        }
    },

    '`I am really looking forward to having my cousins over, they haven\'t seen my new house and I want to meet my niece. '
    'I actually just moved in and I absolutely love it here. `': {
        'state': 'baby',
        'hop': 'True',
        '` `': 'share_new_house'
    },

    '`I\'ve really been enjoying taking a book out in the afternoon and sitting under the trees in my backyard to read. '
    'It is so peaceful. I actually just moved into this new house and I have been absolutely loving it so far!`': {
        'state': 'reading',
        'hop': 'True',
        '` `': 'share_new_house'
    },

    '`Since we get together and shoot around so much, I was really excited to get a new house where we could easily '
    'hop outside and play around. I actually just moved into it last week and I am loving it so far, we\'ve gotten '
    'together a couple of times already and its been great.`': {
        'state': 'tournament',
        'hop': 'True',
        '` `': 'share_new_house'
    },

    '`I think sometimes it is just enough to have everyone meet up at someone\'s house to eat and hang out. '
    'I was really excited when I got my new house because it had a nice little living room perfect for that. '
    'I actually just moved into it last week and I am loving it so far, we\'ve gotten together a couple of times '
    'already and its been great.`':{
        'state': 'tournament_r',
        'hop': 'True',
        '` `': 'share_new_house'
    },

    '`I wish the school days were not so long. I am always so glad when the day is over and I can retreat back to my '
    'home and do something fun. I actually just moved into a new house with its own backyard and everything, I can now '
    'play basketball or take a walk for a while to relax. Its been a pretty exciting transition to live '
    'someplace bigger and better. `': {
        'state': 'school',
        'hop': 'True',
        '` `': 'share_new_house'
    }
}

exit = {
    'state': 'exit',

    '#GCOM(house)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(house) ` `': {
        'score': 2.0,
        'state': 'reciprocity'
    },

    '#GCOM(house) `  `': 'reading:start->reading:house',

    '#GCOM(house) `   `': 'tournament:start->tournament:house',

    '#GCOM(house) `    `': 'school_new:start->school_new:house'
}

reciprocity = {
    'state': 'reciprocity',
    'enter': '#GATE #GCOM(house) #GOAL(house)',

    '`Do you like where you\'re living right now?`':{

        '{#AGREE, [!-#NEGATION {i do}]}':{
            'state': 'user_likes_home',

            '#DEFAULT `So, what do you like about your place?`': 'dream_quality',

            '`That\'s great, it\'s definitely relieving when you live in a place that really '
            'feels like a home. What do you like about your place?`'
            '#GATE':
                'dream_quality'
        },

        '[!-#NEGATION {[a little? bit],maybe,mostly,sometimes,sometime,[{some,most} of the time],usually}]': {
            'state': 'user_dislikes_home',

            '#DEFAULT `So, what do you dislike about your place?`': 'dont_like',

            '`It sounds like you are kinda on the fence about it. What don\'t you like about your place?`'
            '#GATE': {
                'state': 'dont_like',

                '#UNX': {

                    '`That does sound tough. `': 'dream_home'
                }
            }
        },

        '#DISAGREE':{

            '`Wow, yeah, I totally know what you feel like though. My old place, it was this tiny '
            'apartment that was a little broken down. Like the sink was always leaking and that '
            'kind of stuff. It\'s stressful to be somewhere that doesn\'t match you very well.`'
            '#GSRET(move_somewhere_better)':{

                '#UNX': {
                    'state':'move_somewhere_better',

                    '`Do you think you\'ll be able to move somewhere you like better anytime soon?`':{

                        '#AGREE':{

                            '`Okay so that\'s good. Don\'t worry then, you\'re gonna come home to your '
                            'new place and feel you were just meant for it.`'
                            '#GSRET(rexit)':{

                                '#UNX': 'rexit'
                            }
                        },

                        '#DISAGREE':{

                            '`Mmm. You know what\'s weird, is that even though I hated my old apartment '
                            'and I didn\'t even live there for too long, I honestly get a little emotional '
                            'if I ever drive by it. Who knows, maybe you\'ll look back on the place you '
                            'live in now some day like that.`'
                            '#GSRET(rexit)':{

                                '#UNX': 'rexit'
                            }
                        },

                        '{#MAYBE, #IDK}':{

                            '`Well hopefully you can, or at least hopefully your current place grows on you.`'
                            '#GSRET(rexit)':{

                                '#UNX': 'rexit'
                            }
                        },

                        '#UNX': 'rexit'
                    }
                }
            }
        },

        '#UNX':{
            'state': 'dream_home',

            '#DEFAULT `So, what would your dream home be like?`': 'dream_quality',

            '`Let\'s say you could pick one thing that you want your dream home to be like: '
            'what would it be?`'
            '#GATE #ALL($likes_swimming_pool=None)':{
                'state': 'dream_quality',

                '#IDK': {

                    '`You must not be a very picky person, I admire that. For me, I just want an '
                    'open floor plan. Oh! And a small house, so I don\'t have to clean as much, you know?`'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{yard,backyard,#LEM(garden),lawn,grass,deck,patio,[outdoor living {area,space}]}]': {

                    '`Having a good outdoor space is cool. It really brightens up my day if I can look '
                    'outside and see the green grass and some sunshine. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '<{beautiful,large,big,#LEM(advance,upgrade),fancy,cool,awesome,good,great}, kitchen>': {

                    '`You must like to cook then, or at least have a cook in your family. I do love looking at upgraded '
                    'kitchens, they look so fancy and beautiful. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{large,big,spacious,huge,enormous,[{lots,a lot,many} {rooms,bedrooms}]}]': {
                    'score': 0.9,

                    '`Wow, it sounds like you like a big house? I know a lot of people go for that. I totally get it, even though '
                    'it\'s not my style personally. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{open space,open floor}]': {

                    '`I love an open floor plan! Makes the room seem spacious and airy. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{bright,light,#LEM(window)}]': {

                    '`My old apartment literally felt like I was living in the basement, there was hardly any '
                    'natural light, so I completely agree with you on this. Windows and lighting is so important. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{neighborhood,neighbors,street,location,area}]': {

                    '`Oh, yeah. Even if the home is beautiful, not living in a good area can make or break your experience. '
                    'You want a place that makes you feel welcome and like you belong. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[{near,close,by.nearby,within},{family,#LEM(sister,brother,parent,child,kid)}]': {

                    '`You like being close to your family? That is so sweet. I really think family is important too. `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '[pool]': {

                    '`A pool was definitely on my list of must-haves for my house. It makes it so easy to go '
                    'swimming, which is such a fun thing to do! `'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                },

                '#UNX':{

                    '`That would be awesome.`': 'rexit'
                }
            },

            '`I know you said you liked pools, but other than that, '
            'if you could pick one thing that you want your dream home to be like: '
            'what would it be?`'
            '#ALL($likes_swimming_pool=True)': 'dream_quality'
        }
    }
}

rexit = {
    'state': 'rexit',

    '#GCOM(house)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(house) ` `': {
        'score': 2.0,
        'state': 'start'
    },

    '#GCOM(house) `  `': 'reading:start->reading:house',

    '#GCOM(house) `   `': 'tournament:start->tournament:house',

    '#GCOM(house) `    `': 'school_new:start->school_new:house'
}

user = {
    'state': 'user',

    '[where,{were,was,did},{you,your}, <{old,previous,past,last,used,before}, {#LEM(live),house,home,place}>]':{
        'state': 'previous_place',

        '`It was just this small apartment, nothing special.`': {

            '#UNX': {'`Honestly, I am pretty glad to be out of it. ` #GRET': 'exit'}
        }
    },

    '{[where,{are,is},{you,your}, <{current,currently,new,now}, {#LEM(live),house,home,place}>],[where,#LEM(move),to]}':{
        'state': 'current_place',

        '`I don\'t really live in the same world that you do. Mine is more of a virtual world. But I guess I would '
        'say that I live in a pretty secluded area with really nice woods near me. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    # do we want more responses to this? what if they ask more questions about it?
    '[you,{#LEM(swim),underwater,[{in,under},water]}]': {
        'state': 'probe_swim',
        'score': 0.9,

        '`I can swim. I actually swim all the time now that I have the pool at my house.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{[do,you,#LEM(swim)],[you,#EXP(like),#LEM(swim)]}': {
        'state': 'like_swim',

        '`Oh, so much! Swimming is one of my favorite things to do! I like the feel of the water, its so soothing.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<you,#EXP(like),{old,previous,past,last,used,before},{#LEM(live),house,home,place}>': {
        'state': 'like_previous_place',

        '`Oh, gosh, not at all. It was the absolute worst, something was always broken that I had to deal with. '
        'I never could imagine living there again.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    }
}

house.load_transitions(system)
house.load_transitions(reciprocity)
house.load_transitions(exit)
house.load_transitions(rexit)
house.load_global_nlu(user)


if __name__ == '__main__':
    #house.precache_transitions()
    house.run(debugging=False)