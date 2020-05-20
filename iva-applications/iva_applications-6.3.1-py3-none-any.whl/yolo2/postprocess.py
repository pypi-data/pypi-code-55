"""Postprocessing utils for YOLO2."""
from typing import List, Dict, Tuple, Any
import numpy as np
import tensorflow as tf
from PIL import ImageDraw, ImageFont
import keras.backend as K
from iva_applications.mscoco17.config import ANCHORS, CLASS_NAMES


def scale_boxes(boxes, image_shape):
    """
    Scale boxes from output shape to original image shape.

    Parameters
    ----------
    boxes
        Boxes to scale.
    image_shape
        Original image shape.

    Returns
    -------
    Scaled boxes.
    """
    height = image_shape[0]
    width = image_shape[1]
    image_dims = K.stack([height, width, height, width])
    image_dims = K.reshape(image_dims, [1, 4])
    boxes = boxes * image_dims
    return boxes


def yolo_boxes_to_corners(box_xy, box_wh):
    """Convert boxes to corners."""
    box_mins = box_xy - (box_wh / 2.)
    box_maxes = box_xy + (box_wh / 2.)
    return K.concatenate([
        box_mins[..., 1:2],  # y_min
        box_mins[..., 0:1],  # x_min
        box_maxes[..., 1:2],  # y_max
        box_maxes[..., 0:1]  # x_max
    ])


def yolo_filter_boxes(box_confidence, boxes, box_class_probs, confidence_threshold=.5):
    """Filter boxes by confidence threshold."""
    box_scores = box_confidence * box_class_probs
    box_classes = K.argmax(box_scores, axis=-1)
    box_class_scores = K.max(box_scores, axis=-1)
    filtering_mask = box_class_scores >= confidence_threshold
    scores = tf.boolean_mask(box_class_scores, filtering_mask)
    boxes = tf.boolean_mask(boxes, filtering_mask)
    classes = tf.boolean_mask(box_classes, filtering_mask)
    return scores, boxes, classes


def yolo_head(feats, anchors, num_classes):
    """Convert final layer features to bounding box parameters.

    Parameters
    ----------
    feats : tensor
        Final convolutional layer features.
    anchors : array-like
        Anchor box widths and heights.
    num_classes : int
        Number of target classes.

    Returns
    -------
    box_xy : tensor
        x, y box predictions adjusted by spatial location in conv layer.
    box_wh : tensor
        w, h box predictions adjusted by anchors and conv spatial resolution.
    box_confidence : tensor
        Probability estimate for whether each box contains any object.
    box_class_probs : tensor
        Probability distribution estimate for each box over class labels.
    """
    num_anchors = len(anchors)
    feats = K.tf.to_float(feats)
    # Reshape to batch, height, width, num_anchors, box_params.
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
    # Dynamic implementation of conv dims for fully convolutional model.
    conv_dims = K.shape(feats)[1:3]  # assuming channels last
    # In YOLO the height index is the inner most iteration.
    conv_height_index = K.arange(0, stop=conv_dims[0])
    conv_width_index = K.arange(0, stop=conv_dims[1])
    conv_height_index = K.tile(conv_height_index, [conv_dims[1]])
    conv_width_index = K.tile(K.expand_dims(conv_width_index, 0), [conv_dims[0], 1])
    conv_width_index = K.flatten(K.transpose(conv_width_index))
    conv_index = K.transpose(K.stack([conv_height_index, conv_width_index]))
    conv_index = K.reshape(conv_index, [1, conv_dims[0], conv_dims[1], 1, 2])
    conv_index = K.cast(conv_index, feats.dtype)
    feats = K.reshape(feats, [-1, conv_dims[0], conv_dims[1], num_anchors, num_classes + 5])
    conv_dims = K.cast(K.reshape(conv_dims, [1, 1, 1, 1, 2]), K.dtype(feats))
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_xy = K.sigmoid(feats[..., :2])
    box_wh = K.exp(feats[..., 2:4])
    box_class_probs = K.softmax(feats[..., 5:])
    # Adjust preditions to each spatial grid point and anchor size.
    # Note: YOLO iterates over height index before width index.
    box_xy = (box_xy + conv_index) / conv_dims
    box_wh = box_wh * anchors_tensor / conv_dims
    return box_confidence, box_xy, box_wh, box_class_probs


def draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors):
    """Draw boxes at original image."""
    font = ImageFont.truetype(font='/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
                              size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    thickness = (image.size[0] + image.size[1]) // 300
    for index, class_id in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[class_id]
        box = out_boxes[index]
        score = out_scores[index]
        label = '{} {:.2f}'.format(predicted_class, score)
        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label, font)
        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
        print(label, (left, top), (right, bottom))
        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])
        # My kingdom for a good redistributable image drawing library.
        for j in range(thickness):
            draw.rectangle([left + j, top + j, right - j, bottom - j], outline=colors[class_id])
        draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=colors[class_id])
        draw.text(text_origin, label, fill=(0, 0, 0), font=font)
        del draw


