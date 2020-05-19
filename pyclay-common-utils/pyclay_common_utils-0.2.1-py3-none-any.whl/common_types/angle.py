from __future__ import annotations
import math
from ..check_utils import check_type_from_list
from ..constants import number_types
from scipy.spatial.transform import Rotation

class EulerAngle:
    def __init__(self, roll, pitch, yaw):
        check_type_from_list(item_list=[roll, pitch, yaw], valid_type_list=number_types)
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self) -> str:
        return f"EulerAngle({self.roll},{self.pitch},{self.yaw})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_list(self) -> list:
        return [self.roll, self.pitch, self.yaw]

    @classmethod
    def from_list(self, val_list: list, from_deg: bool=False) -> EulerAngle:
        roll, pitch, yaw = val_list
        if from_deg:
            return EulerAngle(roll=roll*math.pi/180, pitch=pitch*math.pi/180, yaw=yaw*math.pi/180)
        else:
            return EulerAngle(roll=roll, pitch=pitch, yaw=yaw)

    def to_quaternion(self, seq: str='xyz') -> Quaternion:
        return Quaternion.from_list(Rotation.from_euler(seq=seq, angles=self.to_list()).as_quat().tolist())

    def to_deg_list(self) -> list:
        return [val * 180 / math.pi for val in self.to_list()]

class Quaternion:
    def __init__(self, qw, qx, qy, qz):
        check_type_from_list(item_list=[qw, qx, qy, qz], valid_type_list=number_types)
        self.qw = qw
        self.qx = qx
        self.qy = qy
        self.qz = qz

    def __str__(self) -> str:
        return f"Quaternion({self.qw},{self.qx},{self.qy},{self.qz})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_list(self) -> list:
        return [self.qw, self.qx, self.qy, self.qz]

    @classmethod
    def from_list(self, val_list: list) -> Quaternion:
        qw, qx, qy, qz = val_list
        return Quaternion(qw=qw, qx=qx, qy=qy, qz=qz)

    def to_euler(self, seq: str='xyz') -> EulerAngle:
        return EulerAngle.from_list(Rotation.from_quat(self.to_list()).as_euler(seq=seq).tolist())