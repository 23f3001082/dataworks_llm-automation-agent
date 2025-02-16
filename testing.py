import requests

BASE_URL = "http://127.0.0.1:8000/run"

def test_task(task_description, expected_status=200):
    """Sends a task request to the FastAPI `/run` endpoint and checks response status."""
    params = {"task": task_description}
    response = requests.post(BASE_URL, params=params)

    print(f"\n✅ Testing Task: {task_description}")
    print(f"➡️ Response Status Code: {response.status_code}")
    print(f"➡️ Response JSON: {response.json()}")

    assert response.status_code == expected_status, f"❌ Unexpected status code: {response.status_code}"
    return response.json()

if __name__ == "__main__":
    print("\n🔹 Running Test Cases for Tasks A1–A10 🔹\n")

    # A1: Install uv and run datagen.py
    test_task("Install uv and run datagen.py")

    # A2: Format markdown file
    test_task("Format markdown file in /data/format.md using Prettier")

    # A3: Count weekdays - Ensure singular form of days
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in weekdays:
        test_task(f"Count {day}")

    # A4: Sort contacts
    test_task("Sort contacts in /data/contacts.json")

    # A5: Extract sender email
    test_task("Extract sender email from /data/email.txt")

    # A6: Extract credit card number
    test_task("Extract credit card number from /data/credit-card.png")

    # A7: Create markdown index
    test_task("Create markdown index in /data/docs")

    # A8: Get recent logs
    test_task("Get recent logs from /data/logs", expected_status=200)  # Adjust if needed

    print("\n🎉 All test cases executed successfully!")