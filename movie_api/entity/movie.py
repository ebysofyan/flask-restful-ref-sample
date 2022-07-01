import dataclasses as dc
import datetime
from dataclasses import field
from typing import List, Optional

from movie_api.core.mixins.dataclass import DataClassMixin


@dc.dataclass
class MovieEntity(DataClassMixin):
    title: str
    description: Optional[str] = None
    genre_id: Optional[str] = None
    image_url: Optional[str] = None
    year: Optional[int] = datetime.datetime.now().year
    tags: Optional[List[str]] = field(default_factory=lambda: [])
