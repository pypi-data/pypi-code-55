import inspect, json, sys
from node import Node
from variable import Variable, Credentials, Enum


class NodeSpec:
    def __init__(self, id: str, icon: str='', name: str='', color: str='', inputs: int=0, outputs: int=0):
        self.id = id
        self.icon = icon
        self.name = name
        self.color = color
        self.inputs = inputs,
        self.inputs = self.inputs[0]
        self.outputs = outputs,
        self.outputs = self.outputs[0]
        self.properties = []


class Property:
    def __init__(self, schema):
        self.schema = schema
        self.formData = {}
        self.uiSchema = {}


class Schema:
    def __init__(self, type: str, title: str):
        self.type = type
        self.title = title
        self.properties = {}


class SProperty:
    type = ''
    title = ''
    subtitle = None
    category = None
    properties = None
    csScope = None
    jsScope = None
    customScope = None
    messageScope = None
    multiple = None
    variableType = None
    enum = []
    enumNames = []


class VarDataProperty:
    def __init__(self, name: str, scope: str):
        self.scope = scope
        self.name = name


class Spec:
    @staticmethod
    def generate(plugin_name, version):
        frm = inspect.stack()[2]
        mod = inspect.getmodule(frm[0])
        clsmembers = inspect.getmembers(sys.modules[mod.__name__], inspect.isclass)
        nodes = []

        for c in clsmembers:
            cls = c[1]
            if issubclass(cls, Node) and cls is not Node:
                id = cls().id
                name = cls().name

                spec = NodeSpec(id=id, name=name, inputs=1, outputs=1)  # FIX

                inProperty = Property(schema=Schema(title='Input', type='object'))
                outProperty = Property(schema=Schema(title='Output', type='object'))
                optProperty = Property(schema=Schema(title='Option', type='object'))

                inProperty.uiSchema['ui:order'] = []
                outProperty.uiSchema['ui:order'] = []
                optProperty.uiSchema['ui:order'] = []

                props = []
                fields = cls().cls().__dict__
                for key in fields.keys():
                    val = fields[key]
                    if hasattr(val, 'title') and isinstance(val.title, str):
                        title = val.title
                        sProp = SProperty()

                        isVar = isinstance(val, Variable)
                        isCred = isinstance(val, Credentials)
                        isEnum = isinstance(val, Enum)

                        if isVar:
                            sProp.type = 'object'
                            sProp.variableType = Spec.get_variable_type(val)
                            sProp.properties = {'scope': {'type': 'string'}, 'name': {'type': 'string'}}
                        elif isCred:
                            sProp.type = 'object'
                            sProp.subtitle = 'Credentials'
                            sProp.category = val.category
                            sProp.properties = {'vaultId': {'type': 'string'}, 'itemId': {'type': 'string'}}
                        elif isEnum:
                            sProp.type = val.type
                            sProp.enum = val.enum
                            sProp.enumNames = val.enumNames
                            sProp.multiple = True

                        else:
                            sProp.type = Spec.get_variable_type(val).lower()

                        if hasattr(val, 'csScope'):
                            sProp.csScope = True
                        if hasattr(val, 'customScope'):
                            sProp.customScope = True
                        if hasattr(val, 'jsScope'):
                            sProp.jsScope = True
                        if hasattr(val, 'messageScope'):
                            sProp.messageScope = True

                        lower_name = Spec.lower_first_letter(key)
                        if lower_name.startswith('in'):  # input
                            inProperty.schema.properties[lower_name] = sProp
                            inProperty.uiSchema['ui:order'].append(lower_name)

                            if isVar:
                                inProperty.formData[lower_name] = VarDataProperty(name=val.name, scope=val.scope)
                                inProperty.uiSchema[lower_name] = {'ui:field': 'variable'}
                            elif isCred:
                                inProperty.uiSchema[lower_name] = {'ui:field': 'credentials'}
                            else:
                                inProperty.formData[lower_name] = val.value

                        elif lower_name.startswith('out'):  # output
                            outProperty.schema.properties[lower_name] = sProp
                            outProperty.uiSchema['ui:order'].append(lower_name)

                            if isVar:
                                outProperty.formData[lower_name] = VarDataProperty(name=val.name, scope=val.scope)
                                outProperty.uiSchema[lower_name] = {'ui:field': 'variable'}
                            elif isCred:
                                outProperty.uiSchema[lower_name] = {'ui:field': 'credentials'}
                            else:
                                outProperty.formData[lower_name] = val.value

                        elif lower_name.startswith('opt'):  # option
                            optProperty.schema.properties[lower_name] = sProp
                            optProperty.uiSchema['ui:order'].append(lower_name)

                            if isVar:
                                optProperty.formData[lower_name] = VarDataProperty(name=val.name, scope=val.scope)
                                optProperty.uiSchema[lower_name] = {'ui:field': 'variable'}
                            elif isCred:
                                optProperty.uiSchema[lower_name] = {'ui:field': 'credentials'}
                            else:
                                optProperty.formData[lower_name] = val.value

                if len(inProperty.schema.properties) > 0:
                    props.append(inProperty)
                if len(outProperty.schema.properties) > 0:
                    props.append(outProperty)
                if len(optProperty.schema.properties) > 0:
                    props.append(optProperty)

                spec.properties = props
                nodes.append(spec)

        js = json.dumps({'nodes': Spec.cleandict(nodes), 'name': plugin_name, 'version': version}, default=lambda o: o.__dict__)
        print(js)

    @staticmethod
    def cleandict(d):
        if not isinstance(d, dict):
            return d
        return dict((k, Spec.cleandict(v)) for k, v in d.iteritems() if v is not None)

    @staticmethod
    def jsonKeys2int(x):
        if isinstance(x, dict):
            return {int(k): v for k, v in x.items()}
        return x

    @staticmethod
    def get_variable_type(val) -> str:
        if isinstance(val, Variable):
            return Spec.upper_first_letter(val.type)

        return 'String'

    @staticmethod
    def lower_first_letter(text: str) -> str:
        if len(text) < 2:
            return text.lower()
        return text[:1].lower() + text[1:]

    @staticmethod
    def upper_first_letter(text: str) -> str:
        if len(text) < 2:
            return text.upper()
        return text[:1].upper() + text[1:]
