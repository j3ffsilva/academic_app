from models.db_credentials import get_session
from sqlalchemy.exc import IntegrityError

class BaseDAO(object):
    """
    A Base class for all managers. Automatically handles session creation,
    the commiting and closing the connections.
    """
    def __init__(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Constructor
        """
        self._session = get_session() if (not session) else session
        self._commit_on_exit = commit_on_exit
        self._close_on_exit = close_on_exit

    def __enter__(self):
        """
        On enter
        """
        return self

    def __exit__(self, *exc_info):
        """
        On exit
        """
        if (self._session and self._commit_on_exit):
            try:
                # Connection must be closed when an exception happens here
                self._session.commit()
            except IntegrityError as e:
                self._session.close()
                raise e
        if (self._session and self._close_on_exit):
            self._session.close()

    def session(self):
        """
        Returns the session
        """
        return self._session
