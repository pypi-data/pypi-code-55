from emora._flows.tournament import tournament
from emora._flows.school import school as school2
from emora._flows.baby import baby
from emora._flows.backstory import backstory
from emora._flows.competition import competition
from emora._flows.house import house
from emora._flows.reading import reading

from _globals import PATHDIR
from emora_stdm import CompositeDialogueFlow,DialogueFlow
import emora_stdm
from emora._flows._global_nlu import personal_nlu, global_update_rules

flow_components = {
    'tournament': tournament,
    'school_new': school2,
    'baby': baby,
    'house': house,
    'reading': reading,
    'competition': competition,
    'backstory': backstory
}

cdf = CompositeDialogueFlow('root', 'recovery_from_failure', 'recovery_from_failure', DialogueFlow.Speaker.USER)
cdf.add_state('root', 'root')
cdf.component('SYSTEM').knowledge_base().load_json_file(PATHDIR.replace('__***__','_common.json'))

for namespace, component in flow_components.items():
    cdf.add_component(component, namespace)

cdf.add_system_transition('root', 'tournament:start', '')
cdf.add_system_transition('root', 'school_new:start', '#GATE(schoolv:None)')
cdf.add_system_transition('root', 'baby:start', '')
cdf.add_system_transition('root', 'house:start', '')
cdf.add_system_transition('root', 'reading:start', '')
# cdf.add_system_transition('root', 'end', '`Oh, I have to go! Bye!`', score=-999)

cdf.add_system_transition('life_opening', 'tournament:start', '')
cdf.add_system_transition('life_opening', 'school_new:start', '#GATE(schoolv:None) #SET($schoolv=True)')
cdf.add_system_transition('life_opening', 'baby:start', '')
cdf.add_system_transition('life_opening', 'house:start', '')
cdf.add_system_transition('life_opening', 'reading:start', '')
cdf.add_system_transition('life_opening', 'root', '', score=0.0)
cdf.controller().update_state_settings('life_opening', system_multi_hop=True)

for component in cdf.components():
    component.load_global_nlu(personal_nlu)
    component.load_update_rules(global_update_rules)
    component.add_macros({'CNC': emora_stdm.CheckNotComponent(cdf)})

if __name__ == '__main__':
    #emora.precache_transitions()
    cdf.run(debugging=True)