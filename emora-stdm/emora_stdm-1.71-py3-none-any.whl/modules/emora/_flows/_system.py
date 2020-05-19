
from emora_stdm import CompositeDialogueFlow

from emora_stdm.modules.emora._flows.tournament import tournament
from emora_stdm.modules.emora._flows.school import school
from emora_stdm.modules.emora._flows.baby import baby
from emora_stdm.modules.emora._flows.backstory import backstory
from emora_stdm.modules.emora._flows.competition import competition
from emora_stdm.modules.emora._flows.house import house
from emora_stdm.modules.emora._flows.reading import reading
from emora_stdm.modules.emora._flows._global_nlu import personal_nlu, global_update_rules

emora = CompositeDialogueFlow('root', 'root', 'root')
emora.component('SYSTEM').knowledge_base().load_json_file('_common.json')

components = {
    # 'component': component,
    'backstory': backstory,
    'tournament': tournament,
    'school_new': school,
    'baby': baby,
    'house': house,
    'reading': reading,
    'competition': competition
}
for namespace, component in components.items():
    emora.add_component(component, namespace)

emora.add_system_transition('root', 'tournament:start', '', score=999)
emora.add_system_transition('root', 'school_new:start', '')
emora.add_system_transition('root', 'baby:start', '')
emora.add_system_transition('root', 'house:start', '')
emora.add_system_transition('root', 'reading:start', '')
emora.add_system_transition('root', 'end', '`Oh, I have to go! Bye!`', score=-999)

for component in emora.components():
    component.load_global_nlu(personal_nlu)
    component.load_update_rules(global_update_rules)

if __name__ == '__main__':
    #emora.precache_transitions()
    emora.run(debugging=True)

