from FireSpark.protos.src.perception.proto import perception_labels_pb2 as PerceptionLabel
from FireSpark.protos.src.perception.proto import perception_labels_pb2 as PerceptionAttribute


# ==========================IMPORTANT=======================================
# this translation table is mirrored in C++ in
# "scale_label_to_perception_label_translator.cc" If you are changing a field here,
# you must ALSO change the corresponding table in the python file.
# ==========================================================================
SCALE_LABEL_TO_PERCEPTION_LABEL_MAP = {
    "car": PerceptionLabel.PERCEPTION_LABEL_CAR,
    "bus": PerceptionLabel.PERCEPTION_LABEL_BUS,
    "truck": PerceptionLabel.PERCEPTION_LABEL_TRUCK,
    "bicycle": PerceptionLabel.PERCEPTION_LABEL_BICYCLE,
    "motorcycle": PerceptionLabel.PERCEPTION_LABEL_MOTORCYCLE,
    "cyclist": PerceptionLabel.PERCEPTION_LABEL_CYCLIST,
    "motorcyclist": PerceptionLabel.PERCEPTION_LABEL_MOTORCYCLIST,
    "pedestrian": PerceptionLabel.PERCEPTION_LABEL_PEDESTRIAN,
    "animal": PerceptionLabel.PERCEPTION_LABEL_ANIMAL,
    "dontcare": PerceptionLabel.PERCEPTION_LABEL_DONTCARE,
    "traffic light": PerceptionLabel.PERCEPTION_TRAFFIC_LIGHT,
    "motorist traffic light": PerceptionLabel.PERCEPTION_TRAFFIC_LIGHT,
    "pedestrian traffic light": PerceptionLabel.PERCEPTION_LABEL_PEDESTRIAN_TRAFFIC_LIGHT,
    "other traffic light": PerceptionLabel.PERCEPTION_LABEL_OTHER_TRAFFIC_LIGHT,
    "traffic light bulb": PerceptionLabel.PERCEPTION_LABEL_TRAFFIC_LIGHT_BULB,
    "emergency vehicle": PerceptionLabel.PERCEPTION_LABEL_EMERGENCY_VEHICLE,
    "other vehicle": PerceptionLabel.PERCEPTION_LABEL_OTHER_VEHICLE,
    "road": PerceptionLabel.PERCEPTION_LABEL_ROAD,
    "sidewalk": PerceptionLabel.PERCEPTION_LABEL_SIDEWALK,
    "rail_track": PerceptionLabel.PERCEPTION_LABEL_RAIL_TRACK,
    "building": PerceptionLabel.PERCEPTION_LABEL_BUILDING,
    "infrastructure": PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    "vegetation": PerceptionLabel.PERCEPTION_LABEL_VEGETATION,
    "terrain": PerceptionLabel.PERCEPTION_LABEL_TERRAIN,
    "obscurant": PerceptionLabel.PERCEPTION_LABEL_OBSCURANT,
    "no label zone": PerceptionLabel.PERCEPTION_LABEL_NO_LABEL_ZONE,
    "road_debris": PerceptionLabel.PERCEPTION_LABEL_ROAD_DEBRIS,
    "pedestrian_accessories": PerceptionLabel.PERCEPTION_LABEL_PEDESTRIAN_ACCESSORIES,
    "static_objects": PerceptionLabel.PERCEPTION_LABEL_STATIC_OBJECTS,
    # TODO(amalhotra) : Remove below hacked classes since they dont actually exist.
    #   These are needed since DCT doesnt obey format for specified classes in request.
    #   https://jira.lyft.net/browse/AVDATA-409
    #   https://jira.lyft.net/browse/AVDATA-413
    "traffic_light": PerceptionLabel.PERCEPTION_TRAFFIC_LIGHT,
    "motorist_traffic_light": PerceptionLabel.PERCEPTION_TRAFFIC_LIGHT,
    "pedestrian_traffic_light": PerceptionLabel.PERCEPTION_LABEL_PEDESTRIAN_TRAFFIC_LIGHT,
    "other_traffic_light": PerceptionLabel.PERCEPTION_LABEL_OTHER_TRAFFIC_LIGHT,
    "traffic_light_bulb": PerceptionLabel.PERCEPTION_LABEL_TRAFFIC_LIGHT_BULB,
    "emergency_vehicle": PerceptionLabel.PERCEPTION_LABEL_EMERGENCY_VEHICLE,
    "other_vehicle": PerceptionLabel.PERCEPTION_LABEL_OTHER_VEHICLE,
    # End hacked classes
}

