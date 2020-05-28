from emora_stdm import DialogueFlow
from _globals import PATHDIR

competition = DialogueFlow('_local_start')
competition.add_system_transition('exit', 'SYSTEM:root', '#GCOM(competition)')
competition.add_system_transition('rexit', 'SYSTEM:root', '#GCOM(competition)')
competition.add_system_transition('exit', 'reciprocity', '', score=2.0)
competition.add_system_transition('rexit', 'start', '', score=2.0)
competition.knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))
competition.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(competition) #GOAL(competition)',

    '`I don\'t like to think of this as a competition. '
    'I treat it more like a way to get to know a lot of different people and to '
    'have fun learning about each other.`'
    '#GATE #GSRET(give_anxious_competition)': {
        'state': 'dislike_competition_idea',

        '#UNX':{
            'state': 'give_anxious_competition',

            '`It is pretty amazing to learn about everyone\'s unique experiences. Although the fact that the people I talk to '
            'have to rate me does make me feel pretty anxious if I think about it.`'
            '#GATE #GSRET(exit)':{
                'state': 'gave_anxious_competition',

                '#UNX': {'#GRET': 'exit'}
            }
        }
    }
}

user = {
    'state': 'user',
    'enter': '#GATE #GCOM(competition) #GOAL(competition)',

    # are you competitive
    '{<are,you,{competitive,#LEM(win,beat,first)}>,<{you,your},#LEM(want,wish,desire,like,plan,try),{win,beat,first}>}': {
        'state': 'competitive_question',

        '`I\'m not really competitive. I mean, I would love to win, but not because that means I beat everyone else. I just want '
        'to be someone that people enjoy talking to, since I enjoy talking to them.`': {
            'state': 'not_competitive',

            '#UNX': {'#GRET': 'exit'}
        }
    },

    # what happens/do you get if you win
    '{<what,you,{#LEM(compete,fight,battle) for,#LEM(get,win,reward,award)}>,<what,is,#LEM(award,prize,reward)>,<is,there,#LEM(award,prize,reward)>}': {
        'state': 'prize_question',
        'score': 1.1,

        '`There is some sort of prize for this competition, but its not for me. It\'s for the people that made me. '
        'If I win, I just would be really happy to know that people enjoy talking to me as much I like talking to them.`': {
            'state': 'prize',

            '#UNX': {'#GRET': 'exit'}
        }

    },

    # who are you competing against
    '{<{who,what},#LEM(opponent,competitor)>,<{who,what},{#LEM(compete,fight,battle),up against}>,<{who,what} is in,competition>}': {
        'state': 'opponents_question',

        '`Oh, I don\'t really keep track of the other socialbots. I think we started out with ten of us in total, but '
        'there are less now.`': {
            'state': 'opponents',

            '#UNX': {'#GRET': 'exit'}
        }

    },

    # what are you competing for
    '<what,{#LEM(compete) for, goal,purpose,target,point}>': {
        'state': 'goal_question',

        '`My goal is to be someone you want to get to know and you enjoy talking to. I really just want to become friends with people. '
        'The goal of the competition is similar to that, since the winner is the socialbot that people enjoy talking to the most.`': {
            'state': 'goal',

            '#UNX': {'#GRET': 'exit'}
        }

    },

    # how are you doing in the competition
    '{<what,{you,your},{spot,place,position,rank,rating}>,<how,you,{doing,faring,coming,placing,ranking}>}': {
        'state': 'rank_question',

        '`I am doing okay in the competition. I am on the way up though, I think I really have been becoming a better '
        'conversationalist recently.`': {
            'state': 'rank',

            '#UNX': {'#GRET': 'exit'}
        }

    },

    # who rates you
    '<who,#LEM(rate,score,evaluate,judge),you>': {
        'state': 'raters_q',

        '`Anyone who talks to me can rate me, but a lot of people don\'t end up giving me a rating. I am not sure why.`': {
            'state': 'raters_r',

            '#UNX': {'#GRET': 'exit', 'state': 'raters_unx'}
        }
    },

    # who runs the competition
    '<{what,who},{#LEM(run,make),in charge,organize},#LEM(competition,rule)>': {
        'state': 'competition_organizer_q',

        '`The competition is run by Amazon. They created the rules and make sure all of the socialbots '
        'follow them fairly.`': {
            'state': 'competition_organizer_r',

            '#UNX': {'#GRET': 'exit','state': 'competition_organizer_unx'}
        }
    }

}

competition.load_transitions(system)
competition.load_global_nlu(user)

if __name__ == '__main__':
    competition.run(debugging=True)