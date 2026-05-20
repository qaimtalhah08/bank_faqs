import requests

API_URL = "http://127.0.0.1:8000/chat"

# ---------------- TEST DATA ----------------
test_cases = [
    {
        "question": "how can i activate my card?",
        "expected_keywords": ["activate", "card", "atm"]
    },
    {
        "question": "what is kyc?",
        "expected_keywords": ["kyc", "identity", "verification"]
    },
    {
        "question": "documents required for account",
        "expected_keywords": ["document", "id", "address"]
    },
    {
        "question": "how to reset atm pin",
        "expected_keywords": ["pin", "reset", "atm"]
    },
]

# ---------------- METRICS ----------------
total = len(test_cases)
passed = 0

print("\n🚀 EVALUATION START\n")

# ---------------- LOOP ----------------
for i, test in enumerate(test_cases, 1):

    q = test["question"]
    expected = test["expected_keywords"]

    try:
        response = requests.post(
            API_URL,
            json={"question": q},
            timeout=20
        )

        data = response.json()
        answer = data.get("answer", "").lower()

    except Exception as e:
        print(f"❌ ERROR on question: {q}")
        print("Reason:", e)
        continue

    # ---------------- SCORE ----------------
    score = sum(word in answer for word in expected)

    print(f"\n🔎 Test {i}")
    print("Q:", q)
    print("A:", answer)
    print("Match Score:", score, "/", len(expected))

    if score > 0:
        print("✅ PASS")
        passed += 1
    else:
        print("❌ FAIL")

    print("-" * 50)

# ---------------- FINAL RESULT ----------------
accuracy = round((passed / total) * 100, 2)

print("\n📊 FINAL RESULTS")
print("Total:", total)
print("Passed:", passed)
print("Accuracy:", accuracy, "%")
