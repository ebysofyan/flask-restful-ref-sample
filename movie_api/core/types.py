import enum


class EnumClass(enum.Enum):
    def __str__(self) -> str:
        return self.value

    @classmethod
    def get_type(cls, value: str) -> "EnumClass":
        return cls._value2member_map_[value]
