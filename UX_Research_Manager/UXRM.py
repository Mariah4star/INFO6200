"""
UX Research Manager - CLI & Web Prototype (Chunk 3)

This is a hybrid application for managing UX research insights and personas.
It includes:
  - Command-line interface for interactive use
  - Flask web API for programmatic access
  - Persistent data storage using JSON
  - AI-assisted summaries via Mistral API

Users can create, view, edit, and delete research insights, manage personas,
and generate AI-assisted summaries of research notes.

"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from flask import Flask, request, jsonify


# Load environment variables from .env file
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass  # no-op if dotenv not installed

load_dotenv()

# Try to import Mistral AI
MISTRAL_IMPORT_ERROR = None
try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except Exception as e:
    MISTRAL_AVAILABLE = False
    MISTRAL_IMPORT_ERROR = str(e)

# Data file paths (web-ready with environment variable override)
DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).parent / "data"))
DATA_FILE = DATA_DIR / "research_data.json"

# Persistent data storage
class DataStore:
    """Manages persistent storage for insights and personas."""
    
    def __init__(self):
        self.insights: List[Dict] = []
        self.personas: List[Dict] = []
        self.next_insight_id = 1
        self.next_persona_id = 1
        self.load_from_file()
    
    def load_from_file(self) -> None:
        """Load insights and personas from JSON file."""
        if not DATA_FILE.exists():
            return
        
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.insights = data.get('insights', [])
                self.personas = data.get('personas', [])
                
                # Recalculate next IDs based on existing data
                if self.insights:
                    self.next_insight_id = max(i['id'] for i in self.insights) + 1
                if self.personas:
                    self.next_persona_id = max(p['id'] for p in self.personas) + 1
        except Exception as e:
            print(f"[WARNING] Error loading data file: {e}")
    
    def save_to_file(self) -> None:
        """Save insights and personas to JSON file."""
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                'insights': self.insights,
                'personas': self.personas
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Error saving data file: {e}")
    
    def add_insight(self, title: str, description: str, persona_id: Optional[int] = None, 
                   journey_stage: Optional[str] = None, ai_summary: Optional[str] = None) -> int:
        """Add a new research insight."""
        insight_id = self.next_insight_id
        self.insights.append({
            'id': insight_id,
            'title': title,
            'description': description,
            'persona_id': persona_id,
            'journey_stage': journey_stage,
            'timestamp': datetime.now().isoformat(),
            'ai_summary': ai_summary
        })
        self.next_insight_id += 1
        self.save_to_file()
        return insight_id
    
    def get_insight(self, insight_id: int) -> Optional[Dict]:
        """Retrieve a specific insight."""
        for insight in self.insights:
            if insight['id'] == insight_id:
                return insight
        return None
    
    def get_all_insights(self) -> List[Dict]:
        """Retrieve all insights."""
        return self.insights
    
    def update_insight(self, insight_id: int, **kwargs) -> bool:
        """Update an insight."""
        for insight in self.insights:
            if insight['id'] == insight_id:
                insight.update(kwargs)
                self.save_to_file()
                return True
        return False
    
    def delete_insight(self, insight_id: int) -> bool:
        """Delete an insight."""
        for i, insight in enumerate(self.insights):
            if insight['id'] == insight_id:
                self.insights.pop(i)
                self.save_to_file()
                return True
        return False
    
    def add_persona(self, name: str, description: str) -> int:
        """Add a new persona."""
        persona_id = self.next_persona_id
        self.personas.append({
            'id': persona_id,
            'name': name,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })
        self.next_persona_id += 1
        self.save_to_file()
        return persona_id
    
    def get_persona(self, persona_id: int) -> Optional[Dict]:
        """Retrieve a specific persona."""
        for persona in self.personas:
            if persona['id'] == persona_id:
                return persona
        return None
    
    def get_all_personas(self) -> List[Dict]:
        """Retrieve all personas."""
        return self.personas
    
    def update_persona(self, persona_id: int, **kwargs) -> bool:
        """Update a persona."""
        for persona in self.personas:
            if persona['id'] == persona_id:
                persona.update(kwargs)
                self.save_to_file()
                return True
        return False
    
    def delete_persona(self, persona_id: int) -> bool:
        """Delete a persona."""
        for i, persona in enumerate(self.personas):
            if persona['id'] == persona_id:
                self.personas.pop(i)
                self.save_to_file()
                return True
        return False


class AIAssistant:
    """Handles AI-assisted summarization using an LLM API."""
    
    def __init__(self):
        """
        Initialize AI Assistant.
        """
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY", "")
    
    def summarize_research(self, research_notes: str) -> str:
        """
        Use Mistral AI to summarize research notes into clear insights.
        
        Args:
            research_notes: The raw research notes to summarize
            
        Returns:
            AI-generated summary or warning message if API call fails
        """
        if not MISTRAL_AVAILABLE:
            details = f" Import error: {MISTRAL_IMPORT_ERROR}" if MISTRAL_IMPORT_ERROR else ""
            return "[WARNING] Mistral AI is unavailable.\n" \
                   "Please install the 'mistralai' package: pip install mistralai" \
                   f"{details}"
        
        if not self.mistral_api_key:
            return "[WARNING] No Mistral API key configured. Skipping AI summarization.\n" \
                   "Set MISTRAL_API_KEY environment variable to enable this feature."
        
        try:
            with Mistral(api_key=self.mistral_api_key) as mistral:
                res = mistral.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a UX research assistant. Summarize research notes into "
                                       "clear, actionable insights for UX designers. Be concise and focus "
                                       "on key findings and implications."
                        },
                        {
                            "role": "user",
                            "content": f"Please summarize the following research notes:\n\n{research_notes}"
                        }
                    ],
                    stream=False
                )
                return res.choices[0].message.content
        except Exception as e:
            return f"[WARNING] Mistral API Error: {str(e)}"


class UXResearchManager:
    """Main CLI application for UX Research Manager."""
    
    def __init__(self):
        """Initialize the application."""
        self.data_store = DataStore()
        self.ai_assistant = AIAssistant()
    
    def prompt_return_or_retry(self, menu_type="main") -> bool:
        """Prompt the user to retry or return to menu on invalid input."""
        while True:
            print("\nWhat would you like to do?")
            print("  1. Try again")
            if menu_type == "persona":
                print("  2. Return to Persona Menu")
            else:
                print("  2. Return to Main Menu")
            choice = input("Select: ").strip()
            if choice == '1':
                return True
            elif choice == '2':
                return False
            else:
                print("[ERROR] Invalid selection. Please enter 1 or 2.")
    
    def confirm_action(self, action_name: str) -> bool:
        """Confirm user wants to proceed with an action."""
        print(f"\n[INFO] You selected: {action_name}")
        while True:
            response = input("Press Enter to continue or type 'back' to return to menu: ").strip().lower()
            if response == '':
                return True
            elif response == 'back':
                print("[INFO] Returning to menu...\n")
                return False
            else:
                print("[ERROR] Invalid input. Press Enter to continue or type 'back'.")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("  UX RESEARCH MANAGER - CLI Prototype")
        print("="*50)
        print("1. Create Research Insight")
        print("2. View All Insights")
        print("3. View Specific Insight")
        print("4. Edit Insight")
        print("5. Delete Insight")
        print("6. Generate AI Summary")
        print("7. Manage Personas")
        print("8. Exit")
        print("-"*50)
    
    def display_persona_menu(self):
        """Display the persona management menu."""
        print("\n" + "-"*50)
        print("  PERSONA MANAGEMENT")
        print("-"*50)
        print("1. Create New Persona")
        print("2. View All Personas")
        print("3. View Specific Persona")
        print("4. Edit Persona")
        print("5. Delete Persona")
        print("6. Back to Main Menu")
        print("-"*50)
    
    # ------------------ Insights ------------------ #
    def create_insight(self):
        """Create a new research insight."""
        if not self.confirm_action("Create Research Insight"):
            return
        title = input("Enter insight title: ").strip()
        if not title:
            print("[ERROR] Title cannot be empty.")
            return
        description = input("Enter research description/notes: ").strip()
        if not description:
            print("[ERROR] Description cannot be empty.")
            return
        
        # Select persona
        persona_id = None
        personas = self.data_store.get_all_personas()
        if personas:
            print("\nAvailable Personas:")
            for persona in personas:
                print(f"  {persona['id']}. {persona['name']}")
            pid_input = input("Enter persona ID (or press Enter to skip): ").strip()
            if pid_input.isdigit():
                pid = int(pid_input)
                if self.data_store.get_persona(pid):
                    persona_id = pid
                else:
                    print("[WARNING] Persona not found. Skipping persona association.")
        
        # Select journey stage
        journey_stage = None
        print("\nJourney Map Stages:")
        print("  1. Awareness")
        print("  2. Consideration")
        print("  3. Decision")
        print("  4. Retention")
        print("  5. Advocacy")
        stage_input = input("Select journey stage (1-5, or press Enter to skip): ").strip()
        if stage_input:
            stage_map = {
                '1': 'Awareness',
                '2': 'Consideration',
                '3': 'Decision',
                '4': 'Retention',
                '5': 'Advocacy'
            }
            journey_stage = stage_map.get(stage_input)
            if not journey_stage:
                print("[WARNING] Invalid selection. Journey stage skipped.")
        
        ai_summary = None
        if input("Generate AI summary? (y/n): ").strip().lower() == 'y':
            print("[PROCESSING] Generating AI summary...")
            ai_summary = self.ai_assistant.summarize_research(description)
        
        insight_id = self.data_store.add_insight(title, description, persona_id, journey_stage, ai_summary)
        print(f"\n[SUCCESS] Insight created! (ID: {insight_id})")
        if ai_summary:
            print(f"\n[AI SUMMARY]\n{ai_summary}")
    
    def view_all_insights(self):
        """View all research insights."""
        insights = self.data_store.get_all_insights()
        if not insights:
            print("\n[INFO] No insights created yet.")
            if input("Would you like to create one? (y/n): ").strip().lower() == 'y':
                self.create_insight()
            return
        print("\n--- All Research Insights ---")
        for insight in insights:
            self.print_insight_summary(insight)
        
        input("\nPress Enter to continue...")
    
    def print_insight_summary(self, insight: Dict):
        """Print a summary of an insight."""
        print(f"\n[INSIGHT] ID: {insight['id']} | Title: {insight['title']}")
        desc = insight['description']
        print(f"   Description: {desc[:100]}..." if len(desc) > 100 else f"   Description: {desc}")
        if insight['persona_id']:
            persona = self.data_store.get_persona(insight['persona_id'])
            print(f"   Persona: {persona['name'] if persona else 'Unknown'}")
        if insight['journey_stage']:
            print(f"   Journey Stage: {insight['journey_stage']}")
        print(f"   Created: {insight['timestamp']}")
    
    def view_specific_insight(self):
        """View details of a specific insight."""
        if not self.confirm_action("View Specific Insight"):
            return
        self.view_all_insights()
        while True:
            try:
                insight_id = int(input("Enter insight ID to view: ").strip())
                insight = self.data_store.get_insight(insight_id)
                if not insight:
                    print("[ERROR] Insight not found.")
                    if not self.prompt_return_or_retry("main"):
                        return
                    continue
                print("\n--- Insight Details ---")
                print(f"ID: {insight['id']}\nTitle: {insight['title']}\nDescription: {insight['description']}")
                if insight['persona_id']:
                    persona = self.data_store.get_persona(insight['persona_id'])
                    print(f"Persona: {persona['name'] if persona else 'Unknown'}")
                if insight['journey_stage']:
                    print(f"Journey Stage: {insight['journey_stage']}")
                print(f"Created: {insight['timestamp']}")
                if insight['ai_summary']:
                    print(f"\n[AI SUMMARY]\n{insight['ai_summary']}")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    def edit_insight(self):
        """Edit an existing insight."""
        if not self.confirm_action("Edit Insight"):
            return
        self.view_all_insights()
        while True:
            try:
                insight_id = int(input("Enter insight ID to edit: ").strip())
                insight = self.data_store.get_insight(insight_id)
                if not insight:
                    print("[ERROR] Insight not found.")
                    if not self.prompt_return_or_retry("main"):
                        return
                    continue
                new_title = input(f"Title [{insight['title']}]: ").strip()
                new_desc = input(f"Description [{insight['description'][:50]}...]: ").strip()
                updates = {}
                if new_title: updates['title'] = new_title
                if new_desc: updates['description'] = new_desc
                
                # Option to connect/change persona
                personas = self.data_store.get_all_personas()
                if personas:
                    print("\nAvailable Personas:")
                    for persona in personas:
                        print(f"  {persona['id']}. {persona['name']}")
                    if insight['persona_id']:
                        print(f"  (Current: {self.data_store.get_persona(insight['persona_id'])['name']})")
                    pid_input = input("Enter persona ID to link (or press Enter to skip): ").strip()
                    if pid_input.isdigit():
                        pid = int(pid_input)
                        if self.data_store.get_persona(pid):
                            updates['persona_id'] = pid
                        else:
                            print("[WARNING] Persona not found. Skipping persona update.")
                    elif pid_input.lower() == 'none':
                        updates['persona_id'] = None
                
                # Option to change journey stage
                print("\nJourney Map Stages:")
                print("  1. Awareness")
                print("  2. Consideration")
                print("  3. Decision")
                print("  4. Retention")
                print("  5. Advocacy")
                if insight['journey_stage']:
                    print(f"  (Current: {insight['journey_stage']})")
                stage_input = input("Select new journey stage (1-5, or press Enter to skip): ").strip()
                if stage_input:
                    stage_map = {
                        '1': 'Awareness',
                        '2': 'Consideration',
                        '3': 'Decision',
                        '4': 'Retention',
                        '5': 'Advocacy'
                    }
                    new_stage = stage_map.get(stage_input)
                    if new_stage:
                        updates['journey_stage'] = new_stage
                    else:
                        print("[WARNING] Invalid selection. Journey stage skipped.")
                elif stage_input == 'none':
                    updates['journey_stage'] = None
                
                if updates:
                    self.data_store.update_insight(insight_id, **updates)
                    print("[SUCCESS] Insight updated!")
                else:
                    print("[INFO] No changes made.")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    def delete_insight(self):
        """Delete an insight."""
        if not self.confirm_action("Delete Insight"):
            return
        self.view_all_insights()
        while True:
            try:
                insight_id = int(input("Enter insight ID to delete: ").strip())
                if self.data_store.delete_insight(insight_id):
                    print("[SUCCESS] Insight deleted!")
                else:
                    print("[ERROR] Insight not found.")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    def generate_ai_summary(self):
        """Generate or regenerate AI summary for an insight."""
        if not self.confirm_action("Generate AI Summary"):
            return
        self.view_all_insights()
        
        # Check if there are any insights after view_all_insights
        if not self.data_store.get_all_insights():
            return
        
        while True:
            try:
                insight_id = int(input("\nEnter insight ID to summarize: ").strip())
                insight = self.data_store.get_insight(insight_id)
                if not insight:
                    print("[ERROR] Insight not found.")
                    if not self.prompt_return_or_retry("main"):
                        return
                    continue
                print("[PROCESSING] Generating AI summary...")
                summary = self.ai_assistant.summarize_research(insight['description'])
                if input("Save this summary to the insight? (y/n): ").strip().lower() == 'y':
                    self.data_store.update_insight(insight_id, ai_summary=summary)
                    print("[SUCCESS] Summary saved!")
                print(f"\n[AI SUMMARY]\n{summary}")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    # ------------------ Personas ------------------ #
    def manage_personas(self):
        """Manage personas."""
        while True:
            self.display_persona_menu()
            choice = input("Select an option: ").strip()
            if choice == '1': self.create_persona()
            elif choice == '2': self.view_all_personas()
            elif choice == '3': self.view_specific_persona()
            elif choice == '4': self.edit_persona()
            elif choice == '5': self.delete_persona()
            elif choice == '6': break
            else:
                if not self.prompt_return_or_retry("persona"):
                    break
    
    def create_persona(self):
        """Create a new persona."""
        if not self.confirm_action("Create New Persona"):
            return
        name = input("Enter persona name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty.")
            return
        desc = input("Enter persona description: ").strip()
        if not desc:
            print("[ERROR] Description cannot be empty.")
            return
        persona_id = self.data_store.add_persona(name, desc)
        print(f"[SUCCESS] Persona created! (ID: {persona_id})")
    
    def view_all_personas(self):
        """View all personas."""
        personas = self.data_store.get_all_personas()
        if not personas:
            print("\n[INFO] No personas created yet.")
            if input("Would you like to create one? (y/n): ").strip().lower() == 'y':
                self.create_persona()
            return
        print("\n--- All Personas ---")
        for persona in personas:
            print(f"\n[PERSONA] ID: {persona['id']} | {persona['name']}")
            desc = persona['description']
            print(f"   Description: {desc[:100]}..." if len(desc) > 100 else f"   Description: {desc}")
            print(f"   Created: {persona['timestamp']}")
        
        input("\nPress Enter to continue...")
    
    def view_specific_persona(self):
        """View details of a specific persona."""
        if not self.confirm_action("View Specific Persona"):
            return
        self.view_all_personas()
        
        # Check if there are any personas after view_all_personas
        if not self.data_store.get_all_personas():
            return
        
        while True:
            try:
                pid = int(input("\nEnter persona ID to view: ").strip())
                persona = self.data_store.get_persona(pid)
                if not persona:
                    print("[ERROR] Persona not found.")
                    if not self.prompt_return_or_retry("persona"):
                        return
                    continue
                print(f"\nID: {persona['id']}\nName: {persona['name']}\nDescription: {persona['description']}\nCreated: {persona['timestamp']}")
                linked = [i for i in self.data_store.get_all_insights() if i['persona_id'] == pid]
                if linked:
                    print(f"\nLinked Insights ({len(linked)}):")
                    for i in linked:
                        print(f" - {i['title']}")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    def edit_persona(self):
        """Edit an existing persona."""
        if not self.confirm_action("Edit Persona"):
            return
        self.view_all_personas()
        
        # Check if there are any personas after view_all_personas
        if not self.data_store.get_all_personas():
            return
        
        while True:
            try:
                pid = int(input("\nEnter persona ID to edit: ").strip())
                persona = self.data_store.get_persona(pid)
                if not persona:
                    print("[ERROR] Persona not found.")
                    if not self.prompt_return_or_retry("persona"):
                        return
                    continue
                new_name = input(f"Name [{persona['name']}]: ").strip()
                new_desc = input(f"Description [{persona['description'][:50]}...]: ").strip()
                updates = {}
                if new_name: updates['name'] = new_name
                if new_desc: updates['description'] = new_desc
                if updates:
                    self.data_store.update_persona(pid, **updates)
                    print("[SUCCESS] Persona updated!")
                else:
                    print("[INFO] No changes made.")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    def delete_persona(self):
        if not self.confirm_action("Delete Persona"):
            return
        self.view_all_personas()
        if not self.data_store.get_all_personas():
            return

        while True:
            try:
                pid = int(input("\nEnter persona ID to delete: ").strip())
                linked = [i for i in self.data_store.get_all_insights() if i.get('persona_id') == pid]
                if linked:
                    print(f"[WARNING] This persona has {len(linked)} linked insights. Deleting will unlink them.")
                if self.data_store.delete_persona(pid):
                    # Unlink any insights referencing this persona
                    changed = False
                    for insight in self.data_store.get_all_insights():
                        if insight.get('persona_id') == pid:
                            insight['persona_id'] = None
                            changed = True
                    if changed:
                        self.data_store.save_to_file()
                    print("[SUCCESS] Persona deleted and linked insights unlinked.")
                else:
                    print("[ERROR] Persona not found.")
                return
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number.")
    
    # ------------------ Run ------------------ #
    def run(self):
        """Run the main CLI loop."""
        print("\nWelcome to UX Research Manager!\n")
        while True:
            self.display_menu()
            choice = input("Select an option: ").strip()
            if choice == '1': self.create_insight()
            elif choice == '2': self.view_all_insights()
            elif choice == '3': self.view_specific_insight()
            elif choice == '4': self.edit_insight()
            elif choice == '5': self.delete_insight()
            elif choice == '6': self.generate_ai_summary()
            elif choice == '7': self.manage_personas()
            elif choice == '8':
                print("\nThank you for using UX Research Manager! Goodbye!\n")
                break
            else:
                if not self.prompt_return_or_retry("main"):
                    continue


def main():
    app = UXResearchManager()
    app.run()


# Flask Web API
flask_app = Flask(__name__)
data_store = DataStore()
ai_assistant = AIAssistant()


@flask_app.route('/')
def index():
    """Root route - Welcome page."""
    return """
    <html>
        <head>
            <title>UX Research Manager</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 50px auto; 
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                h1 { color: #5B72E3; }
                .api-list { background: white; padding: 20px; border-radius: 8px; }
                code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>🎯 UX Research Manager</h1>
            <p>Welcome to the UX Research Manager API!</p>
            <div class="api-list">
                <h2>Available Endpoints:</h2>
                <ul>
                    <li><code>GET /api/insights</code> - List all insights</li>
                    <li><code>POST /api/insights</code> - Create new insight</li>
                    <li><code>GET /api/insights/{id}</code> - Get specific insight</li>
                    <li><code>PUT /api/insights/{id}</code> - Update insight</li>
                    <li><code>DELETE /api/insights/{id}</code> - Delete insight</li>
                    <li><code>GET /api/personas</code> - List all personas</li>
                    <li><code>POST /api/personas</code> - Create new persona</li>
                    <li><code>GET /api/personas/{id}</code> - Get specific persona</li>
                    <li><code>PUT /api/personas/{id}</code> - Update persona</li>
                    <li><code>DELETE /api/personas/{id}</code> - Delete persona</li>
                    <li><code>POST /api/summarize</code> - Generate AI summary</li>
                </ul>
            </div>
        </body>
    </html>
    """


@flask_app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get all insights."""
    return jsonify({'insights': data_store.get_all_insights()})


@flask_app.route('/api/insights', methods=['POST'])
def create_insight_api():
    """Create a new insight."""
    try:
        data = request.json
        insight_id = data_store.add_insight(
            title=data.get('title'),
            description=data.get('description'),
            persona_id=data.get('persona_id'),
            journey_stage=data.get('journey_stage'),
            ai_summary=data.get('ai_summary')
        )
        return jsonify({'success': True, 'id': insight_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@flask_app.route('/api/insights/<int:insight_id>', methods=['GET'])
def get_insight(insight_id):
    """Get a specific insight."""
    insight = data_store.get_insight(insight_id)
    if not insight:
        return jsonify({'error': 'Insight not found'}), 404
    return jsonify(insight)


@flask_app.route('/api/insights/<int:insight_id>', methods=['PUT'])
def update_insight_api(insight_id):
    """Update an insight."""
    try:
        data = request.json
        if data_store.update_insight(insight_id, **data):
            return jsonify({'success': True})
        return jsonify({'error': 'Insight not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@flask_app.route('/api/insights/<int:insight_id>', methods=['DELETE'])
def delete_insight_api(insight_id):
    """Delete an insight."""
    if data_store.delete_insight(insight_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Insight not found'}), 404


@flask_app.route('/api/personas', methods=['GET'])
def get_personas():
    """Get all personas."""
    return jsonify({'personas': data_store.get_all_personas()})


@flask_app.route('/api/personas', methods=['POST'])
def create_persona_api():
    """Create a new persona."""
    try:
        data = request.json
        persona_id = data_store.add_persona(
            name=data.get('name'),
            description=data.get('description')
        )
        return jsonify({'success': True, 'id': persona_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@flask_app.route('/api/personas/<int:persona_id>', methods=['GET'])
def get_persona(persona_id):
    """Get a specific persona."""
    persona = data_store.get_persona(persona_id)
    if not persona:
        return jsonify({'error': 'Persona not found'}), 404
    return jsonify(persona)


@flask_app.route('/api/personas/<int:persona_id>', methods=['PUT'])
def update_persona_api(persona_id):
    """Update a persona."""
    try:
        data = request.json
        if data_store.update_persona(persona_id, **data):
            return jsonify({'success': True})
        return jsonify({'error': 'Persona not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@flask_app.route('/api/personas/<int:persona_id>', methods=['DELETE'])
def delete_persona_api(persona_id):
    """Delete a persona."""
    if data_store.delete_persona(persona_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Persona not found'}), 404


@flask_app.route('/api/summarize', methods=['POST'])
def summarize_api():
    """Generate AI summary for research notes."""
    try:
        data = request.json
        summary = ai_assistant.summarize_research(data.get('notes', ''))
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    # Check if Flask is being used
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        flask_app.run(debug=True)
    else:
        main()