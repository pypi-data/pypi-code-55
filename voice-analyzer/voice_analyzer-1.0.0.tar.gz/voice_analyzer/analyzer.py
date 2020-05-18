import os
import numpy as np
import parselmouth
import tensorflow as tf


class Sex:
    current_path = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(current_path, ".\\models\\sex\\model.h5")
    sex_aliases = ['male', 'female']
    model = None

    def __init__(self, model_path=None):
        if model_path is not None:
            self.model_path = model_path

        self.__create_model()

    def __create_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.Input(shape=1),
            tf.keras.layers.Dense(1, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')
        ])

        model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        self.model = model

    def __load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def train(self, data, save_path):
        self.model.fit(
            data['frequency'].values,
            data['sex'].values,
            epochs=5,
        )

        self.model.save(save_path)

        test_loss, test_acc = self.model.evaluate(data['frequency'].values, data['sex'].values)
        print('Точность после проверки:', test_acc)

        return True

    def tests(self, data):
        self.__load_model()

        test_loss, test_acc = self.model.evaluate(data['frequency'].values, data['sex'].values)
        print('Точность после проверки:', test_acc)

    def predict(self, path):
        self.__load_model()

        snd = parselmouth.Sound(path)
        pitch = snd.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[np.nonzero(pitch_values)]
        pitch = [np.average(pitch_values)]

        predictions = self.model.predict([pitch])

        result = np.argmax(predictions[0])

        return self.sex_aliases[result]
