from typing import Any, Dict, List

from flask import request
from flask.wrappers import Request
from flask_sqlalchemy import Pagination

from movie_api.db.schemas import marsh


class PageNumberPaginationMixin:
    per_page = 10
    schema_class = None
    response_message = "Successfully fetch pagination data"

    @property
    def request(self) -> Request:
        return request

    @property
    def host(self) -> str:
        return self.request.host_url

    def get_schema_class(self, **kwargs) -> Any:
        if not self.schema_class:
            raise NotImplementedError("schema_class should not be NoneType")

        subclasses = (marsh.Schema, marsh.SQLAlchemySchema, marsh.SQLAlchemyAutoSchema)
        if not issubclass(self.schema_class, subclasses):
            raise Exception("schema_class should be subcalss of %s" % subclasses)

        return self.schema_class(**kwargs)

    def get_raw_current_query_params(self):
        for arg in self.request.args.items():
            yield "{}={}".format(*arg)

    def next_prev_url_builder(
        self, pagination: Pagination, queryparams: str, next_or_prev_page: int
    ) -> str:
        queryparams = queryparams.replace(
            "page=%s" % pagination.page, "page=%s" % next_or_prev_page
        )
        return "".join([self.request.base_url, "?", queryparams])

    def get_next_url(self, pagination: Pagination, queryparams: str) -> str:
        if not pagination.has_next:
            return None
        return self.next_prev_url_builder(pagination, queryparams, pagination.next_num)

    def get_prev_url(self, pagination: Pagination, queryparams: str) -> str:
        if not pagination.has_prev:
            return None
        return self.next_prev_url_builder(pagination, queryparams, pagination.prev_num)

    @property
    def current_page(self) -> int:
        try:
            if len(self.search_filters) > 0:
                return 1
            return int(self.request.args.get("page", 1))
        except ValueError:
            return 1

    @property
    def filtersets(self) -> List:
        return []

    @property
    def search_filters(self) -> List:
        return []

    @property
    def ordering(self) -> Dict:
        return {}

    @property
    def current_query_params(self):
        return "&".join(self.get_raw_current_query_params())

    def make_pagination_response(self, pagination: Pagination) -> Dict:
        return {
            "detail": self.response_message,
            "data": {
                "page": pagination.page,
                "next": self.get_next_url(pagination, self.current_query_params),
                "previous": self.get_prev_url(pagination, self.current_query_params),
                "total_pages": pagination.pages,
                "total_results": pagination.total,
                "results": self.get_schema_class().dump(pagination.items, many=True),
            },
        }
