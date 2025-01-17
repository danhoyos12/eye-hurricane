import duckdb as db
import pandas as pd


def process_txt_data(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    hurricane_id = ""
    hurricane_name = ""
    hurricane_number = ""
    
    data = []

    for line in lines:
        line = line.strip()
        if line.startswith("AL"):
            parts = line.split(',')
            hurricane_id = parts[0].strip()
            hurricane_name = parts[1].strip()
            hurricane_number = parts[2].strip()
        else:
            if line:
                data_parts = line.split(',')
                data_row = [hurricane_id, hurricane_name, hurricane_number] + [part.strip() for part in data_parts]
                data.append(data_row)

    columns = ['hurricane_id', 'hurricane_name', 'hurricane_number', 'date', 'time', 'record_id', 'status',
               'latitude', 'longitude', 'max_wind_knots', 'min_pressure_mbar', 'ne_34kt_wind_nm', 
               'se_34kt_wind_nm', 'sw_34kt_wind_nm', 'nw_34kt_wind_nm', 'ne_50kt_wind_nm', 
               'se_50kt_wind_nm', 'sw_50kt_wind_nm', 'nw_50kt_wind_nm', 'ne_64kt_wind_nm', 
               'se_64kt_wind_nm', 'sw_64kt_wind_nm', 'nw_64kt_wind_nm', 'max_wind_radius_nm']

    df = pd.DataFrame(data, columns=columns)

    return df


# insert data into a relevant table
def insert_hurricane_data(df, db_path='hurricane_data.db', table_name='hurricanes'):

    con = db.connect(db_path)
    
    con.execute(f"""
    DROP TABLE IF EXISTS {table_name};

    CREATE TABLE {table_name} (
        hurricane_id VARCHAR,
        hurricane_name VARCHAR,
        hurricane_number INTEGER,
        date VARCHAR,
        time VARCHAR,
        record_id VARCHAR,
        status VARCHAR,
        latitude VARCHAR,
        longitude VARCHAR,
        max_wind_knots INTEGER,
        min_pressure_mbar INTEGER,
        ne_34kt_wind_nm INTEGER,
        se_34kt_wind_nm INTEGER,
        sw_34kt_wind_nm INTEGER,
        nw_34kt_wind_nm INTEGER,
        ne_50kt_wind_nm INTEGER,
        se_50kt_wind_nm INTEGER,
        sw_50kt_wind_nm INTEGER,
        nw_50kt_wind_nm INTEGER,
        ne_64kt_wind_nm INTEGER,
        se_64kt_wind_nm INTEGER,
        sw_64kt_wind_nm INTEGER,
        nw_64kt_wind_nm INTEGER,
        max_wind_radius_nm INTEGER
    );
    """)

    con.register('hurricane_df_view', df)  
    con.execute(f"""
    INSERT INTO {table_name}
    SELECT * FROM hurricane_df_view;
    """)

    print(f"Data successfully inserted into {table_name} in {db_path}.")

# running queries against are newly made table
def run_query(query, connection):
    con = db.connect(connection)
    return con.execute(query).df()

def list_tables(connection):
    # returns a list of tables from the db
    con = db.connect(connection)
    return con.execute("SHOW TABLES").df()

def describe_table(table_name,connection):
    # describes a given table from the db
    con = db.connect(connection)
    return con.execute(f"DESCRIBE {table_name}").df()