import enum


class BaseEnumClass(enum.Enum):
    def __str__(self) -> str:
        return self.value

    @classmethod
    def get_type(cls, value):
        return cls._value2member_map_[value]
