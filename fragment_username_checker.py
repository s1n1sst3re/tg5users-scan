#!/usr/bin/env python3
"""
Fragment Username Availability Checker

This script generates 5-character usernames and checks their availability on Fragment.com
by sending requests to the Fragment API to see if the username is taken or available.
"""

import requests
import itertools
import time
import string
import json
from typing import Generator, Tuple

class FragmentUsernameChecker:
    def __init__(self):
        self.session = requests.Session()
        # Set a user agent to appear more like a regular browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://fragment.com/'
        })
    
    def generate_usernames(self) -> Generator[str, None, None]:
        """
        Generate all possible 5-character usernames using lowercase letters and digits
        """
        chars = string.ascii_lowercase + string.digits
        for combo in itertools.product(chars, repeat=5):
            yield ''.join(combo)
    
    def check_username_availability(self, username: str) -> Tuple[bool, str]:
        """
        Check if a username is available on Fragment.com
        
        Args:
            username: The username to check (without @)
            
        Returns:
            Tuple of (is_available, status_message)
        """
        try:
            # Make a request to the username page
            response = self.session.get(f"https://fragment.com/username/{username}")
            
            # If the URL changes to search (with query parameter), the username doesn't exist and is available
            if f"query={username}" in response.url:
                return True, "Username available"
            # If we're still on the username page, the username exists
            elif f"/username/{username}" in response.url:
                # Check if the page contains auction-related content
                if "auction" in response.text.lower() or "bid" in response.text.lower():
                    return False, "Username in auction"
                else:
                    return False, "Username taken"
            else:
                # Some other case
                return False, "Username taken"
                
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
    def check_usernames_batch(self, max_usernames: int = 100):
        """
        Check a batch of usernames and print results
        
        Args:
            max_usernames: Maximum number of usernames to check (to avoid infinite generation)
        """
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
                
                # Be respectful to the server - add a small delay
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
    
    # For demonstration, check only first 10 usernames
    # To check more, increase the number in the function call
    checker.check_usernames_batch(max_usernames=10)

if __name__ == "__main__":
    main()