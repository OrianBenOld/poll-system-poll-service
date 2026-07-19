-- User Service Database Schema
CREATE DATABASE IF NOT EXISTS user_db;
USE user_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT NOT NULL,
    address VARCHAR(255) NOT NULL,
    joining_date DATE NOT NULL,
    is_registered BOOLEAN NOT NULL DEFAULT FALSE
);

-- Poll Service Database Schema
CREATE DATABASE IF NOT EXISTS poll_db;
USE poll_db;

CREATE TABLE IF NOT EXISTS poll_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS poll_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    option_choice VARCHAR(10) NOT NULL,
    UNIQUE KEY unique_user_question (user_id, question_id),
    FOREIGN KEY (question_id) REFERENCES poll_questions(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_question_id (question_id)
);
