import json
from datetime import datetime
from typing import Any, Dict, Type, TypeVar
from uuid import uuid4

from sqlalchemy import TIMESTAMP, BigInteger, Column, Float
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.sql import func

import movie_api.extensions as extensions

DB = extensions.db
scoped_session: ScopedSession = DB.session


class DictMixin:
    RELATIONSHIPS_TO_DICT = False

    def to_dict(self, rel=None, backref=None) -> Dict:
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {
            column.key: getattr(self, attr)
            for attr, column in self.__mapper__.c.items()
        }
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [
                        i.to_dict(backref=self.__table__) for i in value
                    ]
        return res

    def as_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self, rel=None) -> str:
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)

    def to_json_object(self, rel=None) -> Dict:
        return json.loads(self.to_json(rel=rel))


_T = TypeVar("_T", bound="BaseModel")


class BaseModel(DB.Model, DictMixin):
    __abstract__ = True
    _session = None

    @property
    def session(self) -> ScopedSession:
        return self._session or DB.session

    @session.setter
    def set_session(self, value: Any) -> None:
        if not isinstance(value, (Session, ScopedSession)):
            raise Exception(
                "set_session value should be Session or ScopedSession instance"
            )
        self._session = value

    def save(self, flush: bool = True, commit: bool = True) -> _T:
        self.session.add(self)
        if flush:
            self.session.flush()
        if commit:
            self.session.commit()
        return self

    def delete(self, commit: bool = True) -> _T:
        self.session.delete(self)
        if commit:
            self.session.commit()
        return self

    def refresh_from_db(self) -> _T:
        self.session.refresh(self)
        return self

    @classmethod
    def add(cls: Type[_T], **kwargs) -> _T:
        instance = cls(**kwargs)
        instance.session.add(instance=instance)
        return instance

    @classmethod
    def create(cls: Type[_T], **kwargs) -> _T:
        commit = kwargs.get("commit", True)
        if "commit" in kwargs:
            commit = kwargs.pop("commit")
        return cls(**kwargs).save(commit=commit)

    def commit(self, close_session: bool = False) -> None:
        self.session.commit()
        if close_session:
            self.session.remove()


class TimeStampedModel(BaseModel):
    __abstract__ = True

    time_created = Column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    time_updated = Column(TIMESTAMP(timezone=True), onupdate=func.current_timestamp())


class BaseIntPrimaryModel(TimeStampedModel):
    __abstract__ = True
    id = Column(BigInteger(), primary_key=True, autoincrement=True)


class BaseUuidPrimaryModel(TimeStampedModel):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
