# NewsServiceAutomate

Un petit service Python qui récupère la météo, l'actualité et les cours de cryptomonnaies, construit un corps d'email HTML quotidien et l'envoie aux abonnés.

## Objectif

Ce projet automatise la collecte de données (API météo, API d'actualité, API CoinGecko), assemble le contenu dans un modèle HTML et envoie un email quotidien aux abonnés.

## Arborescence importante

- `src/` : code source
	- `classes/Data_Call.py` : récupère et traite les données des APIs
	- `classes/mail_service.py` : compose le mail HTML, formate et l'envoie
- `data/` : dossiers de sortie (générés par les scripts)
- `src/scripts/` : scripts shell utilitaires (`load.sh`, `checkFile.sh`)
- `env/` : virtualenv local (ignorez si vous utilisez votre propre environnement)
- `logs/` : (recommandé) dossier où sont écrits les logs des exécutions

## Prérequis

- Python 3.10+
- Virtualenv recommandé
- Dépendances (exemples) : `requests`, `python-dotenv`

Installez-les depuis `requirements.txt` si présent :

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` à la racine du projet (ou exportez les variables d'environnement) avec au minimum :

```
WEATHER_MAP_URL=...
NEWS_API_URL=...
GECKO_URL=https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc
SMTP_EMAIL=you@example.com
SMTP_PASS=your_smtp_password
```

Assurez-vous que les URLs/API keys sont valides.

## Exécution manuelle

Pour tester localement (sans cron) :

```bash
source env/bin/activate
python3 -m src.classes.mail_service
```
NB: Concernant le **cron** vous aurez à ajouter au crontab l'exécution du script python avec l'environnement virtuelle créer.
    Pour les système sous windows des alternatives tel que : **Windows Task scheduler**, **APScheduler** ou **schedule** (librairie python).

## Tips & dépannage

- Si des fichiers (ex : `env/`, `.env`) ont été poussés malgré `.gitignore`, vérifiez s'ils étaient déjà suivis par Git. Pour retirer du suivi sans supprimer localement :

```bash
git rm -r --cached env
git rm --cached .env
git add .gitignore
git commit -m "Stop tracking env and .env"
git push
```

- Si vous recevez des erreurs `ModuleNotFoundError: No module named 'email.parser'`, vérifiez qu'il n'y a pas de fichier `email.py` dans votre projet (le module standard `email` est masqué par ce fichier). Renommez-le si besoin.

- Pour les erreurs CSS/premailer lors de l'envoi d'email, le projet strippe aujourd'hui le bloc `<style>` avant envoi (solution courte). Idéalement, utilisez du CSS inline ou `premailer` pour convertir les styles dans des attributs `style` compatibles email.

## Améliorations possibles

- Utiliser Jinja2 pour gérer proprement les templates HTML et éviter l'échappement manuel des accolades.
- Remplacer la méthode de suppression du CSS par une vraie inlining (avec `premailer`) et limiter les règles CSS non compatibles email (grid, flex, object-fit). 
- Ajouter un mécanisme de rotation des logs et un verrou (lockfile) pour empêcher les exécutions simultanées.

## Contact

Pour toute question ou demande d'amélioration, ouvrez une issue dans le dépôt.

