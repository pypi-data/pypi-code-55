import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Command and Control'
        self.tid = 'T1043'
        self.name = 'Commonly Used Port'
        self.description = '''Communicates with C&C over commonly used ports'''

    def run_rules(self, bundles):
        cnt = 0
        common_ports = {
            20: "ftp", 
            21: "ftp", 
            22: "ssh", 
            23: "telnet", 
            25: "smtp", 
            50: "ipsec", 
            51: "ipsec", 
            53: "dns", 
            67: "dhcp", 
            68: "dhcp", 
            69: "tftp", 
            80: "http", 
            8080: "http", 
            110: "pop3", 
            119: "nntp", 
            123: "ntp", 
            135: "netbios", 
            136: "netbios", 
            137: "netbios", 
            138: "netbios", 
            139: "netbios", 
            143: "imap4", 
            161: "snmp", 
            162: "snmp", 
            389: "ldap", 
            443: "https",
            445: "smb", 
            3389: "rdp",
            1433: "sql",
            1434: "sql"
        }
        for entry in bundles['objects']:
            if entry['type'] == 'observed-data':
                objects = entry['objects']
                for obj_data in objects:
                    if objects[obj_data]['type'] == 'network-traffic':
                        if objects[obj_data]['dst_port'] in common_ports:
                            observ_ref = entry['created_by_ref']
                            break
                else:
                    observ_ref = False
                if observ_ref != False:
                    for o_r in bundles['objects']:
                        if o_r['type'] == 'relationship':
                            #get the id of indicator that Dcom created process
                            if o_r['source_ref'] == observ_ref and o_r['relationship_type'] == 'related-to':
                                s_id = o_r['target_ref']
                                break
                    else:
                        s_id = False
                    if s_id != False:
                        for o_i in bundles['objects']:
                            if o_i['id'] == s_id and o_i['type'] == 'indicator':
                                self.oid.append(o_i['id'])
                                cnt += 1
                                break               
        if cnt != 0:
            return self
        else:
            return False