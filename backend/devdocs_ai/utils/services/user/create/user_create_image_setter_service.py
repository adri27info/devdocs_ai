import requests
import uuid

from django.core.files.base import ContentFile

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class UserCreateImageSetterService:
    """
    Service to assign a random profile image to a user using RandomUser API."""

    __RANDOM_USER_API = "https://randomuser.me/api/"
    __TIMEOUT = 2

    @classmethod
    def run(cls, *, user):
        """
        Fetches a random user image and assigns it to the given user's attachment.

        Args:
            user (User): User instance to assign the image to.

        Logs:
            Any request exceptions during image fetching.
        """
        try:
            session = requests.Session()
            retry = Retry(total=0)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)

            response = session.get(cls.__RANDOM_USER_API, timeout=cls.__TIMEOUT)
            response.raise_for_status()
            photo_url = response.json()['results'][0]['picture']['large']

            img_response = session.get(photo_url, timeout=cls.__TIMEOUT)
            img_response.raise_for_status()

            new_file = ContentFile(img_response.content)
            filename = f"profile_{uuid.uuid4().hex}.jpg"
            user.attachment.save(filename, new_file, save=True)

        except requests.RequestException as e:
            LOGGER.error(f"Error fetching image for {user.email}: {e}")
