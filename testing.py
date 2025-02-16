import requests
import json

BASE_URL = "http://127.0.0.1:8000/run"

def test_task(task_description, expected_status=200):
    """Sends a task request to the FastAPI `/run` endpoint and validates response."""
    params = {"task": task_description}
    response = requests.post(BASE_URL, params=params)

    print(f"\n✅ Testing Task: {task_description}")
    print(f"➡️ Response Status Code: {response.status_code}")
    
    try:
        response_json = response.json()
        print(f"➡️ Response JSON: {json.dumps(response_json, indent=4)}")
    except json.JSONDecodeError:
        print("❌ Error: Response is not a valid JSON!")
        response_json = {}

    # Validate expected response
    assert response.status_code == expected_status, f"❌ Unexpected status code: {response.status_code}"
    return response_json


if __name__ == "__main__":
    print("\n🔹 Running Test Cases for Tasks A1–A10 🔹\n")

    # ✅ Task A1: Install uv and run datagen.py
    test_task("Install uv and run datagen.py")

    # ✅ Task A2: Format markdown using Prettier
    test_task("Format markdown file in /data/format.md using Prettier")

    # ✅ Task A3: Count weekdays dynamically
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in weekdays:
        test_task(f"Count {day}s")

    # ✅ Task A4: Sort contacts in JSON
    test_task("Sort contacts in /data/contacts.json")

    # ✅ Task A5: Extract sender email from email.txt
    test_task("Extract sender email from /data/email.txt")

    # ✅ Task A6: Extract credit card number from image
    test_task("Extract credit card number from /data/credit-card.png")

    # ✅ Task A7: Create a markdown index
    test_task("Create markdown index in /data/docs")

    # ✅ Task A8: Get first lines of the 10 most recent log files
    test_task("Get recent logs from /data/logs")

    # ✅ Task A9: Read contents of a test file
    test_task("Read contents of /data/test.txt")

    # ✅ Task A10: Check if a given task is recognized
    test_task("Unknown Task", expected_status=400)

    print("\n🎉 All test cases for A1–A10 executed successfully!\n")