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
- `LocalBrain.reply()` : choisit une réponse amicale à partir des listes
  éditables en haut du fichier (`GREETINGS`, `QUESTIONS`, `REACTIONS`,
  `TOPICS`…). Pour rendre Minou plus malin plus tard : remplacer cette
  méthode (par ex. une IA locale via Ollama).
- Le chat est dessiné 100 % en code avec QPainter (aucune image).
- Humeur : triste 🥺 tant qu'on n'a pas écrit aujourd'hui, content 😺 dès le
  premier message (cœurs + série de jours).

## Lancer
```bash
python3 neko_francais.py &
```
Quitter : clic droit sur Minou → Quitter (ou Ctrl+C).
Besoins : Linux en session **X11**, Python 3, PyQt5.
