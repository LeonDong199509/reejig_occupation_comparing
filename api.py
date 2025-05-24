import logging
from fastapi import FastAPI, Query, HTTPException
from typing import List
from helpers.db import connect


app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)


@app.get("/skill-gap", summary="Get skill gap between two occupations", response_description="List of skill names")
def get_skill_gap(
    from_code: str = Query(
        ...,
        alias="from",
        pattern=r"^\d{2}-\d{4}\.\d{2}$",
        description="Occupation code to compare from (e.g. 47-2231.00)"
    ),
    to_code: str = Query(
        ...,
        alias="to",
        pattern=r"^\d{2}-\d{4}\.\d{2}$",
        description="Occupation code to compare to (e.g. 47-2061.00)"
    )
) -> List[str]:
    """
    Compare skills between two occupations and return the skill names that are
    required by the target occupation but not by the source occupation.
    """
    logger.info(f"Received skill gap request: from_code={from_code}, to_code={to_code}")

    conn = connect()
    try:
        with conn.cursor() as cursor:
            # Find skill names in to_code that are not in from_code in a single query
            cursor.execute("""
                SELECT s.name
                FROM occupation_skills os_to
                JOIN skills s ON s.skill_id = os_to.skill_id
                WHERE os_to.occupation_code = %s
                AND s.skill_id NOT IN (
                    SELECT os_from.skill_id
                    FROM occupation_skills os_from
                    WHERE os_from.occupation_code = %s
                )
            """, (to_code, from_code))

            gap_skills = [row[0] for row in cursor.fetchall()]

            if not gap_skills:
                logger.info(f"No skill gap found between {from_code} and {to_code}")
                raise HTTPException(status_code=404, detail="No skill gap found.")

            logger.info(f"Skill gap for {to_code} not in {from_code}: {gap_skills}")
            return gap_skills
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error computing skill gap: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error computing skill gap: {str(e)}")
    finally:
        conn.close()
