from mistral_client import mistral_chat_completion

def generate_readme(specification: str) -> str:
    prompt = f"""
Tu es un assistant qui écrit un fichier README.md complet et professionnel pour un projet logiciel.
Voici la demande utilisateur : \"{specification}\"

Écris directement le contenu markdown du README.md, avec sections usuelles (titre, description, installation, usage, licence, etc. si pertinent).
"""
    return mistral_chat_completion(prompt)

def save_readme(content: str, filename="README.md") -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"README.md généré et sauvegardé dans {filename}"
