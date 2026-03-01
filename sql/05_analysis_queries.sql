-- Readmission by Age
SELECT age, COUNT(*) AS total, 
SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) AS readmitted
FROM hospital_data
GROUP BY age;

-- Medication vs Readmission
SELECT num_medications, COUNT(*) 
FROM hospital_data
GROUP BY num_medications;
