import pyodbc

def connect_db(driver, server, database):
    """
    Function that allows to connect to local database.

    :param driver: Name of the driver on local db
    :param server: Name of server on local db
    :param database: Name of local db
    :return: Connection to database
    """
    connection_string = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
        f'TrustServerCertificate=yes;'
    )
    try:
        conn = pyodbc.connect(connection_string, timeout=15)
        print('Connection to the database established!')

    except pyodbc.Error as e:
        print('There was an error during connection!')
        raise e

    return conn
