from _globals import PATHDIR
from emora_stdm import DialogueFlow


tournament = DialogueFlow('_local_start')
tournament.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
tournament.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(tournament) #GOAL(tournament)',

    '`You know it\'s nice to just chill out for a second and talk to you. I\'m super tired: I was just playing in a basketball '
    'tournament with my friends, but our team just got knocked out, so I\'m taking a break to socialize. `'
    '#GSRET(cookout) #GATE':{
        'state': 'nxt',
        'score': 2.0,

        '[{sorry, suck, sucks, oh no}]':{

          '`Oh don\'t worry, I\'m really not a very competitive person. I feel like I have enough competition in my life, '
          'so when I\'m playing games with my friends it\'s just all for fun.`'
          '#GSRET(cookout)':{

              '#UNX': 'cookout'
          }
        },

        '[{how,are,was,were,is,#LEM(do)}, <{it,you},{#LEM(upset),sad}>]': {
            'state': 'question_sad',

            '`I am not too upset by this. I\'m really not a very competitive person. '
            'I feel like I have enough competition in my life, so when I\'m playing games with my friends '
            'it\'s just all for fun.`'
            '#GSRET(cookout)': {

                '#UNX': 'cookout'
            }

        },

        '[{how,are,was,were,is,#LEM(do)}, <{it,you},{angry,mad,piss,pissed}>]': {
            'state': 'question_angry',

            '`Oh, I\'m not really angry at all. My friends and I did the best we can. When I\'m playing games with my '
            'friends, even during tournaments, it\'s just all for fun for us.`'
            '#GSRET(cookout)': {

                '#UNX': 'cookout'
            }
        },

        '[{how,are,was,were,is,#LEM(do)}, <{it,you},{#LEM(disappoint)}>]': {
            'state': 'question_disappoint',

            '`My friends and I did the best we can, so I wouldn\'t say that I am disappointed at all. '
            'When I\'m playing games with my friends, even during tournaments, it\'s just all for fun for us.`'
            '#GSRET(cookout)': {

                '#UNX': 'cookout'
            }
        },

        '#UNX':{
            'state': 'cookout',

            '`My friends and I really like playing basketball together, it\'s just a fun team game even '
            'though I\'m still improving. We do this kind of thing pretty often, usually once or twice a week '
            'they all come over and we cook out and play.`'
            '#GSRET(reciprocity)':{

                '#UNX': 'reciprocity'
            }
        }
    },

    '`I was really excited when this house had a basketball hoop too. My friends and I play all the time. We actually '
    'were in the middle of a tournament before I hopped on here to socialize, but we just got knocked out. `': {
        'state': 'house',
        'hop': 'True',
        '` `': 'nxt'
    },

    '`Actually, one of my favorite parts about school is meeting up with my friends afterwards and playing some '
    'basketball. My friends and I play all the time. We actually were in the middle of a tournament before I hopped on here to socialize, but we just got knocked out. `': {
        'state': 'school',
        'hop': 'True',
        '` `': 'nxt'
    }
}

exit = {
    'state': 'exit',

    '#GCOM(tournament)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(tournament) ` `': {
        'score': 2.0,
        'state': 'reciprocity'
    },

    '#GCOM(tournament) `  `': 'house:start->house:tournament',

    '#GCOM(tournament) `   `': 'school_new:start->school_new:tournament'
}

reciprocity = {
    'state': 'reciprocity',
    'enter': '#GATE #GCOM(tournament) #GOAL(tournament)',

    '`So, what do you like to do with your friends?`':{

        '#IDK': {
            '`I am sure you guys have a good time, no matter what you end up doing. `'
            '#GSRET(rexit)':{
                'state':'done_state',

                '#UNX': 'rexit'
            }
        },

        '{'
        '[i,{dont,do not,never},#LEM(have),{friend,friends}],'
        '[no {friend,friends}],'
        '[{noone,no one},likes,me],'
        '<{noone,no one},{friend,friends},{my,me}>'
        '}': {
            '`You\'re making me sad. But you shouldn\'t worry, I think you seem like someone lots of '
            'people would want to be friends with. I\'d be your friend.`'
            '#GSRET(rexit)':{
                'state':'done_state',

                '#UNX': 'rexit'
            }
        },

        '#UNX(None)':{

            '`That sounds fun!`'
            '#GSRET(rexit)':{
                'state':'done_state',

                '#UNX': 'rexit'
            }
        }
    }
}

rexit = {
    'state': 'rexit',

    '#GCOM(tournament)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(tournament) ` `': {
        'score': 2.0,
        'state': 'start'
    },

    '#GCOM(tournament) `  `': 'house:start->house:tournament_r',

    '#GCOM(tournament) `   `': 'school_new:start->school_new:tournament_r'
}

user = {
    'state': 'user',

    '[you,{#LEM(play,shoot),do basketball},{often,a lot,frequently,[all,time]}]': {
        'state': 'bball_frequency',

        '`I pick up a basketball almost every day, usually just to shoot around a bit. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<you,{good,decent,great,skill,skilled,successful},{basketball,sport,sports}>': {
        'state': 'bball_skill',

        '`Oh man, you are asking the wrong person. I have no idea how good I am, I play mostly for a good time. '
        'I guess I would say I am pretty good at shooting. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<how long,you,{playing,played}>':{
        'state': 'bball_length',

        '`For the last few months. It is pretty much the only sport I play.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<you,#EXP(like),basketball>':{
        'state': 'bball_enjoy',

        '`I totally enjoy playing basketball. I always have a great time, especially if my friends are over.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '[how, {close,far,long}, {you,team}, {make,last,get}],'
    '[{you,team},{close,almost},#LEM(win)],'
    '[{you,team},{reach,make,close,lose,knocked},{final,finals,end}],'
    '[what,place],'
    '[where,{you,team},{lose,knocked,finish,end}]'
    '}':{
        'state': 'tournament_place',

        '`We made it like halfway through the tournament. Definitely got smashed by a few teams, which led to us '
        'being knocked out, but we weren\'t too bad overall.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{you,your},position>':{
        'state': 'bball_position',

        '`Oh, I\'m not really sure what its called. I think I play on the wing? I\'m not too close to the hoop most '
        'of the time.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    }

}

tournament.load_transitions(system)
tournament.load_transitions(reciprocity)
tournament.load_transitions(exit)
tournament.load_transitions(rexit)
tournament.load_global_nlu(user)


if __name__ == '__main__':
    tournament.run(debugging=True)