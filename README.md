# 🐱 Neko Chat — Minou

**[Français](#français) · [English](#english)**

---

## Français

Minou est un petit chat de bureau (façon *oneko*) qui se promène sur ton écran.
Clique sur lui et une petite boîte s'ouvre **au-dessus de sa tête** pour
**papoter en français**, juste pour le plaisir.

### ✨ Ce qu'il fait
- 🚶 Se promène tout seul par-dessus tes fenêtres.
- 💬 Clic dessus → boîte de discussion sur sa tête (× ou **Échap** pour fermer).
- 🐱 Discute comme une **amie**, sans jamais corriger tes fautes.
- 🔥 Tient un petit carnet : il est triste 🥺 si tu n'as pas écrit aujourd'hui,
  tout content 😺 dès que tu lui parles, et il compte les jours d'affilée.
- 🔒 **Hors-ligne, rien de sauvegardé** (juste les *dates* où tu écris), 0 token.

### ▶️ Lancer
```bash
python3 neko_francais.py &
```
Pour quitter : clic droit sur Minou → *Quitter* (ou `Ctrl+C`).

### 🧩 Besoins
- Linux en session **X11**
- Python 3
- PyQt5 — `sudo apt install python3-pyqt5`

### 🧠 IA locale (optionnelle)
Par défaut Minou répond avec un petit moteur simple (des phrases pré-écrites).
Si tu installes [**Ollama**](https://ollama.com) et un modèle (ex. `llama3.2:3b`),
Minou utilise une **vraie petite IA qui tourne sur ta machine** — toujours
**gratuit, hors-ligne, sans aucun token**. L'appli démarre Ollama toute seule
si besoin. Si l'IA n'est pas là, Minou repasse automatiquement sur le mode simple.
Tu peux changer le modèle en haut de `neko_francais.py` (`OLLAMA_MODEL`).

### 🛠️ Personnaliser
Tout en haut de `neko_francais.py`, tu peux changer les listes de phrases
(`QUESTIONS`, `GREETINGS`, `REACTIONS`, `TOPICS`…) et les réglages
(vitesse, taille du chat).

Fait avec 💛 — un petit chat pour écrire en français, sans pression.

---

## English

Minou is a little desktop cat (*oneko*-style) that wanders around your screen.
Click on it and a small box opens **above its head** so you can **chat in
French**, just for fun.

### ✨ What it does
- 🚶 Wanders on its own on top of your windows.
- 💬 Click it → a chat box over its head (× or **Esc** to close).
- 🐱 Chats like a **friend**, never correcting your mistakes.
- 🔥 Keeps a little notebook: it's sad 🥺 if you haven't written today,
  happy 😺 as soon as you talk to it, and it counts your streak of days.
- 🔒 **Offline, nothing saved** (only the *dates* you write), 0 tokens.

### ▶️ Run
```bash
python3 neko_francais.py &
```
To quit: right-click Minou → *Quitter* (or `Ctrl+C`).

### 🧩 Requirements
- Linux in an **X11** session
- Python 3
- PyQt5 — `sudo apt install python3-pyqt5`

### 🧠 Local AI (optional)
By default Minou answers with a small simple engine (pre-written sentences).
If you install [**Ollama**](https://ollama.com) and a model (e.g. `llama3.2:3b`),
Minou uses a **real small AI running on your machine** — still **free, offline,
no tokens at all**. The app starts Ollama by itself if needed. If the AI isn't
there, Minou automatically falls back to simple mode.
You can change the model at the top of `neko_francais.py` (`OLLAMA_MODEL`).

### 🛠️ Customize
At the very top of `neko_francais.py`, you can change the sentence lists
(`QUESTIONS`, `GREETINGS`, `REACTIONS`, `TOPICS`…) and the settings
(speed, cat size).

---
Made with 💛 — a little cat for writing in French, no pressure.
