import logging

from FireSpark.protos.src.perception.proto import perception_labels_pb2 as PerceptionAttribute


logger = logging.getLogger(__name__)


# ==========================IMPORTANT=======================================
# this translation file is mirrored in C++ in
# "scale_attribute_to_perception_attribute_translator.cc" If you are changing a field
# here, you must ALSO change the corresponding table in the python file.
# ==========================================================================
PARKED_ATTRIBUTE_MAP = {
    "yes": PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_YES,
    "no": PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_NO,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_UNKNOWN
}


OCCLUDED_ATTRIBUTE_MAP = {
    "0%-20%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_0_TO_20_PERCENT,
    "21%-40%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_21_TO_40_PERCENT,
    "41%-60%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_41_TO_60_PERCENT,
    "61%-80%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_61_TO_80_PERCENT,
    "0%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_0_PERCENT,
    "1%-20%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_1_TO_20_PERCENT,
}

TRUNCATED_ATTRIBUTE_MAP = {
    "0%-20%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_0_TO_20_PERCENT,
    "21%-40%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_21_TO_40_PERCENT,
    "41%-60%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_41_TO_60_PERCENT,
    "61%-80%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_61_TO_80_PERCENT,
    "0%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_0_PERCENT,
    "1%-20%": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_1_TO_20_PERCENT,
}

TRAFFIC_LIGHT_COLOR_ATTRIBUTE_MAP = {
    "red": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_RED,
    "yellow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_YELLOW,
    "green": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_GREEN,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_UNKNOWN,
    "multiple": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_MULTIPLE,
}

TRAFFIC_LIGHT_SHAPE_ATTRIBUTE_MAP = {
    "circle": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_CIRCLE,
    "left arrow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_LEFT_ARROW,
    "right arrow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_RIGHT_ARROW,
    "straight arrow":
        PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_STRAIGHT_ARROW,
    "multiple": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_MULTIPLE,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_UNKNOWN,
    "other": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_OTHER,
    # TODO(amalhotra): Remove below hacked attributes since they dont actually exist.
    # These are needed since DCT doesnt obey format for specified attributes in request.
    # https: //jira.lyft.net/browse/AVDATA-409
    # https: //jira.lyft.net/browse/AVDATA-413
    "left_arrow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_LEFT_ARROW,
    "right_arrow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_RIGHT_ARROW,
    "straight_arrow": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_STRAIGHT_ARROW,
    # End hacked attributes
}

TRAFFIC_LIGHT_DIRECTION_ATTRIBUTE_MAP = {
    "forward facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_FORWARD,
    "left facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_LEFT,
    "right facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_RIGHT,
    "backward facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_BACKWARD,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_UNKNOWN,
    "other": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_OTHER,
    # TODO(amalhotra): Remove below hacked attributes which I am adding just in case there is
    # underscore used between attribute words instead of spaces.
    "forward_facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_FORWARD,
    "left_facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_LEFT,
    "right_facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_RIGHT,
    "backward_facing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_BACKWARD,
    # End hacked attributes
}

EMERGENCY_VEHICLE_LIGHT_STATUS_ATTRIBUTE_MAP = {
    "on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_ON,
    "off": PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_OFF,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_UNKNOWN,
}

VEHICLE_ACTION_ATTRIBUTE_MAP = {
    "lane_change_left": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LANE_CHANGE_LEFT,
    "lane_change_right":
        PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LANE_CHANGE_RIGHT,
    "left_turn": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LEFT_TURN,
    "right_turn": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_RIGHT_TURN,
    "parked": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_PARKED,
    "stopped": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_STOPPED,
    "driving_straight_forward":
        PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_DRIVING_STRAIGHT_FORWARD,
    "reversing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_REVERSING,
    "u_turn": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_U_TURN,
    "loss_of_control": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LOSS_OF_CONTROL,
    "abnormal_or_traffic_violation":
        PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_ABNORMAL_OR_TRAFFIC_VIOLATION,
    "other_motion": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_OTHER_MOTION,
}

OBJECT_ACTION_ATTRIBUTE_MAP = {
    "standing": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_STANDING,
    "lying_down": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LYING_DOWN,
    "sitting": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_SITTING,
    "walking": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_WALKING,
    "running": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_RUNNING,
    "gliding_on_wheels":
        PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_GLIDING_ON_WHEELS,
    "other_motion": PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_OTHER_MOTION,
}

BLINKER_LIGHT_STATUS_ATTRIBUTE_MAP = {
    "left_on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_LEFT_ON,
    "right_on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_RIGHT_ON,
    "off": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_OFF,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_UNKNOWN,
}

