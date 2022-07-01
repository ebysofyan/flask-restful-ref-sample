import logging
import os
from typing import Dict, Optional, Tuple

from werkzeug.exceptions import HTTPException


class QuokkaException(HTTPException):
    errors_data = None

    def __init__(
        self, code: int, description: Optional[str], errors_data: Optional[Dict] = None
    ) -> None:
        """
        If you want to add errors_data to the response, pls use this format
        ```errors_data = {
           'fieldname': [
              'error_message1',
              'error_message2',
          ]}
        QuokkaException(400, "error_message", errors_data)
        ```
        """

        self.code = code
        self.description = description
        self.errors_data = errors_data
        return super().__init__()


def make_exception(e: Exception) -> Tuple:
    response, code = {"message": "Something went wrong", "data": None}, 500
    if isinstance(e, QuokkaException):
        response["message"] = e.description
        response["data"] = e.errors_data
        code = e.code
    else:
        response["message"] = str(e)

    if os.getenv("ENV").lower() in ["local", "development", "testing"]:
        logging.warning(response, code)
    return response, code
