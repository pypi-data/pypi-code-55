


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

    # How do you
    '{'
    '[how, do you]'
    '}':
        'backstory:ask_how',

    # Can we talk about something else
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
        'score': 10.0,
        'state': 'move_on_request',

        '`Alright. `': 'SYSTEM:root'
    },

    # transition to travel
    '[{'
    '[do you, know], [have you, heard],'
    '[!#NOT(not)[{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about?]'
    '}, {travel,traveling,city,cities,vacation,vacations}]'
    '#CNC(travel)':
        'SYSTEM:travel_intro',

    # transition to pets
    '[{'
    '[do you, know], [have you, heard],'
    '[!#NOT(not)[{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about?]'
    '}, {pet,pets,animals,animal,cat,cats,dog,dogs}]'
    '#CNC(pet)':
        'SYSTEM:pet_intro',

    # transition to vr
    '[{'
    '[do you, know], [have you, heard],'
    '[!#NOT(not)[{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about?]'
    '}, {virtual reality, vr, v r,oculus,vive,rift,morpheus}]'
    '#CNC(virtual_reality) #CNC(vr_experience)':
        'SYSTEM:virtual_reality_intro',

    # transition to corona
    '[{'
    '[do you, know], [have you, heard],'
    '[!#NOT(not)[{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about?]'
    '}, '
    '{coronavirus,corona virus,'
    'covid,'
    '[{china,chinese,wuhan,global,widespread,pandemic,epidemic},{virus,disease,illness}],'
    '[{virus,disease,illness},{china,chinese,wuhan,global,widespread,pandemic,epidemic}]'
    '}]'
    '#CNC(coronavirus_op)':
        'SYSTEM:coronavirus_op_intro',

    # Do you know
    '#NOT(travel,traveling,city,cities,vacation,vacations,'
    'pet,pets,animals,animal,cat,cats,dog,dogs,'
    'coronavirus,corona virus,'
    'covid,'
    '[{china,chinese,wuhan,global,widespread,pandemic,epidemic},{virus,disease,illness}],'
    '[{virus,disease,illness},{china,chinese,wuhan,global,widespread,pandemic,epidemic}],'
    'virtual reality, vr, v r,oculus,vive,rift,morpheus)'
    '{'
    '[do you, know $topic_requested=/.*/],'
    '[have you, heard $topic_requested=/.*/]'
    '}':
        'SYSTEM:topic_switch_request',

    # Can we talk about X
    '#NOT(travel,traveling,city,cities,vacation,vacations,'
    'pet,pets,animals,animal,cat,cats,dog,dogs,'
    'coronavirus,corona virus,'
    'covid,'
    '[{china,chinese,wuhan,global,widespread,pandemic,epidemic},{virus,disease,illness}],'
    '[{virus,disease,illness},{china,chinese,wuhan,global,widespread,pandemic,epidemic}],'
    'virtual reality, vr, v r,oculus,vive,rift,morpheus)'
    '{'
    '[! #NOT(not) [{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about $topic_requested=/.+/]'
    '}':{
        'score': 9.0,
        'hop': 'True',
        'state': 'topic_switch_request',

        '[{movie,movies,film,films,tv,shows,television}]':
            'SYSTEM:movies_intro',

        '[{music,musics,tunes,song,songs,melody,melodies,album,albums,concert,concerts}]':
            'SYSTEM:music_intro',

        '[{news,politics,technology,business,events}]':
            'SYSTEM:external_news_intro',

        '[{sport,sports,basketball,football,hockey,tennis,baseball,soccer,superbowl,kobe bryant}]':
            'SYSTEM:sports_intro',

        'error':{
            'state': 'topic_switch_by_sim',

            '`I don\'t think I know anything about that, but `':{
                'hop': 'True',

                '#SBS($topic_requested, cat dog pets animals animal) `We can talk about pets instead! `':
                    'SYSTEM:pet_intro',

                '#SBS($topic_requested, sports basketball football soccer) `We can talk about other sports! `':
                    'SYSTEM:sports_intro',

                '#SBS($topic_requested, video game virtual augmented reality videogame) ` it kind of sounds like it\'s related to virtual reality. `':
                    'SYSTEM:virtual_reality_intro',

                '#SBS($topic_requested, travel vacation city state country location place) ` maybe you are interested in talking about travel plans. `':
                    'SYSTEM:travel_intro',

                '#SBS($topic_requested, movie film show television watch cinema) ` we can talk about some movies! `':
                    'SYSTEM:movies_intro',

                '#SBS($topic_requested, music song album sing dance) ` we can talk about your music interests! `':
                    'SYSTEM:music_intro',

                '#DEFAULT `it sounds interesting so I will put it on my list of things to learn more about! '
                'In the meantime, ` #SCORE(0.0)':
                    'SYSTEM:root'
            }
        }
    },

    # User dislikes emora
    '[{'
    '[{this is, you are, your, [why, {you,this}]}, #NOT(not), #ONT(_insults)],'
    '[{this is, you are, your}, #NOT(not), {difficult,hard,bad}, {talk,conversation,discuss,understand}],'
    '[{do not, dont, cannot, cant}, {talk,conversation,discuss,understand}, you],'
    '[why, you, not, {smart, intelligent, better, capable, understandable, easier}],'
    '[why, <you,not>, brain],'
    '[you, piece, {garbage,shit}],'
    '[i, {hate,dislike,not impressed,[not,like]}, you],'
    '[<{are,arent,are not},you>,#LEM(listen),me]'
    '}]':
        'backstory:user_dislikes_emora',


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

                            '#GRET': 'SYSTEM:root'
                        }
                    }
                },

                '#UNX(None)': {
                    'state': 'joke_unx',

                    '`He just needed a little space!`': 'joke_given'
                }
            }
        },

        '/.*/ #SCORE(0.9)':{
            'state': 'multi_joke',

            '`Oh, I\'m sorry. I seem to only remember the one joke I already told you. ` #GRET': 'SYSTEM:root'
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

            '#UNX': {'#GRET': 'SYSTEM:root'}
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

    # # todo - make sure no crude words are given
    # # User likes
    # '[!-#NEGATION {'
    # '[i {like, love} $user_likes=#ONT(likable)?]'
    # '}]':{
    #     '`Me too! What do you like the most about it?`': {
    #         'state': 'returning_from_global_like',
    #
    #         '#UNX': {'#GRET': 'SYSTEM:root'}
    #     }
    # },

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

    '[{do you know, remember, what, whats, tell me, ask} my name]': {
        'state': 'test_user_name',

        '`It\'s` $username `, right?`': {

            '#UNX': {

                '#GRET': 'SYSTEM:root'
            },

            '{#DISAGREE,wrong,incorrect,false,is not}': {

                '`Oh, my bad. I was so sure you were` $username `, I\'m sorry. What is your name then?`'
                '#SET($username=None)': {
                    'state': 'get_user_name',

                    '{' 
                    '[$username=#ONT(_names)], ' 
                    '[! #ONT_NEG(_names), [name, is, $username=alexa]],' 
                    '[! my, name, is, $username=alexa],' 
                    '[! {can,may,should}, call, me, $username=alexa]' 
                    '}': {

                        '$username `? I\'ll try to remember that.`': {

                            '#DISAGREE'
                            '#SET($username=None)': {
                                'state': 'cant_hear_name',

                                '`Oh no! I think I\'m having trouble getting your name right. '
                                'Sometimes I can\'t hear certain names properly through the microphone, so I hope you '
                                'don\'t take it personally.`': {

                                    '#UNX(Sorry about it.)': {'#GRET': 'SYSTEM:root'}  # expand
                                }
                            },

                            '#UNX': {'#GRET': 'SYSTEM:root'}
                        }
                    },

                    '#UNX(None)': 'cant_hear_name'
                }
            },

            '#NOT(not) [{#AGREE, it is, right, correct, true}]': {

                '`You think I wouldn\'t remember your name? Anyway,` #GRET': 'SYSTEM:root'
            }
        },

        '`Hmm. I don\'t seem to remember your name. What would you like me to call you?`'
        '#UNSET(username)':
            'get_user_name'
    }

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