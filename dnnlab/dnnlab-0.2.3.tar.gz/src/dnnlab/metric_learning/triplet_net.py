# Copyright 2019 Kevin Hirschmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import logging
import os
import time
from datetime import datetime
import numpy as np
import io

import tensorflow as tf 

from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError
from dnnlab.losses.triplet_net.triplet_loss import TripletBatchHardLoss, SimilarityLoss, OverallSimilarityLoss
from dnnlab.metric_learning.similarity_attention import SimilarityAttention

import dnnlab.metric_learning.utils as utils

import matplotlib.pyplot as plt


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class Encoder(tf.keras.Model):
    """Encoder for the Triplet Network.

    Typical usage example:
    
    feature_extractor -> keras.model (pretrained or from scratch) /
                         output of feature_extractor should be a 4-D tensor
                         e.g. a fully convolutional network

    """


    def __init__(self, feature_extractor: tf.keras.Model, normalize='l2'):
        """
        Encoder, where output features will be regularized for the use of triplet learning.

        Attributes:
            feature_extractor (keras.model): Basic nn encoder/feature extractor, output must be a 4-D tensor of [batch_size, h, w, c]
            normalize (string): determine which Regularization should be used, default is L2-regularization
        """
        super(Encoder, self).__init__()
        self.feature_extractor = feature_extractor
        self.pooling = tf.keras.layers.GlobalAveragePooling2D()
        self.normalize = normalize        


    def call(self, inputs):
        """Forward path of Encoder.

        Args:
            inputs (tf.tensor): input tensor of [batch_size, h, w, c]

        Returns:
            y (tf.tensor): 2-D feature vectors [batch_size, num_features]

        Raises:
            ValueError: if shape of output feature vectors is not 2-D
        """
        features = self.feature_extractor(inputs)
        y = self.pooling(features)
        if self.normalize == 'l2':
            y = tf.math.l2_normalize(y, axis=1)

        if len(y.shape) != 2:
            raise ValueError('Output of Encoder has to be Feature Vectors - 2D tensor!')

        return y


    def extract_features(self, inputs):
        """Forward path of Encoder for feature map extraction.

        Args:
            inputs (tf.tensor): input tensor of [batch_size, h, w, c]

        Returns:
            y (tf.tensor): 2-D feature vectors [batch_size, num_features]
            feature (tf.tensor): 4-D feature maps [batch_size, h, w, c] of last convolutional layer du
        """
        features = self.feature_extractor(inputs)
        y = self.pooling(features)
        if self.normalize == 'l2':
            y = tf.math.l2_normalize(y, axis=1)

        return y, features



