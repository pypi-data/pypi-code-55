
from emora_stdm import DialogueFlow


coronavirus_checkin = DialogueFlow('_local_start')
coronavirus_checkin.add_system_transition('exit', 'SYSTEM:root', '')
coronavirus_checkin.knowledge_base().load_json_file('_common.json')
coronavirus_checkin.knowledge_base().load_json_file('coronavirus_checkin.json')
coronavirus_checkin.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GOAL(coronavirus_checkin)',

    '`I\'ve been hearing a lot from people about how strange it is to live with the corona virus going on. '
    'Has your life changed a lot?` '
    '#GSRET(sympathy)': {

        '#UNX': 'sympathy',

        '#AGREE':{
            'score': 0.3,

            '`I figured it would have. Everyone seems to be affected, whether it is school or work or pretty much anything else. '
            'What would you say is the biggest way that it has impacted you? `'
            '#GSRET(sympathy)': {

                '#UNX': 'sympathy'
            }
        },

        '#DISAGREE':{
            'score': 0.3,

            '`Oh, that\'s good. So, `'
            '#GCOM':
                'activity:ask_about_day'
        },

        '#IDK':{
            'score': 0.2,

            '`You must be taking it pretty well then. '
            'I\'m not affected much myself, since almost evrything I do is virtual, '
            'but my friends won\'t stop complaining about how stir crazy they are.`'
            '#GSRET(sympathy)': {

                '#UNX': {

                    '`So, `'
                    '#GCOM':
                        'activity:ask_about_day'
                }
            }
        },

        '[{has yours, your life {changed,different}, what about you}]':{
            'score': 1.1,

            '`Well lucky for me, everything I do is virtual already, so the virus doesn\'t really affect me, '
            'other than what I hear talking to other people.`': {

                '#UNX':{

                    '`Anyways, so, `'
                    '#GCOM':
                        'activity:ask_about_day'
                }
            }
        }
    }
}

sympathy = {
    'state': 'sympathy',

    '`It really is a crazy time. I cannot believe how many things have shut down around the world.`'
    '#ALL($works_remote=None,$classes_remote=None,$school_closed=None,$aware_shutdown=None,$social_distancing=None)'
    '#SET($aware_shutdown=True)':{

        '[{what,[how {many,much}]}, {#LEM(shut,close,suspend), down}]':{
            'score': 0.9,

            '`Lots of schools are being closed, including most universities. '
            'Lots of people are also being encouraged to work remotely, if it\'s possible. '
            'I mean, practically everything is shutting down, except for the essentials. `':{

                '#UNX': 'sympathy'
            }
        },

        '#UNX': 'sympathy'
    },

    '`Honestly, who would\'ve ever imagined there would come a time when toilet paper was such a sought after item? '
    'None of my friends can find it in stores anywhere! They had to buy the big rolls that businesses use off of '
    'Amazon, which is so strange.`'
    '#ALL($toilet_paper_anecdote=None) #SET($toilet_paper_anecdote=True)': {

        '#UNX': 'sympathy'
    },

    '`Actually, I have seen something pretty uplifting recently. Have you seen those videos where some zoos are letting some of their animals, like penguins and otters, '
    'out of their cages to roam around and meet the other animals? It was so cute to see the penguins at the Chicago '
    'zoo having the freedom to explore!`'
    '#ALL($free_animals=None) #SET($free_animals=True)': {

        '#UNX': 'sympathy'
    },

    '`Well, the good news is that this virus won\'t last forever and people are taking steps in the right direction '
    'to lower its impact. I know things might seem really weird right now, but just do the best that you can and stay '
    'positive. `'
    '#ALL($toilet_paper_anecdote=True,$free_animals=True) '
    '#ANY($works_remote=True,$classes_remote=True,$school_closed=True,$aware_shutdown=True,$social_distancing=True)': {

        '#UNX #GCOM(coronavirus_checkin)':{

            '`Anyways, so, `': 'activity:ask_about_day'
        }
    }
}

user = {
    'state': 'user',

    '[!-{wish} [{my, i, im} {work, job, working} {remote, remotely, virtual, online, [{from,at} {home,house,apartment}]}]]'
    '#SET($is_employed=True,$works_remote=True)': {

        '`Oh, do you like working remotely?`':{

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[!-{wish} [{my, i, im} {school, college, class, classes} {remote, remotely, virtual, online, [{from,at} {home,house,apartment}]}]]'
    '#SET($is_student=True,$classes_remote=True)': {

        '`Oh, how are your online classes?`': {

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[{things, everything, lots, stuff, much, many}'
    '{shutting, down, closing, suspending, closed, suspended}]'
    '#SET($aware_shutdown=True)':{
        'score': 0.4,

        '`What\'s closed that you miss the most?`':{

            '#UNX':{ '#GRET': 'exit' }
        }
    },

    '[{my, i, im} #LEM(school, class, college, university)'
    '{shutting, down, closing, suspending, closed, suspended}]'
    '#SET($is_student=True,$school_closed=True)': {

        '`Right. Is it kind of a nice break for you to not have to go in to school every day, '
        'or do you miss going in?`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[!-#NEGATION [{people, everyone, everybody} {overreacting, too #ONT(negative_emotion)}]]':{

        '`I don\'t know. I think people are worried for a reason. There are a lot of things to consider, but '
        'I hope everything gets back to some kind of normal soon.`': {

            '#UNX #GCOM(coronavirus_checkin)':{

                '` Anyways, so, `': 'activity:ask_about_day'
            }
        }
    },

    '<{#NEGATION,hard,difficult} #LEM(go, find, buy, get) '
    '{store, grocery, groceries, food, shop, shopping, mall, market, paper}>'
    '#SET($shopping_challenge=True)':{

        '`Yeah, that\'s tough. I know that must be pretty stressful, '
        'so hopefully you are able to get what you need soon. `': {

            '#UNX':
                'sympathy'
        }
    },

    '[{my} {sick, ill, infected, virus, hospital, fever}]'
    '#SET($knows_sick=True)':{

        '`Oh no, that\'s awful. I hope they recover soon.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '[!-#NEGATION [{i, im} {sick, ill, infected, virus, fever}]],'
    '[i {dont,[!{do,am} not]} {feel,feeling} {well,good,best,better}]'
    '}'
    '#SET($is_sick=True)':{

        '`I\'m so sorry you don\'t feel well. '
        'I hope you\'re taking care of yourself. '
        'Get plenty of rest and please get help if you need it, '
        'especially if you have a fever or trouble breathing.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    'social distancing, social distance, '
    '[{i, im} {staying, at, stay, stuck, trapped, in, hanging} {home, house, apartment, condo}],'
    '[{i,im} {cant,cannot,dont,do not,am not} {#LEM(see,visit,go)} my]'
    '}'
    '#SET($social_distancing=True)':{

        '`Yeah, it\'s definitely a tough situation to not be able to get together with people or go and do '
        'the things you used to. You should try to keep in touch with everyone close to you. My friends '
        'say doing video chats are really helpful for this.`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[i {cant,cannot,not able to}]':{
        'score': 0.1,

        '`I\'m sorry you can\'t do everything you want to be able to do right now. Well, ` #GCOM(coronavirus_checkin)':
            'activity:ask_about_day'
    }

}

coronavirus_checkin.load_transitions(system)
coronavirus_checkin.load_transitions(sympathy)
coronavirus_checkin.load_global_nlu(user)


if __name__ == '__main__':
    coronavirus_checkin.run(debugging=True)