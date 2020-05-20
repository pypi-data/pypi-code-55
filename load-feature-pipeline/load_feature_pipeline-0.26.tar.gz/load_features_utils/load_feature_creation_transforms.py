import pandas as pd
import numpy as np
import pickle
from apache_beam.utils.timestamp import MIN_TIMESTAMP
from apache_beam.utils.windowed_value import WindowedValue
from apache_beam.transforms.window import GlobalWindow
from apache_beam.transforms import PTransform, ParDo, DoFn
from scipy.sparse import hstack, vstack, csr_matrix, identity
from feature_creation_tools.feature_creation_utils import LabelEncoderExt
import google.cloud.storage as storage
from load_features_utils.feature_creation_utils import \
    map_quantiles_for_entry,  \
    get_p50_value,  \
    create_polynomial_features, \
    create_time_features, \
    get_load_quantiles


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


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
        self._bundle_num = 0

    def start_bundle(self):
        # buffer for string of lines
        self._lines = []

    def process(self, element):
        # Input element is anything (example a mongodb document
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

    def process(self, df):
        # Multi Label Binarizer Variables
        # Split out Equipment Types

        download_blob("load_transforms", "load_equipment_mlb.pkl", "load_equipment_mlb.pkl")
        with open('load_equipment_mlb.pkl', 'rb') as f:
            equipment_mlb = pickle.load(f)

        download_blob("load_transforms", "load_quantile_mlb.pkl", "load_quantile_mlb.pkl")
        with open('load_quantile_mlb.pkl', 'rb') as f:
            quantile_mlb = pickle.load(f)

        download_blob("load_transforms", "load_state_lbe.pkl", "load_state_lbe.pkl")
        with open('load_state_lbe.pkl', 'rb') as f:
            state_lbe = pickle.load(f)

        download_blob("load_transforms", "load_state_ohe.pkl", "load_state_ohe.pkl")
        with open('load_state_ohe.pkl', 'rb') as f:
            state_ohe = pickle.load(f)

        download_blob("load_transforms", "load_city_lbe.pkl", "load_city_lbe.pkl")
        with open('load_city_lbe.pkl', 'rb') as f:
            city_lbe = pickle.load(f)

        download_blob("load_transforms", "load_city_ohe.pkl", "load_city_ohe.pkl")
        with open('load_city_ohe.pkl', 'rb') as f:
            city_ohe = pickle.load(f)

        download_blob("load_transforms", "load_source_lbe.pkl", "load_source_lbe.pkl")
        with open('load_source_lbe.pkl', 'rb') as f:
            source_lbe = pickle.load(f)

        download_blob("load_transforms", "load_source_ohe.pkl", "load_source_ohe.pkl")
        with open('load_source_ohe.pkl', 'rb') as f:
            source_ohe = pickle.load(f)

        download_blob("load_transforms", "load_email_lbe.pkl", "load_email_lbe.pkl")
        with open('load_email_lbe.pkl', 'rb') as f:
            email_lbe = pickle.load(f)

        download_blob("load_transforms", "load_email_ohe.pkl", "load_email_ohe.pkl")
        with open('load_email_ohe.pkl', 'rb') as f:
            email_ohe = pickle.load(f)

        df["equipment_type_list"] = df["equipment_type_list"].str.split(pat=", ")
        df.equipment_type_list.fillna(value=u'', inplace=True)

        # Equipment Types
        df["equipment_type_encoded"] = list(equipment_mlb.transform(df["equipment_type_list"]))
        df.drop("equipment_type_list", axis=1, inplace=True)

        # Weight
        df["weight_quantile_encoded"] = list(quantile_mlb.transform(df["weight_quantile"]))
        df.drop("weight_quantile", axis=1, inplace=True)

        # Price
        df["price_quantile_encoded"] = list(quantile_mlb.transform(df["price_quantile"]))
        df.drop("price_quantile", axis=1, inplace=True)

        # Per Mile Rate
        df["per_mile_rate_quantile_encoded"] = list(quantile_mlb.transform(df["per_mile_rate_quantile"]))
        df.drop("per_mile_rate_quantile", axis=1, inplace=True)

        # Distance
        df["distance_quantile_encoded"] = list(quantile_mlb.transform(df["distance_quantile"]))
        df.drop("distance_quantile", axis=1, inplace=True)

        # One Hot Encode Variables
        # Pickup State
        df.pickup_state.fillna(value=u'', inplace=True)
        start_state_encoded = state_lbe.transform(df['pickup_state'])
        df["pickup_state_encoded"] = list(state_ohe.transform(start_state_encoded.reshape(-1, 1)))
        df.drop("pickup_state", axis=1, inplace=True)

        # Dropoff State
        df.dropoff_state.fillna(value=u'', inplace=True)
        end_state_encoded = state_lbe.transform(df['dropoff_state'])
        df["dropoff_state_encoded"] = list(state_ohe.transform(end_state_encoded.reshape(-1, 1)))
        df.drop("dropoff_state", axis=1, inplace=True)

        # Pickup City
        df.pickup_city.fillna(value=u'', inplace=True)
        pickup_city_encoded = city_lbe.transform(df['pickup_city'])
        df["pickup_city_encoded"] = list(city_ohe.transform(pickup_city_encoded.reshape(-1, 1)))
        df.drop("pickup_city", axis=1, inplace=True)

        # Dropoff City
        df.dropoff_city.fillna(value=u'', inplace=True)
        dropoff_city_encoded = city_lbe.transform(df['dropoff_city'])
        df["dropoff_city_encoded"] = list(city_ohe.transform(dropoff_city_encoded.reshape(-1, 1)))
        df.drop("dropoff_city", axis=1, inplace=True)

        # Source
        df.source.fillna(value=u'', inplace=True)
        source_encoded = source_lbe.transform(df['source'])
        df["source_encoded"] = list(source_ohe.transform(source_encoded.reshape(-1, 1)))
        df.drop("source", axis=1, inplace=True)

        # Email
        df.contact_email.fillna(value=u'', inplace=True)
        email_encoded = email_lbe.transform(df['contact_email'])
        df["email_encoded"] = list(email_ohe.transform(email_encoded.reshape(-1, 1)))
        df.drop("contact_email", axis=1, inplace=True)

        return [df, ]


