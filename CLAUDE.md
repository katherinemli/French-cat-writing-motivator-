# Neko Chat 🐱 — guide pour Claude Code

Petit chat de bureau « façon oneko », écrit en Python/PyQt5.
Un seul fichier de code : `neko_francais.py`.

## Le projet
Minou est un petit chat qui se promène sur l'écran (fenêtre transparente,
toujours au-dessus). Quand on clique dessus, une petite boîte de discussion
s'ouvre au-dessus de sa tête pour papoter en français.

## Principes de design (IMPORTANT)
- Minou est une **amie, pas un professeur** : il **ne corrige JAMAIS** les
  fautes de français. Le but est d'écrire sans pression, juste pour le plaisir.
- **Hors-ligne, 0 token** : le chatbot est un petit moteur local à base de
  règles (`LocalBrain`) — pas d'IA distante, pas de clé API.
- **Vie privée** : on ne sauvegarde jamais le contenu des messages. On garde
  seulement les *dates* où l'utilisatrice a écrit
  (`~/.config/neko-francais/state.json`), pour la « série » 🔥 et l'humeur.

## Architecture (tout dans neko_francais.py)
- `MinouPet` : la fenêtre flottante. 2 modes : **promenade** (juste le chat)
  et **discussion** (clic → boîte sur la tête ; × ou Échap pour fermer).
- `Brain.get_reply()` : essaie d'abord une **IA locale via Ollama**
  (modèle `OLLAMA_MODEL`, par défaut `llama3.2:3b`) ; si Ollama/le modèle
  n'est pas dispo, **repli automatique** sur `LocalBrain.reply()` (réponses
  simples à partir des listes éditables `GREETINGS`, `QUESTIONS`, `REACTIONS`,
  `TOPICS`…). Les réponses sont calculées dans un `ReplyWorker` (QThread) pour
  ne pas figer la fenêtre. L'appli démarre `ollama serve` toute seule si besoin.
  Reste 100 % local, gratuit, 0 token.
- Le chat est dessiné 100 % en code avec QPainter (aucune image).
- Humeur : triste 🥺 tant qu'on n'a pas écrit aujourd'hui, content 😺 dès le
  premier message (cœurs + série de jours).

## Lancer
```bash
python3 neko_francais.py &
```
Quitter : clic droit sur Minou → Quitter (ou Ctrl+C).
Besoins : Linux en session **X11**, Python 3, PyQt5.
