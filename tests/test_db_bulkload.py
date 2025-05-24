import unittest
import pymysql


class TestMySQLBulkLoad(unittest.TestCase):
    def setUp(self):
        """Set up the MySQL connection before each test."""
        self.conn = pymysql.connect(
            host="localhost",  # or "mysql" if using Docker Compose
            user="root",
            password="password",
            database="reejig_occupation_api",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def tearDown(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_tables_exist(self):
        """Check that all expected tables exist in the database."""
        expected_tables = {"occupations", "skills", "occupation_skills"}
        with self.conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            rows = cursor.fetchall()
            actual_tables = {list(row.values())[0] for row in rows}

        print("Tables in the database:", actual_tables)
        self.assertEqual(
            actual_tables,
            expected_tables,
            f"Expected tables {expected_tables}, but found {actual_tables}"
        )

    def test_row_counts(self):
        """Verify the expected row counts in each table."""
        expected_counts = {
            "occupations": 1016,
            "skills": 35,
            "occupation_skills": 27463,
        }

        with self.conn.cursor() as cursor:
            for table, expected_count in expected_counts.items():
                cursor.execute(f"SELECT COUNT(*) AS count FROM {table};")
                result = cursor.fetchone()
                actual_count = result["count"]

                print(f"{table}: expected {expected_count}, got {actual_count}")
                self.assertEqual(
                    actual_count,
                    expected_count,
                    f"Table {table} should have {expected_count} rows, but has {actual_count}"
                )