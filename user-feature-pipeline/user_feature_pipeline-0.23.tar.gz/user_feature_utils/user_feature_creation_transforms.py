from apache_beam.utils.timestamp import MIN_TIMESTAMP
from apache_beam.utils.windowed_value import WindowedValue
from apache_beam.transforms.window import GlobalWindow
from apache_beam.transforms import PTransform, ParDo, DoFn
from scipy.sparse import hstack, vstack, csr_matrix
import numpy as np
from feature_creation_tools.feature_creation_utils import LabelEncoderExt
import google.cloud.storage as storage
import pandas as pd
import pickle


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def download_blob(bucket_name, source_file, destination_file):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_file)
    blob.download_to_filename(destination_file)

    print('File {} downloaded to {}.'.format(source_file, destination_file))


class _BatchingFn(DoFn):

    def __init__(self, batch_size=500):
        super(_BatchingFn, self).__init__()
        self._batch_size = batch_size

    def start_bundle(self):
        # buffer for string of lines
        self._lines = []

    def process(self, element):
        # Input element is anything (example a mongodb document)
        self._lines.append(element)
        if len(self._lines) >= self._batch_size:
            yield WindowedValue(self._lines, MIN_TIMESTAMP, [GlobalWindow()])
            self._flush_batch()

    def finish_bundle(self):
        # takes care of the unflushed buffer before finishing
        if self._lines:
            yield WindowedValue(self._lines, MIN_TIMESTAMP, [GlobalWindow()])
            self._flush_batch()

    def _flush_batch(self):
        self._lines = []


class BatchingFn(PTransform):

    def __init__(self, batch_size=500):
        super(BatchingFn, self).__init__()
        self._batch_size = batch_size

    def expand(self, pcoll):
        return pcoll | ParDo(_BatchingFn(self._batch_size))


