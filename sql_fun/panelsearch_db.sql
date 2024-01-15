-- Create panelsearch database if it does not already exist
CREATE DATABASE IF NOT EXISTS panelsearch;

-- Create table for patients IDs
CREATE TABLE IF NOT EXISTS patients(
	id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    patient_id varchar(50),
    search_id int
);

-- Create table for search results
CREATE TABLE IF NOT EXISTS searches(
	id int KEY AUTO_INCREMENT, # patients.search_id
    panel_id int,
    panel_name varchar(500),
    panel_version varchar(50),
    GMS varchar(50),
    gene_number int,
    r_code varchar(5),
    transcript varchar(50),
    genome_build varchar(50),
    bed_file varchar(50), #change to JSON when there is a JSON
    UNIQUE (panel_id, panel_name, panel_version, GMS, gene_number, r_code, transcript, genome_build, bed_file)
    );