class CreateCategoricalEncodedVariables(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateCategoricalEncodedVariables())


class _CreateLoadQuantiles(DoFn):

    def __init__(self):
        super(_CreateLoadQuantiles, self).__init__()

    def process(self, data):
        # Put into dataframe
        df = pd.DataFrame(list(data))
        load_quantile_df = get_load_quantiles()
        weight_quantile = []
        weight_p50 = []
        price_quantile = []
        price_p50 = []
        per_mile_quantile = []
        per_mile_p50 = []
        distance_quantile = []
        distance_p50 = []

        # Iterate through loads
        for i, row in df.iterrows():

            pd.to_numeric(df['weight'], errors='coerce')
            pd.to_numeric(df['price'], errors='coerce')
            pd.to_numeric(df['per_mile_rate'], errors='coerce')
            pd.to_numeric(df['distance'], errors='coerce')

            pickup_state = row["pickup_state"]
            dropoff_state = row["dropoff_state"]
            if row["equipment_type_list"]:

                if "REEFER" in row["equipment_type_list"]:
                    equipment = "reefer"
                elif "STEPDECK" in row["equipment_type_list"] or "FLATBED" in row["equipment_type_list"]:
                    equipment = "flatbed"
                elif "VAN" in row["equipment_type_list"]:
                    equipment = "van"
                else:
                    equipment = "ALL"
            else:
                equipment = "ALL"

            # Find global quantile values
            global_result = load_quantile_df.loc[
                (load_quantile_df['pickup_state'] == "GLOBAL") &
                (load_quantile_df['dropoff_state'] == "GLOBAL") &
                (load_quantile_df['equipment_type'] == equipment)]

            # Find state to state quantile values
            state_to_state_result = load_quantile_df.loc[
                (load_quantile_df['pickup_state'] == pickup_state) &
                (load_quantile_df['dropoff_state'] == dropoff_state) &
                (load_quantile_df['equipment_type'] == equipment)]

            # If no State to State use Global
            if state_to_state_result.empty:
                state_to_state_result = global_result

            weight_quantile.append(map_quantiles_for_entry("weight", global_result, row))
            weight_p50.append(get_p50_value("weight", global_result))

            price_quantile.append(map_quantiles_for_entry("price", state_to_state_result, row))
            price_p50.append(get_p50_value("price", global_result))

            per_mile_quantile.append(map_quantiles_for_entry("per_mile_rate", state_to_state_result, row))
            per_mile_p50.append(get_p50_value("per_mile_rate", global_result))

            distance_quantile.append(map_quantiles_for_entry("distance", state_to_state_result, row))
            distance_p50.append(get_p50_value("distance", global_result))

        df['weight_quantile'] = weight_quantile
        df['weight_p50'] = weight_p50
        df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
        df['weight'] = df.apply(
            lambda row: row['weight_p50']
            if (np.isnan(row['weight']) or row['weight'] in [0, 1.0])
            else row['weight'],
            axis=1
        )

        df['price_quantile'] = price_quantile
        df['price_p50'] = price_p50
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df.apply(
            lambda row: row['price_p50']
            if (np.isnan(row['price']) or row['price'] in [0, 1.0])
            else row['price'],
            axis=1
        )

        df['per_mile_rate_quantile'] = per_mile_quantile
        df['per_mile_rate_p50'] = per_mile_p50
        df['per_mile_rate'] = pd.to_numeric(df['per_mile_rate'], errors='coerce')
        df['per_mile_rate'] = df.apply(
            lambda row: row['per_mile_rate_p50']
            if (np.isnan(row['per_mile_rate']) or row['per_mile_rate'] == 0)
            else row['per_mile_rate'],
            axis=1
        )
        df['distance_quantile'] = distance_quantile
        df['distance_p50'] = distance_p50
        df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
        df['distance'] = df.apply(
            lambda row: row['distance_p50']
            if (np.isnan(row['distance']) or row['distance'] in [0, 1.0])
            else row['distance'],
            axis=1
        )

        return [df, ]


