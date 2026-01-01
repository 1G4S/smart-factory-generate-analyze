from datetime import datetime
from data_generator import get_column, generate_machines_data
from database.db_connector import connect_db
from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == "__main__":
    DRIVER = os.getenv('DRIVER')
    SERVER = os.getenv('SERVER')
    DATABASE = os.getenv('DATABASE')

    conn = connect_db(DRIVER, SERVER, DATABASE)
    machines_id = get_column(conn, 'dim_Machines', 'MachineID')
    failures_id = get_column(conn, 'dim_FailureCodes', 'FailureID')
    amount_of_rows = 400000
    start_date = datetime(2026, 1, 1, 6, 0, 0)
    generate_machines_data(amount_of_rows, start_date, conn, machines_id, failures_id)