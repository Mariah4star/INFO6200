"""
UX Research Manager - CLI Prototype (Chunk 1)

This is a command-line interface prototype for managing UX research insights 
and personas. It provides functionality to create, view, edit, and delete 
research insights, create and manage personas, and use AI to summarize research notes.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

# Try to import requests - AI features will be disabled if not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# In-memory storage
class DataStore:
    """Manages in-memory storage for insights and personas."""
    
    def __init__(self):
        self.insights: Dict = {}
        self.personas: Dict = {}
        self.next_insight_id = 1
        self.next_persona_id = 1
    
    def add_insight(self, title: str, description: str, persona_id: Optional[int] = None, 
                   journey_stage: Optional[str] = None, ai_summary: Optional[str] = None) -> int:
        """Add a new research insight."""
        insight_id = self.next_insight_id
        self.insights[insight_id] = {
            'id': insight_id,
            'title': title,
            'description': description,
            'persona_id': persona_id,
            'journey_stage': journey_stage,
            'timestamp': datetime.now().isoformat(),
            'ai_summary': ai_summary
        }
        self.next_insight_id += 1
        return insight_id
    
    def get_insight(self, insight_id: int) -> Optional[Dict]:
        """Retrieve a specific insight."""
        return self.insights.get(insight_id)
    
    def get_all_insights(self) -> List[Dict]:
        """Retrieve all insights."""
        return list(self.insights.values())
    
    def update_insight(self, insight_id: int, **kwargs) -> bool:
        """Update an insight."""
        if insight_id not in self.insights:
            return False
        self.insights[insight_id].update(kwargs)
        return True
    
    def delete_insight(self, insight_id: int) -> bool:
        """Delete an insight."""
        if insight_id in self.insights:
            del self.insights[insight_id]
            return True
        return False
    
    def add_persona(self, name: str, description: str) -> int:
        """Add a new persona."""
        persona_id = self.next_persona_id
        self.personas[persona_id] = {
            'id': persona_id,
            'name': name,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.next_persona_id += 1
        return persona_id
    
    def get_persona(self, persona_id: int) -> Optional[Dict]:
        """Retrieve a specific persona."""
        return self.personas.get(persona_id)
    
    def get_all_personas(self) -> List[Dict]:
        """Retrieve all personas."""
        return list(self.personas.values())
    
    def update_persona(self, persona_id: int, **kwargs) -> bool:
        """Update a persona."""
        if persona_id not in self.personas:
            return False
        self.personas[persona_id].update(kwargs)
        return True
    
    def delete_persona(self, persona_id: int) -> bool:
        """Delete a persona."""
        if persona_id in self.personas:
            del self.personas[persona_id]
            return True
        return False


class AIAssistant:
    """Handles AI-assisted summarization using an LLM API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Assistant.
        
        Args:
            api_key: API key for the LLM service (OpenAI by default).
                    If not provided, will attempt to load from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.api_endpoint = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
    
    def summarize_research(self, research_notes: str) -> str:
        """
        Use AI to summarize research notes into clear insights.
        
        Args:
            research_notes: The raw research notes to summarize
            
        Returns:
            AI-generated summary or warning message if API call fails
        """
        if not REQUESTS_AVAILABLE:
            return "[WARNING] AI summarization is unavailable.\n" \
                   "Please install the 'requests' package: pip install requests"
        
        if not self.api_key:
            return "[WARNING] No API key configured. Skipping AI summarization.\n" \
                   "Set OPENAI_API_KEY environment variable to enable this feature."
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [
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
                "temperature": 0.7,
                "max_tokens": 300
            }
            response = requests.post(self.api_endpoint, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"[WARNING] API Error (Status {response.status_code}): Unable to generate summary"
        except requests.exceptions.Timeout:
            return "[WARNING] API request timed out. Unable to generate summary."
        except requests.exceptions.RequestException as e:
            return f"[WARNING] API Error: {str(e)}"
        except (KeyError, ValueError) as e:
            return f"[WARNING] Error parsing API response: {str(e)}"


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
                persona_id = int(pid_input)
        
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
        """Delete a persona."""
        if not self.confirm_action("Delete Persona"):
            return
        self.view_all_personas()
        
        # Check if there are any personas after view_all_personas
        if not self.data_store.get_all_personas():
            return
        
        while True:
            try:
                pid = int(input("\nEnter persona ID to delete: ").strip())
                linked = [i for i in self.data_store.get_all_insights() if i['persona_id'] == pid]
                if linked:
                    print(f"[WARNING] This persona has {len(linked)} linked insights. Deleting will unlink them.")
                if self.data_store.delete_persona(pid):
                    print("[SUCCESS] Persona deleted!")
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


if __name__ == "__main__":
    main()
