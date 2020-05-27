import enum


class CustomEnum(enum.Enum):

    @classmethod
    def get_all_enum_values(cls):
        """获取所有枚举值"""

        return [i.value for i in cls.__members__.values()]

    @classmethod
    def get_all_enum_keys(cls):
        """获取所有枚举键"""

        return list(cls.__members__.keys())

    @classmethod
    def get_enum_dict(cls):
        """获取枚举字典"""

        return {
            k: v.value
            for k, v in cls.__members__.items()
        }


if __name__ == '__main__':

    class E(CustomEnum):
        A = 1
        B = 2

    print(E.get_all_enum_values())
    print(E.get_all_enum_keys())
    print(E.get_enum_dict())
