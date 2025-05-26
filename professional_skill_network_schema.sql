-- USERS TABLE
CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fullName VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('individual', 'company', 'admin'),
    created_at DATETIME
);

-- USER PROFILE TABLE
CREATE TABLE UserProfile (
    user_id INT PRIMARY KEY,
    headline VARCHAR(255),
    bio TEXT,
    location VARCHAR(255),
    phone VARCHAR(50),
    birthdate VARCHAR(50),
    gender ENUM('M', 'F'),
    website VARCHAR(255),
    verified BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- SKILLS TABLE
CREATE TABLE Skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(100),
    category VARCHAR(100)
);

-- USER SKILLS TABLE
CREATE TABLE UserSkills (
    user_id INT,
    skill_id INT,
    level ENUM('beginner', 'intermediate', 'advanced'),
    endorsed_count INT DEFAULT 0,
    PRIMARY KEY (user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (skill_id) REFERENCES Skills(id)
);

-- SKILL ENDORSEMENT TABLE
CREATE TABLE SkillEndorsement (
    endorser_id INT,
    endorsed_user_id INT,
    skill_id INT,
    endorsed_at DATETIME,
    PRIMARY KEY (endorser_id, endorsed_user_id, skill_id),
    FOREIGN KEY (endorser_id) REFERENCES Users(id),
    FOREIGN KEY (endorsed_user_id) REFERENCES Users(id),
    FOREIGN KEY (skill_id) REFERENCES Skills(id)
);

-- CONNECTION TABLE
CREATE TABLE Connection (
    user1_id INT,
    user2_id INT,
    status ENUM('pending', 'accepted', 'rejected'),
    requested_at DATETIME,
    PRIMARY KEY (user1_id, user2_id),
    FOREIGN KEY (user1_id) REFERENCES Users(id),
    FOREIGN KEY (user2_id) REFERENCES Users(id)
);

-- FOLLOW TABLE
CREATE TABLE Follow (
    follower_id INT,
    followed_id INT,
    followed_type ENUM('user', 'company'),
    followed_at DATETIME,
    PRIMARY KEY (follower_id, followed_id, followed_type),
    FOREIGN KEY (follower_id) REFERENCES Users(id)
);

-- COMPANY PROFILE TABLE
CREATE TABLE CompanyProfile (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(255),
    description TEXT,
    website VARCHAR(255),
    industry VARCHAR(255),
    size ENUM('1-10', '11-50', '51-200', '200+'),
    location VARCHAR(100),
    FOREIGN KEY (company_id) REFERENCES Users(id)
);

-- JOB POST TABLE
CREATE TABLE JobPost (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    title VARCHAR(255),
    description TEXT,
    requirements TEXT,
    job_type ENUM('full-time', 'part-time', 'internship', 'remote'),
    posted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deadline DATE,
    FOREIGN KEY (company_id) REFERENCES Users(id)
);

-- APPLICATION TABLE
CREATE TABLE Application (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    job_id INT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'reviewed', 'accepted', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (job_id) REFERENCES JobPost(id)
);