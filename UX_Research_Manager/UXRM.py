"""
UX Research Manager - CLI Prototype (Chunk 1)

This is a command-line interface prototype for managing UX research insights 
and personas. It provides functionality to create, view, edit, and delete 
research insights, create and manage personas, and use AI to summarize research notes.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests


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
    
    def summarize_research(self, research_notes: str) -> Optional[str]:
        """
        Use AI to summarize research notes into clear insights.
        
        Args:
            research_notes: The raw research notes to summarize
            
        Returns:
            AI-generated summary or None if API call fails
        """
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
                summary = response.json()['choices'][0]['message']['content']
                return summary
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
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("  UX RESEARCH MANAGER - CLI Prototype")
        print("="*50)
        print("\n1. Create Research Insight")
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
    
    def create_insight(self):
        """Create a new research insight."""
        print("\n--- Create New Research Insight ---")
        
        title = input("Enter insight title: ").strip()
        if not title:
            print("[ERROR] Title cannot be empty.")
            return
        
        description = input("Enter research description/notes: ").strip()
        if not description:
            print("[ERROR] Description cannot be empty.")
            return
        
        print("\nAvailable Personas:")
        personas = self.data_store.get_all_personas()
        if personas:
            for persona in personas:
                print(f"  {persona['id']}. {persona['name']}")
            persona_input = input("Enter persona ID (or press Enter to skip): ").strip()
            persona_id = int(persona_input) if persona_input and persona_input.isdigit() else None
        else:
            print("  (No personas created yet)")
            persona_id = None
        
        journey_stage = input("Enter journey stage (e.g., Awareness, Consideration, etc., or press Enter to skip): ").strip()
        journey_stage = journey_stage if journey_stage else None
        
        ask_summary = input("Generate AI summary? (y/n): ").strip().lower()
        ai_summary = None
        
        if ask_summary == 'y':
            print("[PROCESSING] Generating AI summary...")
            ai_summary = self.ai_assistant.summarize_research(description)
        
        insight_id = self.data_store.add_insight(
            title=title,
            description=description,
            persona_id=persona_id,
            journey_stage=journey_stage,
            ai_summary=ai_summary
        )
        
        print(f"\n[SUCCESS] Insight created successfully! (ID: {insight_id})")
        if ai_summary:
            print(f"\n[AI SUMMARY]\n{ai_summary}")
    
    def view_all_insights(self):
        """View all research insights."""
        insights = self.data_store.get_all_insights()
        
        if not insights:
            print("\n[INFO] No insights created yet.")
            return
        
        print("\n--- All Research Insights ---")
        for insight in insights:
            self.print_insight_summary(insight)
    
    def print_insight_summary(self, insight: Dict):
        """Print a summary of an insight."""
        print(f"\n[INSIGHT] ID: {insight['id']} | Title: {insight['title']}")
        print(f"   Description: {insight['description'][:100]}..." if len(insight['description']) > 100 
              else f"   Description: {insight['description']}")
        if insight['persona_id']:
            persona = self.data_store.get_persona(insight['persona_id'])
            print(f"   Persona: {persona['name'] if persona else 'Unknown'}")
        if insight['journey_stage']:
            print(f"   Journey Stage: {insight['journey_stage']}")
        print(f"   Created: {insight['timestamp']}")
    
    def view_specific_insight(self):
        """View details of a specific insight."""
        self.view_all_insights()
        
        try:
            insight_id = int(input("\nEnter insight ID to view: ").strip())
            insight = self.data_store.get_insight(insight_id)
            
            if not insight:
                print("[ERROR] Insight not found.")
                return
            
            print("\n--- Insight Details ---")
            print(f"ID: {insight['id']}")
            print(f"Title: {insight['title']}")
            print(f"Description: {insight['description']}")
            if insight['persona_id']:
                persona = self.data_store.get_persona(insight['persona_id'])
                print(f"Persona: {persona['name'] if persona else 'Unknown'}")
            if insight['journey_stage']:
                print(f"Journey Stage: {insight['journey_stage']}")
            print(f"Created: {insight['timestamp']}")
            if insight['ai_summary']:
                print(f"\n[AI SUMMARY]\n{insight['ai_summary']}")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def edit_insight(self):
        """Edit an existing insight."""
        self.view_all_insights()
        
        try:
            insight_id = int(input("\nEnter insight ID to edit: ").strip())
            insight = self.data_store.get_insight(insight_id)
            
            if not insight:
                print("[ERROR] Insight not found.")
                return
            
            print("\n--- Edit Insight ---")
            print("(Press Enter to keep current value)")
            
            new_title = input(f"Title [{insight['title']}]: ").strip()
            new_description = input(f"Description [{insight['description'][:50]}...]: ").strip()
            
            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_description:
                updates['description'] = new_description
            
            if updates:
                self.data_store.update_insight(insight_id, **updates)
                print("[SUCCESS] Insight updated successfully!")
            else:
                print("[INFO] No changes made.")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def delete_insight(self):
        """Delete an insight."""
        self.view_all_insights()
        
        try:
            insight_id = int(input("\nEnter insight ID to delete: ").strip())
            
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.data_store.delete_insight(insight_id):
                    print("[SUCCESS] Insight deleted successfully!")
                else:
                    print("[ERROR] Insight not found.")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def generate_ai_summary(self):
        """Generate or regenerate AI summary for an insight."""
        self.view_all_insights()
        
        try:
            insight_id = int(input("\nEnter insight ID to summarize: ").strip())
            insight = self.data_store.get_insight(insight_id)
            
            if not insight:
                print("[ERROR] Insight not found.")
                return
            
            print("[PROCESSING] Generating AI summary...")
            summary = self.ai_assistant.summarize_research(insight['description'])
            
            save = input("\nSave this summary to the insight? (y/n): ").strip().lower()
            if save == 'y':
                self.data_store.update_insight(insight_id, ai_summary=summary)
                print("[SUCCESS] Summary saved!")
            
            print(f"\n[AI SUMMARY]\n{summary}")
        
        except ValueError:
            print("❌ Invalid ID. Please enter a number.")
    
    def manage_personas(self):
        """Manage personas."""
        while True:
            self.display_persona_menu()
            choice = input("Select an option: ").strip()
            
            if choice == '1':
                self.create_persona()
            elif choice == '2':
                self.view_all_personas()
            elif choice == '3':
                self.view_specific_persona()
            elif choice == '4':
                self.edit_persona()
            elif choice == '5':
                self.delete_persona()
            elif choice == '6':
                break
            else:
                print("[ERROR] Invalid option. Please try again.")
    
    def create_persona(self):
        """Create a new persona."""
        print("\n--- Create New Persona ---")
        
        name = input("Enter persona name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty.")
            return
        
        description = input("Enter persona description (characteristics, needs, goals): ").strip()
        if not description:
            print("[ERROR] Description cannot be empty.")
            return
        
        persona_id = self.data_store.add_persona(name=name, description=description)
        print(f"\n[SUCCESS] Persona created successfully! (ID: {persona_id})")
    
    def view_all_personas(self):
        """View all personas."""
        personas = self.data_store.get_all_personas()
        
        if not personas:
            print("\n[INFO] No personas created yet.")
            return
        
        print("\n--- All Personas ---")
        for persona in personas:
            print(f"\n[PERSONA] ID: {persona['id']} | {persona['name']}")
            print(f"   Description: {persona['description'][:100]}..." if len(persona['description']) > 100 
                  else f"   Description: {persona['description']}")
            print(f"   Created: {persona['timestamp']}")
    
    def view_specific_persona(self):
        """View details of a specific persona."""
        self.view_all_personas()
        
        try:
            persona_id = int(input("\nEnter persona ID to view: ").strip())
            persona = self.data_store.get_persona(persona_id)
            
            if not persona:
                print("[ERROR] Persona not found.")
                return
            
            print("\n--- Persona Details ---")
            print(f"ID: {persona['id']}")
            print(f"Name: {persona['name']}")
            print(f"Description: {persona['description']}")
            print(f"Created: {persona['timestamp']}")
            
            # Show insights linked to this persona
            linked_insights = [i for i in self.data_store.get_all_insights() 
                             if i['persona_id'] == persona_id]
            if linked_insights:
                print(f"\nLinked Insights ({len(linked_insights)}):")
                for insight in linked_insights:
                    print(f"  - {insight['title']}")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def edit_persona(self):
        """Edit an existing persona."""
        self.view_all_personas()
        
        try:
            persona_id = int(input("\nEnter persona ID to edit: ").strip())
            persona = self.data_store.get_persona(persona_id)
            
            if not persona:
                print("[ERROR] Persona not found.")
                return
            
            print("\n--- Edit Persona ---")
            print("(Press Enter to keep current value)")
            
            new_name = input(f"Name [{persona['name']}]: ").strip()
            new_description = input(f"Description [{persona['description'][:50]}...]: ").strip()
            
            updates = {}
            if new_name:
                updates['name'] = new_name
            if new_description:
                updates['description'] = new_description
            
            if updates:
                self.data_store.update_persona(persona_id, **updates)
                print("Persona updated successfully")
            else:
                print("[INFO] No changes made.")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def delete_persona(self):
        """Delete a persona."""
        self.view_all_personas()
        
        try:
            persona_id = int(input("\nEnter persona ID to delete: ").strip())
            
            # Check if persona has linked insights
            linked_insights = [i for i in self.data_store.get_all_insights() 
                             if i['persona_id'] == persona_id]
            
            if linked_insights:
                print(f"\n[WARNING] This persona has {len(linked_insights)} linked insight(s).")
                print("Deleting will not remove the insights, but they will be unlinked.")
            
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.data_store.delete_persona(persona_id):
                    print("Persona deleted successfully!")
                else:
                    print("[ERROR] Persona not found.")
        
        except ValueError:
            print("[ERROR] Invalid ID. Please enter a number.")
    
    def run(self):
        """Run the main CLI loop."""
        print("\nWelcome to UX Research Manager!")
        print("Store, organize, and analyze your UX research insights.\n")
        
        while True:
            self.display_menu()
            choice = input("Select an option: ").strip()
            
            if choice == '1':
                self.create_insight()
            elif choice == '2':
                self.view_all_insights()
            elif choice == '3':
                self.view_specific_insight()
            elif choice == '4':
                self.edit_insight()
            elif choice == '5':
                self.delete_insight()
            elif choice == '6':
                self.generate_ai_summary()
            elif choice == '7':
                self.manage_personas()
            elif choice == '8':
                print("\n Thank you for using UX Research Manager!")
                print("Goodbye!\n")
                break
            else:
                print("[ERROR] Invalid option. Please select 1-8.")

    """Application entry point."""
    app = UXResearchManager()
    app.run()


if __name__ == "__main__":
    main()
