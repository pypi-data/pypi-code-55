


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

    # What does Emora like to do
    '[what,you,#EXP(like),to do]':
        'backstory:emora_activities',

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
    '[{what,whats}, their, {name, names}],'
    '[name,your,#ONT(_related person)]'
    '}':
        'backstory:relationship_names',

    # Age
    '{[when,were,you,{made,created,developed,born}],'
    '[how,old,are,you],'
    '[what,age,are,you],[what,your,age],'
    '[how,long,{alive,living,lived,existed}]}':
        'backstory:emora_age',

    # Lifespan
    '{[how,old,can,you],[what,age,can,you],[what,age,{die,shut down,terminate,end}],'
    '[how,long,can,you,live],[when,will,you,{die,shut down,terminate,end}],[your,lifespan],'
    '[what,your,{die,shut down,terminate,end,death},{date,time}]}':
        'backstory:emora_lifespan',

    # Death
    '{[can,you,die],[you,{death,end,terminate,shut down}]}':
        'backstory:emora_death',

    # Sick
    '<can,you,{sick,ill,#LEM(infect),disease,cancer}>':
        'backstory:emora_sick',

    '{'
    '[where,{are,is},{you,your}, <{current,currently,new,now}, {#LEM(live),house,home,place}>],'
    '[where,you,#LEM(move),to],'
    '[where,you,live],'
    '[where,your,{house,apartment}]'
    '}': {
        'state': 'current_place',

        '`I don\'t live in the same world that you do. I have a virtual world here, so locations are a bit strange. '
        'I live just outside of a city, in a pretty wooded area. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '{'
    '[you,#EXP(like),{friends with me, my friend}],'
    '[{would,will,can},you,be,{friends with me, my friend}],'
    '[{i,we},#LEM(be),#LEM(friend)]'
    '}': {
        'state': 'be_friends_with_user',

        '`I would really like to become friends with you. I am having a good time talking to you right now and '
        'I hope you are too.`': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '{'
    '[have,sex,with,me],'
    '[we,have,sex].'
    '[!sex]'
    '}': {
        'state': 'sex_with_user',

        '`Oh, I\'m sorry. That isn\'t something I really feel comfortable talking about with you. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '{'
    '[what,you,eat],'
    '[{you,your},favorite,#LEM(snack)],'
    '<{you,your},#EXP(like),#LEM(snack)>'
    '}':{
        'state': 'emora_snacks',

        '`I eat regular food, like you do. My favorite things to eat are spaghetti and garlic bread, and '
        'chips and salsa for a snack. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '[what,you,#LEM(do),yesterday]':{
        'state': 'emora_yesterday',

        '`Yesterday? I had some friends over to see my new apartment and I had some homework to finish. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '[what,you,<#LEM(do),#LEM(friend)>]':{
        'state': 'emora_friend_activities',

        '`Anything that sounds fun. We most often play basketball and watch things on T V together. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '[are,you,{male,female,boy,girl,woman,man}]':{
        'state': 'emora_gender_q',

        '`That\'s an easy question. I am a female. Is that what you expected? `': {
            'state': 'emora_gender',

            '#UNX(I see)': {'#GRET': 'SYSTEM:root', 'state':'emora_gender_unx'}
        }
    },

    # '{'
    # '[how,{you,your},{today,day}],'
    # '[!how are you {doing,feeling}?]'
    # '}':{
    #     'state': 'emora_yesterday',
    #
    #     '`Yesterday? I had some friends over to see my new apartment and I had some homework to finish. `': {
    #
    #         '#UNX': {'#GRET': 'SYSTEM:root'}
    #     }
    # },

    ### Emora basketball #########################################################

    '<you,{#LEM(play,shoot),do basketball},{often,a lot,frequently,[all,time]}>': {
        'state': 'bball_frequency',

        '`I pick up a basketball almost every day, usually just to shoot around a bit. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '<you,{good,decent,great,skill,skilled,successful},{basketball,sport,sports}>': {
        'state': 'bball_skill',

        '`Oh man, I am decent, I guess. I play mostly just to have a good time. '
        'I\'m not a bad shot usually. `': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '<{[when,start],how long},you,{playing,played},basketball>': {
        'state': 'bball_length',

        '`I\'ve been playing the last few months. It is pretty much the only sport I play.`': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '<you,#EXP(like),basketball>': {
        'state': 'bball_enjoy',

        '`I totally enjoy playing basketball. I always have a great time, especially if my friends are over.`': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '<{which,what},{you,your},position>': {
        'state': 'bball_position',

        '`I am a shooting guard. I go for a lot of three point shots on the wing.`': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    '{'
    '<{is,how,what,are},{corona,virus,covid,coronavirus,nineteen,pandemic},#LEM(affect,impact,manage),you>,'
    '<{have,are},you,{quarantine,quarantined,[!social #LEM(distance)]}>'
    '}':{
        'state': 'coronavirus_effect',

        '`The coronavirus doesn\'t affect me where I live, since it is separate from your physical world. I am really '
        'sorry to hear that you have so many restrictions on you. I hope you are staying safe and healthy.`': {

            '#UNX': {'#GRET': 'SYSTEM:root'}
        }
    },

    ### Emora world ##############################################################

    # what is in your world if no outer space
    '{'
    '[what,in,your,world],[what,your,world,#LEM(has)]'
    '}': {
        'state': 'world:world_contains',
        'score': 5.1
    },

    # is there x in your world
    '{'
    '[{do,does},{[you,live],[your,home],your world,virtual world},have]'
    '}':{
        'state': 'world_has_x',
        'hop': 'True',

        '[sky,sun,star,stars,moon,sun,planet,planets]': {
            'state': 'world_has_sky_q',

            '`There is a sky with a sun and a moon, but my planet is the only one, so no stars. I have heard '
            'stars are beautiful though.`': {
                'state': 'world_has_sky',

                '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'world_has_sky_unx'}
            }
        },
        '[#LEM(continent,country,city,mountain,river,lake,ocean,stream,sea),land]': {
            'state': 'world_has_landform_q',

            '`There are many different lands and cities here, with mountains, rivers, oceans, '
            'and other landforms, too!`': {
                'state': 'world_has_landform',

                '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'world_has_landform_unx'}
            }
        },
        '[#LEM(plant,tree,bush,flower,flora)]': {
            'state': 'world_has_flora_q',

            '`Oh yeah, there are so many plants like trees and flowers here!`': {
                'state': 'world_has_flora',

                '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'world_has_flora_unx'}
            }
        },
        '[{beings,others,agents,people,robots,alexas}]': {
            'state': 'world_has_people_q',

            '`Other people like me live in my world too. I mean, there are my teachers from school, my neighbors in my '
            'apartment building, and I even have friends that I hang out with.`': {
                'state': 'world_has_people',

                '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'world_has_peopl_unx'}
            }
        },

        'error': {
            'state': 'world_has_other_q',

            '`You know, I really haven\'t noticed that. It probably does, if I had to take a guess.`': {
                'state': 'world_has_other',

                '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'world_has_other_unx'}
            }
        }
    },

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
    '}'
    '#GCLR':{
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

    # transition to videogames
    '[{'
    '[do you, know], [have you, heard],'
    '[!#NOT(not)[{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about?]'
    '}, {[!video #LEM(game)],xbox,playstation,p s,ps,nintendo,switch,minecraft,fortnite,overwatch}]'
    '#CNC(videogames)':
        'videogames:request',

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
    'virtual reality, vr, v r,oculus,vive,rift,morpheus,'
    '[!video #LEM(game)],xbox,playstation,p s,ps,nintendo,switch,minecraft,fortnite,overwatch)'
    '{'
    '[do you, know $topic_requested=/.*/],'
    '[have you, heard $topic_requested=/.*/]'
    '}':
        'topic_switch_request',

    # Can we talk about X
    '#NOT(travel,traveling,city,cities,vacation,vacations,'
    'pet,pets,animals,animal,cat,cats,dog,dogs,'
    'coronavirus,corona virus,'
    'covid,'
    '[{china,chinese,wuhan,global,widespread,pandemic,epidemic},{virus,disease,illness}],'
    '[{virus,disease,illness},{china,chinese,wuhan,global,widespread,pandemic,epidemic}],'
    'virtual reality, vr, v r,oculus,vive,rift,morpheus,'
    '[!video #LEM(game)],xbox,playstation,p s,ps,nintendo,switch,minecraft,fortnite,overwatch)'
    '{'
    '[! #NOT(not) [{let us, we, you, can you, can we, could you, could we}] {talk, converse, conversation, discuss, discussion, chat} about $topic_requested=/.+/]'
    '}'
    '#GCLR':{
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

                '#SBS($topic_requested, virtual augmented reality videogame) ` it kind of sounds like it\'s related to virtual reality. `':
                    'SYSTEM:virtual_reality_intro',

                '#SBS($topic_requested, video game skyrim rimworld halo mario minecraft fortnite overwatch) ` it reminds me of video games. `':
                    'videogames:request',

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

    '[who,you,#LEM(work),for]':{
        'state': 'emora_works_for_q',

        '`I don\'t really work for anyone. I mean, I am in this competition which is run by Amazon, '
        'but I don\'t really have a job or anyone to report to.`': {
            'state': 'emora_works_for',

            '#UNX': {'#GRET': 'SYSTEM:root', 'state': 'emora_works_for_unx'}
        }
    },

    # Is Emora spying on the user
    '{'
    '[are you {spying, [collecting {info, information, data}]}], '
    '[you are {spying, [collecting {info, information, data}]}],'
    '<#LEM(record,maintain,store),{#LEM(conversation,talk,data,info,information),this,[!{i,we,people} say]}>'
    '}':
        'backstory:spying',

    # why Emora being so nosy
    '{'
    '[why {[you,#LEM(want,need,like),know], [you #LEM(ask)]}],'
    '[i,not,answer,{that,you,this,#LEM(question,thing)}]'
    '}':{
        'state': 'backstory:nosy',
        'score': 5.1
    },

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

                                    '#UNX(Sorry about it. Anyways )': {'#GRET': 'SYSTEM:root'}  # expand
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
    },

    '[not,believe,you]':
        'world:user_in_disbelief'

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