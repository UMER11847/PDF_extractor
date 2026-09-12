import sqlite3


DATABASE_NAME = "datasets.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            dataset_details TEXT,
            data_types TEXT,
            modalities TEXT,
            tasks TEXT,
            licensing_information TEXT,
            source_url TEXT,
            verification_status TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_dataset(dataset):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO datasets (
            dataset_name,
            dataset_details,
            data_types,
            modalities,
            tasks,
            licensing_information,
            source_url,
            verification_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dataset["dataset_name"],
        str(dataset["dataset_details"]),
        ", ".join(dataset["data_types"]),
        ", ".join(dataset["modalities"]),
        ", ".join(dataset["tasks"]),
        dataset["licensing_information"],
        dataset["source_url"],
        dataset["verification_status"]
    ))

    connection.commit()
    connection.close()


def get_all_datasets():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM datasets")

    rows = cursor.fetchall()

    connection.close()

    return rows
