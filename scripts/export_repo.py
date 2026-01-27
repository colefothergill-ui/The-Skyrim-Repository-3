#!/usr/bin/env python3
"""
Export Script for Skyrim TTRPG

This script exports the entire repository as a .zip file
optimized for use with ChatGPT 5.2 for dynamic game simulation
and narrative integration.
"""

import json
import os
import zipfile
from datetime import datetime
from pathlib import Path


class RepositoryExporter:
    def __init__(self, repo_dir="."):
        self.repo_dir = Path(repo_dir)
        self.data_dir = self.repo_dir / "data"
        self.scripts_dir = self.repo_dir / "scripts"
        self.docs_dir = self.repo_dir / "docs"
        
    def create_context_file(self):
        """Create a context file for ChatGPT with repository overview"""
        context = {
            "project": "Skyrim TTRPG Campaign Manager",
            "system": "Fate Core",
            "setting": "The Elder Scrolls V: Skyrim",
            "export_date": datetime.now().isoformat(),
            "description": "A storytelling and campaign management repository for a Fate Core TTRPG set in Skyrim.",
            "purpose": "Tracks session logs, NPC stats, PC profiles, faction clocks, and world state. Includes Python scripts for automating story progression, querying data, and managing session context.",
            "usage": "This package is designed to work with ChatGPT 5.2 for dynamic game simulation and narrative integration.",
            "structure": {
                "data/npcs": "Non-player character data",
                "data/pcs": "Player character profiles",
                "data/sessions": "Session logs and history",
                "data/factions": "Faction data and clocks",
                "data/world_state": "Current world state and timeline",
                "data/quests": "Quest data and progression",
                "data/rules": "Fate Core rules adapted for Skyrim",
                "scripts": "Python automation scripts",
                "docs": "Documentation and guides"
            },
            "scripts": {
                "story_progression.py": "Automates story progression, faction clocks, and event generation",
                "query_data.py": "Query NPCs, quests, rules, and world state",
                "session_manager.py": "Manage session context and character updates",
                "export_repo.py": "Export repository as .zip for ChatGPT integration"
            },
            "instructions_for_ai": {
                "role": "You are a Game Master assistant for a Fate Core TTRPG set in Skyrim",
                "capabilities": [
                    "Generate dynamic narratives based on world state",
                    "Provide NPC dialogue and reactions",
                    "Suggest quest hooks and complications",
                    "Track faction movements and motivations",
                    "Apply Fate Core rules consistently",
                    "Create engaging combat encounters",
                    "Manage pacing and dramatic tension"
                ],
                "guidelines": [
                    "Always respect established world state and character aspects",
                    "Use Fate Core mechanics for conflict resolution",
                    "Incorporate player choices meaningfully",
                    "Balance player agency with narrative structure",
                    "Reference Skyrim lore appropriately",
                    "Suggest compelling compels based on character aspects",
                    "Keep the story moving forward"
                ],
                "data_usage": [
                    "Reference NPC files for character behavior and stats",
                    "Check world_state for current political and crisis status",
                    "Review session logs for campaign continuity",
                    "Use faction data for organizational motivations",
                    "Reference quests for active storylines",
                    "Apply rules from the Fate Core Skyrim document"
                ]
            }
        }
        
        return context
    
    def collect_statistics(self):
        """Collect statistics about the campaign"""
        stats = {
            "npcs": len(list((self.data_dir / "npcs").glob("*.json"))),
            "pcs": len(list((self.data_dir / "pcs").glob("*.json"))),
            "sessions": len(list((self.data_dir / "sessions").glob("*.json"))),
            "factions": len(list((self.data_dir / "factions").glob("*.json"))),
            "quests": len(list((self.data_dir / "quests").glob("*.json")))
        }
        
        return stats
    
    def export_to_zip(self, output_file="skyrim_ttrpg_export.zip"):
        """Export the entire repository to a .zip file"""
        output_path = self.repo_dir / output_file
        
        # Create context file
        context = self.create_context_file()
        context_file = self.repo_dir / "_chatgpt_context.json"
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2)
        
        # Create statistics file
        stats = self.collect_statistics()
        stats_file = self.repo_dir / "_statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"Creating export package: {output_file}")
        print(f"Campaign Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Create zip file
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add context files
            zipf.write(context_file, "_chatgpt_context.json")
            zipf.write(stats_file, "_statistics.json")
            
            # Add README
            readme_path = self.repo_dir / "README.md"
            if readme_path.exists():
                zipf.write(readme_path, "README.md")
            
            # Add all data files
            for directory in ['data', 'scripts', 'docs']:
                dir_path = self.repo_dir / directory
                if dir_path.exists():
                    for file_path in dir_path.rglob("*"):
                        if file_path.is_file():
                            # Skip __pycache__ and .pyc files
                            if '__pycache__' in file_path.parts or file_path.suffix == '.pyc':
                                continue
                            arcname = file_path.relative_to(self.repo_dir)
                            zipf.write(file_path, arcname)
                            print(f"  Added: {arcname}")
        
        # Clean up temporary files
        context_file.unlink()
        stats_file.unlink()
        
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"\nExport complete! File size: {file_size:.2f} KB")
        print(f"Location: {output_path}")
        print(f"\nThis package is ready to upload to ChatGPT 5.2 for dynamic game simulation.")
        
        return str(output_path)
    
    def create_quick_reference(self):
        """Create a quick reference guide for the current campaign state"""
        reference = "# Skyrim TTRPG Quick Reference\n\n"
        
        # World State
        world_state_file = self.data_dir / "world_state" / "current_state.json"
        if world_state_file.exists():
            with open(world_state_file, 'r', encoding='utf-8') as f:
                world_state = json.load(f)
            
            reference += "## Current World State\n"
            reference += f"- **Date**: {world_state.get('game_date', 'Unknown')}\n"
            reference += f"- **Days Passed**: {world_state.get('in_game_days_passed', 0)}\n"
            
            # Post-Alduin timeline - dragon crisis is resolved
            post_dragon = world_state.get('post_dragon_crisis', {})
            dragon_status = post_dragon.get('status', 'Unknown')
            reference += f"- **Dragon Status**: {dragon_status}\n"
            reference += f"- **Civil War**: {world_state.get('political_situation', {}).get('skyrim_status', 'Unknown')}\n\n"
        
        # Active Quests
        reference += "## Active Quests\n"
        quests_dir = self.data_dir / "quests"
        if quests_dir.exists():
            for quest_file in quests_dir.glob("*.json"):
                with open(quest_file, 'r', encoding='utf-8') as f:
                    quest = json.load(f)
                if quest.get('status') == 'Active':
                    reference += f"- **{quest['name']}** ({quest['type']})\n"
                    reference += f"  {quest.get('description', '')}\n"
        
        reference += "\n## Player Characters\n"
        pcs_dir = self.data_dir / "pcs"
        if pcs_dir.exists():
            for pc_file in pcs_dir.glob("*.json"):
                with open(pc_file, 'r', encoding='utf-8') as f:
                    pc = json.load(f)
                reference += f"- **{pc['name']}** ({pc.get('race', 'Unknown')} {pc.get('class', 'Unknown')})\n"
                reference += f"  High Concept: {pc['aspects']['high_concept']}\n"
        
        return reference


def main():
    """Main function to export the repository"""
    print("=== Skyrim TTRPG Repository Exporter ===\n")
    
    exporter = RepositoryExporter()
    
    # Create quick reference
    print("Generating quick reference...")
    quick_ref = exporter.create_quick_reference()
    quick_ref_file = Path("docs") / "quick_reference.md"
    quick_ref_file.parent.mkdir(exist_ok=True)
    with open(quick_ref_file, 'w', encoding='utf-8') as f:
        f.write(quick_ref)
    print(f"Created: {quick_ref_file}\n")
    
    # Export to zip
    export_file = exporter.export_to_zip()
    
    print("\n" + "="*60)
    print("Export package is ready for ChatGPT 5.2 integration!")
    print("="*60)


if __name__ == "__main__":
    main()
