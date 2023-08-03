# sdg-labelling-app
A web app for labelling texts by SDG written in Python Dash.

## Introduction 

The application is designed to facilitate the collection of texts labelled by [Sustainable Development Goals](https://sdgs.un.org/goals) (SDGs).
It consists of two main components: a front-end web application written [Python Dash](https://dash.plotly.com) and a back-end database which can be
either a native [MongoDB](https://www.mongodb.com) or [Azure Cosmos DB for MongoDB](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/introduction).

The application can be run locally or on the remote server using Docker. For details about deployment, read the sections below.

## Getting Started

The application has been developed in Python `3.10`.

### Using Docker

The simplest way to get started with the app is
to clone the repository and follow the instructions in another [README.md](docker/README.md).

### Using Dash and MongoDB

To run the application without Docker, you will need two things: a virtual Python environment and a connection to a MongoDB instance (either local or remote).

1. Create a virual environment by following the [instructions](https://docs.python.org/3/library/venv.html) from the official documentation.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Specify the required environment variables (see below), including the connection to MongoDB.
4. Run the app with `python app.py`.

You also need a connection to a MongoDB instance which must have two collections populated with data in a specific format. The two collections are `users` (which cannot be called anything else) and
`texts` collection (whose can be called anything you want). You can manually import sample data JSON files under [docker/](docker/) directory or use your own data that follows the exact same format.

TBC.

## Build and Test

 
Before deploying a web app to Azure Web Services via GitHub Actions, set
both `WEBSITE_WEBDEPLOY_USE_SCM` ([source](https://learn.microsoft.com/en-gb/azure/app-service/deploy-github-actions?tabs=applevel#tabpanel_1_applevel)) and `SCM_DO_BUILD_DURING_DEPLOYMENT` ([source](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Czip-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli#tabpanel_4_zip-deploy))
to `true` in application settings.

## Contribute

TBC.