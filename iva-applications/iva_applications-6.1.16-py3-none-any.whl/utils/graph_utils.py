"""Useful instruments for work with graphs."""
import os
import tensorflow as tf
from tensorflow.summary import FileWriter
from tensorflow.python.platform import gfile


def pb_to_tensorboard_event(model_filename: str, save_dir: str) -> tf.compat.v1.Event:
    """Save TF event from pb-file."""
    with tf.compat.v1.Session() as sess:
        with gfile.FastGFile(model_filename, 'rb') as read_file:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(read_file.read())
            tf.import_graph_def(graph_def)
        train_writer = tf.summary.FileWriter(save_dir)
        train_writer.add_graph(sess.graph)


def freeze_session(
        session: tf.compat.v1.Session,
        keep_var_names=None,
        output_names=None):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.

    Parameters
    ----------
    session
        The TensorFlow session to be frozen.
    keep_var_names
        A list of variable names that should not be frozen, or None to freeze all the variables in the graph.
    output_names
        Names of the relevant graph outputs.

    Returns
    -------
        The frozen graph definition.
    """
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(
            set(v.op.name for v in tf.global_variables()).difference(
                keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        for node in input_graph_def.node:
            node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
        return frozen_graph


def load_graph(graph_path: str) -> tf.Graph:
    """Load tensorflow graph from a .pb file.

    Parameters
    ----------
    graph_path : str
        Path to .pb file to load

    Returns
    -------
    tf.Graph
        Loaded graph

    Raises
    ------
    FileNotFoundError
        If graph_path doesn't exist
    """
    if not os.path.exists(graph_path):
        raise FileNotFoundError("File {} not found".format(graph_path))

    graph = tf.Graph()
    with graph.as_default():
        graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(graph_path, 'rb') as fid:
            graph_def.ParseFromString(fid.read())
            tf.import_graph_def(graph_def, name='')
    return graph


def freeze_graph_from_ckpt(
        ckpt_dir: str,
        output_node_names: str,
        to_dump: bool = False,
        tensorboad_event: bool = False) -> tf.Graph:
    """
    Extract the checkpoint files defined by the output nodes and convert all its variables into constant.

    Parameters
    ----------
    ckpt_dir
        the root folder containing the checkpoint state file
    output_node_names
        a string, containing all the output node's names, comma separated
    to_dump
        boolean flag indicates save graph to the filesystem or not
    tensorboad_event
        Set it true in case of lack of information about node's names to get tensorboard event
    Returns
    -------
        Frozen TensorFlow graph
    """
    if not tf.gfile.Exists(ckpt_dir):
        raise AssertionError(
            "Export directory doesn't exists. Please specify an export "
            "directory: %s" % ckpt_dir)

    if not output_node_names:
        print("You need to supply the name of a node to --output_node_names.")
        return -1

    # We retrieve our checkpoint fullpath
    checkpoint = tf.train.get_checkpoint_state(ckpt_dir)
    input_checkpoint = checkpoint.model_checkpoint_path

    # We clear devices to allow TensorFlow to control on which device it will load operations
    clear_devices = True

    # We start a session using a temporary fresh Graph
    with tf.Session(graph=tf.Graph()) as sess:
        # We import the meta graph in the current default Graph
        saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=clear_devices)
        if tensorboad_event:
            FileWriter(ckpt_dir, sess.graph)  # view the nodes of a meta graph

        # We restore the weights
        saver.restore(sess, input_checkpoint)

        # We use a built-in TF helper to export variables to constants
        frozen_graph = tf.compat.v1.graph_util.convert_variables_to_constants(
            sess,  # The session is used to retrieve the weights
            tf.compat.v1.get_default_graph().as_graph_def(),  # The graph_def is used to retrieve the nodes
            output_node_names.split(",")  # The output node names are used to select the usefull nodes
        )
        if to_dump:
            # We precise the file fullname of our freezed graph
            absolute_model_dir = "/".join(input_checkpoint.split('/')[:-1])
            output_graph = absolute_model_dir + "/frozen_graph.pb"
            # Finally we serialize and dump the output graph to the filesystem
            with tf.gfile.GFile(output_graph, "wb") as graph_file:
                graph_file.write(frozen_graph.SerializeToString())
            print("%d ops in the final graph." % len(frozen_graph.node))

    return frozen_graph
