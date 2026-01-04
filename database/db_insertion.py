
def telemetry_insertion(conn, machine_id, date_key, timestamp, temperature, vibration_level, rpm, power_usage):
    """
    Function that inserts given values to fct_Telemetry table in SmartFactory database.
    It also prints info log about values being inserted to this table. All params are generated in python simulator.

    :param conn:
    :param machine_id:
    :param date_key:
    :param timestamp:
    :param temperature:
    :param vibration_level:
    :param rpm:
    :param power_usage:
    :return:
    """
    sql_query = ("EXEC LoadTelemetry @MachineID=?, @DateKey=?, @Timestamp=?, @Temperature=?, @VibrationLevel=?, @RPM=?, "
                 "@PowerUsage=?")

    cursor = conn.cursor()
    cursor.execute(sql_query, machine_id, date_key, timestamp, temperature, vibration_level, rpm, power_usage)
    print(f'[LOG]: Insertion to fct_Telemetry: MachineID :{machine_id} | DateKey: {date_key} '
          f'| Timestamp: {timestamp} | Temperature: {temperature} | VibrationLevel: {vibration_level} '
          f'| RPM: {rpm} | PowerUsage: {power_usage}')

def machine_events_insertion(conn, machine_id, failure_id, start_time, end_time, state_code):
    """
    Function that inserts given values to fct_MachineEvents table in SmartFactory database.
    It also prints info log about values being inserted to this table. All params are generated in python simulator.
    :param conn:
    :param machine_id:
    :param failure_id:
    :param start_time:
    :param end_time:
    :param state_code:
    :return:
    """

    sql_query = ("INSERT INTO fct_MachineEvents ("
                    "MachineID,"
                    "FailureID,"
                    "StartTime,"
                    "EndTime,"
                    "StateCode"
                 ")"
                 "VALUES ("
                    "?,"
                    "?,"
                    "?,"
                    "?,"
                    "?"
                 ")"
                 )

    cursor = conn.cursor()
    cursor.execute(sql_query, machine_id, failure_id, start_time, end_time, state_code)
    print(f'[LOG]: Insertion to fct_MachineEvents: MachineID :{machine_id} | FailureID: {failure_id} '
          f'| StartTime: {start_time} | EndTime: {end_time} | StateCode: {state_code} ')


def machine_events_update(conn, end_time, machine_id):
    """
    Function that inserts given values to fct_MachineEvents table in SmartFactory database.
    It also prints info log about values being inserted to this table. All params are generated in python simulator.
    :param conn:
    :param machine_id:
    :param end_time:
    :return:
    """

    sql_query = "UPDATE fct_MachineEvents SET EndTime = ? WHERE EndTime IS NULL AND MachineID = ?"

    cursor = conn.cursor()
    cursor.execute(sql_query, end_time, machine_id)
    print(f'[LOG]: Update in MachineEvents: MachineID :{machine_id} '
          f' | EndTime: {end_time}')

def production_output_insertion(conn, machine_id, product_id, date_key, timestamp, is_good, is_scrap):
    sql_query = """
    INSERT INTO fct_ProductionOutput (MachineID, ProductID, DateKey, Timestamp, IsGood, IsScrap)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(sql_query, machine_id, product_id, date_key, timestamp, is_good, is_scrap)