class TripletNet:
    """Triplet Network.
    """


    def __init__(self, model: tf.keras.Model, loss_fn='online', margin=0.1, doSimAtt=False, sim_threshold=1e-3):
        """TripletNetwork, where we have 3 sub networks with shared weight -> 1 network with multiple inputs

        Args:
            model (keras.Model): encoder
            loss_fn (string): determine if "standard" or "online" triplet loss will be used
            margin (float): threshold used in triplet loss functions
            doSimAtt (boolean): dettermine if SimilarityAttention is performed
        """
        self.model = model

        # OnlineTripletLoss or TripletLoss
        if loss_fn == 'online':
            self.triplet_loss = TripletBatchHardLoss(margin=margin) #
            self.similarity_loss = SimilarityLoss()
            self.overall_similarity_loss = OverallSimilarityLoss()
        else: 
            self.triplet_loss = TripletLoss(margin=margin)
           

        # learning similiarity attention
        print("Similarity Attention Learning: ", doSimAtt)
        if doSimAtt:
            self.simAtt = SimilarityAttention(encoder=self.model, alpha=0.5, beta=0.5)
            self.doSimAtt = doSimAtt
        else:
            self.doSimAtt = doSimAtt

        
        self.optimizer = None
        self.init_timestamp = "TripletNet-" + datetime.now().strftime("%dm%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None

        self.metrics = Metrics()
        self.sim_threshold = sim_threshold

        self.mined_triplets = None # store current mined triplets


    def summary(self):
        return self.model.summary()

    def predict(self):
        pass

    def compile(self, optimizer="adam", lr=1e-4):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): Optimizer. Defaults to "adam".
            lr (Float, optional): Learning rate. Defaults to 1e4.
        """

        if optimizer == "adam":
            self.optimizer = tf.keras.optimizers.Adam(lr)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(optimizer=self.optimizer,
                                                  model=self.model)
            self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                           self.ckpt_dir,
                                                           max_to_keep=5)

    def fit(self,
            training_data,#
            validation_data,#
            epochs,#
            batch_size,#
            len_dataset,#
            save_ckpt=5,#
            verbose=1,#
            max_outputs=2,
            initial_step=0,#
            mlflow=False):
        """Train model for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            training_data (tf.dataset): tf.Dataset with
                shape(None, width, height, depth).
            validation_data (tf.dataset): tf.Dataset with
                shape(None, width, height, depth).
            epochs (int): Number of epochs.
            batch_size (int): Batch length.
            save_ckpt (int): Save ckpts every n Epochs.
            verbose (int, optional): Keras Progbar verbose lvl. Defaults to 1.
            max_outputs (int, optional): Number of images shown in TB.
                Defaults to 2.
            initial_step (int, optional): Initial step for tb output.
            mlflow(bool, optional): Tracks validation loss as metric.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """
        if self.optimizer is None:
            raise ModelNotCompiledError("use compile() first.")
        if mlflow:
            import mlflow

        # Retrace workaround @function signature only tensors.
        step = tf.Variable(initial_step, name="step", dtype=tf.int64)

        num_batches = len_dataset / batch_size
        print("Num Batches: ", num_batches)

        # Keras Progbar
        progbar = tf.keras.utils.Progbar(target=num_batches, verbose=verbose)

        file_writer = tf.summary.create_file_writer(self.tensorboard)
        eval_file_writer = tf.summary.create_file_writer(
            os.path.join(self.tensorboard, "eval"))
        file_writer.set_as_default()

        for epoch in range(epochs):
            step_float = 1
            start = time.time()
            i = 0
            for elements in training_data:
                print("Train Iteration per Batch: ", i)
                i+=1

                images = elements[0]
                labels = elements[1]

                #TODO: tb_predction, tb_label
                prediction, loss, selected_triplets, all_triplet_att_images = self.train_step(
                    inputs=images, targets=labels, 
                    batch_size=batch_size, step=step,
                    file_writer=file_writer)

                tb_normal, tb_attention = self.prediction_to_tensorboard(normal_triplets=selected_triplets, 
                                                                        att_triplets=all_triplet_att_images)

                with file_writer.as_default():
                    tf.summary.scalar("train_loss_simAtt_" + str(self.doSimAtt), loss, step=step)
                    tf.summary.image("normal", tb_normal, step=step)
                    tf.summary.image("attention", tb_attention, step=step)
                
                # update Keras Progbar
                progbar.update(current=(step_float))
                step_float += 1
                step.assign(step + 1)

            # Save the model every n epochs
            if (epoch + 1) % save_ckpt == 0:
                ckpt_save_path = self.ckpt_manager.save()
                print("\nSaving checkpoint for epoch {} at {}".format(
                    epoch + 1, ckpt_save_path))

            print(" - Epoch {} finished after {} sec".format(
            epoch + 1, int(time.time() - start)))


            # Validation epoch
            print("Start validation loop...")

            val_loss, val_metrics, val_tb_prediction = self.evaluate(dataset=validation_data, file_writer=eval_file_writer, step=step,
                                            threshold=self.sim_threshold)
            
            # TODO: prediction to tensorboard of images
            

            with eval_file_writer.as_default():
                # Todo into same graph in tb. Verbose lvl
                tf.summary.scalar("val_loss_simAtt_" + str(self.doSimAtt), val_loss, step=step)
                tf.summary.scalar("val mAP", val_metrics['mAP'], step=step)

                
            eval_file_writer.flush()

            #TODO: integrate MLFLOW
            # if mlflow:
            #     # Convert to native python type (db).
            #     mlflow.log_metric("val_loss",
            #                       val_loss.numpy().item(),
            #                       step=step_float)




    def restore(self, ckpt_path):
        """Restore model weights from the latest checkpoint.

        Args:
            ckpt_path (str): Relative path to ckpt files.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """

        restore_path = os.path.dirname(ckpt_path)
        self.logdir = restore_path
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        if self.ckpt_manager is None:
            raise ModelNotCompiledError("use compile() first.")
        self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                       self.ckpt_dir,
                                                       max_to_keep=5)
        # if a checkpoint exists, restore the latest checkpoint.
        if self.ckpt_manager.latest_checkpoint:
            self.checkpoint.restore(self.ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored!!")
        else:
            print("Can not find ckpt files at {}".format(ckpt_path))

    
    def export(self, model_format="hdf5"):
        """Exports the trained models in hdf5 or SavedModel format.

        Args:
            model_format (str, optional): SavedModel or HDF5. Defaults to hdf5.
        """
        model_dir = os.path.join(self.logdir, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if model_format == "hdf5":
            self.model.save(os.path.join(model_dir, "triplet_net.h5"))

        elif model_format == "SavedModel":
            self.generator.save(os.path.join(model_dir, "triplet_net"))
        pass
    

    @tf.function
    def train_step(self, inputs, targets, batch_size, step, file_writer):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function.
        """
        all_triplet_att_images = None
        
        self.simAtt.encoder = self.model
        with file_writer.as_default():
            with tf.GradientTape(persistent=True) as tape:
                # Predict
                start_time = time.time()
                prediction = self.model(inputs, training=True)
                end_time = time.time()
                img_per_second = (end_time - start_time) / batch_size
                tf.summary.scalar("img/sec", img_per_second, step=step)

                # setup loss input list
                loss_inputs = (prediction,)
                if targets is not None:
                    targets = (targets, )
                    loss_inputs += targets

                # calc triplet loss
                loss_ml, hardest_ap_indices, hardest_an_indices = self.triplet_loss.call(*loss_inputs)
                
                # get selected/mined triplets
                mined_triplets = utils.construct_mined_triplets(inputs=inputs, ap_indices=hardest_ap_indices, 
                                                                    an_indices=hardest_an_indices)

                tf.summary.scalar("loss_ml_train", loss_ml, step=step)

                # check if similarity attention needs to be called
                if self.doSimAtt:

                    feature_vectors_hat, all_triplet_att_images = self.simAtt.call(mined_triplets)
                
                    sim_att_loss = self.similarity_loss.call(feature_vectors_hat)
                    tf.summary.scalar("loss_sm_train", sim_att_loss, step=step)

                    overall_loss = self.overall_similarity_loss.call(loss_ml=loss_ml, loss_sm=sim_att_loss)
                else:
                    overall_loss = loss_ml
                    selected_triplets = utils.construct_mined_triplets(inputs, hardest_ap_indices, hardest_an_indices)
                    # TODO: call method to draw images with heatmap
                    # all_triplet_att_images = add_heatmap_to_image(...)


            # Calculate gradient
            gradient = tape.gradient(overall_loss, self.model.feature_extractor.trainable_variables)

            # Apply gradient to weights
            self.optimizer.apply_gradients(zip(gradient, self.model.feature_extractor.trainable_variables))

            # check is similarity attention needs to be called and update the learnable parameters alpha and beta
            if self.doSimAtt:
                train_vars_simAtt = [(v) for v in self.simAtt.trainable_variables 
                                        if v.name in ("sim_alpha:0", "sim_beta:0")]
                gradient = tape.gradient(overall_loss, train_vars_simAtt)
                self.optimizer.apply_gradients(zip(gradient, train_vars_simAtt))

        # TODO: necessary???
        return prediction, overall_loss, mined_triplets, all_triplet_att_images


    def evaluate(self, dataset: tf.data.Dataset, file_writer, step, threshold):
        """ Computes a target for each sample in the given dataset.

        Args:
            model (tf.keras.Model): the encoding network to be applied.
            dataloader (tf.data.Dataset): The dataloader of the dataset,
                        should retrieve every sample in an epoch exactly once.
        Returns:
            encodings (tf.tensor): Tensor consisting of the encodings for each sample
            targets (tf.tensor): target class of the samples
        """
        all_batches_triplet_att_images = []

        encodings_list = []
        targets_list = []
        loss = []

        self.simAtt.encoder = self.model

        with file_writer.as_default():
            for elements in dataset:


                images = elements[0]
                labels = elements[1]

                encoding = self.model(images, training=True)
                encodings_list.append(encoding)
                targets_list.append(labels)

                prediction = encoding
                targets = labels

                # setup loss input list
                loss_inputs = (prediction,)
                if targets is not None:
                    targets = (targets, )
                    loss_inputs += targets

                # calc triplet loss
                loss_ml, hardest_ap_indices, hardest_an_indices = self.triplet_loss.call(*loss_inputs)
                self.mined_triplets = utils.construct_mined_triplets(inputs=images, ap_indices=hardest_ap_indices, 
                                                                    an_indices=hardest_an_indices)


                tf.summary.scalar("loss_ml_val", loss_ml, step=step)


                # check if similarity attention needs to be called
                if self.doSimAtt:

                    # feature_vectors_hat, all_triplet_att_images = self.simAtt.call(images, hardest_ap_indices, hardest_an_indices)
                    feature_vectors_hat, all_triplet_att_images = self.simAtt.call(self.mined_triplets)
                   
                    sim_att_loss = self.similarity_loss.call(feature_vectors_hat)
                    tf.summary.scalar("loss_sm_val", sim_att_loss, step=step)

                    overall_loss = self.overall_similarity_loss.call(loss_ml=loss_ml, loss_sm=sim_att_loss)
                else:
                    overall_loss = loss_ml
                    selected_triplets = utils.construct_mined_triplets(inputs, hardest_ap_indices, hardest_an_indices)
                    # TODO: call method to draw images with heatmap
                    # all_triplet_att_images = draw_images_with_simiarlity_maps(...)

                loss.append(overall_loss)
                all_batches_triplet_att_images.append(all_triplet_att_images)

                

        # convert list to tensors
        encodings = tf.convert_to_tensor(encodings_list, dtype=tf.float32)
        targets = tf.convert_to_tensor(targets_list, dtype=tf.float32)

        # reshape to 2-D tensors
        # (num_batch, feature, channels) -> (num_batch*feature, channels)
        b, n, c = encodings.shape
        encodings = tf.reshape(encodings, shape=[b*n, c])
        b, n = targets.shape
        targets = tf.reshape(targets, shape=[b*n])

        metrics_dict = self.metrics.calc_validation_metrics(encodings=encodings, labels=targets, relevant_samples=2,
                                        threshold=threshold)

        print("Metrics Dist: ", metrics_dict)
        
        return tf.reduce_mean(loss), metrics_dict, all_batches_triplet_att_images
    

    def prediction_to_tensorboard(self, normal_triplets, att_triplets):
        """ create triplet images for tensorboard

        Args:
            normal_triplets (tf.tensor): tensor [b, 3, h, w, c] of original images
            att_triplets (tf.tensor): tensor [b, 3, h, w, c] of images with similarity attention heatmap
        """

        batch, t, h, w, c = normal_triplets.shape
        
        images_normal = []
        images_attention= []
        for b in range(batch):
            figure_normal = plt.figure()

            plt.subplot(131)
            plt.imshow(normal_triplets[b][0].numpy().astype('uint8'))

            plt.subplot(132)
            plt.imshow(normal_triplets[b][1].numpy().astype('uint8'))

            plt.subplot(133)
            plt.imshow(normal_triplets[b][2].numpy().astype('uint8'))

            image_normal = self.plot_to_image(figure_normal)
            images_normal.append(image_normal)

            plt.close(figure_normal)
            
            if att_triplets is not None:
                figure_attention = plt.figure()

                plt.subplot(131)
                plt.imshow(att_triplets[b][0].numpy().astype('uint8'))

                plt.subplot(132)
                plt.imshow(att_triplets[b][1].numpy().astype('uint8'))

                plt.subplot(133)
                plt.imshow(att_triplets[b][2].numpy().astype('uint8'))

                image_attention = self.plot_to_image(figure_attention)
                images_attention.append(image_attention)

                plt.close(figure_attention)
                
        
      
        tb_normal = tf.concat(images_normal, axis=0)
        tb_attention = tf.concat(images_attention, axis=0)

        return tb_normal, tb_attention

          
        
    def plot_to_image(self, figure):
        """Converts the matplotlib plot specified by 'figure' to a PNG image and returns it. 

        Args:
            figure (pyplot figure): created pyplot figure
        
        Returns:
            image (tf.summary.Image): converted pyplot figure as a tf.summary.Image
        """
        # Save the plot to a PNG in memory.
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # Convert PNG buffer to TF image
        image = tf.image.decode_png(buf.getvalue(), channels=3)
        # Add the batch dimension
        image = tf.expand_dims(image, 0)
        return image



    