BRAKE_LIGHT_STATUS_ATTRIBUTE_MAP = {
    "on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_ON,
    "off": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_OFF,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_UNKNOWN,
}

HAZARD_LIGHT_STATUS_ATTRIBUTE_MAP = {
    "on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_ON,
    "off": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_OFF,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_UNKNOWN,
}

EMERGENCY_LIGHT_STATUS_ATTRIBUTE_MAP = {
    "on": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_ON,
    "off": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_OFF,
    "unknown": PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_UNKNOWN,
}

SCALE_ATTRIBUTE_TO_PERCEPTION_ATTRIBUTE_MAP = {
        "parked": PARKED_ATTRIBUTE_MAP,
        "occluded": OCCLUDED_ATTRIBUTE_MAP,
        "truncated": TRUNCATED_ATTRIBUTE_MAP,
        "shape": TRAFFIC_LIGHT_SHAPE_ATTRIBUTE_MAP,
        "light_color": TRAFFIC_LIGHT_COLOR_ATTRIBUTE_MAP,
        "bulb_shape": TRAFFIC_LIGHT_SHAPE_ATTRIBUTE_MAP,
        "bulb_color": TRAFFIC_LIGHT_COLOR_ATTRIBUTE_MAP,
        "direction": TRAFFIC_LIGHT_DIRECTION_ATTRIBUTE_MAP,
        "lights_status": EMERGENCY_VEHICLE_LIGHT_STATUS_ATTRIBUTE_MAP,
        # TODO(amalhotra) : Remove below hacked attributes since they dont actually exist.
        # These are needed since DCT doesnt obey format for specified attributes in request.
        # https: //jira.lyft.net/browse/AVDATA-409
        # https: //jira.lyft.net/browse/AVDATA-413
        "occlusion": OCCLUDED_ATTRIBUTE_MAP,
        "truncation": TRUNCATED_ATTRIBUTE_MAP,
        # End hacked attributes
        "light_shape": TRAFFIC_LIGHT_SHAPE_ATTRIBUTE_MAP,
        "VehicleAction": VEHICLE_ACTION_ATTRIBUTE_MAP,
        "ObjectAction": OBJECT_ACTION_ATTRIBUTE_MAP,
        "BlinkerLightStatus": BLINKER_LIGHT_STATUS_ATTRIBUTE_MAP,
        "BrakeLightStatus": BLINKER_LIGHT_STATUS_ATTRIBUTE_MAP,
        "HazardLightStatus": HAZARD_LIGHT_STATUS_ATTRIBUTE_MAP,
        "emergency_light": EMERGENCY_LIGHT_STATUS_ATTRIBUTE_MAP,
}

