# UX Research Manager

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