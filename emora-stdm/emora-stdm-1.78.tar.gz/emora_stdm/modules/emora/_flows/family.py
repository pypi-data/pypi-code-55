
from _globals import PATHDIR
from emora_stdm import DialogueFlow


family = DialogueFlow('_local_start')
family.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
family.knowledge_base().load_json_file(PATHDIR.replace('__***__', 'family.json'))
family.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(family) #GOAL(family)',

    '`So you said you live with your` $sibling=#I($lives_with, #U(brother, sister)) ` right?`': {
        'state': 'sibling',

        '#UNX': { '`I always wanted an older ` $sibling `.`': 'exit' }
    },

    '`So you said you live with your` $sibling=#I($lives_with, #U(brothers, sisters)) ` right?`': {
        'state': 'siblings',

        '#UNX': { '`I always wanted older ` $sibling `.`': 'exit' }
    },
}

exit = {
    'state': 'exit',

    '#GCOM(family) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

family.load_transitions(system)
family.load_transitions(exit)
family.load_global_nlu(user)


if __name__ == '__main__':
    family.run(debugging=True)