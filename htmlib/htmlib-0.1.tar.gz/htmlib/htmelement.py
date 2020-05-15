class HTMLUtils:
    def getTopElements(data): ## Return a dictionary
        tops={}
class HTMLElement:
    def __init__(self,elemtype="text",content=None,properties={},children=[],parent=None,root=False):
        self.elemtype=elemtype
        self.root=root
        if elemtype=="text":
            self.content=content
        else:
            self.children=children
            self.parent=parent
            self.properties=properties
    def _uponaddtoparent(self,parent):
        self.parent=parent
    def addchild(self,child):
        self.children.append(child)
        child._uponaddtoparent(self)
    def addchildren(self,children):
        self.children+=children
        for x in children:
            x._uponaddtoparent(self)
    def getHTML(self):
        toreturn=""
        if self.elemtype=="text":
            toreturn=self.content
        else:
            toreturn="<"+self.elemtype
            for x in self.properties:
                prop=self.properties[x]
                if type(prop)==str:
                    if "'" in prop:
                        prop='"'+prop+'"'
                    else:
                        prop="'"+prop+"'"
                toreturn+=" "+x+"="+str(prop)
            toreturn+=">"
            for x in self.children:
                toreturn+=x.getHTML()
            toreturn+="</"+self.elemtype+">"
        return toreturn
    def fromHTMLText(htmltext):


