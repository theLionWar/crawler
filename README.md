How to run install and run my Pastebin crawler:

1. Unzip project

2. Create and new virtual environment:
```sh
   python3 -m venv crawler
```
3. Install requirements:
```sh
   source crawler/bin/activate
   cd /path/to/crawler/directory
   pip install -r requirements.txt
```

4. Run crawler:
```sh
   export PYTHONPATH=/path/to/crawler/directory
   cd /path/to/crawler/directory
   python crawler/runner.py
```
