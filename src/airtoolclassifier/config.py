import os
import subprocess
from dotenv import load_dotenv


load_dotenv()


class Config:
    @staticmethod
    def get_key_from_env(key_name: str) -> str:
        """
        Retrieves the key from environment variables.

        Args:
            key_name (str): The environment variable name to retrieve the API key for.

        Returns:
            str: The key, or None if not found.
        """
        return os.getenv(key_name)

    @staticmethod
    def get_api_key_from_1password(address: str) -> str:
        """
        Retrieves the API key from 1Password for the given address.

        Args:
            address (str): The address to retrieve the API key for.

        Returns:
            str: The API key retrieved from 1Password, or None if an error occurred.
        """
        command = f"op read '{address}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error while loading API-key from 1Password: {result.stderr}")
            return None
        else:
            return result.stdout.strip()

    @classmethod
    def load_configuration(cls, use_1password: bool = False) -> dict:
        """
        Loads all necessary configurations either directly from environment variables or from 1Password.

        Args:
            use_1password (bool):
                If True, configurations will be loaded from 1Password address.
                If False, configurations will be retrieved directly from environment variables.

        Returns:
            dict: A dictionary containing all configurations.
        """

        if use_1password:
            openai_api_key = cls.get_api_key_from_1password(os.getenv("OPENAI_API_KEY"))
            airtable_api_key = cls.get_api_key_from_1password(
                os.getenv("AIRTABLE_API_KEY")
            )
        else:
            openai_api_key = cls.get_key_from_env("OPENAI_API_KEY")
            airtable_api_key = cls.get_key_from_env("AIRTABLE_API_KEY")

        airtable_base_id = cls.get_key_from_env("AIRTABLE_BASE_ID")
        airtable_table_name = cls.get_key_from_env("AIRTABLE_TABLE_NAME")

        prompts_dir_path = cls.get_key_from_env("PROMPTS_DIR_PATH")

        missing_configs = [
            key
            for key, value in locals().items()
            if value is None and key in ["openai_api_key", "airtable_api_key"]
        ]
        if missing_configs:
            raise ValueError(
                f"Missing configurations for: {', '.join(missing_configs)}"
            )

        return {
            "openai_api_key": openai_api_key,
            "airtable_api_key": airtable_api_key,
            "airtable_base_id": airtable_base_id,
            "airtable_table_name": airtable_table_name,
            "prompts_dir_path": prompts_dir_path,
        }
