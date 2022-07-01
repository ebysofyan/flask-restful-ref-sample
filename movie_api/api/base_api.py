from typing import Any, Dict, Optional, Tuple, Union

from flask.globals import request
from flask.helpers import make_response
from flask_apispec.views import MethodResource
from flask_restful import Resource

from movie_api.core.exceptions import QuokkaException


class BaseApi(MethodResource, Resource):
    """
    :permission_classes: is sets of permission who can access the resource
        it could be a using AND / OR operator.
        AND -> permission_classes = (IsAuthenticated & IsAdminUser, )
        OR -> permission_classes = (IsAdminUser | IsStaffUser, )
    """

    __info__ = "Base API class"

    @property
    def page(self) -> int:
        """
        property for getting page
        :return: int
        """
        return int(request.args.get("page", "0"))

    @property
    def limit(self) -> int:
        """
        property for getting limit
        :return: int
        """
        return int(request.args.get("limit", "10"))

    def get(self, **kwargs) -> Union[Optional[Dict[str, Any]], Tuple]:
        raise QuokkaException(code=405, description="Method not allowed")

    def post(self, **kwargs) -> Union[Optional[Dict[str, Any]], Tuple]:
        raise QuokkaException(code=405, description="Method not allowed")

    def put(self, **kwargs) -> Union[Optional[Dict[str, Any]], Tuple]:
        raise QuokkaException(code=405, description="Method not allowed")

    def delete(self, **kwargs) -> Union[Optional[Dict[str, Any]], Tuple]:
        raise QuokkaException(code=405, description="Method not allowed")

    def make_response(
        self,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        status: int = 200,
    ) -> Dict[str, Any]:
        message = message if message else "Success"
        response = {"message": message, "data": data}
        return make_response(response, status)
