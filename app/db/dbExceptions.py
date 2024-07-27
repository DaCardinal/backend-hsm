from sqlite3 import IntegrityError as SQLiteIntegrityError
from pymysql import IntegrityError as PYIntegrityError
from asyncpg.exceptions import ForeignKeyViolationError, IntegrityConstraintViolationError


class DatabaseConnectionException(Exception):
    def __init__(self, pymysql_msg):
        self.msg = "Failed Connecting to database, please check credentials and, or connectivity"
        self.msg += "\n" + str(pymysql_msg)
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class DatabaseCredentialException(Exception):
    def __init__(self, key_, msg=""):
        if msg:
            self.msg = msg
        else:
            self.msg = "{} is required".format(key_)
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class RecordNotFoundException(Exception):
    def __init__(self, msg="The record does not exist"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class IntegrityError(PYIntegrityError, SQLiteIntegrityError, IntegrityConstraintViolationError):
    def __init__(self, err_msg="Integrity error during SQL operation."):
        self.msg = err_msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
