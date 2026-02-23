# UX Research Manager

## General Instruction
 I am providing a general overview of the UX Research Manager app and will break its development into smaller chunks to ensure functionality is solid. This submission includes the general overview followed by Chunk 1, which focuses on a working CLI prototype. In future iterations, I will include all previous information along with the next chunk.

## Project Overview 
My app, UX Research Manager, is designed to help UX designers and researchers securely store, organize, and review user research insights. The app allows users to create, view, edit, and delete research findings, link insights to defined personas and stages in the user journey, and use AI to summarize research notes into clear insights. The goal is to provide a simple, easy-to-use platform that supports evidence-based design decisions and helps users manage their research in one place. 

## Core Features 
- As a UX designer or researcher: 
    - I want to be able to register and log in so that my research data is secure.
- As a UX designer or researcher (logged-in user):
    - I want to create, view, edit, and delete research insights so I can manage all my research findings in one place.
- As a UX designer or researcher:
    - I want to be able to create and define personas and link research insights to them so I can better understand user needs and behavioral patterns.
- As a UX designer or researcher:
    - I want an AI-assisted summarization of my research notes so I can quickly generate clear insights from the data. 

## Target Audience
- UX Designers
- UX Researchers
- Product designers conducting usability tests
- Students learning UX research

## Technical Stack (High-level) 
- Backend: Python
- Database: SQL
- AI Integration: Large Language Model API for research summaries
- Frontend: HTML and CSS (maybe JavaScript for interactivity)
- Deployment: Heroku

## Data Model 
- User Login
    - User ID (integer): unique login
    - Email (string)
    - Password (string): hashed
- Research Insight (record)
    - Id (integer): unique identifier for the research insight
    - Title (string): Short name for the insight
    - Description (string): Text describing the research observation
    - Persona ID (integer): Name or identifier of the associated persona
    - Journey Stage (string): The user journey map stage is linked to the insight
    - Date and time stamp (datetime)
    - AI summary (string)
- Persona (record)
    - Id (integer): unique identifier for the persona
    - Name (string): Persona name
    - Description (string): Persona’s details and characteristics
    - Date and time stamp (datetime)

## Future Enhancements 
- Filtering or sorting insights by persona or journey map stage
- AI-assisted editing to improve clarity and quality
- AI-generated journey maps based on personas and insights

# Chunking the Program – Breaking the development into smaller chunks

## Chunk 1: CLI Application Prototype

## Goal: 
Create a working CLI prototype of the UX Research Manager app.

# Tasks:
1. Initialize the program and activate the CLI menu.
2. Set up a Python virtual environment for the project.
3. Accept text-based user input for adding research insights.
4. Connect to an LLM API for AI-assisted summarization of research notes.
5. Allow creation of personas and link research insights to personas.
6. Store insights and personas in in-memory storage (dictionary) for the duration of the session.
7. Loop the CLI interaction so users can continue adding or viewing data until they choose to exit.

# Core files to create:
- UXRM.py (main application file)
- requirements.txt (dependencies)
- Initialize a Git repository and commit the prototype

## Chunk 2: Refactoring for structured data

# Goal: 
Design and implement a data model for the UX Research Manager app. Refactor the existing CLI program to handle data in a more structured way. I want the research insights and personas to be represented as Python dictionaries and managed within lists. Keep this structured data in a file so it can be accessed across sessions.

# Tasks: 
1. Modify the existing Python script so each research insight and persona is represented as a single Python dictionary with keys matching the fields defined in the project data model.
2. Store all dictionaries in master lists for insights and personas, and update the program logic to iterate over these lists when displaying data.
3. Save the structured data to a file so it can be loaded in future sessions and updated after each session.
4. Make sure that the CLI behavior and user experience remain unchanged from Chunk 1.

# Files to create:
- A new directory for stored data files
- A data file (.JSON file) for persisting research insights and personas

## Chunk 2.5: Achieving Data Persistence

# Goal: 
Make sure that research insights and personas persist across sessions by saving structured data to an external file and loading it on application startup.

