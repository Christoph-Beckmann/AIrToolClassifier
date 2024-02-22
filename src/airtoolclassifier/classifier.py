import os
import json
from typing import Set, List, Dict

from airtoolclassifier.openai_service import OpenAIService
from airtoolclassifier.airtable_service import AirTableService


class Classifier:
    def __init__(self, prompts_dir_path):
        """
        Initialize the Classifier object.

        Args:
            prompts_dir_path (str): The directory path where the prompt files are located.

        Attributes:
            role_prompt_path (str): The file path of the role prompt file.
            task_prompt_path (str): The file path of the task prompt file.
        """
        self.role_prompt_path = os.path.join(prompts_dir_path, "role.txt")
        self.task_prompt_path = os.path.join(prompts_dir_path, "task.txt")
        self.openai_service = OpenAIService()
        self.airtable_service = AirTableService()

    @staticmethod
    def load_prompt_from_file(file_path: str) -> str:
        """
        Load a prompt from a file.

        Args:
            file_path (str): The path to the file containing the prompt.

        Returns:
            str: The content of the file as a string.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"File not found: {file_path}. Please check the file path in the .env file."
            )

    def create_role_prompt(
        self, categories: Set, existing_classifications: List[Dict]
    ) -> str:
        """
        Creates a role prompt by loading a template from a file and formatting it with the given categories and existing classifications.

        Args:
            categories (Set): A set of categories.
            existing_classifications (List[Dict]): A list of existing classifications.

        Returns:
            str: The formatted role prompt.
        """
        role_template = self.load_prompt_from_file(self.role_prompt_path)
        categories_list = ", ".join(categories)
        return role_template.format(
            categories=categories_list,
            existing_classifications=existing_classifications,
        )

    def create_task_prompt(self, tool_name: str, tool_link: str):
        """
        Creates a task prompt by loading a template from a file and formatting it with the provided tool name and link.

        Args:
            tool_name (str): The name of the tool.
            tool_link (str): The link to the tool.

        Returns:
            str: The formatted task prompt.
        """
        task_template = self.load_prompt_from_file(self.task_prompt_path)
        return task_template.format(tool_name=tool_name, tool_link=tool_link)

    def classify_tool(self, tool_name: str, tool_link: str) -> json:
        """
        Classify a tool using OpenAI's GPT-3.5 Turbo model.

        Args:
            tool_name (str): The name of the tool.
            tool_link (str): The link to the tool.

        Returns:
            str: The classification response.
        """

        role_prompt = self.create_role_prompt(
            categories=self.airtable_service.fetch_categories(),
            existing_classifications=self.airtable_service.fetch_all_records(),
        )

        task_prompt = self.create_task_prompt(tool_name, tool_link)
        return self.openai_service.create_classification(role_prompt, task_prompt)
