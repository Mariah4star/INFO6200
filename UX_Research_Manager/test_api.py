"""
API Test Script for UX Research Manager
Demonstrates how to interact with the API endpoints programmatically.
"""

import requests
import json


# Configuration
BASE_URL = 'http://localhost:8000'
API_BASE = f'{BASE_URL}/api/v1'

# Test credentials (use your actual credentials)
EMAIL = 'admin@uxrm.local'
PASSWORD = '@dm1n@cc0unt!'


def test_api():
    """Test all API endpoints."""
    
    # Create a session to persist cookies
    session = requests.Session()
    
    print("=" * 60)
    print("UX Research Manager API Test")
    print("=" * 60)
    print()
    
    # Test 1: Health Check (no authentication needed)
    print("1. Testing health check endpoint...")
    try:
        response = session.get(f'{API_BASE}/status')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 2: Login
    print("2. Logging in...")
    try:
        login_data = {
            'email': EMAIL,
            'password': PASSWORD
        }
        response = session.post(f'{BASE_URL}/login', data=login_data)
        
        if response.status_code == 200:
            print(f"   ✓ Login successful")
        else:
            print(f"   ✗ Login failed: {response.status_code}")
            print("   Cannot continue with authenticated tests.")
            return
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # Test 3: Get all insights
    print("3. Fetching all insights...")
    try:
        response = session.get(f'{API_BASE}/insights')
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success')}")
        print(f"   Count: {data.get('count')}")
        if data.get('count', 0) > 0:
            print(f"   First insight: {data['insights'][0]['title']}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 4: Get specific insight
    print("4. Fetching specific insight (ID=1)...")
    try:
        response = session.get(f'{API_BASE}/insights/1')
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success')}")
        if data.get('success'):
            print(f"   Title: {data['insight']['title']}")
            print(f"   Description: {data['insight']['description'][:50]}...")
        else:
            print(f"   Message: {data.get('message')}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 5: Get non-existent insight
    print("5. Fetching non-existent insight (ID=99999)...")
    try:
        response = session.get(f'{API_BASE}/insights/99999')
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success')}")
        print(f"   Message: {data.get('message')}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 6: Get all personas
    print("6. Fetching all personas...")
    try:
        response = session.get(f'{API_BASE}/personas')
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success')}")
        print(f"   Count: {data.get('count')}")
        if data.get('count', 0) > 0:
            print(f"   First persona: {data['personas'][0]['name']}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 7: Get specific persona
    print("7. Fetching specific persona (ID=1)...")
    try:
        response = session.get(f'{API_BASE}/personas/1')
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success')}")
        if data.get('success'):
            print(f"   Name: {data['persona']['name']}")
            print(f"   Description: {data['persona']['description'][:50]}...")
        else:
            print(f"   Message: {data.get('message')}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 8: Logout
    print("8. Logging out...")
    try:
        response = session.post(f'{BASE_URL}/logout')
        print(f"   Status: {response.status_code}")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    # Test 9: Try to access insights without authentication
    print("9. Attempting to access insights without authentication...")
    try:
        response = session.get(f'{API_BASE}/insights', allow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   ✓ Correctly redirected to login")
        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        print()
    
    print("=" * 60)
    print("API Test Complete")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
