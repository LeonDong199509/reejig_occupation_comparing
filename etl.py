import csv
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Constants for input and output paths
INPUT_DIR = Path("data")
OUTPUT_DIR = INPUT_DIR / "bulk"
OCCUPATION_INPUT = INPUT_DIR / "Occupation.txt"
SKILLS_INPUT = INPUT_DIR / "Skills.txt"
OCCUPATION_CSV = OUTPUT_DIR / "occupations.csv"
SKILLS_CSV = OUTPUT_DIR / "skills.csv"
OCCUPATION_SKILLS_CSV = OUTPUT_DIR / "occupation_skills.csv"


def ensure_output_dir():
    """Ensure the output directory exists."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(f"Ensured output directory exists: {OUTPUT_DIR}")


def extract_occupations():
    """Extract occupation data and write to CSV."""
    logging.info(f"Extracting occupations from {OCCUPATION_INPUT}")
    count = 0

    with open(OCCUPATION_INPUT, "r", encoding="utf-8", newline="") as occ_file, \
            open(OCCUPATION_CSV, "w", encoding="utf-8", newline="") as occ_out:
        reader = csv.DictReader(occ_file, delimiter="\t")
        writer = csv.writer(occ_out, delimiter="\t", lineterminator="\n")

        for row in reader:
            writer.writerow([
                row["O*NET-SOC Code"].replace("\r", "").strip(),
                row["Title"].replace("\r", "").strip()
            ])
            count += 1

    logging.info(f"Wrote {count} occupation records to {OCCUPATION_CSV}")


def extract_skills_and_relationships():
    """Extract skills and occupation-skill relationships to separate CSVs."""
    logging.info(f"Extracting skills and relationships from {SKILLS_INPUT}")

    inserted_skills = set()
    skill_count = 0
    rel_count = 0

    with open(SKILLS_INPUT, encoding="utf-8") as skills_file, \
         open(SKILLS_CSV, "w", newline="", encoding="utf-8") as skills_out, \
         open(OCCUPATION_SKILLS_CSV, "w", newline="", encoding="utf-8") as rel_out:

        reader = csv.DictReader(skills_file, delimiter="\t")
        skills_writer = csv.writer(skills_out, delimiter="\t", lineterminator="\n")
        rel_writer = csv.writer(rel_out, delimiter="\t", lineterminator="\n")

        for row in reader:
            skill_id = row["Element ID"].replace("\r", "").strip()
            skill_name = row["Element Name"].replace("\r", "").strip()
            occupation_code = row["O*NET-SOC Code"].replace("\r", "").strip()
            scale_id = row.get("Scale ID", "").replace("\r", "").strip()
            not_relevant = row.get("Not Relevant", "N").replace("\r", "").strip()

            # Write unique skills only once (regardless of Scale ID)
            if skill_id not in inserted_skills:
                skills_writer.writerow([skill_id, skill_name])
                inserted_skills.add(skill_id)
                skill_count += 1

            # Skip if Scale ID is IM
            if scale_id == "IM":
                continue

            # For LV scale, write occupation-skill relation only if not_relevant == "N"
            if scale_id == "LV" and not_relevant == "N":
                rel_writer.writerow([occupation_code, skill_id])
                rel_count += 1

    logging.info(f"Wrote {skill_count} unique skills to {SKILLS_CSV}")
    logging.info(f"Wrote {rel_count} occupation-skill relationships to {OCCUPATION_SKILLS_CSV}")


def main():
    """Run the ETL process: extract from text files and write to CSVs."""
    logging.info("Starting ETL process to CSV files")
    ensure_output_dir()
    extract_occupations()
    extract_skills_and_relationships()
    logging.info("ETL process completed successfully")


if __name__ == "__main__":
    main()
