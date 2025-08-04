import re
from dotenv import load_dotenv
from tools.email_sender import send_email
from tools.README_writer import generate_readme, save_readme
from mistral_client import mistral_chat_completion
import os
load_dotenv()

NAME = os.getenv("NAME", "AI Assistant")

def extract_email_data(command: str):
    prompt = f"""
Tu es un assistant intelligent qui extrait les informations nécessaires à l'envoi d'un email depuis une commande utilisateur imparfaite.
Extrait en JSON uniquement, sans explications, avec les champs :
{{"to": "adresse email", "subject": "objet du mail", "body": "contenu complet du mail, signé avec le nom {NAME}"}}
Commande : \"{command}\"
"""
    reply = mistral_chat_completion(prompt)
    try:
        to = re.search(r'"to"\s*:\s*"([^"]+)"', reply).group(1)
        subject = re.search(r'"subject"\s*:\s*"([^"]+)"', reply).group(1)
        body = re.search(r'"body"\s*:\s*"((?:[^"]|\\")*)"', reply, re.DOTALL).group(1)
        body = body.replace('\\"', '"').replace("\\n", "\n")
        return to.strip(), subject.strip(), body.strip()
    except Exception as e:
        raise ValueError(f"Impossible d'extraire les données depuis la réponse Mistral : {reply}") from e

def parse_and_execute(command: str) -> str:
    lowered = command.lower()
    if "readme" in lowered:
        import re
        match = re.search(r"readme\s*(.*)", command, re.IGNORECASE)
        spec = match.group(1).strip() if match else ""
        if not spec:
            return "Précisez la spécification du README à générer."
        content = generate_readme(spec)
        return save_readme(content)

    # reste inchangé...


    try:
        to, subject, body = extract_email_data(command)
        return send_email(to, subject, body)
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == "__main__":
    print("Agent AI prêt. Tape 'exit' pour quitter.")
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ("exit", "quit"):
            break
        print(parse_and_execute(user_input))
