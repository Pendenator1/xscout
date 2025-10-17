from dotenv import load_dotenv
import os

load_dotenv()

print(f"AUTO_REPLY value: {repr(os.getenv('AUTO_REPLY'))}")
print(f"AUTO_REPLY after lower(): {repr(os.getenv('AUTO_REPLY', 'true').lower())}")
print(f"Comparison result: {os.getenv('AUTO_REPLY', 'true').lower() == 'true'}")
print(f"Length of value: {len(os.getenv('AUTO_REPLY', ''))}")
