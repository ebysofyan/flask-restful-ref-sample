import dataclasses
from typing import Any, Dict

from dacite import from_dict


class DataClassMixin:
    @classmethod
    def from_dict(cls, dict_data: Dict):
        return from_dict(data_class=cls, data=dict_data)

    def asdict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)
