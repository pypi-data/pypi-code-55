
from emora_stdm import CompositeDialogueFlow

#from emora_stdm.modules.emora.component import component
from emora_stdm.modules.emora.pleasant_opening import opening
from emora_stdm.modules.emora.coronavirus_checkin import coronavirus_checkin
from emora_stdm.modules.emora.general_activity import df as activity
from emora_stdm.modules.emora.worklife import df as worklife
from emora_stdm.modules.emora.school import df as school

#from emora_stdm.modules.emora._flows.component import component


emora = CompositeDialogueFlow('root', 'root', 'root')

components = {
    # 'component': component,
    'pleasant_opening': opening,
    'coronavirus_checkin': coronavirus_checkin,
    'activity': activity,
    'worklife': worklife,
    'school': school
}
for namespace, component in components.items():
    emora.add_component(component, namespace)

emora.add_system_transition('root', 'pleasant_opening:start', '', score=999)
emora.add_system_transition('root', 'coronavirus_checkin:start', '')
emora.add_system_transition('root', 'end', '`Oh, I have to go! Bye!`', score=-999)

if __name__ == '__main__':
    emora.precache_transitions()
    emora.run(debugging=True)

