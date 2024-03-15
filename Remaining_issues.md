# Remaining issues
* when selecting disease name from list - would be nice if we could select by numbered position on list rather than having to write out the whole condition name - any typo and goes straight back to beginning. 
* documentation - needs major rework.
* You have chosen cystic renal disease
    GRch37 build selected.
    Traceback (most recent call last):
    File "/app/PanelSearch/main.py", line 213, in <module>
        main()
    File "/app/PanelSearch/main.py", line 127, in main
        panel_data = panelapp_search_parse(RESPONSE.json(), SEARCH.genome_build)
    File "/app/PanelSearch/PanelApp_Request_Parse.py", line 97, in panelapp_search_parse
        OUTPUT = vv_request_parse(VV_RESP.json(), OUTPUT)
    File "/app/PanelSearch/VV_Request_Parse.py", line 14, in vv_request_parse
        genome_direction = list(vv_gene_record['transcripts'][0]['genomic_spans'].values())[0]['orientation']
    IndexError: list index out of range
from vv request parse
    try:
            transcript = vv_gene_record['transcripts'][0]['reference'] # if the gene record has no transcript, this line can IndexError
* have actual transcript instead of placeholder.
* follow pylint suggestions
* error when choose not to generate bed file