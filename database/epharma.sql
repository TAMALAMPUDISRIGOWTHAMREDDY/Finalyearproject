-- Create the ePharma database
CREATE DATABASE IF NOT EXISTS epharma;

-- Use the ePharma database
USE epharma;

-- Create the medicines table to store symptoms and corresponding medicines
CREATE TABLE IF NOT EXISTS medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symptom VARCHAR(255) NOT NULL,
    medicine VARCHAR(255) NOT NULL
);

-- Example data (you can add more rows as needed)
INSERT INTO medicines (symptom, medicine) VALUES
('headache', 'Paracetamol'),
('fever', 'Ibuprofen'),
('cold', 'Antihistamine'),
('stomach pain', 'Omeprazole');
