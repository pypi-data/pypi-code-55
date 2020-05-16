
# supported devices
#   Mi Body Composition Scale 2 (XMTZC05HM)

import logging
import time

from datetime import date, datetime
from typing import Any, Dict, List, Union

import miblepy.devices.xbm as xbm

from bluepy import btle

from .. import ATTRS


SUPPORTED_ATTRS = [
    ATTRS.WEIGHT,
    ATTRS.IMPEDANCE,
    ATTRS.UNIT,
    # ATTRS.USER,
    ATTRS.TIMESTAMP,
]


MISCALE_USERS: List[Dict[str, Union[int, float, str, date]]] = [
    dict(
        user="Ben",
        height=181,
        birthdate=date(1989, 6, 15),
        sex="male",
        weightOver=60,
        weightBelow=80,
    ),
    dict(
        user="Syra",
        height=159,
        birthdate=date(1990, 2, 21),
        sex="female",
        weightOver=40,
        weightBelow=60,
    ),
    dict(
        user="Shiva",
        height=42,
        birthdate=date(2011, 4, 11),
        sex="female",
        weightOver=3,
        weightBelow=20,
    ),
]


sensor_data = {}

SCAN_TIMEOUT = 10


def fetch_data(mac: str, interface: str) -> Dict[str, Any]:
    """Get data from one Sensor."""

    try:
        btle.Scanner().withDelegate(ScanProcessor(mac)).scan(SCAN_TIMEOUT)
    except btle.BTLEDisconnectError as error:
        logging.error(f"btle disconnected: {error}")
    except btle.BTLEManagementError as error:
        logging.error(f"(temporary) bluetooth connection error: {error}")

    if not sensor_data:
        time.sleep(1)

    logging.debug(f"{sensor_data = }")

    return sensor_data


def find_user(weight: float) -> str:

    def get_age(birthdate: Any) -> int:
        today = date.today()
        return int(today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day)))

    current_user: Dict[str, Union[int, float, str, date]] = {}

    # determine current user by weight
    for user in MISCALE_USERS:

        if user["weightOver"] and not user["weightBelow"]:
            if weight > user["weightOver"]:
                current_user = user

        elif user["weightOver"] and user["weightBelow"]:
            if weight > user["weightOver"] and weight < user["weightBelow"]:
                current_user = user

        elif user["weightOver"] and user["weightBelow"]:
            if weight > user["weightOver"] and weight < user["weightBelow"]:
                current_user = user

        # if current user found, fill profile values and exit
        if current_user:
            current_user[ATTRS.WEIGHT.value] = weight
            current_user[ATTRS.AGE.value] = get_age(current_user["birthdate"])
            break

    return current_user


class ScanProcessor:
    def __init__(self, mac):
        self.mac = mac
        self.mqtt_client = None
        self.connected = False
        btle.DefaultDelegate.__init__(self)

    def swapi16(self, data: bytes, start_byte: int, end_byte: int) -> int:
        return int((data[end_byte - 2 : end_byte] + data[start_byte : start_byte + 2]), 16)

    def handleDiscovery(self, dev, new_dev, new_data):
        """Handle discovered devices"""
        global sensor_data

        if dev.addr == self.mac.lower() and new_dev:

            for (sdid, desc, data) in dev.getScanData():

                dt = None
                impedance = None
                measurement_weight = None
                unit = None

                # Mi Body Composition Scale 2 (XMTZC05HM) / Xiaomi Scale 2 (XMTZC02HM)
                if data.startswith("1b18") and sdid == 22:

                    # parse weight & unit
                    measurement_weight = self.swapi16(data, 26, 30) * 0.01
                    measurement_unit = data[4:6]

                    # check weight unit
                    if measurement_unit == "03":
                        unit = "lbs"
                    if measurement_unit == "02":
                        unit = "kg"
                        measurement_weight = measurement_weight / 2
                    else:
                        logging.error(f"No known unit found! Got: {measurement_unit}")
                        return

                    # parse received bytes
                    impedance = int((data[24:26] + data[22:24]), 16)
                    measurement_date = f"{self.swapi16(data, 8, 12)}-{int((data[12:14]), 16)}-{int((data[14:16]), 16)}"
                    measurement_time = f"{int((data[16:18]), 16)}:{int((data[18:20]), 16)}:{int((data[20:22]), 16)}"
                    dt = datetime.strptime(
                        f"{measurement_date} {measurement_time}", "%Y-%m-%d %H:%M:%S"
                    )

                    logging.debug(f"{measurement_weight = }")
                    logging.debug(f"{impedance = }")
                    logging.debug(f"{dt = }")

                    # fake data
                    measurement_weight = 8.05
                    impedance = 1500

                    if (current_user := find_user(measurement_weight)):
                        bm = xbm.bodyMetrics(
                            current_user[ATTRS.WEIGHT.value],
                            current_user[ATTRS.HEIGHT.value],
                            current_user[ATTRS.AGE.value],
                            current_user[ATTRS.SEX.value],
                            impedance,
                        )

                        # check if we got everything we need
                        if not all([dt, impedance, (impedance > 0 and impedance < 3000), measurement_weight, unit]):
                            logging.warning(
                                f"missing data! measurement_weight: {measurement_weight} | unit: {unit} | dt: {dt} | impedance: {impedance}"
                            )
                            return

                        sensor_data = {
                            ATTRS.USER.value: current_user[ATTRS.USER.value],
                            ATTRS.AGE.value: current_user[ATTRS.AGE.value],
                            ATTRS.SEX.value: current_user[ATTRS.SEX.value],
                            ATTRS.HEIGHT.value: current_user[ATTRS.HEIGHT.value],
                            ATTRS.WEIGHT.value: round(measurement_weight, 2),
                            ATTRS.UNIT.value: unit,
                            ATTRS.IMPEDANCE.value: impedance,
                            ATTRS.BASAL_METABOLISM.value: f"{bm.get_bmr():.2f}",
                            ATTRS.VISCERAL_FAT.value: f"{bm.getVisceralFat():.2f}",
                            ATTRS.BMI.value: f"{bm.getBMI():.2f}",
                            ATTRS.WATER.value: f"{bm.getWaterPercentage():.2f}",
                            ATTRS.BONE_MASS.value: f"{bm.getBoneMass():.2f}",
                            ATTRS.BODY_FAT.value: f"{bm.getFatPercentage():.2f}",
                            ATTRS.LEAN_BODY_MASS.value: f"{bm.get_lbm_coefficient():.2f}",
                            ATTRS.MUSCLE_MASS.value: f"{bm.getMuscleMass():.2f}",
                            ATTRS.PROTEIN.value: f"{bm.getProteinPercentage():.2f}",
                            ATTRS.TIMESTAMP.value: dt.timestamp(),
                            ATTRS.MQTT_SUFFIX.value: current_user[ATTRS.USER.value],
                        }
