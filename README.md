
## How to set up the environment

### Set up the virtual environment using venv
```bash
python -m venv env
```

### Activate the virtual environment
On Windows:
```bash
.\env\Scripts\activate
```

On MacOS/Linux:
```bash
source env/bin/activate
```

### Install the required packages
```bash
pip install pandas fuzzywuzzy python-Levenshtein
```

## How to run the script
```
python ./extract_data.py ./test/input.txt ./test/output.csv
```