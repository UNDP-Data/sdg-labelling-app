# sdg-labelling-app
A web app for labelling texts by SDG written in Python Dash.

## Docker 

This file explains how to use Docker containers to set up a local environment for developing the application. Using Docker
allows to run the application locally and connect it to a MongoDB database that resembles the database used in production.
To run both a Dash web-app and mock-up MongoDB database, do the following:

1. Make sure the docker engine is running on your machine (see [Docker Desktop](https://www.docker.com/products/docker-desktop/)).
2. Open the terminal.
3. Navigate to the `/docker` directory inside this project.
4. Run `docker compose up --build -d`. This will spin up two containers and populate the database in the background.
5. Go to http://localhost:8050/login to open the web app in your browser.
6. Use `name.surname@email.com` and `password` to log in to the app.
7. You can perform any actions you'd like as the application is connected to your local database instance.
8. To remove the containers, run `docker compose down`.
9. When you make changes to the source code of the application, repeat steps 4 through 8 to view them.
