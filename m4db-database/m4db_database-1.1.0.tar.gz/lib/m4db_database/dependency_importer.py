r"""
Tree like structure to resolve import dependencies.
"""


class DependencyImporter:
    def __init__(self, get_uid, get_puid, save_function):
        r"""
        Construct a dependency importer object.
        Args:
            get_uid: a function that will return an id for an object in list of import items.
            get_puid: a function that will return a parent id for an object in list of import items.
            save_function: a function that knows how to save an object in the list of import items.
        """
        # Add a reference to the function that will resolve unique ids.
        self.get_uid = get_uid

        # Add a reference to the function that will resolve parent unique ids.
        self.get_puid = get_puid

        # Add a reference to the function that knows how to save a data object.
        self.save_function = save_function

        # Member variables used as part of the input context are defined here.

        # Unique id to object dictionary lookup.
        self.uid_to_obj_lookup = {}

        # A list of unique ids of root object dictionaries.
        self.root_uids = []

        # An adjacency tree mapping with unique ids of parent object dictionaries as keys and lists of
        # child unique ids as children.
        self.puid_to_cuids = {}

    def initialize_context(self):
        r"""
        Function to initialize the running context of an import, it initializes the internal variables
        required when importing a list of objects.
        Returns:
            None.
        """
        # Unique id to object dictionary lookup.
        self.uid_to_obj_lookup = {}

        # A list of unique ids of root object dictionaries.
        self.root_uids = []

        # An adjacency tree mapping with unique ids of parent object dictionaries as keys and lists of
        # child unique ids as children.
        self.puid_to_cuids = {}

    def traverse(self, puid):
        r"""
        A recursive function that takes a parent unique id and saves the function associated with it. If there
        are any children associated with this puid, then they are subsequently processed.
        Args:
            puid: a unique id that is (local to the recursion) treated as a parent unique id.

        Returns:
            None.
        """
        self.save_function(self.uid_to_obj_lookup[puid])
        if puid in self.puid_to_cuids.keys():
            for cuid in self.puid_to_cuids[puid]:
                self.traverse(cuid)

    def perform_import(self, objs):
        # Initialize the import context.
        self.initialize_context()

        # Iterate though each object dict from the input object dictionaries.
        for obj in objs:
            # Get the unique id of the object dictionary.
            uid = self.get_uid(obj)

            # Get the unique id of the object dictionary's parent.
            puid = self.get_puid(obj)

            # Add the object dictionary to the lookup.
            self.uid_to_obj_lookup[uid] = obj

            # Check if the object has a parent,
            if puid is None:
                # if not then add the object's id to the list of roots,
                self.root_uids.append(uid)
            else:
                # otherwise insert an entry in the parent/child mapping.
                if puid in self.puid_to_cuids.keys():
                    self.puid_to_cuids[puid].append(uid)
                else:
                    self.puid_to_cuids[puid] = [uid]

        # Iterate through each root_uid
        for root_uid in self.root_uids:
            self.traverse(root_uid)
