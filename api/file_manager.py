import os

def read_file(path):
    if not path.startswith("/data/"):
        raise PermissionError("Access outside /data/ is restricted.")
    if not os.path.exists(path):
        raise FileNotFoundError()
    with open(path, 'r') as f:
        return f.read()