-- Total Patients
SELECT COUNT(*) AS total_patients
FROM hospital_data;

-- Readmission Rate
SELECT 
  SUM(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS readmission_rate
FROM hospital_data;

-- Avg Length of Stay
SELECT AVG(time_in_hospital) AS avg_stay
FROM hospital_data;
