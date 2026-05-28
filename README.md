# Flask Quiz Platform

Kahoot-inspired quiz platform built with Flask, Jinja and Python.
The application was created as a web-based quiz platform where users can create and participate in quiz sessions through a browser-based interface.

This project was developed as part of the Python development program at Teknikhögskolan Göteborg.
This repository was originally created on a school-linked GitHub account and has been reuploaded to preserve the project in an active portfolio.

⚠️ This is an older project and does not fully reflect my current coding standards or development workflow, but it represents one of my earlier backend and web development projects.

---

## Tech Stack

- Python
- Flask
- Jinja
- HTML/CSS
- SQLite
- Web Development

---

## Project Structure

The project follows a structured Flask application architecture with separation between:
- Backend logic
- Templates
- Static assets
- Routing
- Application configuration

---

## Challenges & Learnings

During development we worked with several important backend and web development concepts, including:

- Flask application structure
- Routing and request handling
- Dynamic template rendering with Jinja
- Session management
- Frontend/backend integration
- Web application architecture

---

Features:

- a login-system, and authentication.
- Create your own multiple-choice questions, and send them to your friends and let them take it.
- standard CRUD-features from database
- profile-pages linked to each user, containting that users created_quizzes


Planned features:
- SocketIO integration - users will be able to create lobbies and send an invite-link to friends in order to take a Quiz in realtime and compete against each other (Kahoot-style)
- quiz-page where the user can take a quiz and get a highscore


### UML Diagram

![UML diagram of the MongoDB documents in the project](assets/pyhoot_uml.png?raw=true "Pyhoot UML diagram")


## Setup

1. Install packages from requirements.txt
2. Add an environment file called `.env` in the projects root directory with values set for these following keys:

> .env

    # Flask
    SECRET_KEY=...
    PROJECT_ENV=...  # set to development, testing or production

    # DB
    MONGO_DB_URL=...  # only used if config type is set to production
    MONGO_DB_NAME=database-name
    MONGO_DB_PROTOCOL=mongodb
    MONGO_DB_USER=root
    MONGO_DB_PASS=super-secret-password
    MONGO_DB_HOST=localhost
    MONGO_DB_PORT=27017  # 27017 by default or something like 27020 if it does not work
    
    # Mail 
    # (Example is for gmail, you will need to enable 'Less secure app access' in your Google settings)
    MAIL_SERVER=smtp.gmail.com
    MAIL_USERNAME=jane.doe@gmail.com
    MAIL_PASSWORD=super-secret-password
    MAIL_USE_TLS=True
    MAIL_SENDER=jane.doe@gmail.com
    MAIL_PORT=587

    
## Contributors

This project was developed as a group project together with fellow students at Teknikhögskolan Göteborg.

---

## Course Information

Python Development program
Teknikhögskolan Göteborg
