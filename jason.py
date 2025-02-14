import os
import json
from pathlib import Path
from typing import Dict, Any
import aiofiles

class JASON:
    """
    A simple JSON-based database for MVP chatbots.
    Each user's data is stored in a separate JSON file.
    """

    def __init__(self, db_folder: str, default_structure: Dict[str, Any]):
        """
        Initialize the JSON database.

        Args:
            db_folder (str): Path to the folder where user JSON files will be stored.
            default_structure (Dict[str, Any]): Default structure for user data.
        """
        self.db_folder = db_folder
        self.default_structure = default_structure
        self.user_cache = {}

        # Create the DB folder if it doesn't exist
        os.makedirs(self.db_folder, exist_ok=True)

    def _get_user_filepath(self, user_id: str) -> str:
        """
        Get the filepath for a user's JSON file.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            str: Full path to the user's JSON file.
        """
        return os.path.join(self.db_folder, f"{user_id}.json")

    async def load_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Load user data from a JSON file. If the file doesn't exist, return the default structure.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            Dict[str, Any]: User data as a dictionary.
        """
        # Check cache first
        if user_id in self.user_cache:
            return self.user_cache[user_id]

        # Load from file if not in cache
        filepath = self._get_user_filepath(user_id)
        if os.path.exists(filepath):
            try:
                async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
                    data = json.loads(await f.read())
                    self.user_cache[user_id] = data  # Update cache
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Return default structure if file is missing or corrupted
        self.user_cache[user_id] = self.default_structure.copy()
        return self.default_structure.copy()

    async def save_user_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """
        Save user data to a JSON file.

        Args:
            user_id (str): Unique identifier for the user.
            data (Dict[str, Any]): User data to save.
        """
        # Update cache
        self.user_cache[user_id] = data

        # Save to file
        filepath = self._get_user_filepath(user_id)
        async with aiofiles.open(filepath, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))
