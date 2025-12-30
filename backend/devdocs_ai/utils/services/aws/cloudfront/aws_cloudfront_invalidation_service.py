import time
import boto3

from django.conf import settings

from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class AWSCloudFrontInvalidationService:
    """
    Service to invalidate CloudFront cache for given paths.
    """

    @staticmethod
    def run(*, paths):
        """
        Creates a CloudFront cache invalidation for the specified paths.

        Args:
            paths (Union[str, list[str]]): Single path or list of paths to invalidate.

        Returns:
            int: Number of paths submitted for invalidation.
        """
        if isinstance(paths, str):
            paths = [paths]
        paths = [f"/{path.lstrip('/')}" for path in paths]

        client = boto3.client("cloudfront")
        client.create_invalidation(
            DistributionId=getattr(settings, "CLOUDFRONT_DISTRIBUTION_ID", None),
            InvalidationBatch={
                "Paths": {
                    "Quantity": len(paths),
                    "Items": paths,
                },
                "CallerReference": str(time.time()),
            },
        )
        return len(paths)
