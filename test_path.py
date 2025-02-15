import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
print(f"Resolved BASE_DIR: {BASE_DIR}")

file_path = os.path.join(BASE_DIR, "dates.txt")
if os.path.exists(file_path):
    print(f"✅ File exists: {file_path}")
else:
    print(f"❌ File not found: {file_path}")