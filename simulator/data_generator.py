from datetime import timedelta

from database.db_insertion import (telemetry_insertion, machine_events_insertion,
                                   machine_events_update, production_output_insertion)
import random


def fetch_machine_config(conn):

    cursor = conn.cursor()

    cursor.execute("SELECT ProductID, IdealCycleTime_sec FROM dim_Products")
    products_info = {row[0]: float(row[1]) for row in cursor.fetchall()}

    cursor.execute("SELECT MachineID, LineID FROM dim_Machines")
    machines = cursor.fetchall()

    machine_config = {}

    for m_id, line_id in machines:

        if line_id == 1:
            p_id = 1
        elif line_id == 2:
            p_id = 3
        elif line_id == 3:
            p_id = 3
        else:
            p_id = 1

        cycle_time = products_info.get(p_id, 60.0)

        machine_config[m_id] = {
            'product_id': p_id,
            'cycle_time': cycle_time
        }

    return machine_config


def get_column(conn, table_name, column_name):
    allowed_tables = {'dim_Machines', 'dim_Lines', 'dim_FailureCodes', 'dim_Products', 'dim_Shifts'}

    if table_name not in allowed_tables:
        raise ValueError('Niedozwolona tabela!')

    sql_query = f"SELECT {column_name} FROM {table_name}"

    cursor = conn.cursor()
    cursor.execute(sql_query)
    column_values = [i[0] for i in cursor.fetchall()]

    return column_values


def generate_telemetry_data(machine_status):
    if machine_status == 'RUNNING':
        # W tym przypadku dane są normalne

        temperature = random.uniform(60.0, 90.0)
        vibration_level = random.uniform(0.1, 3.5)
        rpm = random.uniform(1400, 1600)
        power_usage = random.uniform(10.0, 18.0)
        return temperature, vibration_level, rpm, power_usage

    else:
        # Dane postojowe

        temperature = random.uniform(0.0, 60.0)
        rpm = 0
        vibration_level = 0
        power_usage = 0
        return temperature, vibration_level, rpm, power_usage


def generate_machines_data(amount_of_rows, start_date, conn, machines_id, failures_id):
    rows_count_telemetry = 0
    rows_count_events = 0
    rows_count_production = 0
    machines_status = {m_id: 'RUNNING' for m_id in machines_id}
    machines_cycle_progress = {m_id: 0.0 for m_id in machines_id}
    machine_config = fetch_machine_config(conn)

    for i in range(amount_of_rows):
        time_step = random.randint(5, 15)
        start_date += timedelta(seconds=time_step)
        date_key = int(start_date.strftime('%Y%m%d'))
        for machine in machines_id:
            config = machine_config.get(machine)
            cycle_time = config['cycle_time']
            product_id = config['product_id']
            machine_status = machines_status[machine]
            if machine_status == 'RUNNING':
                temperature, vibration_level, rpm, power_usage = generate_telemetry_data(machine_status)

                if random.random() < 0.0005:
                    machines_status[machine] = 'BROKEN'
                    machines_cycle_progress[machine] = 0.0
                    rows_count_events += 1
                    temperature, vibration_level, rpm, power_usage = generate_telemetry_data(machine_status)
                    failure_id = random.choice(failures_id)
                    end_time = None
                    machine_events_insertion(conn, machine, failure_id, start_date, end_time, machine_status)

            else:
                temperature, vibration_level, rpm, power_usage = generate_telemetry_data(machine_status)

                if random.random() < 0.01:
                    rows_count_events += 1
                    machines_status[machine] = 'RUNNING'
                    temperature, vibration_level, rpm, power_usage = generate_telemetry_data(machine_status)
                    end_time = start_date
                    machine_events_update(conn, end_time, machine)

            if machine_status == 'RUNNING':
                machines_cycle_progress[machine] += time_step

                if machines_cycle_progress[machine] >= cycle_time:

                    if random.random() < 0.98:
                        is_good, is_scrap = 1, 0
                    else:
                        is_good, is_scrap = 0, 1

                    production_output_insertion(conn, machine, product_id, date_key, start_date, is_good, is_scrap)
                    rows_count_production += 1

            if random.random() < 0.001:
                anomaly_type = random.choice(['HIGH_TEMP', 'NEG_VIB', 'NEG_RPM'])
                if anomaly_type == 'HIGH_TEMP':
                    temperature = 999.9
                elif anomaly_type == 'NEG_VIB':
                    vibration_level = -5.0
                elif anomaly_type == 'NEG_RPM':
                    rpm = -100

            telemetry_insertion(conn, machine, date_key, start_date, temperature, vibration_level, rpm, power_usage)
            rows_count_telemetry += 1

        if rows_count_telemetry % 1000 == 0:
            conn.commit()

    conn.commit()
    print(f'Załadowano: {rows_count_telemetry} wierszy do tabeli fct_Telemetry!')
    print(f'Załadowano: {rows_count_events} wierszy do tabeli fct_MachineEvents!')
    print(f'Załadowano: {rows_count_production} wierszy do tabeli fct_ProductionOutput!')