#!/usr/bin/env python3
import argparse
import fitz  # PyMuPDF
from collections import defaultdict
import os
import json
from typing import Dict, List, DefaultDict

# Constants
SKILLS_DB_FILE = "skills_db.json"
DEFAULT_SKILLS = {
    "Programming": ["Python", "Java", "C++", "JavaScript", "SQL", "R", "Go"],
    "Data": ["SQL", "NoSQL", "Spark", "Pandas", "Tableau", "PowerBI", "Excel"],
    "ML/AI": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP"],
    "DevOps": ["Docker", "Kubernetes", "AWS", "Azure", "CI/CD", "Terraform"],
    "Soft Skills": ["Leadership", "Communication", "Teamwork", "Problem Solving"]
}

class ResumeAnalyzer:
    def __init__(self, skills_db: Dict[str, List[str]] = None):
        self.skills_db = skills_db if skills_db else self.load_skills_db()

    @staticmethod
    def load_skills_db() -> Dict[str, List[str]]:
        """Load skills database from JSON file or use defaults."""
        if os.path.exists(SKILLS_DB_FILE):
            with open(SKILLS_DB_FILE, 'r') as f:
                return json.load(f)
        return DEFAULT_SKILLS

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract lowercase text from PDF."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.lower()

    def analyze_skills(self, text: str) -> DefaultDict[str, int]:
        """Count occurrences of each skill."""
        skill_counts = defaultdict(int)
        for _, skills in self.skills_db.items():
            for skill in skills:
                if skill.lower() in text:
                    skill_counts[skill] += text.count(skill.lower())
        return skill_counts

    def suggest_improvements(self, skill_counts: DefaultDict[str, int]) -> List[str]:
        """Suggest adding or improving skill categories."""
        suggestions = []
        for category, skills in self.skills_db.items():
            found = [s for s in skills if s in skill_counts]
            if not found:
                suggestions.append(
                    f"⚠️ Missing {category} skills. Consider adding {', '.join(skills[:3])}..."
                )
            elif len(found) < 2:
                missing = [s for s in skills if s not in found][:2]
                suggestions.append(
                    f"ℹ️ Few {category} skills. Could add {', '.join(missing)}"
                )
        return suggestions

    def generate_report(self, skill_counts: DefaultDict[str, int], suggestions: List[str]) -> str:
        """Create the final printable report."""
        lines = ["\n=== SKILL ANALYSIS ==="]
        if not skill_counts:
            lines.append("No skills detected in resume.")
        else:
            for skill, cnt in sorted(skill_counts.items(), key=lambda x: (-x[1], x[0])):
                lines.append(f"• {skill}: {cnt} mention{'s' if cnt > 1 else ''}")
        if suggestions:
            lines.append("\n=== SUGGESTIONS ===")
            lines.extend(suggestions)
        else:
            lines.append("\n✅ All good! Your resume covers diverse skill areas.")
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Resume Analyzer CLI – skill insights & improvement suggestions"
    )
    parser.add_argument("resume", help="Path to PDF resume")
    parser.add_argument("--skills", help="Custom JSON skill database", default=None)
    args = parser.parse_args()

    try:
        # Load custom skills if provided
        skills_db = None
        if args.skills:
            with open(args.skills, 'r') as sf:
                skills_db = json.load(sf)
        analyzer = ResumeAnalyzer(skills_db)

        text = analyzer.extract_text(args.resume)
        counts = analyzer.analyze_skills(text)
        suggestions = analyzer.suggest_improvements(counts)

        print(f"\n📄 Analyzing: {os.path.basename(args.resume)}")
        print(analyzer.generate_report(counts, suggestions))

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
