"""Postprocessing utils for YOLO3."""
from typing import Dict, Tuple, List, Any
import numpy as np
import tensorflow as tf

from PIL import Image, ImageDraw, ImageFont
from iva_applications.yolo2.postprocess import get_spaced_colors
from iva_applications.mscoco17.config import CLASS_NAMES


YOLO3_ANCHORS = [
        (10, 13), (16, 30), (33, 23),
        (30, 61), (62, 45), (59, 119),
        (116, 90), (156, 198), (373, 326)
]
TINY_YOLO3_ANCHORS = [
        (10, 14), (23, 27), (37, 58),
        (81, 82), (135, 169), (344, 319),
]

MAX_OUT_SIZE = 80


def draw_boxes(
        img: Image,
        boxes: Any,
        font: str = '/usr/share/fonts/liberation/LiberationSans-Regular.ttf') -> Image:
    """
    Draws detected boxes on a single image.

    Parameters
    ----------
    img
        Pillow image used to be drawn at
    boxes
        boxes that should be drawn (in dict or np.ndarray format)
    font
        any font
    Returns
    -------
    Pillow image with drawn boxes
    """
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=font,
                              size=(img.size[0] + img.size[1]) // 100)
    colors = get_spaced_colors(len(CLASS_NAMES))
    if isinstance(boxes, dict):
        for cls in list(boxes.keys()):
            box_ = boxes[cls]
            if np.shape(box_)[0] != 0:
                box = box_[0]
                color = colors[cls]
                xy_coords, confidence = box[:4], box[4]
                xy_coords = np.asarray([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]])
                x0_coord, y0_coord = xy_coords[0], xy_coords[1]
                thickness = (img.size[0] + img.size[1]) // 200
                for tick in np.linspace(0, 1, thickness):
                    xy_coords[0], xy_coords[1] = xy_coords[0] + tick, xy_coords[1] + tick
                    xy_coords[2], xy_coords[3] = xy_coords[2] - tick, xy_coords[3] - tick
                    draw.rectangle(xy_coords, outline=tuple(color))
                text = '{} {:.1f}%'.format(CLASS_NAMES[cls],
                                           confidence * 100)
                text_size = draw.textsize(text, font=font)
                draw.rectangle(
                    [x0_coord, y0_coord - text_size[1], x0_coord + text_size[0], y0_coord],
                    fill=tuple(color))
                draw.text((x0_coord, y0_coord - text_size[1]), text, fill='black',
                          font=font)
    elif isinstance(boxes, np.ndarray):
        confidence = 0
        for cls in range(boxes.shape[0]):
            box = boxes[cls]
            color = colors[int(box[0])]
            class_ = int(box[0])
            if box.shape[0] == 6:
                xy_coords, confidence = box[1:5], box[5]
            else:
                xy_coords = box[1:5]
            xy_coords = np.asarray([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]])
            x0_coord, y0_coord = xy_coords[0], xy_coords[1]
            thickness = (img.size[0] + img.size[1]) // 200
            for tick in np.linspace(0, 1, thickness):
                xy_coords[0], xy_coords[1] = xy_coords[0] + tick, xy_coords[1] + tick
                xy_coords[2], xy_coords[3] = xy_coords[2] - tick, xy_coords[3] - tick
                draw.rectangle([xy_coords[0], xy_coords[1], xy_coords[2], xy_coords[3]], outline=tuple(color))
            if box.shape[0] == 6:
                text = '{} {:.1f}%'.format(CLASS_NAMES[class_], confidence * 100)
            else:
                text = '{}'.format(CLASS_NAMES[class_])
            text_size = draw.textsize(text, font=font)
            draw.rectangle(
                [x0_coord, y0_coord - text_size[1], x0_coord + text_size[0], y0_coord],
                fill=tuple(color))
            draw.text((x0_coord, y0_coord - text_size[1]), text, fill='white',
                      font=font)
    else:
        raise TypeError('unsupported type of boxes %s' % type(boxes))
    img = img.convert('RGB')
    return img


