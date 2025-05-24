import pymysql
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def fetch_skill_counts():
    query = """
    SELECT 
        occupation_code,
        COUNT(DISTINCT skill_id) AS skill_count
    FROM 
        occupation_skills
    GROUP BY 
        occupation_code
    ORDER BY 
        skill_count ASC;
    """

    try:
        conn = pymysql.connect(
            host="localhost",  # or "mysql" if using Docker Compose
            user="root",
            password="password",
            database="reejig_occupation_api",
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cursor:
            logging.info("Running skill count query...")
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(f"{row['occupation_code']}: {row['skill_count']} skills")
    except Exception as e:
        logging.error(f"Error executing query: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    fetch_skill_counts()