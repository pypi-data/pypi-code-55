from strix import value_validation as vv

__all__ = ["valid_geom_types", "GCA"]

valid_geom_types = ('PT', 'LS', 'POLY')


class GCA:
    """
    Creates a GCA Object

    Attributes
    ----------
    geometry_type : str
        GCA object's geometry type - 'PT', 'LS', 'POLY'
    headers : list of str
        Headers that describe the attributes of each feature in GCA object
    attributes : collection
        The attributes of the GCA object
    coord_sets : collection
        The coordinate sets of the GCA object
    features : collection
        Produces ([Attributes], [Coordinates]) for each feature in GCA object
    """

    def __init__(self, geom_type, coords, attrs):
        """
        Initialises a GCA object

        Parameters
        ----------
        geom_type : str
            One of the valid geometry types - 'PT', 'LS', 'POLY'
        coords : collection
            Coordinates of features
        attrs : collection
            2D list of attributes

        """

        if geom_type not in valid_geom_types:
            raise ValueError(f"'{geom_type}' is not a valid geometry type")
        else:
            self.geometry_type = geom_type

        self.headers = attrs[0]
        self.attributes = attrs[1:]
        self.coord_sets = coords
        self.coord_set_depth()
        self.valid_coordinates()
        self.header_attribute_match()
        self.attribute_row_for_every_feature_check()
        # Min coord set check
        self.features = list(zip(self.attributes, self.coord_sets))

    def __repr__(self):
        return "Point()"

    def __str__(self):
        description = f"'{self.geometry_type}' GCA object containing {len(self)} feature(s) with the following attributes: {self.headers}"
        return description

    def __len__(self):
        """
        Counts the number of features contained within the GCA object.

        Returns
        -------
        count : int
            The number of features contained within the GCA object.

        """

        count = len(self.features)

        return count

    def coord_set_depth(self):
        """
        Determines if the provided coordinate sets are of the correct depth for the specified geometry type

        Returns
        -------
        bool

        """

        def list_assert(obj, geom_type, is_list=True):
            """
            Asserts that provided object is a list for determining if the provided coordinate sets are of the correct depth for the specified geometry type

            Parameters
            ----------
            obj : collection
            geom_type : str
            is_list : bool

            Returns
            -------
            bool

            """

            message = f"Depth of the provided coordinate sets is invalid for expected geometry type of '{geom_type}'"
            if is_list is True:
                assert isinstance(obj, list), message
            if is_list is False:
                assert not isinstance(obj, (list, tuple, dict, set)), message

        def pt_coord_depth():
            for pt in self.coord_sets:
                list_assert(pt, self.geometry_type)
                for coord in pt:
                    list_assert(coord, self.geometry_type, False)

            return True

        def ls_coord_depth():
            for ls in self.coord_sets:
                list_assert(ls, self.geometry_type)
                for coord_set in ls:
                    list_assert(coord_set, self.geometry_type)
                    for coord in coord_set:
                        list_assert(coord, self.geometry_type, False)

            return True

        def poly_coord_depth():
            for poly in self.coord_sets:
                list_assert(poly, self.geometry_type)
                for ring in poly:
                    list_assert(ring, self.geometry_type)
                    for coord_set in ring:
                        list_assert(coord_set, self.geometry_type)
                        for coord in coord_set:
                            list_assert(coord, self.geometry_type, False)

            return True

        if self.geometry_type == 'PT':
            pt_coord_depth()
        elif self.geometry_type == 'LS':
            ls_coord_depth()
        elif self.geometry_type == 'POLY':
            poly_coord_depth()
        else:
            raise ValueError(f"'{self.geometry_type}' is not a valid geometry type")

        return True

    def valid_coordinates(self):
        """
        Tests if provided coordinate values are valid as decimal degrees and that there are 3 coordinates per set.

        Returns
        -------

        """

        def coordinate_set_len(coord_set, extend=True):
            assert len(coord_set) <= 3, f"Coordinate sets cannot have more than 3 coordinate values. {len(coord_set)} given {coord_set}"

            if extend is True:
                if len(coord_set) < 3:
                    x = [0] * (3 - len(coord_set))
                    coord_set.extend(x)
            else:
                assert len(coord_set) == 3, f"Coordinate sets are required to have 3 coordinate values. {len(coord_set)} given {coord_set}"

            return coord_set

        def pt_coordinates():
            for pt in self.coord_sets:
                pt = coordinate_set_len(pt)
                for coord in pt:
                    vv.decimal_degree_validate(coord)

            return True

        def ls_coordinates():
            for ls in self.coord_sets:
                for coord_set in ls:
                    coord_set = coordinate_set_len(coord_set)
                    for coord in coord_set:
                        vv.decimal_degree_validate(coord)

            return True

        def poly_coordinates():
            for poly in self.coord_sets:
                for ring in poly:
                    for coord_set in ring:
                        coord_set = coordinate_set_len(coord_set)
                        for coord in coord_set:
                            vv.decimal_degree_validate(coord)

            return True

        if self.geometry_type == 'PT':
            pt_coordinates()
        elif self.geometry_type == 'LS':
            ls_coordinates()
        elif self.geometry_type == 'POLY':
            poly_coordinates()
        else:
            raise ValueError(f"'{self.geometry_type}' is not a valid geometry type")

    def header_attribute_match(self):
        header_len = len(self.headers)

        for attr in self.attributes[1:]:
            attr_len = len(attr)
            assert attr_len == header_len, f"Headers have {header_len} attributes. Provided feature has {attr_len} attributes. Both need to match. Feature attributes: {attr}"

    def attribute_row_for_every_feature_check(self):
        attr_records = len(self.attributes)
        features = len(self.coord_sets)

        assert attr_records == features, f"There are {attr_records} attribute rows for {features} features. Both need to match."
