-- Load CSV into table (MySQL example)

LOAD DATA INFILE 'diabetes_130_raw.csv'
INTO TABLE hospital_data
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;

# Data was ingested from CSV into SQL for structured querying
