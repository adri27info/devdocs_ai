from utils.exceptions.instance.instance_exceptions import InstanceInvalidValueException
from utils.services.response.response_checker_type_service import ResponseCheckerTypeService


class ResponseHandlerService:
    @staticmethod
    def run(*, response, data=None):
        """
        Format and update a DRF Response object with provided data and status code.

        This method validates the response and the data. If the response status is
        successful (<400), it updates the response data and status code.

        Args:
            response (Response): The DRF Response object to be updated.
            data (dict, optional): The data to attach to the response. Must include
                a 'status_code' key if you want to override the response status.

        Raises:
            InstanceInvalidValueException: If data is missing or response is invalid.

        Returns:
            Response: The modified DRF Response object with updated data and status.
        """
        if not data:
            raise InstanceInvalidValueException("Data is invalid or missing")

        if not ResponseCheckerTypeService.run(response=response):
            raise InstanceInvalidValueException("Response is invalid or missing")

        if response.status_code < 400:
            response.status_code = data.pop("status_code", response.status_code)
            response.data = data
            return response
        else:
            return response