PERCEPTION_ATTRIBUTE_TO_STRING_MAP = {
    # Parked attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_YES: "parked yes",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_NO: "parked no",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_UNKNOWN: "parked unknown",
    # Occlusion attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_0_TO_20_PERCENT: "0-20% occluded",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_21_TO_40_PERCENT: "21-40% occluded",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_41_TO_60_PERCENT: "41-60% occluded",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_61_TO_80_PERCENT: "61-70% occluded",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_0_PERCENT: "0% occluded",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OCCLUDED_1_TO_20_PERCENT: "1-20% occluded",
    # Truncation attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_0_TO_20_PERCENT: "0-20% truncated",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_21_TO_40_PERCENT: "21-40% truncated",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_41_TO_60_PERCENT: "41-60% truncated",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_61_TO_80_PERCENT: "61-70% truncated",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_0_PERCENT: "0% truncated",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRUNCATED_1_TO_20_PERCENT: "1-20% truncated",
    # Traffic light color attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_RED: "traffic light red",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_YELLOW: "traffic light yellow",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_GREEN: "traffic light green",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_MULTIPLE:
        "traffic light multiple color",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_UNKNOWN:
        "traffic light unknown color",
    # Traffic light shape attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_CIRCLE: "traffic light circle",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_LEFT_ARROW:
        "traffic light left arrow",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_RIGHT_ARROW:
        "traffic light right arrow",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_STRAIGHT_ARROW:
        "traffic light straight arrow",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_MULTIPLE:
        "traffic light multiple shape",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_UNKNOWN:
        "traffic light unknown shape",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_OTHER:
        "traffic light other shape",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_FORWARD:
        "traffic light facing forward",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_LEFT:
        "traffic light facing left",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_RIGHT:
        "traffic light facing right",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_BACKWARD:
        "traffic light facing backward",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_UNKNOWN:
        "traffic light facing unknown",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_FACING_OTHER:
        "traffic light facing other",
    # Emergency vehicle light attributes,
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_ON:
        "emergency vehicle lights status on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_OFF:
        "emergency vehicle lights status off",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_EMERGENCY_VEHICLE_LIGHTS_STATUS_UNKNOWN:
        "emergency vehicle lights status unknown",
    # Other attributes.
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_IS_STATIONARY: "stationary",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_NOT_SET: "not set",
    # Object(vehicle / pedestrian / animal) action attributes
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LANE_CHANGE_LEFT:
        "object action lane change left",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LANE_CHANGE_RIGHT:
        "object action lane change right",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LEFT_TURN: "object action left turn",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_RIGHT_TURN:
        "object action right turn",
    # Deprecated
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_MOVE_STRAIGHT:
        "object action move straight (deprecated)",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_PARKED: "object action parked",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_STOPPED: "object action stopped",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_UNKNOWN:
        "object action unknown (deprecated)",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_DRIVING_STRAIGHT_FORWARD:
        "object action driving straight forward",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_REVERSING: "object action reversing",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_U_TURN: "object action u-turn",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LOSS_OF_CONTROL:
        "object action loss of control",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_ABNORMAL_OR_TRAFFIC_VIOLATION:
        "object action abnormal or traffic violation",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_STANDING: "object action standing",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_LYING_DOWN:
        "object action lying down",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_SITTING: "object action sitting",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_WALKING: "object action walking",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_RUNNING: "object action running",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_GLIDING_ON_WHEELS:
        "object action gliding on wheels",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_OBJECT_ACTION_OTHER_MOTION:
        "object action other motion",
    # Traffic light attributes
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_LEFT_ON:
        "blinker light left on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_RIGHT_ON:
        "blinker light right on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_OFF: "blinker light off",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BLINKER_LIGHT_UNKNOWN:
        "blinker light status unknown",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_ON: "brake light on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_OFF: "brake light off",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_BRAKE_LIGHT_UNKNOWN:
        "brake light status unknown",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_ON: "hazard light on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_OFF: "hazard light off",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_HAZARD_LIGHT_UNKNOWN:
        "hazard light status unknown",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_ON:
        "emergency light on",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_OFF:
        "emergency light off",
    PerceptionAttribute.PERCEPTION_ATTRIBUTE_LIGHT_STATUS_EMERGENCY_LIGHT_UNKNOWN:
        "emergency light status unknown",
}


def scale_attributes_to_perception_attributes(attributes):
    """
    Convert list of scale attributes to perception attributes.
    Input: Dict[str, str], example:
    {
        "parked": "yes",
        "occluded": "0%-20%",
        "truncated": "0%-20%",
        "light_color": "red",
        "light_shape": "circle",
        "VehicleAction": "parked",
    }
    Output: List[PerceptionAttribute], example:
    [
        PERCEPTION_ATTRIBUTE_PARKED_YES,
        PERCEPTION_ATTRIBUTE_OCCLUDED_0_TO_20_PERCENT,
        PERCEPTION_ATTRIBUTE_TRUNCATED_0_TO_20_PERCENT,
        PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_COLOR_RED,
        PERCEPTION_ATTRIBUTE_TRAFFIC_LIGHT_SHAPE_CIRCLE,
        PERCEPTION_ATTRIBUTE_OBJECT_ACTION_PARKED,
    ]
    """
    perception_attributes = []
    for key, value in attributes.items():
        attribute = SCALE_ATTRIBUTE_TO_PERCEPTION_ATTRIBUTE_MAP.get(key)  # find "parked", "occluded", etc
        if attribute is None:
            logger.info("Cannot find attribute: {}".format(key))
            continue

        attribute_value = attribute.get(value.lower())  # use the attribute map to find the attribute value
        if attribute_value is None:
            logger.info("Cannot find attribute: {} with value: ".format(key, value))
            continue

        perception_attributes.append(attribute_value)
    return perception_attributes


def perception_attribute_to_string(attribute):
    if PERCEPTION_ATTRIBUTE_TO_STRING_MAP.get(attribute) is not None:
        return PERCEPTION_ATTRIBUTE_TO_STRING_MAP[attribute]
    return "unknown attribute"


def string_to_perception_attribute(attribute_str):
    for k, v in PERCEPTION_ATTRIBUTE_TO_STRING_MAP.items():
        if attribute_str.lower() == v:
            return k
    return PerceptionAttribute.PERCEPTION_ATTRIBUTE_NOT_SET


def get_attribute_set(attribute_str):
    attribute_list = attribute_str.split(",")
    perception_attributes = []
    for attr in attribute_list:
        perception_attributes.append(string_to_perception_attribute(attr))
    return perception_attributes
