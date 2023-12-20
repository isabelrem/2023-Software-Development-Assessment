Installation
------------

Install PanelSearch by running:

    # Clone GitHub repository
    git clone https://github.com/isabelrem/2023-Software-Development-Assessment
    
    # Create conda environment
    conda env create -f environment.yaml

    # Activate conda environment
    conda activate vv_panelget

    # Install python packages
    pip install -r requirements.txt

    # Run PanelSearch
    cd PanelSearch
    python main.py

Alternatively, use the pyproject.toml:
    
    # Clone GitHub repository
    git clone https://github.com/isabelrem/2023-Software-Development-Assessment
    
    # Create conda environment
    conda env create -f environment.yaml

    # Activate conda environment
    conda activate vv_panelget

    # Install pyproject.toml
    pip install -e .

    # Run PanelSearch
    python main.py
    
**Then create SQL database by running panelsearch_db.sql file in MySQL Workbench**
