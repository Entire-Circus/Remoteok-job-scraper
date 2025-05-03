import json
import os
from datetime import datetime
from typing import Callable, Optional

CONFIG_FILE = "../config/user_config.json"

def cached_input(
    prompt_key: str,
    prompt_text: Optional[str] = None,
    overwrite: bool = False,
    validator: Optional[Callable[[str], bool]] = None
) -> str:
    """
    Retrieves user input and caches it in a JSON config file. If a value exists and overwrite is False,
    the stored value is returned. Otherwise, the user is prompted for input.

    Args:
        prompt_key (str): Key to identify the input in the config file.
        prompt_text (str, optional): Text displayed to the user. Defaults to prompt_key.
        overwrite (bool): If True, re-asks for input even if it already exists.
        validator (Callable[[str], bool], optional): Function to validate the input.

    Returns:
        str: The user input (either newly entered or cached).
    """
    # Load existing config if available
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            saved_answers = json.load(f)
    else:
        saved_answers = {}

    # Default prompt text is the same as the key
    if prompt_text is None:
        prompt_text = prompt_key

    while overwrite or prompt_key not in saved_answers:
        answer = input(f"{prompt_text}: ").strip()
        if validator and not validator(answer):
            print("Invalid input. Try again.")
            continue
        saved_answers[prompt_key] = answer
        with open(CONFIG_FILE, "w") as f:
            json.dump(saved_answers, f, indent=4)
        return answer

    return saved_answers[prompt_key]


# ----------------------
# Input Validators
# ----------------------

def yes_no_validator(s: str) -> bool:
    """Validates that the input is 'y' or 'n' (case-insensitive)."""
    return s.strip().lower() in ["y", "n"]

def url_validator(s: str) -> bool:
    """Validates that the URL starts with 'https://remoteok.com/'."""
    return s.startswith("https://remoteok.com/")

def numbers_validator(i: str) -> bool:
    """Validates that the input is one of the allowed numbers."""
    return i in ["1", "2", "3"]

def date_validator(d: str) -> bool:
    """Validates that the input is a date in YYYY-MM-DD format."""
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except ValueError:
        return False