class CreateLoadQuantiles(PTransform):

    def __init__(self):
        super(CreateLoadQuantiles, self).__init__()

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateLoadQuantiles())


class _CreateCyclicTimeFeatures(DoFn):

    def process(self, df):
        feature_names = [
            'pickup_start_hour',
            'pickup_start_day_of_week',
            'pickup_start_month',
            'pickup_start_day_of_year',
            'pickup_start_year',
            'pickup_end_hour',
            'pickup_end_day_of_week',
            'pickup_end_month',
            'pickup_end_day_of_year',
            'pickup_end_year',
            'dropoff_start_hour',
            'dropoff_start_day_of_week',
            'dropoff_start_month',
            'dropoff_start_day_of_year',
            'dropoff_start_year',
            'dropoff_end_hour',
            'dropoff_end_day_of_week',
            'dropoff_end_month',
            'dropoff_end_day_of_year',
            'dropoff_end_year',
            'assigned_hour',
            'assigned_day_of_week',
            'assigned_month',
            'assigned_day_of_year',
            'assigned_year']

        df = create_time_features(feature_names, df)
        return [df, ]


class CreateCyclicTimeFeatures(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateCyclicTimeFeatures())


class _CreateLoadPolyFeatures(DoFn):

    def process(self, df):

        feature_names = ["weight", "price", "per_mile_rate", "distance"]
        df = create_polynomial_features(feature_names, df)
        return [df, ]


class CreateLoadPolyFeatures(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateLoadPolyFeatures())


class _SaveDataframeToGCS(DoFn):

    def process(self, df):

        load_id_column = df[['load_id']].copy()
        bundle_num = load_id_column.iloc[0]["load_id"]
        # drop load_id column
        df.drop('load_id', axis=1, inplace=True)

        # fix bool values
        df['ftl'] = (df['ftl'] == 'True').astype(int)

        # expand lists into in dataframe
        split_out = df['equipment_type_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'equipment_type_encoded' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('equipment_type_encoded', axis=1, inplace=True)

        split_out = df['weight_quantile_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'weight_quantile_encoded' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('weight_quantile_encoded', axis=1, inplace=True)

        split_out = df['price_quantile_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'price_quantile_encoded' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('price_quantile_encoded', axis=1, inplace=True)

        split_out = df['per_mile_rate_quantile_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'per_mile_rate_quantile_encoded' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('per_mile_rate_quantile_encoded', axis=1, inplace=True)

        split_out = df['distance_quantile_encoded'].apply(pd.Series)
        split_out = split_out.rename(columns=lambda x: 'distance_quantile_encoded' + str(x))
        df = pd.concat([df, split_out], axis=1, sort=False)
        df.drop('distance_quantile_encoded', axis=1, inplace=True)

        # Combine all the sparse column features into a csr matrix
        sparse_loads = vstack(df['pickup_state_encoded'].values)
        df.drop('pickup_state_encoded', axis=1, inplace=True)

        dropoff_state = vstack(df['dropoff_state_encoded'].values)
        df.drop('dropoff_state_encoded', axis=1, inplace=True)
        sparse_loads = hstack((sparse_loads, dropoff_state))

        pickup_city = vstack(df['pickup_city_encoded'].values)
        df.drop('pickup_city_encoded', axis=1, inplace=True)
        sparse_loads = hstack((sparse_loads, pickup_city))

        dropoff_city = vstack(df['dropoff_city_encoded'].values)
        df.drop('dropoff_city_encoded', axis=1, inplace=True)
        sparse_loads = hstack((sparse_loads, dropoff_city))

        source = vstack(df['source_encoded'].values)
        df.drop('source_encoded', axis=1, inplace=True)
        sparse_loads = hstack((sparse_loads, source))

        email = vstack(df['email_encoded'].values)
        df.drop('email_encoded', axis=1, inplace=True)
        sparse_loads = hstack((sparse_loads, email))

        # combine remaining dataframe features into a csr matrix
        remaining_features = csr_matrix(df.values)
        sparse_loads = hstack((sparse_loads, remaining_features))

        # Add Identity Matrix to feature matrix as suggested in documentation
        sparse_loads.data = np.nan_to_num(sparse_loads.data, copy=False)
        sparse_loads = csr_matrix(sparse_loads)

        data = {"index": load_id_column, "data": sparse_loads}
        
        filename = "load_features_" + str(bundle_num) + ".pkl"
        pickle.dump(data, open(filename, "wb"))
        upload_blob("load_features", filename, filename)

        return [data, ]


class SaveDataframeToGCS(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_SaveDataframeToGCS())

