import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    host = os.getenv("DB_HOST", "mysql")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("MYSQL_ROOT_PASSWORD", "1234")
    database = os.getenv("MYSQL_DATABASE", "weapon_db")
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weapons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        weapon_id VARCHAR(255),
        weapon_name VARCHAR(255),
        weapon_type VARCHAR(255),
        range_km INT,
        weight_kg FLOAT,
        manufacturer VARCHAR(255),
        origin_country VARCHAR(255),
        storage_location VARCHAR(255),
        year_estimated INT,
        risk_level VARCHAR(50)
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()

def insert_data(connection, df):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO weapons (weapon_id, weapon_name, weapon_type, range_km, weight_kg, 
                         manufacturer, origin_country, storage_location, year_estimated, risk_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    records = df.to_records(index=False)
    cursor.executemany(insert_query, records)
    connection.commit()
    return cursor.rowcount