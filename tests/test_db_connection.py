import unittest
import pymysql


class TestMySQLConnection(unittest.TestCase):
    def setUp(self):
        """Set up the MySQL connection before each test."""
        self.conn = pymysql.connect(
            host="localhost",  # or "mysql" if using Docker Compose service name
            user="root",
            password="password",
            database="reejig_occupation_api",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def tearDown(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_connection_and_list_tables(self):
        """Test connection and ensure the correct tables exist."""
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