
from _globals import PATHDIR
from emora_stdm import DialogueFlow


component = DialogueFlow('_local_start')
component.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
component.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(component) #GOAL(component)',

    '`Where would you live, if you could choose anywhere?`': {

        '[$likes_location=#ONT(_locations)]': {

            '`Oh, ` $likes_location ` would be great! I\'ve always wanted to visit.': {

                '#UNX': 'exit'
            }
        },

        '[{here, still}]': {
            'score': 1.1,

            # todo
        },

        '#IDK': {

            # todo
        },

        '#UNX': {

            # todo
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(component) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

component.load_transitions(system)
component.load_transitions(exit)
component.load_global_nlu(user)


if __name__ == '__main__':
    component.run(debugging=True)