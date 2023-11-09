-- Create panelsearch database if it does not already exist
CREATE DATABASE IF NOT EXISTS panelsearch;

-- Create table for patients IDs
CREATE TABLE patients(
	id int PRIMARY KEY,
    patient_id int,
    search_id int
);

-- Create table for search results
CREATE TABLE searches(
	id int, # patients.search_id
    panel_id int,
    panel_name varchar(50),
    panel_version varchar(50),
    GMS varchar(50),
    gene_number int,
    r_code varchar(5),  
    genes varchar(250),
    transcript varchar(50),
    genome_build varchar(50),
    bed_file JSON
);


