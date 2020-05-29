from ezdnac import DnaC, Template, Device

dnac = DnaC('90.139.96.170', 'johalath', 'Avaya119')

switch = Device(dnac, sn='FCW2335A0DE')

print(switch.hostname, switch.platform)

templates = Template(dnac, all=True)

template = Template(dnac, name='VLAN_INTERFACE')
#template = Template(dnac, id='79800340-6171-412e-a47e-00b0e1624e9f')

print(template.name, template.id)
print("\r\n")
print(template.data)