class Metrics:

    def __init__(self):
        pass


    def auc_roc(self, similarities, labels, threshold, num_thresholds=200):
        """Calculate  AUC (Area Under The Curve) ROC (Receiver Operating Characteristics) curve.

        Args:
            similarities (tf.tensor): output [n, n] of the applied triplet network model
            labels (tf.tensor): labels/ground truth [n,] of the used samples
            threshold (float): value used to determine if two image are equal or not
            num_thresholds (int): number of threshold values used for approximating the AUC, default is 200

        Returns:
            tpr (float): true positive rate, to draw roc curve
            fpr (float): false positive rate, to draw roc curve
            auc (float): auc of the roc curve
        """

        # cast labels which are float to int
        labels = tf.cast(labels, dtype=tf.int32)

        n = labels.shape[0] # should be n, similarities should be n x n

        # get distinct label values, their indices and number of occurence
        distinct_labels, idx, occurences = tf.unique_with_counts(labels)
        num_distinct_labels = distinct_labels.shape[0]


        y_true=[] # store labels/ground-truth for metrics calculation
        y_pred=[] # store predictions for metrics calculation

        for i in range(n):
            sim_row = similarities[i] 

            # convert distances to "predictions" using the given threshold
            # 0 if <= threshold, 1 if > threshold
            # label 0 for images which should be equal - same class
            # label 1 for images which should be not equal - different class
            threshed = tf.where(tf.less_equal(sim_row, threshold), 0, 1)
           
            for l in range(num_distinct_labels):
                # append current threshed distances for all possible label values in the batch 
                # predictions for metric calculation
                y_pred.extend(threshed.numpy())

                # get current possible label
                curr_label = distinct_labels[l]

                # convert labels to 0 if == curr_label, 1 if != curr_label
                threshed_labels = tf.where(tf.equal(labels, curr_label), 0, 1)

                # append current threshed labels for all possible label values in the batch 
                # labels for metric calculation
                y_true.extend(threshed_labels.numpy())
            

        # TruePositive
        m = tf.keras.metrics.TruePositives()
        m.update_state(y_true=y_true, y_pred=y_pred)
        tp = m.result().numpy()

        # FalsePositive
        m = tf.keras.metrics.FalsePositives()
        m.update_state(y_true=y_true, y_pred=y_pred)
        fp = m.result().numpy()

        # FalseNegative
        m = tf.keras.metrics.FalseNegatives()
        m.update_state(y_true=y_true, y_pred=y_pred)
        fn = m.result().numpy()

        # TrueNegative
        m = tf.keras.metrics.TrueNegatives()
        m.update_state(y_true=y_true, y_pred=y_pred)
        tn = m.result().numpy()
        
        # Sensitivity/Recall/TPR = TP / (TP + FN)
        # FPR = 1 - TNR = FP / (FP + TN)
        # [TNR/Specificity/Selectivity = TN / (TN + FP)]
        tpr = tp / (tp + fn) 
        fpr = fp / (tn + fp)

        # calc AUC (Area-Under-the-Curve)
        m = tf.keras.metrics.AUC(num_thresholds=num_thresholds) # 200 is default
        m.update_state(y_true=y_true, y_pred=y_pred)
        auc = m.result().numpy()
        
        return tpr, fpr, auc


    # TODO: set model to evaluation for apply-model function???
    def calc_validation_metrics(self, encodings, labels, relevant_samples=2, threshold=1e-3):
        """ Calulate validation metrics
            - Area-Under-The-Curve (auc)
            - TruePositiveRate (tpr)
            - FalsePositiveRate (fpr)
            - Mean-Average-Precision (mAP)
        
        Args:
            model (tf.keras.Model): the trained model
            dataset (tf.data.Dataset): validation data
            relevant_samples (int): number of relevant samples for mAP calculation, 
                                    should be equal to the number of samples per class for one batch
        
        Returns:
            metrics (dictonary): dictonary with metric key/name and calculated value
        """

        similarities = self.pairwise_distances(encodings, squared=False)

        similarities_dist_class = tf.zeros((similarities.shape[0], similarities.shape[1]*2))        
        
        # make pairs (value, label) of unsorted distance matrix
        # sort distancte matrix according to key which is the distance between the feature samples
        list_sorted_pairs = []
        for i in range(similarities.shape[0]):
            dist_label_dict = {}

            ta_column = tf.TensorArray(tf.float32, size=2)
            column = similarities[: , i]

            # build dict for one column
            for d in range(column.shape[0]):
                dist_label_dict[column.numpy()[d]] = labels.numpy()[d]

            sorted_pairs = sorted(dist_label_dict.items(), key=lambda t: t[0]) # dict is converted to list of pairs

            # assign current dist_label_dict to dict_columns_list
            list_sorted_pairs.append(sorted_pairs)


        # auc/roc
        tpr, fpr, auc = self.auc_roc(similarities=similarities, labels=labels, threshold=threshold, num_thresholds=200)

        # mAP
        mAP = self.mean_avg_precision(rankings=list_sorted_pairs, relevant_samples=relevant_samples)

        # construct metrics dictonary
        metrics = {}
        metrics['mAP'] = mAP
        metrics['auc'] = auc
        metrics['tpr'] = tpr
        metrics['fpr'] = fpr

        return metrics
    

    def pairwise_distances(self, feature, squared=False):
        """Computes the pairwise distance matrix of all possible image pairs with numerical stability.
        output[i, j] = || feature[i, :] - feature[j, :] ||_2

        D_ij = || x_i - x_j ||^2_2
        or:
        D_ij = (x_i - x_j)^T (x_i - x_j) = || x_i ||^2_2 - 2(x_i)^T x_j + || x_j ||^2_2

        Args:
        feature (tf.tensor): 2-D Tensor of size [number of data, feature dimension].
        squared (boolean): Boolean, whether or not to square the pairwise distances.

        Returns:
        pairwise_distances (tf.tensor): 2-D Tensor of size [number of data, number of data].
        """
        pairwise_distances_squared = tf.math.add(
            tf.math.reduce_sum(
                tf.math.square(feature), axis=[1], keepdims=True),
            tf.math.reduce_sum(
                tf.math.square(tf.transpose(feature)), axis=[0], keepdims=True)) - 2.0 * tf.matmul(feature, tf.transpose(feature))
        
        # set small negatives to zero to have numerical inaccuracies
        pairwise_distances_squared = tf.math.maximum(pairwise_distances_squared, 0.0)

        # create mask where the zero distances are placed
        error_mask = tf.math.less_equal(pairwise_distances_squared, 0.0)

        # Optionally take the sqrt
        if squared:
            pairwise_distances = pairwise_distances_squared
        else:
            # Because the gradient of sqrt is infinite when distances == 0.0 (ex: on the diagonal)
            # we need to add a small epsilon where distances == 0.0
            pairwise_distances = tf.math.sqrt(
                pairwise_distances_squared + tf.cast(error_mask, dtype=tf.float32) * 1e-16)

        # Undo conditionally adding 1e-16.
        pairwise_distances = tf.math.multiply(
            pairwise_distances,
            tf.cast(tf.math.logical_not(error_mask), dtype=tf.float32))

        # Explicitly set diagonals to zero.
        num_data = tf.shape(feature)[0]
        mask_offdiagonals = tf.ones_like(pairwise_distances) - tf.linalg.diag(tf.ones([num_data]))
        pairwise_distances = tf.math.multiply(pairwise_distances, mask_offdiagonals)

        return pairwise_distances
 


    def avg_precision(self, ranking, target, relevant_samples):
        """ Calculate verage-Precision (AP)

        Args:
            ranking (list(pair(distance, label))): list of pairs (distance, label)
            target (int): target/label for which the average precision needs to be calculated
            relevant_samples (int): number of relevant samples for mAP calculation

        Return
            ap (float): value of Average-Precision

        """
        hits = 0
        count = 0
        precision = 0.0

        for curr_ranking in ranking:
            count += 1

            # get current itation target
            curr_target = curr_ranking[1] 

            # only use same targets for AP calculation
            if curr_target == target:
                hits += 1
                precision += hits / count

                if hits == relevant_samples:
                    break
        
        return precision / relevant_samples

    
    def mean_avg_precision(self, rankings, relevant_samples=2):
        """ Calculate Mean-Average-Precision (mAP)

        Args:
            rankings (list(pair(distance, label))): list of pairs (distance, label)
            relevant_samples (int): number of relevant samples for mAP calculation, 

        Return
            mAP (float): value of Mean-Average-Precision

        """
        count = 0
        avg_prec = 0.0
        
        length_rankings = len(rankings) 
        for i in range(length_rankings):
            # setup current ranking and current target
            ranking = rankings[i]
            target = ranking[0][1]
            
            count += 1
            avg_prec += self.avg_precision(ranking, target, relevant_samples)

        return avg_prec / count


