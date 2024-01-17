
General Usage (for manual non-Docker use; not recommended)
=============

Please see :doc:`docker`.

*WARNING: If the user does not want to run their SQL database inside a docker container, please ask Isabel to turn on the cloud-based SQL database before attempting to run code. Alternatively, use MySQL Workbench to manually create a database and modify the code to run locally.*

If the user wishes to run PanelSearch outside of a docker container, the user must install all requirements from requirements.txt locally.

To run PanelSearch, the user should type this code into the command line::

    cd PanelSearch
    python main.py


When prompted choose option 1 for the GRCh37 reference genome build or
option 2 for the GRCh38::

    Which genome build would you like to use? Enter 1 for GRCh37. Enter 2 for GRCh38.
    > 1

When prompted, choose option 1 if you know the R-code or option 2 if you would like to
search by disease name using keywords.

R-code example::

    If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.
    > 1
    Enter your search term:
    > R128

Genetic disease keyword example::

    If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.
    > 2
    Enter your search term:
    > Brugada

When prompted choose whether to generate a BED file::

    Generate BED file? (Y/N)
    > Y

    For exon coordinates on transcript, press \'1\'. For genomic coordinates, press \'2\'.
    > 1


A bed_files folder will be created and your BED file can be found here.

Finally, it will ask whether you would like to save your results::

    Would you like to save this search against a patient ID? (Y/N)
    > Y

    What patient ID would you like to save this search against?
    > Example123

    Your search was saved

    Thank you for using PanelSearch. Goodbye.

Once you have finished remember to deactivate the conda environment::

    conda deactivate

Testing
-------
To run tests make sure you are in the root directory before typing the following into the terminal::

    pytest -vv

You should see::

    ================================================================== test session starts ===================================================================
    platform win32 -- Python 3.10.5, pytest-7.4.3, pluggy-1.3.0 -- C:\Users\jessica\AppData\Local\Programs\Python\Python310\python.exe
    cachedir: .pytest_cache
    rootdir: C:\Users\jessica\2023-Software-Development-Assessment
    collected 23 items

    Tests/test_PanelApp_API_Request.py::test_request_data PASSED                                                                                        [  4%]
    Tests/test_PanelApp_API_Request.py::test_pk_search PASSED                                                                                           [  8%]
    Tests/test_PanelApp_API_Request.py::test_r_search_works PASSED                                                                                      [ 13%]
    Tests/test_PanelApp_API_Request.py::test_r_search_fails PASSED                                                                                      [ 17%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_works PASSED                                                                       [ 21%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_fails PASSED                                                                       [ 26%]
    Tests/test_VV_API_Request.py::test_genome_build_convert_GRch37 PASSED                                                                               [ 30%] 
    Tests/test_VV_API_Request.py::test_genome_build_convert_fails PASSED                                                                                [ 34%] 
    Tests/test_VV_API_Request.py::test_request_data_works PASSED                                                                                        [ 39%]
    Tests/test_VV_API_Request.py::test_gene_to_transcripts_works PASSED                                                                                 [ 43%]
    Tests/test_VV_Request_Parse.py::test_vv_request_parse PASSED                                                                                        [ 47%]
    Tests/test_generate_bed.py::test_parse_panel_data PASSED                                                                                            [ 52%]
    Tests/test_generate_bed.py::test_write_bed_file_works PASSED                                                                                        [ 56%]
    Tests/test_generate_bed.py::test_write_bed_file_no_filename PASSED                                                                                  [ 60%]
    Tests/test_generate_bed.py::test_write_bed_file_no_beds PASSED                                                                                      [ 65%] 
    Tests/test_main.py::test_get_genome_build_works PASSED                                                                                              [ 69%] 
    Tests/test_main.py::test_get_genome_build_errors PASSED                                                                                             [ 73%] 
    Tests/test_main.py::test_get_input_string_type_works PASSED                                                                                         [ 78%] 
    Tests/test_main.py::test_get_input_string_type_errors PASSED                                                                                        [ 82%] 
    Tests/test_main.py::test_get_input_string PASSED                                                                                                    [ 86%] 
    Tests/test_main.py::test_create_bed_filename PASSED                                                                                                 [ 91%] 
    Tests/test_select_disease.py::test_find_match_works PASSED                                                                                          [ 95%]
    Tests/test_select_disease.py::test_find_match_errors PASSED                                                                                         [100%]

    ================================================================== 23 passed in 34.72s ===================================================================
    