# Azure Function App for a simple geoparser

## Features

This sample API uses Azure Functions to enable basic geoparse capabilities through nlp operations:

- ✨geoparse✨
- ✨apiversion✨

## References:

<a href="https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#folder-structure">
    <img src="https://raw.githubusercontent.com/Azure/azure-functions-python-worker/dev/docs/Azure.Functions.svg" alt="Azure Functions Python developer guide" width="40" height="40"/>
    Azure Functions Python developer guide
</a>

<a href="https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal">
    <img src="https://raw.githubusercontent.com/Azure/azure-functions-python-worker/dev/docs/Azure.Functions.svg" alt="Azure Functions Python developer guide" width="40" height="40"/>
    Create Azure Function App
</a>

<a href="https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser">
    <img src="https://raw.githubusercontent.com/Azure/azure-functions-python-worker/dev/docs/Azure.Functions.svg" alt="Azure Functions Python developer guide" width="40" height="40"/>
    Create a Python function in Azure from the command line
</a>


## Install Dependencies:

- Python 3.8x (with all packages defined in requirements.txt installed)
- Azure-CLI
- Az. Functions Core Tools
- VS Code
- VS Code extensions: Python, Azure Account, Azure Functions, Optional: (Azure Resources, Azure Storage)
- Make sure the python .venv existst. If not: python -m venv .venv

## Nice to have in your install:

- Postman
- Azure Storage Explorer


### Environment Variables


Local environment variables (a.k.a Application Settings) are handled through the settings in `local.settings.json` file. This file is in .gitingore and also does not get copied over to Azure when publishing the app


### Run the Client locally for debugging and testing

To run the server, run `func start` from the terminal.

Recommend using Postman to create some test cases. For heavier unit testing pip install unittest


## Authors

Jon Ujkani