def yolo_non_max_suppression(scores, boxes, classes, max_boxes=10, iou_threshold=0.5):
    """Non max suppression for boxes and scores."""
    nms_indices = tf.image.non_max_suppression(boxes, scores, max_boxes, iou_threshold)
    scores = K.gather(scores, nms_indices)
    boxes = K.gather(boxes, nms_indices)
    classes = K.gather(classes, nms_indices)
    return scores, boxes, classes


def yolo_eval(yolo_outputs, image_shape=(720., 1280.), max_boxes=10, confidence_threshold=.5, iou_threshold=.5):
    """Build yolo2 postprocessing graph."""
    box_confidence, box_xy, box_wh, box_class_probs = yolo_outputs
    boxes = yolo_boxes_to_corners(box_xy, box_wh)
    scores, boxes, classes = yolo_filter_boxes(
        box_confidence,
        boxes,
        box_class_probs,
        confidence_threshold=confidence_threshold)
    boxes = scale_boxes(boxes, image_shape)
    scores, boxes, classes = yolo_non_max_suppression(scores, boxes, classes,
                                                      max_boxes=max_boxes, iou_threshold=iou_threshold)
    return scores, boxes, classes


def get_spaced_colors(number):
    """Get spaced colors for drawing."""
    max_value = 255 ** 3
    interval = int(max_value / number)
    colors = [hex(ind)[2:].zfill(6) for ind in range(0, max_value, interval)]
    return [(int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)) for color in colors]


def make_graph_def(confidence_threshold: float = 0.5, iou_threshold: float = 0.5, fmap_size: int = 19) -> \
        Tuple[Any, Any, Any]:
    """
    Define yolo2 postprocessing graph.

    Parameters
    ----------
    confidence_threshold
        Confidence threshold value.
    iou_threshold
        IOU threshold value.
    fmap_size
        size of a feature map cell

    Returns
    -------
        Tensors with scores, boxes, classes.

    """
    anchors = np.array(ANCHORS)
    conv_output = tf.placeholder(
        shape=(1, fmap_size, fmap_size, 425),
        dtype='float32', name='input')
    image_shape = tf.placeholder(dtype=tf.float32, shape=[2], name='image_shape')
    yolo_outputs = yolo_head(conv_output, anchors, len(CLASS_NAMES))
    scores, boxes, classes = yolo_eval(yolo_outputs, image_shape, confidence_threshold=confidence_threshold,
                                       iou_threshold=iou_threshold)
    return scores, boxes, classes


def build_detection_graph(
        input_tensors: Dict[str, tf.placeholder],
        original_image_shape: tf.placeholder,
        class_names: List[str],
        anchors: List,
        iou_threshold: float,
        confidence_threshold: float) -> Tuple[Any, Any, Any]:
    """
    Build TensorFlow graph to postprocess yolo2 tensors.

    Parameters
    ----------
    input_tensors
        postprocessing input placeholders
    original_image_shape
        original input image's shape
    class_names
        neural network class names
    anchors
        neural network anchors
    iou_threshold
        intersection over union threshold
    confidence_threshold
        confidence threshold

    Returns TensorFlow postprocessing graph nodes
    -------
    scores tf.Tensor: scores node
    boxes tf.Tensor: boxes node
    classes tf.Tensor: classes node
    """
    input_tensors_name = list(input_tensors.keys())
    yolo_outputs = yolo_head(input_tensors[input_tensors_name[0]], anchors, len(class_names))
    scores, boxes, classes = yolo_eval(
        yolo_outputs,
        original_image_shape,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold
    )
    return scores, boxes, classes


def run_predict(sess, scores, boxes, classes, conv_output, image_shape):
    """Run inference."""
    out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes], feed_dict={
        sess.graph.get_tensor_by_name('input:0'): conv_output,
        sess.graph.get_tensor_by_name('image_shape:0'): image_shape})
    return out_scores, out_boxes, out_classes


def tpu_tensor_to_classes(tensor: np.ndarray, image_shape: tuple,
                          confidence_threshold: float = 0.5, iou_threshold: float = 0.5,
                          fmap_size: int = 19) -> tuple:
    """Convert output convolution tensor to final scores, boxes, classes."""
    graph = tf.Graph()
    sess = tf.Session(graph=graph)
    with sess.as_default():
        with graph.as_default():
            scores, boxes, classes = make_graph_def(confidence_threshold, iou_threshold, fmap_size)
    out_scores, out_boxes, out_classes = run_predict(sess, scores, boxes, classes, tensor, image_shape)
    return out_scores, out_boxes, out_classes
