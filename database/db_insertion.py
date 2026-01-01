
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

    sql_query = ("INSERT INTO fct_Telemetry ("
                "MachineID, "
                "DateKey, "
                "Timestamp, "
                "Temperature, "
                "VibrationLevel, "
                "RPM, "
                "PowerUsage"
            ") "
             "VALUES ("
                "?,"
                "?,"
                "?,"
                "?,"
                "?,"
                "?,"
                "?,"
             ")")

    cursor = conn.cursor()
    cursor.execute(sql_query, machine_id, date_key, timestamp, temperature, vibration_level, rpm, power_usage)
    print(f'[LOG]: Insertion to fct_Telemetry: MachineID :{machine_id} | DateKey: {date_key} '
          f'| Timestamp: {timestamp} | Temperature: {temperature} | VibrationLevel: {vibration_level} '
          f'| RPM: {rpm} | PowerUsage: {power_usage}')
    conn.commit()

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
                    "?,"
                 ")"
                 )

    cursor = conn.cursor()
    cursor.execute(sql_query, machine_id, failure_id, start_time, end_time, state_code)
    print(f'[LOG]: Insertion to fct_Telemetry: MachineID :{machine_id} | FailureID: {failure_id} '
          f'| StartTime: {start_time} | EndTime: {end_time} | StateCode: {state_code} ')
    conn.commit()