from pyairtable import Table
from airtoolclassifier.config import Config


class AirTableService:
    def __init__(self):
        """
        Initializes an instance of the AirtableService class.

        This constructor loads the configuration using 1Password and initializes the Airtable client.

        Args:
            None

        Returns:
            None
        """
        config = Config.load_configuration(use_1password=True)
        self.airtable_client_table = Table(
            api_key=config["airtable_api_key"],
            base_id=config["airtable_base_id"],
            table_name=config["airtable_table_name"],
        )

    def fetch_all_records(self) -> list[dict]:
        """
        Fetches all records from the Airtable table.

        Returns:
            A cleaned list of dictionaries representing the fields of each record.
        """
        records = self.airtable_client_table.all()
        return [record["fields"] for record in records]

    def fetch_categories(self) -> set:
        """
        Fetches all categories from the Airtable table.

        Returns:
            A list of categories.
        """
        records = self.airtable_client_table.all()

        categories = set(
            category
            for record in records
            for category in record["fields"].get("Category", [])
        )
        return categories

    def create_record(self, record: dict):
        """
        Creates a new record in Airtable.

        Args:
            record (dict): The record to be created.

        Raises:
            Exception: If an error occurs while creating the record.

        """
        try:
            self.airtable_client_table.create(record)
        except Exception as e:
            print(f"An error occurred while trying to create a record in Airtable: {e}")
