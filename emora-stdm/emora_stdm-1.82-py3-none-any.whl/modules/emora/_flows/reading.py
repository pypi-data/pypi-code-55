from _globals import PATHDIR
#from emora._flows.globals import PATHDIR
from emora_stdm import DialogueFlow


reading = DialogueFlow('_local_start')
reading.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
reading.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(reading) #GOAL(reading)',

    '`So I\'ve been taking the time to read a little bit every day, '
    'and I have to say it was slow going at first, but now I really enjoy it.`'
    '#GSRET(share_hobbit)': {
        'state': 'share_like_reading',
        'score': 2.0,

        '[i,#EXP(like),{read,reading,books,book}]': {

            '`Oh, cool! I\'m glad to find something in common. `': 'share_hobbit'
        },

        '[i,#NEGATION,#EXP(like),{read,reading,books}]': {
            'score': 1.1,

            '`I had a hard time getting into it at first too. I think the key is finding books that '
            'you really enjoy reading and can\'t put down.`'
            '#GSRET(share_hobbit)': {

                '#UNX': 'share_hobbit'
            }
        },

        'error': {
            'state': 'share_hobbit',

            '`I\'ve been reading the hobbit. I really like Bilbo. '
            'I feel like I can relate a lot to someone who gets swept up '
            'in an adventure that\'s exhilarating, but where they are forced to '
            'struggle and learn to overcome tough new challenges.`'
            '#GSRET(reciprocity)':{

                '[why]': {

                    '`I mean, I feel like I am constantly being challenged each day to learn about '
                    'the world and become a better friend. It\'s both exciting and terrifying, but '
                    'I wouldn\'t change a thing about it.`'
                    '#GSRET(reciprocity)': {

                        '#UNX': 'reciprocity'
                    }
                },

                '#UNX': 'reciprocity'
            }
        }
    },

    '`My cousin is super into reading and she started collecting baby books as soon as she found out she was expecting. '
    'I thought it was kinda weird, because I haven\'t typically enjoyed reading, but it kinda makes more sense to '
    'me now, since I just got into reading recently and its actually pretty fun!`': {
        'state': 'baby',
        'hop': 'True',
        '` `': 'share_like_reading'
    },

    '`I\'ve really been enjoying taking a book out in the afternoon and sitting under the trees in my backyard to read. '
    'It is so peaceful. I have not liked reading for a long time but have started to enjoy it a bit more. '
    'I think I was finally able to find something that is fun for me to read.`':{
        'state': 'house',
        'hop': 'True',
        '` `': 'share_like_reading'
    },

    '`One of the worst things about school for me personally is reading those textbooks for class. '
    'It is so hard to find one that isn\'t so boring you cannot keep your eyes open. Although to be fair, I haven\'t '
    'really liked reading anything until recently. It took me a while to find stuff I actually enjoy reading.`': {
        'state': 'school',
        'hop': 'True',
        '` `': 'share_like_reading'
    }
}

exit = {
    'state': 'exit',

    '#GCOM(reading)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(reading) ` `': {
        'score': 2.0,
        'state': 'reciprocity'
    },

    '#GCOM(reading) `  `': 'house:start->house:reading',

    '#GCOM(reading) `   `': 'school_new:start->school_new:reading',

    '#GCOM(reading) `    `': 'baby:start->baby:reading'
}

reciprocity = {
    'state': 'reciprocity',
    'enter': '#GATE #GCOM(reading) #GOAL(reading)',

    '`Do you have a favorite book?`': {

        '{#DISAGREE,#IDK}': {

            '`I get you.`'
            '#GSRET(rexit)':
                'rexit'
        },

        '#UNX':{

            '`Cool! What do you like about it?`'
            '#GATE': {
                'state': 'user_fave_book_quality',

                'error': {

                    '`Well I\'ll have to check it out. Maybe that will be the '
                    'second book I read once I\'m done with the hobbit!`'
                    '#GSRET(rexit)': {

                        '#UNX': 'rexit'
                    }
                }
            },

            '#DEFAULT `So, what about your favorite book has made it stand out to you so much?`': 'user_fave_book_quality'
        }
    }
}

rexit = {
    'state': 'rexit',

    '#GCOM(reading)': {
        'score': 0.0,
        'state':'SYSTEM:root'
    },

    '#GCOM(reading) ` `': {
        'score': 2.0,
        'state': 'start'
    },

    '#GCOM(reading) `  `': 'house:start->house:reading',

    '#GCOM(reading) `   `': 'school_new:start->school_new:reading',

    '#GCOM(reading) `    `': 'baby:start->baby:reading'
}

user = {
    'state': 'user',

    '[{do you know,heard of,have you read}] /.+/': {

        '`I am starting with The Hobbit, I haven\'t had the chance to read anything else. My list of books '
        'to read next is going to be so long!`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[{you,your},favorite,{[thing,read],book}]':{

        '`I guess it would have to be the Hobbit. Mostly because I haven\'t read anything else!`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '<{[lord,rings],hobbit},movie>': {

        '`I have heard there is a movie but I want to finish the book first. Then the movie is definitely '
        'going to be the next thing I watch! Don\'t give me any spoilers please!`': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '[{you,your},favorite,character]': {

        '`Probably Bilbo honestly. I just feel like I see myself in what he is going through. `': {

            '#UNX': {'#GRET': 'exit'}
        }
    },

    '{'
    '[{why,[what,mean]},slow],'
    '[what,{didnt,not},#EXP(like),{read,reading,book,books}],'
    '[what,{dislike,hate},{read,reading,book,books}]'
    '}': {

        '`I don\'t really know what it was. I feel like I read kind of slow compared to other people, '
        'which made it feel like reading took forever. '
        'But I do think it also just took me a while to find a book that I liked, you know?`': {

            '#UNX': {'#GRET': 'exit'}
        }
    }

}

reading.load_transitions(system)
reading.load_transitions(reciprocity)
reading.load_transitions(exit)
reading.load_transitions(rexit)
reading.load_global_nlu(user)


if __name__ == '__main__':
    reading.run(debugging=True)