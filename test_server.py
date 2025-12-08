import requests
from requests.exceptions import RequestException

base_url = "http://127.0.0.1:8000"

print("\n=== TESTING DJANGO SERVER ===\n")

# Test endpoints
endpoints = [
    ('/', 'Home Page'),
    ('/homepage/', 'Homepage'),
    ('/login/', 'Login Page'),
    ('/signup/', 'Signup Page'),
    ('/algorthim/', 'Algorithms Page'),
    ('/computer_org/', 'Computer Organization Page'),
    ('/software_eng/', 'Software Engineering Page'),
    ('/operating_systems/', 'Operating Systems Page'),
    ('/logic_proof/', 'Logic & Proof Page'),
    ('/about/', 'About Page'),
    ('/role/', 'Role Selection Page'),
]

working = 0
broken = 0

for endpoint, name in endpoints:
    try:
        response = requests.get(base_url + endpoint, timeout=5)
        if response.status_code == 200:
            print(f"✓ {name:30} - OK (200)")
            working += 1
        elif response.status_code == 302:
            print(f"↻ {name:30} - Redirect (302)")
            working += 1
        else:
            print(f"✗ {name:30} - Error ({response.status_code})")
            broken += 1
    except RequestException as e:
        print(f"✗ {name:30} - Connection Failed")
        broken += 1

print(f"\n{'='*50}")
print(f"Working: {working}/{len(endpoints)}")
print(f"Broken: {broken}/{len(endpoints)}")
print(f"{'='*50}\n")

if working == len(endpoints):
    print("✓ ALL PAGES WORKING! Server is ready for testing.")
else:
    print("⚠ Some pages have issues. Check server logs.")