class _CreateCategoricalEncodedVariables(DoFn):

    def process(self, data):

        # Multi Label Binarizer Variables
        # Split out Equipment Types

        download_blob("user_transforms", "user_equipment_mlb.pkl", "user_equipment_mlb.pkl")
        with open('user_equipment_mlb.pkl', 'rb') as f:
            equipment_mlb = pickle.load(f)

        download_blob("user_transforms", "user_state_lbe.pkl", "user_state_lbe.pkl")
        with open('user_state_lbe.pkl', 'rb') as f:
            state_lbe = pickle.load(f)

        download_blob("user_transforms", "user_state_ohe.pkl", "user_state_ohe.pkl")
        with open('user_state_ohe.pkl', 'rb') as f:
            state_ohe = pickle.load(f)

        download_blob("user_transforms", "user_city_lbe.pkl", "user_city_lbe.pkl")
        with open('user_city_lbe.pkl', 'rb') as f:
            city_lbe = pickle.load(f)

        download_blob("user_transforms", "user_city_ohe.pkl", "user_city_ohe.pkl")
        with open('user_city_ohe.pkl', 'rb') as f:
            city_ohe = pickle.load(f)

        download_blob("user_transforms", "user_email_lbe.pkl", "user_email_lbe.pkl")
        with open('user_email_lbe.pkl', 'rb') as f:
            email_lbe = pickle.load(f)

        download_blob("user_transforms", "user_email_ohe.pkl", "user_email_ohe.pkl")
        with open('user_email_ohe.pkl', 'rb') as f:
            email_ohe = pickle.load(f)

        download_blob("user_transforms", "user_zip_code_lbe.pkl", "user_zip_code_lbe.pkl")
        with open('user_zip_code_lbe.pkl', 'rb') as f:
            zip_code_lbe = pickle.load(f)

        download_blob("user_transforms", "user_zip_code_ohe.pkl", "user_zip_code_ohe.pkl")
        with open('user_zip_code_ohe.pkl', 'rb') as f:
            zip_code_ohe = pickle.load(f)

        download_blob("user_transforms", "user_channel_lbe.pkl", "user_channel_lbe.pkl")
        with open('user_channel_lbe.pkl', 'rb') as f:
            channel_lbe = pickle.load(f)

        download_blob("user_transforms", "user_channel_ohe.pkl", "user_channel_ohe.pkl")
        with open('user_channel_ohe.pkl', 'rb') as f:
            channel_ohe = pickle.load(f)

        download_blob("user_transforms", "user_dot_lbe.pkl", "user_dot_lbe.pkl")
        with open('user_dot_lbe.pkl', 'rb') as f:
            dot_lbe = pickle.load(f)

        download_blob("user_transforms", "user_dot_ohe.pkl", "user_dot_ohe.pkl")
        with open('user_dot_ohe.pkl', 'rb') as f:
            dot_ohe = pickle.load(f)

        download_blob("user_transforms", "user_hos_home_timezone_lbe.pkl", "user_hos_home_timezone_lbe.pkl")
        with open('user_hos_home_timezone_lbe.pkl', 'rb') as f:
            hos_home_timezone_lbe = pickle.load(f)

        download_blob("user_transforms", "user_hos_home_timezone_ohe.pkl", "user_hos_home_timezone_ohe.pkl")
        with open('user_hos_home_timezone_ohe.pkl', 'rb') as f:
            hos_home_timezone_ohe = pickle.load(f)

        download_blob("user_transforms", "user_hos_cycle_lbe.pkl", "user_hos_cycle_lbe.pkl")
        with open('user_hos_cycle_lbe.pkl', 'rb') as f:
            hos_cycle_lbe = pickle.load(f)

        download_blob("user_transforms", "user_hos_cycle_ohe.pkl", "user_hos_cycle_ohe.pkl")
        with open('user_hos_cycle_ohe.pkl', 'rb') as f:
            hos_cycle_ohe = pickle.load(f)

        download_blob("user_transforms", "user_mc_number_lbe.pkl", "user_mc_number_lbe.pkl")
        with open('user_mc_number_lbe.pkl', 'rb') as f:
            mc_number_lbe = pickle.load(f)

        download_blob("user_transforms", "user_mc_number_ohe.pkl", "user_mc_number_ohe.pkl")
        with open('user_mc_number_ohe.pkl', 'rb') as f:
            mc_number_ohe = pickle.load(f)

        download_blob("user_transforms", "user_type_lbe.pkl", "user_type_lbe.pkl")
        with open('user_type_lbe.pkl', 'rb') as f:
            user_type_lbe = pickle.load(f)

        download_blob("user_transforms", "user_type_ohe.pkl", "user_type_ohe.pkl")
        with open('user_type_ohe.pkl', 'rb') as f:
            user_type_ohe = pickle.load(f)

        download_blob("user_transforms", "user_safer_result_safety_rating_lbe.pkl", "user_safer_result_safety_rating_lbe.pkl")
        with open('user_safer_result_safety_rating_lbe.pkl', 'rb') as f:
            safety_rating_lbe = pickle.load(f)

        download_blob("user_transforms", "user_safer_result_safety_rating_ohe.pkl", "user_safer_result_safety_rating_ohe.pkl")
        with open('user_safer_result_safety_rating_ohe.pkl', 'rb') as f:
            safety_rating_ohe = pickle.load(f)

        df = pd.DataFrame(data)
        df.equipment_types.fillna(value=u'', inplace=True)
        df["equipment_types"] = df["equipment_types"].str.split(pat=", ")
        df["equipment_types_encoded"] = list(equipment_mlb.transform(df["equipment_types"]))
        df.drop("equipment_types", axis=1, inplace=True)

        # Split out Predicted Equipment Types
        df.predicted_equipment_types.fillna(value=u'', inplace=True)
        df["predicted_equipment_types"] = df["predicted_equipment_types"].str.split(pat=", ")
        df["predicted_equipment_types_encoded"] = list(equipment_mlb.transform(df["predicted_equipment_types"]))
        df.drop("predicted_equipment_types", axis=1, inplace=True)

        # One Hot Encode Variables
        # State
        state_encoded = state_lbe.transform(df['state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["state_encoded"] = list(data)
        df.drop("state", axis=1, inplace=True)

        # City
        city_encoded = city_lbe.transform(df['city'])
        df["city_encoded"] = list(city_ohe.transform(city_encoded.reshape(-1, 1)))
        df.drop("city", axis=1, inplace=True)

        # Zip Code
        zip_code_encoded = zip_code_lbe.transform(df['zip_code'])
        df["zip_code_encoded"] = list(zip_code_ohe.transform(zip_code_encoded.reshape(-1, 1)))
        df.drop("zip_code", axis=1, inplace=True)

        # Email
        email_encoded = email_lbe.transform(df['email'])
        df["email_encoded"] = list(email_ohe.transform(email_encoded.reshape(-1, 1)))
        df.drop("email", axis=1, inplace=True)

        # DOT
        dot_encoded = dot_lbe.transform(df['dot'])
        df["dot_encoded"] = list(dot_ohe.transform(dot_encoded.reshape(-1, 1)))
        df.drop("dot", axis=1, inplace=True)

        # Channel
        channel_encoded = channel_lbe.transform(df['channel'])
        df["channel_encoded"] = list(channel_ohe.transform(channel_encoded.reshape(-1, 1)))
        df.drop("channel", axis=1, inplace=True)

        # hos_cycle
        hos_cycle_encoded = hos_cycle_lbe.transform(df['hos_cycle'])
        df["hos_cycle_encoded"] = list(hos_cycle_ohe.transform(hos_cycle_encoded.reshape(-1, 1)))
        df.drop("hos_cycle", axis=1, inplace=True)

        # hos_home_timezone
        hos_home_timezone_encoded = hos_home_timezone_lbe.transform(df['hos_home_timezone'])
        df["hos_home_timezone_encoded"] = list(
            hos_home_timezone_ohe.transform(hos_home_timezone_encoded.reshape(-1, 1)))
        df.drop("hos_home_timezone", axis=1, inplace=True)

        # mc_number
        mc_number_encoded = mc_number_lbe.transform(df['mc_number'])
        df["mc_number_encoded"] = list(mc_number_ohe.transform(mc_number_encoded.reshape(-1, 1)))
        df.drop("mc_number", axis=1, inplace=True)

        # user_type
        user_type_encoded = user_type_lbe.transform(df['user_type'])
        df["user_type_encoded"] = list(user_type_ohe.transform(user_type_encoded.reshape(-1, 1)))
        df.drop("user_type", axis=1, inplace=True)

        # Operating Lanes Pickup States
        state_encoded = state_lbe.transform(df['operating_lanes_1_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_1_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_1_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_2_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_2_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_2_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_3_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_3_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_3_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_4_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_4_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_4_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_5_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_5_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_5_pickup_state", axis=1, inplace=True)

        # Operating Lanes Dropoff States
        state_encoded = state_lbe.transform(df['operating_lanes_1_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_1_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_1_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_2_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_2_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_2_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_3_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_3_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_3_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_4_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_4_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_4_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_5_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_5_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_5_dropoff_state", axis=1, inplace=True)

        # Operating Lanes Pickup Cities
        city_encoded = city_lbe.transform(df['operating_lanes_1_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_1_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_1_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_2_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_2_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_2_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_3_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_3_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_3_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_4_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_4_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_4_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_5_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_5_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_5_pickup_city", axis=1, inplace=True)

        # Operating Lanes Dropoff Cities
        city_encoded = city_lbe.transform(df['operating_lanes_1_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_1_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_1_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_2_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_2_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_2_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_3_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_3_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_3_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_4_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_4_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_4_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_5_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_5_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_5_dropoff_city", axis=1, inplace=True)

        # Common Lanes Pickup States
        state_encoded = state_lbe.transform(df['common_lane_1_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_1_pickup_state_encoded"] = list(data)
        df.drop("common_lane_1_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_2_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_2_pickup_state_encoded"] = list(data)
        df.drop("common_lane_2_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_3_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_3_pickup_state_encoded"] = list(data)
        df.drop("common_lane_3_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_4_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_4_pickup_state_encoded"] = list(data)
        df.drop("common_lane_4_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_5_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_5_pickup_state_encoded"] = list(data)
        df.drop("common_lane_5_pickup_state", axis=1, inplace=True)

        # Common Lanes Dropoff States
        state_encoded = state_lbe.transform(df['common_lane_1_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_1_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_1_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_2_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_2_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_2_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_3_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_3_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_3_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_4_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_4_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_4_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_5_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_5_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_5_dropoff_state", axis=1, inplace=True)

        # Common Lanes Pickup Cities
        df.loc[~df["common_lane_1_pickup_city"].isin(city_lbe.classes_), "common_lane_1_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_1_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_1_pickup_city_encoded"] = list(data)
        df.drop("common_lane_1_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_2_pickup_city"].isin(city_lbe.classes_), "common_lane_2_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_2_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_2_pickup_city_encoded"] = list(data)
        df.drop("common_lane_2_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_3_pickup_city"].isin(city_lbe.classes_), "common_lane_3_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_3_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_3_pickup_city_encoded"] = list(data)
        df.drop("common_lane_3_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_4_pickup_city"].isin(city_lbe.classes_), "common_lane_4_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_4_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_4_pickup_city_encoded"] = list(data)
        df.drop("common_lane_4_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_5_pickup_city"].isin(city_lbe.classes_), "common_lane_5_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_5_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_5_pickup_city_encoded"] = list(data)
        df.drop("common_lane_5_pickup_city", axis=1, inplace=True)

        # Common Lanes Dropoff Cities
        df.loc[~df["common_lane_1_dropoff_city"].isin(city_lbe.classes_), "common_lane_1_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_1_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_1_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_1_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_2_dropoff_city"].isin(city_lbe.classes_), "common_lane_2_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_2_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_2_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_2_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_3_dropoff_city"].isin(city_lbe.classes_), "common_lane_3_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_3_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_3_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_3_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_4_dropoff_city"].isin(city_lbe.classes_), "common_lane_4_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_4_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_4_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_4_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_5_dropoff_city"].isin(city_lbe.classes_), "common_lane_5_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_5_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_5_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_5_dropoff_city", axis=1, inplace=True)

        safety_rating_encoded = safety_rating_lbe.transform(df['safer_result_safety_rating'])
        df["safer_result_safety_rating_encoded"] = list(safety_rating_ohe.transform(safety_rating_encoded.reshape(-1, 1)))
        df.drop("safer_result_safety_rating", axis=1, inplace=True)

        return [df, ]


class CreateCategoricalEncodedVariables(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateCategoricalEncodedVariables())


class _SaveDataframeToGCS(DoFn):

    def process(self, df):

        person_id_column = df[['person_id']].copy()
        bundle_num = person_id_column.iloc[0]["person_id"]

        # drop person_id column
        df.drop('person_id', axis=1, inplace=True)

        # Drop useless features for now
        df.drop('safer_result_oosr_hazmat_us', axis=1, inplace=True)
        df.drop('safer_result_oosr_vehicle_ca', axis=1, inplace=True)
        df.drop('safer_result_oosr_vehicle_us', axis=1, inplace=True)
        df.drop('operating_lanes_1_pickup_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_2_pickup_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_3_pickup_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_4_pickup_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_5_pickup_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_1_dropoff_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_2_dropoff_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_3_dropoff_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_4_dropoff_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_5_dropoff_state_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_1_pickup_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_2_pickup_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_3_pickup_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_4_pickup_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_5_pickup_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_1_dropoff_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_2_dropoff_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_3_dropoff_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_4_dropoff_city_encoded', axis=1, inplace=True)
        df.drop('operating_lanes_5_dropoff_city_encoded', axis=1, inplace=True)
        df.fillna(0, inplace=True)

        # fix bool values
        df['safer_result_allowed_hire'] = (df['safer_result_allowed_hire'] == 'True').astype(int)
        df['safer_result_cargo_carried_agricultural_farm_supplies'] = (
                df['safer_result_cargo_carried_agricultural_farm_supplies'] == 'True').astype(int)
        df['safer_result_cargo_carried_beverages'] = (
                df['safer_result_cargo_carried_beverages'] == 'True').astype(int)
        df['safer_result_cargo_carried_building_materials'] = (
                df['safer_result_cargo_carried_building_materials'] == 'True').astype(int)
        df['safer_result_cargo_carried_chemicals'] = (
                df['safer_result_cargo_carried_chemicals'] == 'True').astype(int)
        df['safer_result_cargo_carried_coal_coke'] = (
                df['safer_result_cargo_carried_coal_coke'] == 'True').astype(int)
        df['safer_result_cargo_carried_commodities_dry_bulk'] = (
                df['safer_result_cargo_carried_commodities_dry_bulk'] == 'True').astype(int)
        df['safer_result_cargo_carried_construction'] = (
                df['safer_result_cargo_carried_construction'] == 'True').astype(int)
        df['safer_result_cargo_carried_drive_tow_away'] = (
                df['safer_result_cargo_carried_drive_tow_away'] == 'True').astype(int)
        df['safer_result_cargo_carried_fresh_produce'] = (
                df['safer_result_cargo_carried_fresh_produce'] == 'True').astype(int)
        df['safer_result_cargo_carried_garbage_refuse'] = (
                df['safer_result_cargo_carried_garbage_refuse'] == 'True').astype(int)
        df['safer_result_cargo_carried_general_freight'] = (
                df['safer_result_cargo_carried_general_freight'] == 'True').astype(int)
        df['safer_result_cargo_carried_grain_feed_hay'] = (
                df['safer_result_cargo_carried_grain_feed_hay'] == 'True').astype(int)
        df['safer_result_cargo_carried_household_goods'] = (
                df['safer_result_cargo_carried_household_goods'] == 'True').astype(int)
        df['safer_result_cargo_carried_intermodal_cont'] = (
                df['safer_result_cargo_carried_intermodal_cont'] == 'True').astype(int)
        df['safer_result_cargo_carried_liquids_gases'] = (
                df['safer_result_cargo_carried_liquids_gases'] == 'True').astype(int)
        df['safer_result_cargo_carried_livestock'] = (
                df['safer_result_cargo_carried_livestock'] == 'True').astype(int)
        df['safer_result_cargo_carried_logs_poles_beams_lumber'] = (
                df['safer_result_cargo_carried_logs_poles_beams_lumber'] == 'True').astype(int)
        df['safer_result_cargo_carried_machinery_large_objects'] = (
                df['safer_result_cargo_carried_machinery_large_objects'] == 'True').astype(int)
        df['safer_result_cargo_carried_meat'] = (df['safer_result_cargo_carried_meat'] == 'True').astype(int)
        df['safer_result_cargo_carried_metal_sheets_coils_rolls'] = (
                df['safer_result_cargo_carried_metal_sheets_coils_rolls'] == 'True').astype(int)
        df['safer_result_cargo_carried_mobile_homes'] = (
                df['safer_result_cargo_carried_mobile_homes'] == 'True').astype(int)
        df['safer_result_cargo_carried_motor_vehicles'] = (
                df['safer_result_cargo_carried_motor_vehicles'] == 'True').astype(int)
        df['safer_result_cargo_carried_oilfield_equipment'] = (
                df['safer_result_cargo_carried_oilfield_equipment'] == 'True').astype(int)
        df['safer_result_cargo_carried_paper_products'] = (
                df['safer_result_cargo_carried_paper_products'] == 'True').astype(int)
        df['safer_result_cargo_carried_passengers'] = (
                df['safer_result_cargo_carried_passengers'] == 'True').astype(int)
        df['safer_result_cargo_carried_refrigerated_food'] = (
                df['safer_result_cargo_carried_refrigerated_food'] == 'True').astype(int)
        df['safer_result_cargo_carried_us_mail'] = (
                df['safer_result_cargo_carried_us_mail'] == 'True').astype(
            int)
        df['safer_result_cargo_carried_utilities'] = (
                df['safer_result_cargo_carried_utilities'] == 'True').astype(int)
        df['safer_result_cargo_carried_water_well'] = (
                df['safer_result_cargo_carried_water_well'] == 'True').astype(int)

        # expand lists in dataframe
        split_out = df['equipment_types_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'equipment_types_encoded_' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('equipment_types_encoded', axis=1, inplace=True)

        split_out = df['predicted_equipment_types_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'predicted_equipment_types_encoded_' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('predicted_equipment_types_encoded', axis=1, inplace=True)

        # Combine all the sparse column features into a csr matrix
        sparse_users = vstack(df['state_encoded'].values)
        df.drop('state_encoded', axis=1, inplace=True)

        city = vstack(df['city_encoded'].values)
        df.drop('city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        state = vstack(df['common_lane_1_pickup_state_encoded'].values)
        df.drop('common_lane_1_pickup_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_2_pickup_state_encoded'].values)
        df.drop('common_lane_2_pickup_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_3_pickup_state_encoded'].values)
        df.drop('common_lane_3_pickup_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_4_pickup_state_encoded'].values)
        df.drop('common_lane_4_pickup_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_5_pickup_state_encoded'].values)
        df.drop('common_lane_5_pickup_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_1_dropoff_state_encoded'].values)
        df.drop('common_lane_1_dropoff_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_2_dropoff_state_encoded'].values)
        df.drop('common_lane_2_dropoff_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_3_dropoff_state_encoded'].values)
        df.drop('common_lane_3_dropoff_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_4_dropoff_state_encoded'].values)
        df.drop('common_lane_4_dropoff_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        state = vstack(df['common_lane_5_dropoff_state_encoded'].values)
        df.drop('common_lane_5_dropoff_state_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, state))

        city = vstack(df['common_lane_1_pickup_city_encoded'].values)
        df.drop('common_lane_1_pickup_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_2_pickup_city_encoded'].values)
        df.drop('common_lane_2_pickup_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_3_pickup_city_encoded'].values)
        df.drop('common_lane_3_pickup_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_4_pickup_city_encoded'].values)
        df.drop('common_lane_4_pickup_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_5_pickup_city_encoded'].values)
        df.drop('common_lane_5_pickup_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_1_dropoff_city_encoded'].values)
        df.drop('common_lane_1_dropoff_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_2_dropoff_city_encoded'].values)
        df.drop('common_lane_2_dropoff_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_3_dropoff_city_encoded'].values)
        df.drop('common_lane_3_dropoff_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_4_dropoff_city_encoded'].values)
        df.drop('common_lane_4_dropoff_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        city = vstack(df['common_lane_5_dropoff_city_encoded'].values)
        df.drop('common_lane_5_dropoff_city_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, city))

        zip_code = vstack(df['zip_code_encoded'].values)
        df.drop('zip_code_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, zip_code))

        email = vstack(df['email_encoded'].values)
        df.drop('email_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, email))

        dot = vstack(df['dot_encoded'].values)
        df.drop('dot_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, dot))

        channel = vstack(df['channel_encoded'].values)
        df.drop('channel_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, channel))

        hos_cycle = vstack(df['hos_cycle_encoded'].values)
        df.drop('hos_cycle_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, hos_cycle))

        hos_home_timezone = vstack(df['hos_home_timezone_encoded'].values)
        df.drop('hos_home_timezone_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, hos_home_timezone))

        mc_number = vstack(df['mc_number_encoded'].values)
        df.drop('mc_number_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, mc_number))

        user_type = vstack(df['user_type_encoded'].values)
        df.drop('user_type_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, user_type))

        safer_result_safety_rating = vstack(df['safer_result_safety_rating_encoded'].values)
        df.drop('safer_result_safety_rating_encoded', axis=1, inplace=True)
        sparse_users = hstack((sparse_users, safer_result_safety_rating))

        # combine remaining dataframe features into a csr matrix
        remaining_features = csr_matrix(df.values)
        sparse_users = hstack((sparse_users, remaining_features))

        # Add Identity Matrix to feature matrix as suggested in documentation
        sparse_users.data = np.nan_to_num(sparse_users.data, copy=False)
        sparse_users = csr_matrix(sparse_users)

        data = {"index": person_id_column, "data": sparse_users}
        filename = "user_features_" + str(bundle_num) + ".pkl"
        pickle.dump(data, open(filename, "wb"))
        upload_blob("user_features", filename, filename)

        return [data, ]


class SaveDataframeToGCS(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_SaveDataframeToGCS())