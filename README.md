# GasHunter on Discord

## Setup Instructions

1. Clone the repository:
   ```
   git clone [repository_url]
   cd nasVer
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up the environment variables:
   - Copy the `.env.example` file to `.env`  
   - Fill in the required values in the `.env` file  
   - get your discord token, etherscan api key and discord channel id from [here](https://discord.com/developers/applications) and [here](https://etherscan.io/)

6. Run the main script:
   ```
   python main.py
   ```

## Requirements

- Python 3.7+
- Discord account and bot token
- Etherscan API key
