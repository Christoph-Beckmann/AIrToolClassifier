# AIrToolClassifier Documentation

## Overview

_Have you ever stumbled upon an online tool and thought, **"This could come in handy someday,"** only to bookmark it or jot it down on a list, but never really keep track of it?_ **Enter AIrToolClassifier.**

Designed to revolutionize how we handle digital tools, this tool automates the categorization process into predefined categories and uncovers potential use-cases. Utilizing artificial intelligence through _OpenAI's GPT-3.5 Turbo model_, this Python-based application creates a bridge to **Airtable**, facilitating the classification and identification of use-cases, which are then stored in an Airtable database. This enables your personal AI agent to access this database, ensuring you have the right tools at your fingertips to tackle future challenges more effectively. AIrToolClassifier not only helps you maintain a comprehensive database of online tools but also ensures _your personal AI agent can leverage this knowledge_ to support your future projects efficiently.

## Features

- **Automated Categorization:** Simplifies the organization of digital tools into predefined categories.
- **Use-Case Identification:** Uncovers potential applications for each tool, enhancing productivity.
- **AI-Powered:** Utilizes artificial intelligence through OpenAI's GPT-3.5 Turbo model.
- **Integration with Airtable:** Facilitates classification and use-case identification, storing this valuable information in an Airtable database.

## Installations

1. Ensure Python 3.8+ is installed on your system.
2. Clone the repository to your local machine.
3. Install required dependencies by running `pip install -r requirements.txt`.

## Configuration

The tool requires configuration of API keys and other parameters through environment variables or 1Password. The necessary variables include:

- `OPENAI_API_KEY`: API key for OpenAI.
- `AIRTABLE_API_KEY`: API key for Airtable.
- `AIRTABLE_BASE_ID`: Base ID for the target Airtable base.
- `AIRTABLE_TABLE_NAME`: Name of the table within the Airtable base.
- `PROMPTS_DIR_PATH`: Directory path where prompt templates are stored.

For these configurations, a `.env_template` file is provided. To use it, remove the "\_template" from the file name.

## Usage

To start the AirToolClassifier, navigate to the project directory and execute the CLI script:

```bash
python -m airtoolclassifier
```

Follow the interactive prompts to input the tool's name and link. The system will classify the tool and allow for manual adaptations before saving the classification to Airtable.

## Development

This project is structured into several modules:

- _airtable_service.py_: Manages interactions with Airtable.
- _classifier.py_: Handles the creation of prompts and the classification logic.
- _cli.py_: Provides a command-line interface for user interaction.
- _config.py_: Loads and manages configuration settings.
- _openai_service.py_: Manages communication with OpenAI's API.

## Contributing

Contributions to the AirToolClassifier are welcome. Please follow the standard fork and pull request workflow.

## License

For support and queries, please open an issue on the project's GitHub repository.
