import urllib
import re
import webbrowser
from casatools import ctsys

from casashell import extra_task_modules as __extra_mods

def toolhelp( ):
    import casatools
    from casashell.private.stack_manip import find_frame
    glbl = find_frame( )
    groups = { }     
    for tname in sorted(dir(casatools)):
        if not tname.startswith('_') and tname != 'ctsys' and all( x in dir(getattr(casatools,tname)) for x in ['_info_group_','_info_desc_'] ):
            group = getattr(getattr(casatools,tname),'_info_group_')
            if group in groups:
                groups[group].append((tname,getattr(getattr(casatools,tname),'_info_group_'),getattr(getattr(casatools,tname),'_info_desc_'),getattr(casatools,tname)))
            else:
                groups[group] = [(tname,getattr(getattr(casatools,tname),'_info_group_'),getattr(getattr(casatools,tname),'_info_desc_'),getattr(casatools,tname))]

    toolnames = sorted(groups.keys())
    label_width = max(map(lambda x: len(x),toolnames)) + 1
    print("=" * (label_width + 52))
    print("CASA tools")
    for i in [t for t in toolnames]:
        last_group = ''
        for t in groups[i]:
            if t[1] != last_group:
                last_group = t[1]
                print('-' * (label_width + 52))
                print("> %s" % t[1])
                print('-' * (label_width) + '-' * 52)
            print(("%%%ds : %%s" % label_width) % (t[0].replace('\n',''),t[2].replace('\n','')))
            glbl = find_frame( )
            ctor = [x for x in glbl.keys( ) if x != 'ctsys' and glbl[x] == t[3]]
            if len(ctor) > 0:
                print(("%%%ds |    create: %%s" % label_width) % ('',", ".join(ctor)))
            inst = [x for x in glbl.keys( ) if x != 'ctsys' and isinstance(glbl[x],t[3])]
            if len(inst) > 0:
                print(("%%%ds | instances: %%s" % label_width) % ('',", ".join(inst)))
    print("-" * (label_width + 52))
    print("> singleton objects (used directly)")
    print("-" * (label_width + 52))
    print(("%%%ds : %%s" % label_width) % ('ctsys','set/get casa state'))
    print("=" * (label_width + 52))

def taskhelp( ):

    def collect(groups,module):
        for tname in sorted(dir(module)):
            if not tname.startswith('_') and tname != 'ctsys' and all( x in dir(getattr(module,tname)) for x in ['_info_group_','_info_desc_'] ):
                # split group up by group name separated by misc space and a comma
                for group in ''.join(getattr(getattr(module,tname),'_info_group_').split( )).split(','):
                    if group in groups:
                        groups[group].append((tname,group,getattr(getattr(module,tname),'_info_desc_'),getattr(module,tname)))
                    else:
                        groups[group] = [(tname,group,getattr(getattr(module,tname),'_info_desc_'),getattr(module,tname))]

    import casatasks
    groups = { }
    collect( groups, casatasks )

    try:
        import casaviewer
        collect( groups, casaviewer )
    except: pass

    try:
        import casaplotms
        collect( groups, casaplotms )
    except: pass

    extra_groups = { }
    for m in __extra_mods:
        try:
            collect( extra_groups, m )
        except: pass

    tasknames = sorted(groups.keys())
    label_width = max(map(lambda x: len(x),tasknames)) + 1
    print("=" * (label_width + 52))
    print("CASA tasks")
    for i in tasknames:
        last_group = ''
        for t in groups[i]:
            if t[1] != last_group:
                last_group = t[1]
                print('-' * (label_width + 52))
                print("> %s" % t[1])
                print('-' * (label_width) + '-' * 52)
            print(("%%%ds : %%s" % label_width) % (t[0].replace('\n',''),t[2].replace('\n','')))
    print("-" * (label_width + 52))
    print("> singleton objects (used directly)")
    print("-" * (label_width + 52))
    print(("%%%ds : %%s" % label_width) % ('casalog','add messages to the CASA log'))
    print("=" * (label_width + 52))
    if len(extra_groups) > 0:
        tasknames = sorted(extra_groups.keys())
        label_width = max(map(lambda x: len(x),tasknames)) + 1
        print("Extra tasks")
        for i in tasknames:
            last_group = ''
            for t in extra_groups[i]:
                if t[1] != last_group:
                    last_group = t[1]
                    print('-' * (label_width + 52))
                    print("> %s" % t[1])
                    print('-' * (label_width) + '-' * 52)
                print(("%%%ds : %%s" % label_width) % (t[0].replace('\n',''),t[2].replace('\n','')))
        print("=" * (label_width + 52))


class __doc(object):
    "command-line Plone help"

    def __init__( self ):

        try:
            import casalith as _casalith
            version = "%d.%d.%d" % tuple(_casalith.version( )[:3])
        except:
            version = "5.6.0"

        self.__task_url = "https://casa.nrao.edu/PloneResource/casa-" + version + "/taskXml/"
        self.__tool_url = "https://casa.nrao.edu/PloneResource/casa-" + version + "/toolXml/"
        self.__toc_url = "https://casa.nrao.edu/casadocs/casa-" + version + "/global-task-list"
        self.__start_url = "https://casa.nrao.edu/casadocs/casa-" + version

        self.__task_prefix = "https://casa.nrao.edu/casadocs/casa-" + version + "/global-task-list/task_"
        self.__tool_prefix = "https://casa.nrao.edu/casadocs/casa-" + version + "/global-tool-list/tool_"

        self.__task_list = [ ]
        self.__tool_list = [ ]

    def __call__( self, topic=None ):
        "open browser with documentation, try \"doc('toc')\""

        if len(self.__task_list) == 0:
            try:
                self.__task_list = re.findall("\w+.xml", urllib.urlopen(self.__task_url).read().decode())
            except:
                self.__task_list = [ ]

        if len(self.__tool_list) == 0:
            try:
                self.__tool_list = re.findall("\w+.xml", urllib.urlopen(self.__tool_url).read().decode())
            except:
                self.__tool_list = [ ]

        if type(topic) != str or topic == "toc":
            webbrowser.open_new_tab(self.__toc_url)
        elif topic == "start":
            webbrowser.open_new_tab(self.__start_url)
        elif topic+'.xml' in self.__task_list:
            webbrowser.open_new_tab(self.__task_prefix+topic+"/parameters")
        elif topic+'.xml' in self.__tool_list:
            webbrowser.open_new_tab(self.__tool_prefix+topic+"/methods")
        else:
            webbrowser.open_new_tab(self.__toc_url)

doc = __doc( )
del __doc