# Tasks: 
1. Check for the existence of a JSON data file on application startup.
2. Load existing research insights and personas from the file if it exists.
3. Initialize empty data structures if the file does not exist.
4. Save the full updated dataset to the JSON file immediately whenever data is modified.
5. Make sure the data is stored in a structured, human-readable format.
6. Maintain the same CLI behavior and user experience as previous chunks.

# Files:
- Updated Python file (UXRM.py)
- The research_data.json file has at least two records

## Chunk 3: Web Interface Using Flask

# Goal: 
Introduce a minimal web interface using Flask as the first step in transitioning from a CLI application to a web application.

# Tasks: 
1. Define a single route for the URL.
2. When the user lands on the root URL (/), the application must return a simple string or HTML response (e.g., a “Hello, Web!” message).

# User Experience:
- For the color, the "Aquatic" palette was selected to create a calm, high-focus environment that reduces cognitive load for researchers. 
  - Royal Blue (#5B72E3): Primary Action Color. Reserved for the most important interactions, such as "Create New Insight," "Register," and the main navigation sidebar. 
  - Medium Blue (#5B9DE3): Secondary Interaction. Used for active states, secondary buttons (like "Edit"), and highlighting selected filters. 
  - Bright Turquoise (#5BE3D2): AI & Insights. Specifically designated for the AI-assisted summarization feature. 
  - Sky Blue (#5BC8E3): Categorization & Tags. Used for persona labels and journey stage chips. 
  - Pink (#EC4899): Success & Validation. Utilized for "Save" confirmations and indicating that an insight has been successfully "Validated" or linked to a persona.
  -  Soft Blue (#A6D7E3): UI Accents. Best for hover states, subtle borders, or search bar backgrounds. 
  - Pure White (#FFFFFF): The Workspace Canvas. Used as the background for all research cards and data entries. 
- User Interface 
  - The design is a Filter-Centric Dashboard. This layout prioritizes data discoverability through a top-level filtering system, allowing researchers to slice data by persona or journey stage. 
- I would like to know when the AI is loading the research summary
- I would like the navigation to be on the top with an easy-to-use interface
- I would like each main menu option to be on its own page

# Files to create:
- web_app.py file containing the minimal Flask application

## Chunk 4: Gathering User Data

# Goal:
Replace command-line input with web-based forms that allow users to submit UX research data through a Flask web interface while continuing to use persistent JSON storage.

# Tasks: 
1. Create Flask routes that render HTML forms from the templates folder for entering research insights and personas.
2. Handle form submissions using POST requests and extract user input with request.form.
3. Save submitted data to the persistent JSON file using the existing data model.

# Files to create:
- Updated web_app.py
- templates/ directory with the HTML files used to display and submit forms

## Chunk 5: Bringing Data to the Web

# Goal: 
Display all research insights and personas dynamically on the web using Jinja2 templates and persistent JSON storage.

# Tasks: 
1. Create Flask routes that load insights and personas from the JSON file.
2. Pass the data to Jinja2 templates and use for loops to render each item in a readable HTML layout.
3. Include links for viewing, editing, or deleting items while keeping the dashboard style consistent.

# Files to create:
- Updated web_app.py
- templates/insights.html and templates/personas.html

## Chunk 6: Data Migration

# Goal: 
Refactor the application’s backend to replace the JSON file with a robust SQL database using SQLAlchemy, enabling structured, persistent storage for insights and personas, while keeping AI-assisted research summarization functional.

# Tasks: 
1. Define SQLAlchemy models that match the existing data structures for research insights and personas.
2. Configure the Flask application to connect to an SQLite database (or another SQL database compatible with Heroku and future AWS deployment).
3. Refactor "add" and "list" functionality to create, commit, and query records via SQLAlchemy instead of reading/writing the JSON file.
4. Make sure that the AI-assisted features (e.g., research summarization) continue to function with the new database.
5. Make sure that administrators and developers can access and manage the database easily

# Core Files:
- Updated web_app.py with SQLAlchemy integration
- New Python files with database models
- The SQLite database file (project.db)

# Note: 
 With the deployment of this app, I want to have the most seamless SQL database experience. I am planning on initially launching with Heroku because of cost and simplicity. Choose the database system that will integrate best with Heroku and allow for the eventual migration to AWS.



