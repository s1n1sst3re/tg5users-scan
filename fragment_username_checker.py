#!/usr/bin/env python3

import requests
import itertools
import time
import string
import json
from typing import Generator, Tuple

class FragmentUsernameChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://fragment.com/'
        })
    
    def generate_usernames(self) -> Generator[str, None, None]:
        chars = string.ascii_lowercase + string.digits
        for combo in itertools.product(chars, repeat=5):
            yield ''.join(combo)
    
    def check_username_availability(self, username: str) -> Tuple[bool, str]:
        try:
            response = self.session.get(f"https://fragment.com/username/{username}")
            
            if f"query={username}" in response.url:
                return True, "Username available"
            elif f"/username/{username}" in response.url:
                if "auction" in response.text.lower() or "bid" in response.text.lower():
                    return False, "Username in auction"
                else:
                    return False, "Username taken"
            else:
                return False, "Username taken"
                
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
    def check_usernames_batch(self, max_usernames: int = 100):
        print("Starting username availability check...")
        print("Note: This may take a very long time as there are 36^5 = 60,466,176 possible 5-character usernames")
        print("Press Ctrl+C to stop at any time\n")
        
        checked_count = 0
        available_count = 0
        taken_count = 0
        
        try:
            for username in self.generate_usernames():
                if checked_count >= max_usernames:
                    break
                
                is_available, status = self.check_username_availability(username)
                
                if is_available is True:
                    print(f"[AVAILABLE] @{username} - {status}")
                    available_count += 1
                elif is_available is False:
                    print(f"[TAKEN] @{username} - {status}")
                    taken_count += 1
                else:
                    print(f"[UNKNOWN] @{username} - {status}")
                
                checked_count += 1
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user.")
        
        print(f"\nSummary:")
        print(f"Total checked: {checked_count}")
        print(f"Available: {available_count}")
        print(f"Taken: {taken_count}")

def main():
    checker = FragmentUsernameChecker()
    
    print("Fragment Username Availability Checker")
    print("=====================================")
    print("This script will generate and check 5-character usernames on Fragment.com")
    print("WARNING: Checking all possible usernames will take a very long time!")
    print("The script will check the first 100 usernames by default.")
    print()
    
    checker.check_usernames_batch(max_usernames=10)

if __name__ == "__main__":
    main()