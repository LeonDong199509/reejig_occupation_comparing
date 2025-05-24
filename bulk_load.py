import logging
import os
from helpers.db import connect
from concurrent.futures import ThreadPoolExecutor

# Configure logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Directory where CSV files are stored
DATA_DIR = "data/bulk"

# Mapping of table name to (filename, columns)
CSV_FILES_1 = {
    "occupations": ("occupations.csv", "occupation_code, title"),
    "skills": ("skills.csv", "skill_id, name"),
}

CSV_FILES_2 = {
    "occupation_skills": ("occupation_skills.csv", "occupation_code, skill_id"),
}


def load_file(table_name: str, filename: str, columns: str):
    """
    Load data from a single CSV file into the specified MySQL table.

    Args:
        table_name (str): Name of the MySQL table to load data into.
        filename (str): Name of the CSV file containing the data.
        columns (str): Comma-separated list of column names in the file.
    """
    abs_path = os.path.abspath(os.path.join(DATA_DIR, filename)).replace("\\", "\\\\")
    conn = connect()
    try:
        with conn.cursor() as cursor:
            query = f"""
                LOAD DATA LOCAL INFILE '{abs_path}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY '\\t'
                LINES TERMINATED BY '\\n'
                ({columns});
            """
            logging.info(f"[{table_name}] Loading data from {filename}...")
            logging.info(f"running query: {query} ...")
            cursor.execute(query)
            conn.commit()
            logging.info(f"[{table_name}] Load complete.")
    except Exception as e:
        logging.error(f"[{table_name}] Error: {e}")
    finally:
        conn.close()


def main():
    """
    Run the bulk load process concurrently for all defined CSV files using ThreadPoolExecutor.
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(load_file, table, filename, columns)
            for table, (filename, columns) in CSV_FILES_1.items()
        ]
        for future in futures:
            future.result()  # Will raise any exception that occurred

    # Load the second set of files, which are dependent on CSV_FILES_1
    for table, (filename, columns) in CSV_FILES_2.items():
        load_file(table, filename, columns)

    logging.info("All loads complete.")


if __name__ == "__main__":
    main()
