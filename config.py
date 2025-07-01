import os
from dotenv import load_dotenv, set_key

ENV_FILE = '.env'

def ensure_env_file():
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'w') as f:
            f.write("TOGETHER_API_KEY=your_api_key_here\n")
        print(f"[INFO] Created {ENV_FILE} with placeholder key.")
    else:
        print(f"[INFO] Using existing {ENV_FILE}.")

def get_api_key():
    load_dotenv(ENV_FILE)
    return os.getenv("TOGETHER_API_KEY")