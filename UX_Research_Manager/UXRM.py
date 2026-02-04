"""
UX Research Manager - CLI Prototype (Chunk 1)

This is a command-line interface prototype for managing UX research insights 
and personas. It provides functionality to create, view, edit, and delete 
research insights, create and manage personas, and use AI to summarize research notes.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("KEY PREFIX:", os.getenv("MISTRAL_API_KEY", "")[:10])


# Try to import Mistral AI
try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False


# ------------------ Data Store ------------------ #
class DataStore:
    """Manages in-memory storage for insights and personas."""

    def __init__(self):
        self.insights: Dict = {}
        self.personas: Dict = {}
        self.next_insight_id = 1
        self.next_persona_id = 1

    def add_insight(
        self,
        title: str,
        description: str,
        persona_id: Optional[int] = None,
        journey_stage: Optional[str] = None,
        ai_summary: Optional[str] = None,
    ) -> int:
        insight_id = self.next_insight_id
        self.insights[insight_id] = {
            "id": insight_id,
            "title": title,
            "description": description,
            "persona_id": persona_id,
            "journey_stage": journey_stage,
            "timestamp": datetime.now().isoformat(),
            "ai_summary": ai_summary,
        }
        self.next_insight_id += 1
        return insight_id

    def get_insight(self, insight_id: int) -> Optional[Dict]:
        return self.insights.get(insight_id)

    def get_all_insights(self) -> List[Dict]:
        return list(self.insights.values())

    def update_insight(self, insight_id: int, **kwargs) -> bool:
        if insight_id not in self.insights:
            return False
        self.insights[insight_id].update(kwargs)
        return True

    def delete_insight(self, insight_id: int) -> bool:
        return self.insights.pop(insight_id, None) is not None

    def add_persona(self, name: str, description: str) -> int:
        persona_id = self.next_persona_id
        self.personas[persona_id] = {
            "id": persona_id,
            "name": name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        }
        self.next_persona_id += 1
        return persona_id

    def get_persona(self, persona_id: int) -> Optional[Dict]:
        return self.personas.get(persona_id)

    def get_all_personas(self) -> List[Dict]:
        return list(self.personas.values())

    def update_persona(self, persona_id: int, **kwargs) -> bool:
        if persona_id not in self.personas:
            return False
        self.personas[persona_id].update(kwargs)
        return True

    def delete_persona(self, persona_id: int) -> bool:
        return self.personas.pop(persona_id, None) is not None


# ------------------ AI Assistant ------------------ #
class AIAssistant:
    """Handles AI-assisted summarization using Mistral."""

    def __init__(self):
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY", "")

    def summarize_research(self, research_notes: str) -> str:
        if not MISTRAL_AVAILABLE:
            return (
                "[WARNING] Mistral AI is unavailable.\n"
                "Install with: pip install mistralai"
            )

        if not self.mistral_api_key:
            return (
                "[WARNING] No Mistral API key configured.\n"
                "Set MISTRAL_API_KEY in your environment."
            )

        try:
            mistral = Mistral(api_key=self.mistral_api_key)

            res = mistral.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a UX research assistant. Summarize research notes "
                            "into clear, actionable insights for UX designers. Be concise "
                            "and focus on key findings and implications."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Please summarize the following research notes:\n\n"
                            f"{research_notes}"
                        ),
                    },
                ],
            )

            return res.choices[0].message.content

        except Exception as e:
            return f"[WARNING] Mistral API Error: {e}"


# ------------------ Main Application ------------------ #
class UXResearchManager:
    """Main CLI application."""

    def __init__(self):
        self.data_store = DataStore()
        self.ai_assistant = AIAssistant()

    def display_menu(self):
        print("\n" + "=" * 50)
        print("  UX RESEARCH MANAGER - CLI Prototype")
        print("=" * 50)
        print("1. Create Research Insight")
        print("2. View All Insights")
        print("3. Generate AI Summary")
        print("4. Manage Personas")
        print("5. Exit")
        print("-" * 50)

    def create_insight(self):
        title = input("Enter insight title: ").strip()
        description = input("Enter research notes: ").strip()

        ai_summary = None
        if input("Generate AI summary? (y/n): ").lower() == "y":
            print("[PROCESSING] Generating AI summary...")
            ai_summary = self.ai_assistant.summarize_research(description)

        insight_id = self.data_store.add_insight(
            title=title,
            description=description,
            ai_summary=ai_summary,
        )

        print(f"\n[SUCCESS] Insight created (ID: {insight_id})")
        if ai_summary:
            print(f"\n[AI SUMMARY]\n{ai_summary}")

    def view_all_insights(self):
        insights = self.data_store.get_all_insights()
        if not insights:
            print("[INFO] No insights found.")
            return

        for i in insights:
            print(f"\n[{i['id']}] {i['title']}")
            print(i["description"])
            if i["ai_summary"]:
                print("\n[AI SUMMARY]")
                print(i["ai_summary"])

    def manage_personas(self):
        print("[INFO] Persona management coming next chunk 😉")

    def run(self):
        print("\nWelcome to UX Research Manager!\n")
        while True:
            self.display_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.create_insight()
            elif choice == "2":
                self.view_all_insights()
            elif choice == "3":
                self.create_insight()
            elif choice == "4":
                self.manage_personas()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("[ERROR] Invalid option.")


def main():
    UXResearchManager().run()


if __name__ == "__main__":
    main()
