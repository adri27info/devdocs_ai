from django.db import transaction


class TransactionExecutorService:
    """
    Service to execute database operations within an atomic transaction.
    """

    @staticmethod
    def run(*, db_ops, next_ops=None):
        """
        Executes DB operations atomically and optionally runs additional operations.

        Args:
            db_ops (Callable): Primary database operation to execute within a transaction.
            next_ops (Callable or Iterable[Callable], optional): Additional operations
                to run after `db_ops`. Defaults to None.

        Returns:
            tuple: (result of db_ops, list of results of next_ops)
        """
        with transaction.atomic():
            db_result = db_ops()

            if next_ops:
                if callable(next_ops):
                    next_ops_list = [next_ops]
                else:
                    next_ops_list = list(next_ops)
                next_results = [op() for op in next_ops_list]
            else:
                next_results = []

        return db_result, next_results
