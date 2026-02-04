"""
UX Research Manager - CLI Prototype (Web-Ready)
This is a CLI application with persistent data storage for managing UX research 
insights and personas. It can optionally summarize research notes using an AI API.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import requests

# Data file paths
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "research_data.json"


# ------------------ Persistent Data ------------------ #
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
            with open(DATA_FILE, 'w') as f:
                json.dump({'insights': self.insights, 'personas': self.personas}, f, indent=2)
        except Exception as e:
            print(f"[WARNING] Error saving data file: {e}")

    # ------------------ Insight Methods ------------------ #
    def add_insight(self, title: str, description: str, persona_id: Optional[int] = None,
                    journey_stage: Optional[str] = None, ai_summary: Optional[str] = None) -> int:
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
        return next((i for i in self.insights if i['id'] == insight_id), None)

    def get_all_insights(self) -> List[Dict]:
        return self.insights

    def update_insight(self, insight_id: int, **kwargs) -> bool:
        insight = self.get_insight(insight_id)
        if insight:
            insight.update(kwargs)
            self.save_to_file()
            return True
        return False

    def delete_insight(self, insight_id: int) -> bool:
        for i, insight in enumerate(self.insights):
            if insight['id'] == insight_id:
                self.insights.pop(i)
                self.save_to_file()
                return True
        return False

    # ------------------ Persona Methods ------------------ #
    def add_persona(self, name: str, description: str) -> int:
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
        return next((p for p in self.personas if p['id'] == persona_id), None)

    def get_all_personas(self) -> List[Dict]:
        return self.personas

    def update_persona(self, persona_id: int, **kwargs) -> bool:
        persona = self.get_persona(persona_id)
        if persona:
            persona.update(kwargs)
            self.save_to_file()
            return True
        return False

    def delete_persona(self, persona_id: int) -> bool:
        for i, persona in enumerate(self.personas):
            if persona['id'] == persona_id:
                self.personas.pop(i)
                self.save_to_file()
                return True
        return False


# ------------------ AI Assistant ------------------ #
class AIAssistant:
    """Handles AI-assisted summarization using a REST API."""

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY", "")
        self.api_url = "https://api.mistral.ai/v1/chat/completions"  # replace with actual API URL

    def summarize_research(self, research_notes: str) -> str:
        """Summarize research notes via API or return mock summary if API is unavailable."""
        if not self.api_key:
            return "[MOCK SUMMARY] No API key provided. Here's a placeholder summary."

        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": "You are a UX research assistant."},
                        {"role": "user", "content": research_notes}
                    ]
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[WARNING] API error: {str(e)}"


# ------------------ CLI Application ------------------ #
class UXResearchManager:

    def __init__(self):
        self.data_store = DataStore()
        self.ai_assistant = AIAssistant()

    # ---------- CLI Helpers ---------- #
    def prompt_return_or_retry(self, menu_type="main") -> bool:
        while True:
            print("\n1. Try again\n2. Return to menu")
            choice = input("Select: ").strip()
            if choice == '1': return True
            if choice == '2': return False
            print("[ERROR] Invalid selection.")

    def confirm_action(self, action_name: str) -> bool:
        print(f"\n[INFO] You selected: {action_name}")
        response = input("Press Enter to continue or type 'back' to cancel: ").strip().lower()
        return response == ''

    def display_menu(self):
        print("\n" + "="*50)
        print("  UX RESEARCH MANAGER - CLI")
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

    # ---------- Insights ---------- #
    def create_insight(self):
        if not self.confirm_action("Create Research Insight"): return
        title = input("Enter insight title: ").strip()
        if not title: return print("[ERROR] Title cannot be empty.")
        description = input("Enter research notes: ").strip()
        if not description: return print("[ERROR] Description cannot be empty.")

        # Persona association
        persona_id = None
        personas = self.data_store.get_all_personas()
        if personas:
            print("\nAvailable Personas:")
            for p in personas: print(f"  {p['id']}. {p['name']}")
            pid = input("Enter persona ID (or Enter to skip): ").strip()
            if pid.isdigit() and self.data_store.get_persona(int(pid)):
                persona_id = int(pid)

        # Journey stage
        journey_stage = None
        stages = ["Awareness","Consideration","Decision","Retention","Advocacy"]
        print("\nJourney Stages:")
        for idx, s in enumerate(stages,1): print(f"{idx}. {s}")
        stage_input = input("Select journey stage (1-5 or Enter to skip): ").strip()
        if stage_input in [str(i) for i in range(1,6)]: journey_stage = stages[int(stage_input)-1]

        # AI summary
        ai_summary = None
        if input("Generate AI summary? (y/n): ").strip().lower() == 'y':
            print("[PROCESSING] Generating AI summary...")
            ai_summary = self.ai_assistant.summarize_research(description)

        insight_id = self.data_store.add_insight(title, description, persona_id, journey_stage, ai_summary)
        print(f"\n[SUCCESS] Insight created! (ID: {insight_id})")
        if ai_summary: print(f"\n[AI SUMMARY]\n{ai_summary}")

    def view_all_insights(self):
        insights = self.data_store.get_all_insights()
        if not insights:
            print("[INFO] No insights yet."); return
        print("\n--- All Insights ---")
        for i in insights:
            print(f"\nID: {i['id']} | Title: {i['title']}")
            print(f"Description: {i['description'][:100]}..." if len(i['description'])>100 else f"Description: {i['description']}")
            if i['persona_id']:
                persona = self.data_store.get_persona(i['persona_id'])
                print(f"Persona: {persona['name'] if persona else 'Unknown'}")
            if i['journey_stage']: print(f"Journey Stage: {i['journey_stage']}")
            if i['ai_summary']: print(f"AI Summary: {i['ai_summary'][:100]}...")

    # ---------- Personas ---------- #
    def manage_personas(self):
        while True:
            self.display_persona_menu()
            choice = input("Select: ").strip()
            if choice == '1': self.create_persona()
            elif choice == '2': self.view_all_personas()
            elif choice == '3': self.view_specific_persona()
            elif choice == '4': self.edit_persona()
            elif choice == '5': self.delete_persona()
            elif choice == '6': break
            else:
                if not self.prompt_return_or_retry("persona"): break

    def create_persona(self):
        if not self.confirm_action("Create Persona"): return
        name = input("Enter persona name: ").strip()
        if not name: return print("[ERROR] Name cannot be empty.")
        desc = input("Enter description: ").strip()
        if not desc: return print("[ERROR] Description cannot be empty.")
        pid = self.data_store.add_persona(name, desc)
        print(f"[SUCCESS] Persona created! (ID: {pid})")

    def view_all_personas(self):
        personas = self.data_store.get_all_personas()
        if not personas: return print("[INFO] No personas yet.")
        for p in personas:
            print(f"\nID: {p['id']} | {p['name']}")
            print(f"Description: {p['description'][:100]}..." if len(p['description'])>100 else f"Description: {p['description']}")
            print(f"Created: {p['timestamp']}")

    # ---------- Run ---------- #
    def run(self):
        print("\nWelcome to UX Research Manager!\n")
        while True:
            self.display_menu()
            choice = input("Select: ").strip()
            if choice == '1': self.create_insight()
            elif choice == '2': self.view_all_insights()
            elif choice == '7': self.manage_personas()
            elif choice == '8': break
            else: print("[ERROR] Invalid option.")


# ------------------ Main ------------------ #
def main():
    app = UXResearchManager()
    app.run()


if __name__ == "__main__":
    main()
