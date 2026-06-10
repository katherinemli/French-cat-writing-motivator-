# 🐱 Neko Chat — Minou

Minou est un petit chat de bureau (façon *oneko*) qui se promène sur ton écran.
Clique sur lui et une petite boîte s'ouvre **au-dessus de sa tête** pour
**papoter en français**, juste pour le plaisir.

## ✨ Ce qu'il fait
- 🚶 Se promène tout seul par-dessus tes fenêtres.
- 💬 Clic dessus → boîte de discussion sur sa tête (× ou **Échap** pour fermer).
- 🐱 Discute comme une **amie**, sans jamais corriger tes fautes.
- 🔥 Tient un petit carnet : il est triste 🥺 si tu n'as pas écrit aujourd'hui,
  tout content 😺 dès que tu lui parles, et il compte les jours d'affilée.
- 🔒 **Hors-ligne, rien de sauvegardé** (juste les *dates* où tu écris), 0 token.

## ▶️ Lancer
```bash
python3 neko_francais.py &
```
Pour quitter : clic droit sur Minou → *Quitter* (ou `Ctrl+C`).

## 🧩 Besoins
- Linux en session **X11**
- Python 3
- PyQt5 — `sudo apt install python3-pyqt5`

## 🧠 IA locale (optionnelle)
Par défaut Minou répond avec un petit moteur simple (des phrases pré-écrites).
Si tu installes [**Ollama**](https://ollama.com) et un modèle (ex. `llama3.2:3b`),
Minou utilise une **vraie petite IA qui tourne sur ta machine** — toujours
**gratuit, hors-ligne, sans aucun token**. L'appli démarre Ollama toute seule
si besoin. Si l'IA n'est pas là, Minou repasse automatiquement sur le mode simple.
Tu peux changer le modèle en haut de `neko_francais.py` (`OLLAMA_MODEL`).

## 🛠️ Personnaliser
Tout en haut de `neko_francais.py`, tu peux changer les listes de phrases
(`QUESTIONS`, `GREETINGS`, `REACTIONS`, `TOPICS`…) et les réglages
(vitesse, taille du chat).

---
Fait avec 💛 — un petit chat pour écrire en français, sans pression.
