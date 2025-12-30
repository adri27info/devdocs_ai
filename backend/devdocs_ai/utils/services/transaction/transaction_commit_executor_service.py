from django.db import transaction


class TransactionCommitExecutorService:
    """
    Service to schedule functions to run after a database commit.
    """

    @staticmethod
    def run(func, *args, **kwargs):
        """
        Schedules a function to execute after the current transaction commits.

        Args:
            func (Callable): Function to run after commit.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        transaction.on_commit(lambda: func(*args, **kwargs))
