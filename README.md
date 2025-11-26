# Fragment Username Checker

This Python script checks the availability of 5-character usernames on Fragment.com (the platform for Telegram username auctions).

## Features

- Generates all possible 5-character usernames using lowercase letters (a-z) and digits (0-9)
- Checks each username's availability on Fragment.com
- Identifies whether a username is:
  - Available (redirects to search page, meaning it doesn't exist)
  - In auction (has a username page with auction details)
  - Taken (otherwise)

## How It Works

The script works by:

1. Making HTTP requests to `https://fragment.com/username/{username}`
2. Checking the response URL and content:
   - If the URL changes to `https://fragment.com/?query={username}`, the username doesn't exist and is available
   - If the URL stays as `https://fragment.com/username/{username}` and contains auction-related terms, it's in auction
   - Otherwise, it's considered taken

## Usage

```bash
python3 fragment_username_checker.py
```

The script will:
- Generate and check 5-character usernames (a-z, 0-9)
- Show availability status for each username
- Limit to 10 usernames by default for demonstration

## Important Notes

- There are 36^5 = 60,466,176 possible 5-character usernames
- Checking all usernames would take a very long time
- Be respectful of Fragment.com's servers by not making too many requests too quickly
- The script includes a 0.5 second delay between requests

## Requirements

- Python 3.x
- requests library

## Disclaimer

This script is for educational purposes only. Please use responsibly and respect Fragment.com's terms of service and rate limits.