def yolo_layer(inputs, n_classes, anchors, img_size):
    """
    Create Yolo final detection layer. Detect boxes with respect to anchors.

    Parameters
    ----------
    inputs
        Tensor input.
    n_classes
        Number of labels.
    anchors
        A list of anchor sizes.
    img_size
        The input size of the model.

    Returns
    -------
         Tensor output.
    """
    n_anchors = len(anchors)
    inputs = tf.placeholder(shape=inputs.shape, dtype='float32', name='detection_placeholder')
    shape = inputs.get_shape().as_list()
    grid_shape = shape[1:3]
    inputs = tf.reshape(inputs, [-1, n_anchors * grid_shape[0] * grid_shape[1],
                                 5 + n_classes])

    strides = (img_size[0] // grid_shape[0], img_size[1] // grid_shape[1])

    box_centers, box_shapes, confidence, classes = \
        tf.split(inputs, [2, 2, 1, n_classes], axis=-1)
    width = tf.range(grid_shape[0], dtype=tf.float32)
    heigth = tf.range(grid_shape[1], dtype=tf.float32)
    width_offset, heigth_offset = tf.meshgrid(width, heigth)
    width_offset = tf.reshape(width_offset, (-1, 1))
    heigth_offset = tf.reshape(heigth_offset, (-1, 1))
    x_y_offset = tf.concat([width_offset, heigth_offset], axis=-1)
    x_y_offset = tf.tile(x_y_offset, [1, n_anchors])
    x_y_offset = tf.reshape(x_y_offset, [1, -1, 2])
    box_centers = tf.nn.sigmoid(box_centers)
    box_centers = (box_centers + x_y_offset) * strides

    anchors = tf.tile(anchors, [grid_shape[0] * grid_shape[1], 1])
    box_shapes = tf.exp(box_shapes) * tf.to_float(anchors)

    confidence = tf.nn.sigmoid(confidence)

    classes = tf.nn.sigmoid(classes)

    inputs = tf.concat([box_centers, box_shapes,
                        confidence, classes], axis=-1)

    return inputs


def build_boxes(inputs):
    """Compute top left and bottom right points of the boxes."""
    center_x, center_y, width, height, confidence, classes = \
        tf.split(inputs, [1, 1, 1, 1, 1, -1], axis=-1)

    top_left_x = center_x - width / 2
    top_left_y = center_y - height / 2
    bottom_right_x = center_x + width / 2
    bottom_right_y = center_y + height / 2

    boxes = tf.concat([top_left_x, top_left_y,
                       bottom_right_x, bottom_right_y,
                       confidence, classes], axis=-1)

    return boxes


def non_max_suppression(inputs, n_classes, max_output_size, iou_threshold,
                        confidence_threshold):
    """
    Perform non-max suppression separately for each class.

    Parameters
    ----------
    inputs
        Tensor input.
    n_classes
        Number of classes.
    max_output_size
        Max number of boxes to be selected for each class.
    iou_threshold
        Threshold for the IOU.
    confidence_threshold
        Threshold for the confidence score.

    Returns
    -------
        A list containing class-to-boxes dictionaries for each sample in the batch.
    """
    batch = tf.unstack(inputs)
    boxes_dicts = []
    for boxes in batch:
        boxes = tf.boolean_mask(boxes, boxes[:, 4] > confidence_threshold)
        classes = tf.argmax(boxes[:, 5:], axis=-1)
        classes = tf.expand_dims(tf.to_float(classes), axis=-1)
        boxes = tf.concat([boxes[:, :5], classes], axis=-1)

        boxes_dict = dict()
        for cls in range(n_classes):
            mask = tf.equal(boxes[:, 5], cls)
            mask_shape = mask.get_shape()
            if mask_shape.ndims != 0:
                class_boxes = tf.boolean_mask(boxes, mask)
                boxes_coords, boxes_conf_scores, _ = tf.split(class_boxes,
                                                              [4, 1, -1],
                                                              axis=-1)
                boxes_conf_scores = tf.reshape(boxes_conf_scores, [-1])
                indices = tf.image.non_max_suppression(boxes_coords,
                                                       boxes_conf_scores,
                                                       max_output_size,
                                                       iou_threshold)
                class_boxes = tf.gather(class_boxes, indices)
                boxes_dict[cls] = class_boxes[:, :5]

        boxes_dicts.append(boxes_dict)

    return boxes_dicts


def build_detection_graph(
                output_tensors: Dict,
                input_shape: Tuple,
                class_names: List,
                anchors: List,
                iou_threshold: float,
                confidence_threshold: float):
    """Build Tiny-YOLO3 or YOLO3 tensorflow postprocessing graph for detection."""
    n_classes = len(class_names)
    keys = list(output_tensors.keys())
    if len(keys) == 2:
        detect0 = yolo_layer(output_tensors[keys[0]],
                             n_classes=n_classes,
                             anchors=anchors[3:6],
                             img_size=input_shape)
        detect1 = yolo_layer(output_tensors[keys[1]],
                             n_classes=n_classes,
                             anchors=anchors[0:3],
                             img_size=input_shape)
        output_tensors = tf.concat([detect0, detect1], axis=1)
    else:
        detect0 = yolo_layer(output_tensors[keys[0]],
                             n_classes=n_classes,
                             anchors=anchors[6:9],
                             img_size=input_shape)
        detect1 = yolo_layer(output_tensors[keys[1]],
                             n_classes=n_classes,
                             anchors=anchors[3:6],
                             img_size=input_shape)
        detect2 = yolo_layer(output_tensors[keys[2]],
                             n_classes=n_classes,
                             anchors=anchors[0:3],
                             img_size=input_shape)
        output_tensors = tf.concat([detect0, detect1, detect2], axis=1)
    raw_boxes = build_boxes(output_tensors)
    boxes_dicts = non_max_suppression(
        raw_boxes, n_classes=n_classes,
        max_output_size=MAX_OUT_SIZE,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold)
    return boxes_dicts
