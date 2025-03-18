import pypyodbc as odbc

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = '192.168.192.88\\A2006'
DATABASE_NAME = 'MACC'
USER_NAME = 'panda_dev'
PASSWORD = 'panda123'

connection_string = f"""
        DRIVER={DRIVER_NAME};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trusted_Connection=yes;
    """

def retrieve_data(connection_string, status):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM Pallet 
        WHERE rec_stat = ?
        """,
        (status,)
        )
    rows = cursor.fetchall()
    zlinx_data = {"ZLINXDATA": []}  # Initialize parent object with a list

    for row in rows:
        rec_stat, term_id, pallet_id, model, serial, prd_date, prd_time, prd_line, order_in, dater, datetime_str, date_fill = row
        
        # Create a dictionary for each record
        entry = {
            "ZLINENO": prd_line.strip(),
            "PALLID": pallet_id.strip(),
            "MATERIAL": model.strip(),
            "SERIAL": serial.strip()
        }
        
        zlinx_data["ZLINXDATA"].append(entry) 

    with open("LinxProductOutput.txt", "w") as file:
        file.write(json.dumps(zlinx_data, indent=4))
        # trigger api waiting for response

        # if response:
            # update_pallet_status(connection_string, serial)

def update_pallet_status(connection_string, serial):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Pallet 
        SET rec_stat = 'D'
        WHERE Serial = ?
        """,
        (serial,)
        )

    conn.commit()
    cursor.close()
    conn.close()

# retrieve_data(connection_string, 'O')
# update_pallet_status(connection_string, '4914100057')
