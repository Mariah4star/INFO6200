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
