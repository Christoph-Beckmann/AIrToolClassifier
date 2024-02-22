from validators import url
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import (
    input_dialog,
    button_dialog,
    message_dialog,
    checkboxlist_dialog,
    PromptSession,
)
from airtoolclassifier.config import Config
from airtoolclassifier.classifier import Classifier


class URLValidator(Validator):
    def validate(self, document):
        url_str = document.text.strip()
        if not url(url_str):
            raise ValidationError(
                message="Invalid URL", cursor_position=len(document.text)
            )


def classification_approval_dialog(title: str, text: str):
    return button_dialog(title=title, text=text, buttons=[("Yes", True), ("No", False)])


class CLI:
    def __init__(self):
        """
        Initializes an instance of the CLI class.
        Loads the configuration using 1Password and initializes the classifier.
        """
        self.config = Config.load_configuration(use_1password=True)
        self.classifier = Classifier(self.config["prompts_dir_path"])

    def manual_adaptations(
        self, existing_categories: set[str], classification: dict
    ) -> dict:

        category_list = sorted(list(existing_categories))

        selected_categories = checkboxlist_dialog(
            title="Category Selection",
            text="Select new categories:",
            values=[(category, category) for category in category_list],
        ).run()

        if not selected_categories:
            selected_categories = []

        new_use_case = input_dialog(
            title="New Use-Case",
            text="Enter new use-case (Leave empty to remain the current):",
            default=classification.get("Use-Case", ""),
        ).run()

        if selected_categories:
            classification["Category"] = selected_categories
        if new_use_case.strip():
            classification["Use-Case"] = new_use_case

        return classification

    def run(self):
        """
        Runs the AirTool Classifier CLI.

        Prompts the user to enter the name and link of a tool, classifies the tool using the classifier,
        and displays the classification result. If the user does not approve the classification,
        prompts the user to manually adapt the classification. Finally, creates a record in Airtable
        with the classification information.

        Returns:
            None
        """
        session = PromptSession()

        tool_name = input_dialog(
            title="Tool Name Input", text="Enter the name of the tool:"
        ).run()
        tool_link = input_dialog(
            "Enter the link to the tool's website: ", validator=URLValidator()
        ).run()

        classification = self.classifier.classify_tool(tool_name, tool_link)

        classification_text = f"""
        The tool was classified.
        Tool-Name: {tool_name}
        Tool_link: {tool_link}
        Category: {classification['Category']}
        Use-Case: {classification['Use-Case']}
        """

        user_approval = classification_approval_dialog(
            "Classification Confirmation", classification_text
        ).run()

        if not user_approval:
            existing_categories = self.classifier.airtable_service.fetch_categories()

            classification = self.manual_adaptations(
                existing_categories, classification
            )

        self.classifier.airtable_service.create_record(classification)
        message_dialog(
            title="Success", text=f"{tool_name} successfully created in Airtable!"
        ).run()