# ==========================IMPORTANT=======================================
# this translation table is mirrored in C++ in
# "scale_label_to_perception_label_translator.cc" If you are changing a field here,
# you must ALSO change the corresponding table in the python file.
# ==========================================================================
SCALE_LABEL_TO_ATTRIBUTES_MAP = {'parked_motorcycle': {PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_YES},
                                 'non_parked_motorcycle': {PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_NO},
                                 'parked_bicycle': {PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_YES},
                                 'non_parked_bicycle': {PerceptionAttribute.PERCEPTION_ATTRIBUTE_PARKED_NO}
                                 }

# ==========================IMPORTANT=======================================
# this translation table is mirrored in C++ in
# "scale_label_to_perception_label_translator.cc" If you are changing a field here,
# you must ALSO change the corresponding table in the python file.
# ==========================================================================
SCALE_LABEL_LIDAR_SEGMENTATION_TO_PERCEPTION_LABEL_MAP = {
    'standalone_sign': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'any_road_sign': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'motorist_traffic_light': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'pedestrian_traffic_light': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'other_traffic_light': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'parking': PerceptionLabel.PERCEPTION_LABEL_ROAD,
    'wall': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'fence': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'guardrail': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'bridge': PerceptionLabel.PERCEPTION_LABEL_BUILDING,
    'tunnel': PerceptionLabel.PERCEPTION_LABEL_BUILDING,
    'pole': PerceptionLabel.PERCEPTION_LABEL_INFRASTRUCTURE,
    'parked_motorcycle': PerceptionLabel.PERCEPTION_LABEL_MOTORCYCLE,
    'non_parked_motorcycle': PerceptionLabel.PERCEPTION_LABEL_MOTORCYCLE,
    'parked_bicycle': PerceptionLabel.PERCEPTION_LABEL_BICYCLE,
    'non_parked_bicycle': PerceptionLabel.PERCEPTION_LABEL_BICYCLE
}


def scale_label_to_lidar_segmentation_perception_label(scale_label):
    perception_label = SCALE_LABEL_LIDAR_SEGMENTATION_TO_PERCEPTION_LABEL_MAP.get(scale_label.lower())
    if perception_label is None:
        perception_label = SCALE_LABEL_TO_PERCEPTION_LABEL_MAP.get(scale_label.lower())
        if perception_label is None:
            perception_label = PerceptionLabel.PERCEPTION_LABEL_UNKNOWN
    return perception_label


def scale_label_to_perception_label(scale_label):
    perception_label = SCALE_LABEL_TO_PERCEPTION_LABEL_MAP.get(scale_label.lower())
    if perception_label is None:
        perception_label = PerceptionLabel.PERCEPTION_LABEL_UNKNOWN
    return perception_label


# Finds the PerceptionAttributes corresponding to the scale_label string.
# Returns empty unorderd_set if that scale_label doesnt have any attributes attached
# example: "parked_bicycle" -> {PERCEPTION_ATTRIBUTE_PARKED_YES}
# In Lidar segmentation, scale returns a compound label like 'parked_bicycle'
# instead of separate label and attribute. We handle it with following function.
def scale_label_to_perception_attributes(scale_label):
    perception_attributes = SCALE_LABEL_TO_ATTRIBUTES_MAP.get(scale_label.lower())
    if perception_attributes is None:
        perception_attributes = set([])
    return perception_attributes


def get_class_set(classes_str):
    classes_list = classes_str.split(",")
    classes = []
    for c in classes_list:
        classes.append(scale_label_to_perception_label(c))
    return classes
