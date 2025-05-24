import pymysql.cursors


def connect():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        pymysql.connections.Connection: MySQL database connection object.
    """
    return pymysql.connect(
        host="mysql",
        user="root",
        password="password",
        database="reejig_occupation_api",
        local_infile=True,  # Allows LOAD DATA LOCAL INFILE
        cursorclass=pymysql.cursors.Cursor
    )