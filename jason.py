import os
import asyncio
from collections import defaultdict
from typing import Dict, Any, Optional

import aiofiles
import orjson


class JASON:
    """
    A robust JSON-based database with atomic writes, orjson serialization,
    and per-user locking. Maintains simple load/save interface.
    
    Features:
    - Atomic writes using temporary files
    - Per-user locking for concurrent safety
    - orjson for fast serialization
    - In-memory caching of user data
    - Automatic creation of database folder
    """

    def __init__(self, db_folder: str, default_structure: Dict[str, Any]):
        self.db_folder = os.path.expanduser(db_folder)
        self.default_structure = default_structure
        self.user_cache = {}
        self.locks = defaultdict(asyncio.Lock)
        os.makedirs(self.db_folder, exist_ok=True)

    def _get_user_filepath(self, user_id: str) -> str:
        return os.path.join(self.db_folder, f"{user_id}.json")

    async def load_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Load user data with cache support and automatic recovery from corruption.
        Returns a copy of the data to prevent accidental in-place modifications.
        """
        async with self.locks[user_id]:
            # Try cache first
            if user_id in self.user_cache:
                return self.user_cache[user_id].copy()

            filepath = self._get_user_filepath(user_id)
            data: Optional[Dict[str, Any]] = None

            # Try disk load
            if os.path.exists(filepath):
                try:
                    async with aiofiles.open(filepath, "rb") as f:
                        content = await f.read()
                        if content:
                            data = orjson.loads(content)
                except (orjson.JSONDecodeError, FileNotFoundError, OSError):
                    pass  # Proceed to create new data

            # Fallback to default structure if load failed
            if data is None:
                data = self.default_structure.copy()

            # Update cache and return copy
            self.user_cache[user_id] = data
            return data.copy()

    async def save_user_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """
        Save user data with atomic write pattern and error recovery.
        Returns True if save was successful, False otherwise.
        """
        async with self.locks[user_id]:
            # Update cache with new data
            self.user_cache[user_id] = data
            filepath = self._get_user_filepath(user_id)
            temp_path = f"{filepath}.tmp"

            try:
                # Serialize with orjson (faster than standard json)
                serialized = orjson.dumps(
                    data,
                    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                )
                
                # Write to temporary file first
                async with aiofiles.open(temp_path, "wb") as f:
                    await f.write(serialized)
                
                # Atomic replace using blocking call in executor
                await asyncio.to_thread(os.replace, temp_path, filepath)
                return True
            except Exception as e:
                # Cleanup temporary file on failure
                try:
                    await asyncio.to_thread(os.remove, temp_path)
                except OSError:
                    pass
                return False
            finally:
                # Ensure cache is cleared if save failed to prevent stale data
                if not os.path.exists(filepath):
                    self.user_cache.pop(user_id, None)
