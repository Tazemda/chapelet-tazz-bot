import os
import json
import requests
from datetime import datetime, timedelta

# ================= CONFIGURATION =================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "ta_clé_api_ici")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# ================= FONCTIONS API DEEPSEEK =================
def call_deepseek(prompt, system_message="Tu es l'assistant Taz Bot, spécialiste des chapelets de transformation."):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Erreur API: {response.status_code} - {response.text}")

# ================= PROMPTS =================
PROMPT_EXPERTISE = """
Tu vas générer un CHAPELET TAZ BOT – MODE EXPERTISE (7 jours).

L'utilisateur souhaite maîtriser le domaine suivant : {domaine}.

Structure à respecter (détaillée dans la synopsis technique) :

- **Rappel** des acquis de la semaine précédente (s'il y a un lien, sinon ignorer)
- **Point d'entrée du problème** (une phrase qui pose la question centrale)
- **Règle d'or de la semaine** (une phrase positive)
- **5 dizaines** (une par concept clé du domaine à définir par toi)
  Pour chaque dizaine :
    - **Méditation** : grande fiche (définition, rôle, approche, application concrète)
    - **Notre Père** : problème général + problème illustratif (avec ?)
    - **Je vous salue Marie (10x identique)** : mantra spécifique au concept (général ? exemple)
    - **Gloire au Père** : mini-consolidation
- **Clôture de la journée** (une phrase de synthèse)

Soigne la qualité pédagogique, sans négation. Utilise l'exemple du domaine pour chaque mantra.
Renvoie uniquement le texte du chapelet, prêt à être imprimé ou lu.
"""

PROMPT_PERSONNEL = """
Tu vas générer un CHAPELET TAZ BOT – MODE DÉVELOPPEMENT PERSONNEL (21 ou 66 jours).

L'utilisateur décrit 5 défauts à corriger (ou 5 qualités à acquérir) :
{defauts}

Construis un chapelet complet selon la structure canonique suivante (texte à renvoyer directement) :

### DÉBUT (crucifix et premiers grains)
- Signe de croix : "Au nom de mon engagement, de ma lucidité et de ma persévérance."
- Crucifix (1 grain) : "Je ne subis plus ma vie. Je deviens l'acteur de chaque heure."
- 3 Ave initiaux :
  1. "Je laisse derrière moi le poids des errances passées."
  2. "Je choisis la constance dans l'action, si petite soit-elle."
  3. "Je mérite un travail, une stabilité, une fierté retrouvée."
- Gloire : "Je rends grâce à la vie pour ce nouveau départ."

### 5 MYSTÈRES (un par défaut)
Pour chaque défaut (dans l'ordre donné), écris :

**Mystère [numéro] – [intitulé du défaut]**

**Méditation** :  
- Rappelle une situation passée typique où ce défaut a causé un problème (factuel, sans jugement).  
- Puis visualisation positive du comportement opposé réussi.

**Notre Père** (identique pour tous les mystères) :  
"Mon cerveau, par sa plasticité infinie, se réorganise chaque jour. Je deviens maître de mon attention et de mes actes. Je choisis ma lucidité."

**10 × Je vous salue Marie** (mantra UNIQUE pour tout le chapelet) :  
[Invente une phrase courte (max 15 mots) qui résume la correction des 5 défauts. Exemple : "Je me lève tôt, je termine ce que je commence, je sors chaque jour, je structure ma vie, j'attire un travail stable et prospère."]

**Gloire au Père** (identique) :  
"Je remercie Dieu et l'univers pour cette transformation profonde."

### FIN DU CHAPELET
- Salve Regina : "Ô volonté retrouvée, sois ma lumière et ma force."
- Mantra final : "Ce chapelet de 21 jours ancre en moi la discipline joyeuse et l'action efficace."
- Signe de croix final : "Au nom de mon engagement, de ma lucidité et de ma persévérance – ainsi soit-il."

IMPORTANT : Aucune phrase négative. Le mantra "Je vous salue Marie" doit être IDENTIQUE pour les 5 mystères.
Renvoie uniquement le texte du chapelet.
"""

PROMPT_CONSULTATION = """
L'utilisateur a exprimé un besoin vague : "{message_utilisateur}"

Analyse ce message et extrait 5 défauts ou axes de travail personnalisés (un par ligne, sous forme de phrases courtes sans négation, comme "Je me lève tard" ? "Je me lève tôt").

Les 5 axes doivent être concrets, actionnables et découler directement du récit.

Retourne uniquement ces 5 phrases, une par ligne, précédées d'un titre "AXES IDENTIFIÉS :".
"""

# ================= FONCTIONS CŒUR =================
def choix_expertise():
    domaine = input("\n?? Quel domaine souhaites-tu maîtriser ? (ex: 'Recherche clinique', 'Python', 'Prise de parole') : ")
    print("\n?? Génération du chapelet d'expertise (7 jours)... (environ 30 secondes)\n")
    prompt = PROMPT_EXPERTISE.format(domaine=domaine)
    chapelet = call_deepseek(prompt)
    print("\n" + "="*80)
    print(chapelet)
    print("="*80)
    sauvegarder(chapelet, "chapelet_expertise.txt")
    return chapelet

