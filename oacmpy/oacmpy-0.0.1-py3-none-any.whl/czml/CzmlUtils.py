from czml3 import Packet
from czml3.enums import InterpolationAlgorithms
from czml3.properties import (
    Color,
    Ellipsoid,
    Label,
    Material,
    Orientation,
    Path,
    Polyline,
    Position,
    PositionList,
    SolidColorMaterial,
)
from czml3.types import IntervalValue, TimeInterval

from ..Attitude import Attitude
from ..State import State


def format_id_name(name):
    return name.strip().replace(" ", "_")


def construct_material(solid_color):
    solid = SolidColorMaterial(color=Color.from_list(solid_color))
    return Material(solidColor=solid)


def construct_label(text_label):
    return Label(
        scale=0.7,
        horizontalOrigin="LEFT",
        text=text_label,
        show=True,
        fillColor={"rgba": [0, 255, 127, 255]},
        font="11pt Lucida Console",
        outlineColor={"rgba": [0, 0, 0, 255]},
        outlineWidth=2,
        # pixelOffset = {"cartesian2":[12,0]},
        style="FILL_AND_OUTLINE",
        # verticalOrigin = "CENTER"
    )


def add_satellite_trajectory(
    satellite_name,
    availability_interval,
    ephem,
    reference_frame,
    attitude=None,
    lead_time=None,
    trail_time=None,
    path_color=None,
):
    """

    :param satellite_name:
    :param availability_interval:
    :param ephem:
    :param reference_frame:
    :param attitude:
    :param lead_time:
    :param trail_time:
    :param path_color:
    :return:
    """
    if path_color is None:
        path_color = [0.0, 0.5, 0.9, 0.5]

    # satellite label
    label = construct_label(satellite_name)

    start_epoch, _ = ephem[0]
    end_epoch, _ = ephem[-1]

    # path to display with +/- 3000s lead/trail relative time
    interval = IntervalValue(start=start_epoch.str(), end=end_epoch.str(), value=True)
    material = construct_material(solid_color=path_color)
    path = Path(
        show=interval,
        width=2,
        resolution=120,
        material=material,
        leadTime=lead_time,
        trailTime=trail_time,
    )

    # time-positions from orekit states list
    state = [State(t, pv) for t, pv in ephem]
    cartesian_positions = [
        [
            s.get_date().duration_from(start_epoch),
            s.get_position()[0],
            s.get_position()[1],
            s.get_position()[2],
        ]
        for s in state
    ]
    flat_car_pos = [item for sublist in cartesian_positions for item in sublist]

    position = Position(
        interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
        interpolationDegree=5,
        referenceFrame=reference_frame,
        epoch=start_epoch.str(),
        cartesian=flat_car_pos,
    )

    orientation = None
    if attitude:
        att_start_epoch, _ = attitude[0]
        state = [Attitude(t, q) for t, q in attitude]
        quaternions = [
            [
                a.get_date().duration_from(att_start_epoch),
                a.get_quaternion()[0],
                a.get_quaternion()[1],
                a.get_quaternion()[2],
                a.get_quaternion()[3],
            ]
            for a in state
        ]
        flat_quat = [item for sublist in quaternions for item in sublist]
        orientation = Orientation(unitQuaternion=flat_quat, reference=None)

    packet = Packet(
        id="Satellite/" + format_id_name(satellite_name),
        name=satellite_name,
        availability=availability_interval,
        label=label,
        path=path,
        position=position,
        orientation=orientation,
    )

    return packet


def add_groundstation(station_name, station_pos, availability_interval):
    """

    :param station_name:
    :param station_pos:
    :param availability_interval:
    :return:
    """
    label = construct_label(station_name)
    position = Position(cartographicDegrees=station_pos)
    packet = Packet(
        id="Facility/" + format_id_name(station_name),
        name=station_name,
        label=label,
        availability=availability_interval,
        position=position,
    )
    return packet


def add_groundstation_visi(
    station_name, satellite_name, parent, start, end, list_visi_events, path_color=None
):
    """

    :param station_name:
    :param satellite_name:
    :param parent:
    :param availability_interval:
    :param list_visi_events: list of [start date, end date] for all n visibilities, 2 x n
    :return: czml packet
    """

    if path_color is None:
        path_color = [0.0, 1.0, 0.0, 0.8]

    availability_interval = TimeInterval(start=start, end=end)

    # We have to indicate *all* visible and invisible lines
    visi_intervals = []
    start_epoch = start
    for event in list_visi_events:
        end_epoch = event[0]
        interval = IntervalValue(start=start_epoch, end=end_epoch, value=False)
        visi_intervals.append(interval)

        start_epoch = event[0]
        end_epoch = event[1]
        interval = IntervalValue(start=start_epoch, end=end_epoch, value=True)
        visi_intervals.append(interval)
        start_epoch = end_epoch

    interval = IntervalValue(start=start_epoch, end=end, value=False)
    visi_intervals.append(interval)

    material = construct_material(solid_color=path_color)
    # this is the magic: reuse entities position
    reference = PositionList(
        references=[
            "Facility/" + station_name + "#position",
            "Satellite/" + satellite_name + "#position",
        ]
    )
    polyline = Polyline(
        show=visi_intervals,
        positions=reference,
        material=material,
        width=1,
        followSurface=False,
    )

    packet = Packet(
        id="Facility/" + station_name + "/" + satellite_name,
        name=station_name + "-" + satellite_name,
        parent=parent,
        availability=availability_interval,
        polyline=polyline,
    )
    return packet


def add_ellipsoid(
    satellite_name,
    availability_interval,
    raxis,
    entity_id=None,
    entity_name=None,
    orientation=None,
    fill_color=None,
    outline_color=None,
):
    """

    :param entity_id:
    :param entity_name:
    :param satellite_name:
    :param availability_interval:
    :param raxis:
    :param orientation:
    :param color:
    :return:
    """
    if outline_color is None and fill_color is None:
        outline_color = [255, 0, 0, 100]

    satellite_name = format_id_name(satellite_name)

    if entity_name is None:
        entity_name = satellite_name + "_Ellipsoid"

    if entity_id is None:
        entity_id = "Satellite/" + satellite_name + "/ellipsoid"

    radii = {"cartesian": raxis}
    # this is the magic: reuse entities position
    reference = Position(reference="Satellite/" + satellite_name + "#position")

    has_outline = False
    is_filled = False
    material = None
    if fill_color:
        is_filled = True
        material = construct_material(fill_color)
    if outline_color:
        has_outline = True
        outline_color = {"rgba": outline_color}

    ellipsoid = Ellipsoid(
        show=availability_interval,
        radii=radii,
        fill=is_filled,
        material=material,
        outline=has_outline,
        outlineColor=outline_color,
    )

    packet = Packet(
        id=entity_id,
        name=entity_name,
        position=reference,
        availability=availability_interval,
        ellipsoid=ellipsoid,
        orientation=orientation,
    )
    return packet


def set_attractor_ellipsoid(radii, map_image):
    """ Set the central body visual.
    Useful to set other ellipsoidal bodies such as Mars.

    :param radii:
    :param map_image: URL to the image of the projected map
    :return:
    """

    #ellipsoid = Ellipsoid(
    #    radii=radii,
    #)

    custom_props = {
        "custom_attractor": True,
        "ellipsoid": [{"array": radii}],
        "map_url": map_image,
        "scene3D": True,
    }

    return Packet(id="new_body", properties=custom_props)
