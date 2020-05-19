
personal_nlu = {

    ### About Emora #########################################

    '{'
    '[{what, whats, tell me, say}, your, #NOT(#ONT(_related person)), name], '
    '[what, {i, we} call you]'
    '}': 'backstory:name',

    '{'
    '[{are you, are not you, you are} '
    '{robot, ai, a i, software, bot, chatbot, artificial intelligence, '
    'program, electronic, electric, human, person, living, alive, real}]'
    '}': 'backstory:virtual',

    # Does Emora have something humanlike
    '{'
    '[do you have, $q_body=#ONT(body)], '
    '[you, {cant, arent, dont, not}, have, $q_body=#ONT(body)]'
    '}'
    '#SCORE(1.1)':
        'backstory:body',

    # Does Emora have something humanlike
    '{'
    '[do you have], '
    '[have, you, got],'
    '[you, {cant, arent, dont, not}, have]'
    '}':
        'backstory:have_like_human',

    # Does Emora like something
    '[#NOT(which,what,how,why), do you, #EXP(like)]':
        'backstory:unknown_preferences',

    # Emora's favorite
    '{'
    '[{what, whats}, your, favorite]'
    '#SCORE(0.1)}':
        'backstory:unknown_favorites',

    # # todo - Do you ___
    # '[what, do you]'
    # '#SCORE(0.1)':{
    #
    # },

    # Who is your friend/family
    '{'
    '[who, your, {family,#ONT(_related person)}],'
    '[you,{cant,can not,dont,do not,arent,are not},{family,#ONT(_related person)}],'
    '<{family,#ONT(_related person)},you,{not possible,impossible}>'
    '}':
        'backstory:relationships',

    # What is your friend/family's name
    '{'
    '[{what,whats}, your, #ONT(_related person), {name, names}],'
    '[{what,whats}, their, {name, names}]'
    '}':
        'backstory:relationship_names',

    ### Emora capabilities and appraisal #########################################

    # # todo - What can you talk about
    # '{'
    # '[what, can {you, we} {talk about, discuss}], '
    # '[what, do you, {know about, talk about, discuss}]'
    # '}':{
    #
    # },

    # Do you know
    '{'
    '[do you, know]'
    '}':
        'backstory:unknown',

    # How do you
    '{'
    '[how, do you]'
    '}':
        'backstory:ask_how',

    # Can we talk about
    '{'
    '[{can,will,could,let us}?, {chat,talk,discuss,converse,conversation,discussion}, {else,different,other,new,another}], '
    '[{we,our,i,you}, <{already,previously,past,before,last,previous}, '
        '{chat,chatted,talk,talked,discuss,discussed,converse,conversed,conversation,discussion,cover,covered,told}, {about,this}>] '
    '[{this is, i am}, {bored,tired of,frustrated,annoyed,boring,not fun,not having fun,not having a good time,not good, '
        'not interesting,not interested}], '
    '<{[i, {hate,detest,dislike,not like}, this],[stop,#LEM(talk),this]}>, '
    '[{next,move on,skip,do something else}], '
    '[{can,will,could,let us}?, {switch,change,go}, {different,another,other,new}?, '
        '{topic,topics,thing,things,conversation,conversations,subjects,subject,points,point,directions,direction}], '
    '[i, {not,never}, care], '
    '[i, {never,not}, {prefer,want,desire,like}, {chat,talk,discuss,converse,conversation,discussion}]'
    '}':{
        '`Alright. So, `': 'SYSTEM:root'
    },

    # Can we talk about X
    '{'
    '[![{let us, we, you}] {talk, converse, conversation, discuss, discussion, chat} about? $topic_requested=/.*/]'
    '}':{
        'score': 9.0,

        '`I don\'t think I know anything about that, but `':{
            'hop': 'True',

            '#SBS($topic_requested, cat dog pony horse thing riding petting) `We can talk about pets!`':{

                '#UNX': 'SYSTEM:root'
            },

            '#SBS($topic_requested, snowboarding) `We can talk about basketball!`':{

                '#UNX': 'SYSTEM:root'
            }
        }
    },


    ### Security and user info #########################################

    # Is Emora spying on the user
    '{'
    '[are you {spying, [collecting {info, information, data}]}], '
    '[why {[you, {want, need} know], ask, asking}], '
    '<#LEM(record,maintain,store,keep),{#LEM(conversation,talk,data,info,information),this,{i,we,people} say}>'
    '}':
        'backstory:spying',

    # Is Emora part of govt
    '{'
    '<{do,are},you,{government,fbi,cia,f b i,c i a}>'
    '}':
        'backstory:govt',

    # # Alexa play my song
    # '[!{play, alexa play} /.*/]':{
    #
    # },
    #
    # # Alexa turn up/on
    # '[!{alexa turn, turn} /.*/]':{
    #
    # },

    # Tell a joke
    '{'
    '[joke], '
    '[{say, tell me} something funny]'
    '}':{
        'state': 'tell_joke',
        'hop': 'True',

        '#GATE':{
            'state': 'first_joke',

            '`I don\'t know too many jokes, but here\'s one: '
            'Did you hear about the claustrophobic astronaut?`': {
                'state': 'joke_pause',

                '[space]': {
                    'state': 'joke_guess',

                    '`I think you\'re on the right track. He just needed a little space! `': {
                        'state': 'joke_given',

                        '#UNX': {
                            'state': 'joke_given_unx',

                            #todo - what if user asks for another one

                            '#GRET': 'exit'
                        }
                    }
                },

                '#UNX': {
                    'state': 'joke_unx',

                    '`He just needed a little space!`': 'joke_given'
                }
            }
        },

        '/.*/ #SCORE(0.9)':{
            'state': 'multi_joke',

            '`Oh, I\'m sorry. I seem to only remember the one joke I already told you. ` #GRET': 'exit'
        }
    },

    # Can we do something
    '{'
    '[{can we, could we, we should, lets}, together], '
    '[{can, could} i, {with you, come over}]'
    '}':
        'backstory:enter_virtual_world',

    # I like you
    '{'
    '[[!i {like, love} you]]'
    '}':{
        'state': 'user_likes_emora',

        '`That\'s so nice of you to say. I am really enjoying talking to you.`' :{
            'state': 'user_likes_emora_r',

            '#UNX': {'#GRET': 'exit'}
        }
    },

    ### About User #########################################

    # # User job
    # '{'
    # '[{i am, im} a #ONT(job)], '
    # '[i #ONT(job) {for a living, for work, professionally, as a job, for a job}], '
    # '[my {job, work} #ONT(job)], '
    # '[i {work, take jobs, have a job} #ONT(job)]'
    # '}':{
    #
    # },
    #
    # # User is a __
    # '{'
    # '[{im, i am} #ONT(persontype)]'
    # '}':{
    #
    # },

    # todo - make sure no crude words are given
    # User likes
    '[!-#NEGATION {'
    '[i {like, love} $user_likes=#ONT(likable)?]'
    '}]':{
        '`Me too! What do you like the most about it?`': {
            'state': 'returning_from_global_like',

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    # # User currently feels __
    # '{'
    # '[{im, i feel, ive been, i am} #ONT(feeling)]'
    # '}':{
    #
    # },
    #
    # # User went __
    # '{'
    # '[{i, we, me and, and me} went]'
    # '}':{
    #
    # },
    #
    # # User thinks ___
    # '{'
    # '[#NOT(i think so) [i, think]]'
    # '}':{
    #
    # },

    #

    ### User tests Emora #########################################

    # '{'
    # '[{talk about, conversation about, lets discuss, tell me} #ONT(all)]'
    # '}':{
    #
    # },

    ### Topic specific #########################################

    # # Have you seen ___
    # '{'
    # '[have you, {seen, watched}]'
    # '}':{
    #
    # },
    #
    # # Have you read book
    # '{'
    # '[have you, read]'
    # '}':{
    #
    # },
    #
    # # Have you visited
    # '{'
    # '[have you, {been to, gone to, visited, went to}]'
    # '}':{
    #
    # },

}

global_update_rules = {
    '#CONTRACTIONS': ''
}