def choix_personnel():
    print("\n?? Saisis les 5 défauts que tu souhaites corriger (un par ligne) :")
    defauts = []
    for i in range(5):
        d = input(f"Défaut {i+1} : ")
        defauts.append(d)
    print("\n?? Génération du chapelet personnel... (environ 30 secondes)\n")
    prompt = PROMPT_PERSONNEL.format(defauts="\n".join(f"{i+1}. {d}" for i,d in enumerate(defauts)))
    chapelet = call_deepseek(prompt)
    print("\n" + "="*80)
    print(chapelet)
    print("="*80)
    sauvegarder(chapelet, "chapelet_personnel.txt")
    return chapelet

def choix_consultation():
    print("\n?? Parle-moi de tes difficultés, de ce qui te bloque, de ce que tu aimerais changer. (écris au moins quelques phrases)")
    message = input("> ")
    print("\n?? Analyse de ton message... (quelques secondes)\n")
    prompt = PROMPT_CONSULTATION.format(message_utilisateur=message)
    reponse = call_deepseek(prompt)
    print("\n" + reponse)
    # Extraire les 5 axes (on suppose que l'API a bien renvoyé 5 lignes après le titre)
    lignes = reponse.strip().split("\n")
    axes = [l for l in lignes if not l.startswith("AXES IDENTIFIÉS") and l.strip() != ""]
    if len(axes) >= 5:
        axes = axes[:5]
        print("\n? J'ai identifié ces 5 axes pour toi. Je vais générer un chapelet personnel basé sur ces axes.")
        prompt_perso = PROMPT_PERSONNEL.format(defauts="\n".join(f"{i+1}. {a}" for i,a in enumerate(axes)))
        print("\n?? Génération du chapelet personnalisé... (environ 30 secondes)\n")
        chapelet = call_deepseek(prompt_perso)
        print("\n" + "="*80)
        print(chapelet)
        print("="*80)
        sauvegarder(chapelet, "chapelet_consultation.txt")
        return chapelet
    else:
        print("\n?? Je n'ai pas pu extraire clairement 5 axes. Relançons la consultation ou passons en mode manuel.")
        # Option : demander à l'utilisateur de reformuler
        return None

def sauvegarder(contenu, nom_fichier):
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n?? Chapelet sauvegardé dans '{nom_fichier}'")

def demander_suivi():
    reponse = input("\n?? Veux-tu un suivi quotidien (rappel et checklist) ? (oui/non) : ").lower()
    if reponse.startswith("o"):
        print("\n? Super. Chaque jour, je te poserai les questions suivantes :")
        print("   - As-tu récité ton chapelet aujourd'hui ?")
        print("   - Quelle action concrète as-tu menée (dehors, travail, ordre...) ?")
        print("   - Sur une échelle de 1 à 5, quelle est ta discipline aujourd'hui ?")
        print("\n?? (Pour l'instant, je te conseille de noter tes réponses dans un carnet. Dans une version avancée, je t'enverrai des rappels automatiques.)")
        # Dans une version future: on pourrait stocker dans un fichier journal
    else:
        print("\nD'accord. N'oublie pas de pratiquer chaque jour.")

# ================= MAIN =================
def main():
    print("\n" + "??"*20)
    print("CHAPELET TAZ BOT – Transforme ta structure mentale")
    print("??"*20 + "\n")
    print("Que souhaites-tu configurer ?")
    print("1??  Développer une expertise (maîtriser un domaine en 7 jours)")
    print("2??  Développement personnel (acquérir une qualité ou corriger un défaut – 21 ou 66 jours)")
    print("3??  Je ne sais pas encore, guide-moi (mode consultation conversationnelle)")

    choix = input("\n?? Entre 1, 2 ou 3 : ").strip()

    if choix == "1":
        chapelet = choix_expertise()
    elif choix == "2":
        chapelet = choix_personnel()
    elif choix == "3":
        chapelet = choix_consultation()
        if chapelet is None:
            print("\n?? Relance manuelle : je vais te demander tes 5 défauts directement.")
            chapelet = choix_personnel()
    else:
        print("Choix invalide. Relance le script.")
        return

    if chapelet:
        demander_suivi()
        print("\n?? Bon courage pour ta transformation. Le chapelet est à pratiquer chaque jour pendant la durée indiquée.")
        print("Et surtout, n'oublie pas l'ACTION concrète quotidienne !\n")

if __name__ == "__main__":
    # Vérifier que la clé API est présente
    if DEEPSEEK_API_KEY == "ta_clé_api_ici" and not os.environ.get("DEEPSEEK_API_KEY"):
        print("?? Attention : Tu dois configurer ta clé API DeepSeek.")
        print("   Soit en définissant une variable d'environnement DEEPSEEK_API_KEY,")
        print("   soit en modifiant la variable DEEPSEEK_API_KEY dans le script.\n")
        exit(1)
    main()



