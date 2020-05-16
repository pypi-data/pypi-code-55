import pathlib

import regression_model

import pandas as pd

pd.options.display.max_rows = 10
pd.options.display.max_columns = 10

PACKAGE_ROOT = pathlib.Path(regression_model.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
DATASET_DIR = PACKAGE_ROOT / "datasets"

#data
TESTING_DATA_FILE = "test.csv"
TRAINING_DATA_FILE = "train.csv"
TARGET = "Energy_kWh"
DATETIME_INDEX = "datetime_converted"
PREDICTION_PLACE = 'Kumpula'

#special vars
RADIATION_ACCUMULATION = 'radiation_global_accumulation'
GLOBAL_RADIATION = 'GlobalRadiation_W_m2'

#fmi_weather related vars
FORECAST_TO_DROP = [
    'precipitation',
    'weather_symbol',
    'radiation_global_accumulation',
    'radiation_long_wave_accumulation',
    'radiation_netsurface_long_wave_accumulation',
    'radiation_netsurface_short_wave_accumulation',
    'radiation_diffuse_accumulation'
]
#used to rename variables after merging forecasts from FMI_weather into a DF
# so that they comply with our variables names
FEATURES = [
            'datetime_converted',
            'AirTemperature_degC',
            'WindSpeed_m_s',
            'GustSpeed_m_s',
            'WindDirection',
            'RelativeHumidity_percent',
            'CloudAmount',
            'Pressure_msl_hpa',
            'DewPointTemperature_degC',
            'PrecipitationIntensity_mm_h',
            'GlobalRadiation_W_m2'
]

#variables

WIND_DISCRETE = 'WindDirection'

NUM_TO_BINARY = [
    'CloudAmount',
    'PrecipitationIntensity_mm_h'
]

BINARY_BOUNDARIES = {
    'CloudAmount': 5,
    'PrecipitationIntensity_mm_h': 0
}

TEMPORAL_HOUR = 'Hour'

TEMPORAL_DAY = 'DayofYear'

SOLAR_ANGLE = 'SolarElevationAngle_deg'

SUN_AZIMUTH = 'SunAzimuth_deg'

THEOR_SRAD = 'TheoreticalSolarRadiation'

#variables that can be later dropped after used in calculation:
DROP_FEATURES = [
    'GustSpeed_m_s',
    'datetime_converted'
]

# think of more stuff here

PIPELINE_NAME  = "rf_pipeline"
PIPELINE_SAVE_FILE = f"{PIPELINE_NAME}_output_v"

#for differential testing
ACCEPTABLE_MODEL_DIFFERENCE = 0.05
