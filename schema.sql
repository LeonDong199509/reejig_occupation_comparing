-- Table for occupations
CREATE TABLE occupations (
    occupation_code VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255)
);

-- Table for skills
CREATE TABLE skills (
    skill_id VARCHAR(20) PRIMARY KEY,  -- This stores element_id
    name VARCHAR(255)
);

-- Occupation - Skill relationship
CREATE TABLE occupation_skills (
    occupation_code VARCHAR(10),
    skill_id VARCHAR(20),
    PRIMARY KEY (occupation_code, skill_id),
    FOREIGN KEY (occupation_code) REFERENCES occupations(occupation_code),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
);