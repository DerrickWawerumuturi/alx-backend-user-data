#!/usr/bin/env python3
""" Regex-ing
"""
import re
import logging
import os
import mysql.connector as db


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ("name", "email", "phone", "ssn", "password,")


def filter_datum(
    fields: list[str],
    redaction: str,
    message: str,
    separator: str
):
    """ returns the log message
    """
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger():
    """ returns logging.Logger object
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> db.connection.MySQLConnection:
    """ returns a connector the database
    """
    dbName = os.getenv('PERSONAL_DATA_DB_NAME', "")
    dbUsername = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    dbHost = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbPwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = db.connect(
        host=dbHost,
        port=3306,
        user=dbUsername,
        password=dbPwd,
        database=dbName
    )

    return connection


def main():
    """ obtains a db connection and retrieves all rows
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(",")
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row)
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formats a log record
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == '__main__':
    main()
