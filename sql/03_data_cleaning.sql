-- Replace invalid values

UPDATE hospital_data
SET readmitted = NULL
WHERE readmitted = '?';
