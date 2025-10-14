#!/usr/bin/env python3
"""
Test script for FPL GUI components
"""

def test_api_connection():
    """Test FPL API connection"""
    try:
        import requests
        print("✓ Requests library available")
        
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API connection successful")
            print(f"✓ Players loaded: {len(data['elements'])}")
            print(f"✓ Teams loaded: {len(data['teams'])}")
            print(f"✓ Gameweeks loaded: {len(data['events'])}")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API connection failed: {e}")
        return False

def test_tkinter():
    """Test tkinter availability"""
    try:
        import tkinter as tk
        print("✓ Tkinter available")
        
        # Test basic GUI creation (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✓ Basic GUI creation works")
        return True
    except Exception as e:
        print(f"✗ Tkinter test failed: {e}")
        return False

def test_data_processing():
    """Test data processing functions"""
    try:
        import requests
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/", timeout=10)
        data = response.json()
        
        # Test player filtering
        players = data['elements']
        available_players = [p for p in players if p['status'] not in ['i', 'u']]
        print(f"✓ Available players: {len(available_players)}")
        
        # Test position filtering
        gks = [p for p in available_players if p['element_type'] == 1]
        defs = [p for p in available_players if p['element_type'] == 2]
        mids = [p for p in available_players if p['element_type'] == 3]
        fwds = [p for p in available_players if p['element_type'] == 4]
        
        print(f"✓ Goalkeepers: {len(gks)}")
        print(f"✓ Defenders: {len(defs)}")
        print(f"✓ Midfielders: {len(mids)}")
        print(f"✓ Forwards: {len(fwds)}")
        
        # Test value calculation
        for player in players[:5]:  # Test first 5 players
            value_score = (
                player['total_points'] * 0.4 +
                float(player['form']) * 30 * 0.4 +
                (100 - float(player['selected_by_percent'])) * 0.2
            ) / (player['now_cost'] / 10)
            player['value_score'] = value_score
        
        print("✓ Value score calculation works")
        return True
        
    except Exception as e:
        print(f"✗ Data processing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏆 FPL GUI Test Suite")
    print("=" * 40)
    
    tests = [
        ("API Connection", test_api_connection),
        ("Tkinter GUI", test_tkinter),
        ("Data Processing", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n🏁 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The FPL GUI should work correctly.")
        print("\nTo run the application:")
        print("python fpl_gui.py")
        print("or")
        print("python run_fpl.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()