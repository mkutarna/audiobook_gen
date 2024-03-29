"""
Notes
-----
This module contains the configuration entries for audiobook_gen.
"""

from pathlib import Path

output_path = Path("outputs")
resource_path = Path("resources")
INSTRUCTIONS = Path("resources/instructions.md")

DEVICE = 'cpu'
LANGUAGE = 'en'
MAX_CHAR_LEN = 140
MODEL_ID = 'v3_en'
SAMPLE_RATE = 24000
SPEAKER_LIST = {
    'Voice 1 (Female)': 'en_0',
    'Voice 2 (Male)': 'en_29',
    'Voice 3 (Female)': 'en_41',
    'Voice 4 (Male)': 'en_110'
}
