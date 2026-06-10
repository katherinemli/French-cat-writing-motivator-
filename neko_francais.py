#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neko_francais.py — Minou, ton petit chat français. 🐱

Minou se PROMÈNE par-dessus tes fenêtres (sur tout l'écran), et il porte
une petite BOÎTE DE DISCUSSION au-dessus de sa tête : tu écris dedans, en
français, comme avec une amie.

  - Quand tu écris (ou que ta souris est dessus), Minou s'arrête pour
    que tu puisses taper tranquillement. Il repart se promener après.
  - Tu peux l'ATTRAPER avec la souris pour le déplacer où tu veux.

Minou tient un petit CARNET : il retient les jours où tu écris.
  - Pas encore écrit aujourd'hui -> il est un peu triste 🥺.
  - Dès que tu lui parles -> il devient tout content 😺 et il compte
    les jours d'affilée (ta « série » 🔥).

Il NE corrige PAS tes fautes (c'est juste pour le plaisir 💛). C'est un
chatbot tout simple, hors-ligne, qui ne consomme AUCUN token. On ne
sauvegarde QUE les dates où tu as écrit — jamais le contenu de tes messages.

Pour quitter : Ctrl+C dans le terminal (ou clic droit sur Minou -> Quitter).
"""

import sys
import os
import json
import math
import random
import subprocess
import unicodedata
from datetime import date, timedelta

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QPoint, QPointF


# ----------------------------------------------------------------------
# Petits réglages que tu peux changer
# ----------------------------------------------------------------------
DRIFT_SPEED = 1.7      # vitesse de promenade (pixels par image)
FRAME_MS = 33          # ~30 images/seconde
CAT_SCALE = 1.7        # taille du chat
WIN_W, WIN_H = 320, 300        # taille quand la boîte de discussion est ouverte
CAT_W, CAT_H = 120, 120        # taille quand Minou se promène (juste le chat)

REMINDER_TITLE = "🐱 Minou t'attend"
REMINDER_TEXT = "Viens papoter un peu en français aujourd'hui ! 💛"

# -------- Les phrases de Minou (tu peux en AJOUTER / CHANGER librement !) ------
GREETINGS = [
    "Coucou toi ! 🐱",
    "Salut salut ! Contente de te voir 💛",
    "Hellooo ! 😺",
    "Coucou ! J'attendais que tu viennes me parler 🐾",
]

QUESTIONS = [
    "Raconte-moi, qu'est-ce que tu as fait aujourd'hui ?",
    "Tu as bien mangé ? C'était quoi ?",
    "Comment tu te sens là, maintenant ?",
    "C'est quoi le meilleur moment de ta journée ?",
    "Tu as des projets pour ce week-end ?",
    "Qu'est-ce qui te ferait plaisir aujourd'hui ?",
    "Tu écoutes quoi comme musique en ce moment ?",
    "Il y a un petit truc qui t'a fait sourire aujourd'hui ?",
    "Qu'est-ce que tu aimerais faire ce soir ?",
    "Si tu pouvais partir en voyage demain, tu irais où ?",
    "C'est quoi ton plat préféré ? Moi j'adore le poisson 😸",
    "Tu as regardé un film ou une série récemment ?",
    "Qu'est-ce qui te rend heureuse ces temps-ci ?",
    "Parle-moi d'une personne que tu aimes bien 💛",
]

REACTIONS = [
    "Oh, c'est chouette ça ! 🐱",
    "Ahh je vois, merci de me raconter !",
    "Trop bien !",
    "Mmh d'accord, intéressant !",
    "Haha j'adore. 😺",
    "Oh super !",
    "C'est gentil de partager ça avec moi 💛",
    "Je t'écoute, continue !",
]

GOODBYES = [
    "À bientôt ! Reviens me voir quand tu veux 🐱💛",
    "Bisous ! Je vais faire une petite sieste 😴🐾",
    "Au revoir toi ! Passe une belle journée 💛",
]

THANKS = [
    "Mais de rien, c'est avec plaisir ! 💛",
    "Oh, c'est moi qui te remercie de papoter avec moi 🐱",
]

ABOUT_ME = [
    "Moi ça va super, je ronronne tranquille au chaud 🐱.",
    "Moi tout va bien, j'ai bien dormi sur le clavier 😸.",
    "Ça va trop bien depuis que tu es là 💛.",
]

SAD_REPLIES = [
    "Oh, je suis là pour toi 💛. Tu veux m'en dire un peu plus ? Ça aide parfois.",
    "Ça a l'air pas facile... 🐱 Viens, raconte-moi tranquillement.",
    "Je t'envoie un gros câlin de chat 🐾💛. Qu'est-ce qui se passe ?",
]

HAPPY_REPLIES = [
    "Yay ! Ça me rend heureuse aussi ! 😸",
    "Aww j'adore quand tu es contente ! 💛",
    "Trop bien, je ronronne de joie pour toi 🐱 !",
]

SAD_WORDS = ["triste", "fatigu", " mal ", "deprim", "marre", " dur ", "difficile",
             "stress", "pleur", "seul", "angoiss", " nul ", "epuis", "decourag"]
HAPPY_WORDS = ["content", "heureu", "genial", "super", "trop bien", "joie",
               "jadore", "cool", "magnifique", "ravi", "youpi", "excellent"]

TOPICS = [
    (["mang", "dejeun", "diner", "repas", "cuisine", "faim", "gateau",
      "chocolat", "pizza", "pomme", "cafe"],
     ["Miam, ça me donne faim tout ça ! 🐱",
      "Oh j'adore quand on parle de nourriture 😋",
      "Mmmh, ça a l'air délicieux !"]),
    (["chat", "chien", "animal", "minou", "chaton", "oiseau", "lapin"],
     ["Miaou ! 🐱 J'adore parler des animaux.",
      "Les animaux c'est mes préférés, évidemment 😼 !"]),
    (["travail", "boulot", "bureau", "etude", "etudi", "ecole", "cours",
      "program", "code", "ordinateur", "projet"],
     ["Ah, le travail et les études ! 🐱 Courage à toi.",
      "Tu bosses dur dis donc ! N'oublie pas de faire des pauses 🐾."]),
    (["musique", "chanson", "ecoute", "chante", "concert", "piano", "guitare"],
     ["Oh la musique, j'adore ronronner en rythme 🎶🐱 !",
      "La musique ça met de bonne humeur 😺 !"]),
    (["pluie", "soleil", "froid", "chaud", "neige", "temps", "orage", "vent"],
     ["Ici dans l'ordi il fait toujours bon 😸.",
      "Moi j'aime bien me rouler en boule quand il fait froid 🐾."]),
    (["week", "samedi", "dimanche", "vacances", "voyage", "plage", "montagne"],
     ["Oh, des projets ça fait du bien ! 🐱",
      "J'adore l'idée d'une petite escapade 😺 !"]),
    (["famille", "maman", "papa", "soeur", "frere", "ami", "copain", "copine"],
     ["Oh, c'est précieux les gens qu'on aime 💛.",
      "Ça fait du bien de parler des gens importants pour toi 🐱."]),
    (["film", "serie", "netflix", "cinema", "livre", "lire"],
     ["Oh raconte ! J'adore les bonnes histoires 🐱.",
      "Un bon film ou un bon livre, rien de mieux 😸 !"]),
]

CONFIG_DIR = os.path.expanduser("~/.config/neko-francais")
STATE_FILE = os.path.join(CONFIG_DIR, "state.json")


# ----------------------------------------------------------------------
# Le carnet : on ne garde QUE des dates (jamais le contenu des messages)
# ----------------------------------------------------------------------
def load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state: dict) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass


def wrote_today(state: dict) -> bool:
    return date.today().isoformat() in state.get("written_dates", [])


def mark_written_today(state: dict) -> dict:
    today = date.today().isoformat()
    dates = state.get("written_dates", [])
    if today not in dates:
        state["written_dates"] = sorted(set(dates + [today]))[-120:]
        save_state(state)
    return state


def current_streak(state: dict) -> int:
    dates = set(state.get("written_dates", []))
    d = date.today()
    if d.isoformat() not in dates:
        d = d - timedelta(days=1)
    streak = 0
    while d.isoformat() in dates:
        streak += 1
        d = d - timedelta(days=1)
    return streak


def send_notification() -> None:
    try:
        subprocess.Popen(
            ["notify-send", "-a", "Neko Français", "-i", "face-smile",
             REMINDER_TITLE, REMINDER_TEXT]
        )
    except Exception:
        pass


# ----------------------------------------------------------------------
# Le « cerveau » de Minou : tout simple, hors-ligne, 0 token.
# ----------------------------------------------------------------------
def _strip_accents(s: str) -> str:
    s = s.lower()
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


class LocalBrain:
    def __init__(self):
        self.recent_q = []

    def _question(self) -> str:
        pool = [q for q in QUESTIONS if q not in self.recent_q] or list(QUESTIONS)
        q = random.choice(pool)
        self.recent_q.append(q)
        if len(self.recent_q) > 6:
            self.recent_q.pop(0)
        return q

    def reply(self, message: str) -> str:
        t = " " + _strip_accents(message) + " "
        if any(w in t for w in ["au revoir", "bonne nuit", "a plus", "a bientot",
                                "ciao", "bye", "adieu", "bonne soiree"]):
            return random.choice(GOODBYES)
        if "merci" in t:
            return random.choice(THANKS) + " " + self._question()
        if any(w in t for w in ["et toi", "comment tu vas", "tu vas bien",
                                "ca va toi", "tu fais quoi"]):
            return random.choice(ABOUT_ME) + " " + self._question()
        if len(t) < 32 and any(w in t for w in ["bonjour", "coucou", "salut",
                                                "bonsoir", "hello", "hey", "cc "]):
            return random.choice(GREETINGS) + " " + self._question()
        for keys, reacts in TOPICS:
            if any(k in t for k in keys):
                return random.choice(reacts) + " " + self._question()
        if any(w in t for w in SAD_WORDS):
            return random.choice(SAD_REPLIES)
        if any(w in t for w in HAPPY_WORDS):
            return random.choice(HAPPY_REPLIES) + " " + self._question()
        return random.choice(REACTIONS) + " " + self._question()


# ----------------------------------------------------------------------
# Minou : fenêtre transparente qui flotte sur l'écran.
# En haut = la boîte de discussion ; en bas = le chat qui se promène.
# ----------------------------------------------------------------------
class MinouPet(QtWidgets.QWidget):
    CAT_AREA = 96   # hauteur réservée au chat (en bas)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.chatting = False          # la boîte n'apparaît qu'au clic
        self.setFixedSize(CAT_W, CAT_H)

        self.record = load_state()
        self.brain = LocalBrain()
        self.history = []
        self._thinking = False

        # -- animation / déplacement --
        self.frame = 0
        self.facing = 1
        self.walk = False
        self.idle_time = 0.0
        self.celebrate_time = 0.0
        self.tail_phase = 0.0
        self.pause_left = 1.0
        self.tx, self.ty = self.x(), self.y()
        self._dragging = False
        self._moved = False
        self._press_pos = QPoint()
        self._drag_off = QPoint()

        self._build_box()
        self._place_start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(FRAME_MS)

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_daily_reminder)
        self.reminder_timer.start(60 * 1000)

        QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, self._exit_chat)
        QTimer.singleShot(0, self._refresh_mask)

    # ------------------------------------------------------------------
    def _build_box(self):
        self.box = QtWidgets.QFrame(self)
        self.box.setObjectName("box")
        self.box.setStyleSheet(
            "QFrame#box{background:rgba(255,253,246,235);"
            "border:2px solid #f0a8bc;border-radius:14px;}")
        self.box.setGeometry(8, 8, WIN_W - 16, WIN_H - self.CAT_AREA - 14)

        v = QtWidgets.QVBoxLayout(self.box)
        v.setContentsMargins(10, 8, 10, 10)
        v.setSpacing(6)

        hrow = QtWidgets.QHBoxLayout()
        hrow.setSpacing(4)
        self.header = QtWidgets.QLabel()
        self.header.setStyleSheet("font-weight:bold;font-size:12px;color:#d2548a;"
                                  "background:transparent;border:none;")
        hrow.addWidget(self.header, 1)
        close = QtWidgets.QPushButton("×")
        close.setFixedSize(22, 22)
        close.setToolTip("Fermer (Minou repart se promener)")
        close.setStyleSheet(
            "QPushButton{background:transparent;border:none;color:#c06;"
            "font-size:18px;font-weight:bold;}"
            "QPushButton:hover{color:#e2356a;}")
        close.clicked.connect(self._exit_chat)
        hrow.addWidget(close)
        v.addLayout(hrow)

        self.view = QtWidgets.QTextBrowser()
        self.view.setStyleSheet("background:transparent;border:none;font-size:13px;")
        v.addWidget(self.view, 1)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(6)
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Écris en français… (Entrée)")
        self.input.setStyleSheet(
            "QLineEdit{background:white;border:1px solid #ccc;border-radius:8px;"
            "padding:6px;font-size:13px;}")
        self.input.returnPressed.connect(self.on_send)
        row.addWidget(self.input, 1)
        self.send_btn = QtWidgets.QPushButton("✍️")
        self.send_btn.setFixedWidth(40)
        self.send_btn.setStyleSheet(
            "QPushButton{background:#f08aa0;color:white;border:none;"
            "border-radius:8px;padding:6px;font-size:14px;}"
            "QPushButton:hover{background:#e87890;}"
            "QPushButton:disabled{background:#ddd;}")
        self.send_btn.clicked.connect(self.on_send)
        row.addWidget(self.send_btn)
        v.addLayout(row)

        self._update_header()
        self._append("Minou", self._greeting())
        self.box.hide()

    def _place_start(self):
        scr = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = scr.x() + (scr.width() - self.width()) // 2
        y = scr.y() + (scr.height() - self.height()) // 3
        self.move(x, y)
        self.tx, self.ty = x, y

    def _refresh_mask(self):
        if self.chatting:
            region = QtGui.QRegion(self.box.geometry(), QtGui.QRegion.Rectangle)
            cw = 26
            region = region.united(QtGui.QRegion(
                self.width() // 2 - cw // 2, self.box.geometry().bottom() - 2,
                cw, self.CAT_AREA))
            region = region.united(QtGui.QRegion(
                self.width() // 2 - 46, self.height() - 96, 92, 96,
                QtGui.QRegion.Ellipse))
        else:
            region = QtGui.QRegion(
                self.width() // 2 - 46, self.height() - 100, 92, 100,
                QtGui.QRegion.Ellipse)
        self.setMask(region)

    def _move_clamped(self, x, y):
        scr = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = max(scr.x(), min(x, scr.x() + scr.width() - self.width()))
        y = max(scr.y(), min(y, scr.y() + scr.height() - self.height()))
        self.move(x, y)

    def _cat_screen_pos(self):
        return self.pos() + QPoint(self.width() // 2, self.height() - 14)

    def _enter_chat(self):
        if self.chatting:
            return
        cat = self._cat_screen_pos()
        self.chatting = True
        self.setFixedSize(WIN_W, WIN_H)
        self._move_clamped(cat.x() - WIN_W // 2, cat.y() - (WIN_H - 14))
        self.box.show()
        self._refresh_mask()
        self.update()
        self.raise_()
        self.activateWindow()
        self.input.setFocus()

    def _exit_chat(self):
        if not self.chatting:
            return
        cat = self._cat_screen_pos()
        self.chatting = False
        self.box.hide()
        self.setFixedSize(CAT_W, CAT_H)
        self._move_clamped(cat.x() - CAT_W // 2, cat.y() - (CAT_H - 14))
        self._refresh_mask()
        self.tx, self.ty = self.x(), self.y()
        self.pause_left = 2.5
        self.update()

    # -- humeur / série -----------------------------------------------
    @property
    def mood(self):
        if self.celebrate_time > 0:
            return "happy"
        return "happy" if wrote_today(self.record) else "sad"

    def _greeting(self):
        streak = current_streak(self.record)
        if wrote_today(self.record):
            return (f"Coucou ! 🐱 Déjà écrit aujourd'hui, bravo "
                    f"(série : {streak} j 🔥). Raconte-moi encore un truc ?")
        if streak >= 1:
            return (f"Coucou Katherine ! 🐱 Jolie série de {streak} jour"
                    f"{'s' if streak > 1 else ''}... écris-moi un mot pour "
                    "la continuer ? 💛")
        return ("Coucou Katherine ! 🐱 Écris-moi un petit mot en français, "
                "comme tu veux ! 💛")

    def _update_header(self):
        streak = current_streak(self.record)
        if wrote_today(self.record):
            self.header.setText(f"🐱 Minou  ·  🔥 {streak} j  ·  bravo !")
        elif streak > 0:
            self.header.setText(f"🐱 Minou  ·  🥺 série de {streak} j en attente")
        else:
            self.header.setText("🐱 Minou  ·  🥺 il t'attend...")

    # -- affichage de la discussion -----------------------------------
    def _append(self, who, text):
        t = (text.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace("\n", "<br>"))
        if who == "Minou":
            html = (f'<p style="margin:4px 0;"><b style="color:#d2548a;">'
                    f'🐱</b> {t}</p>')
        else:
            html = (f'<p style="margin:4px 0;text-align:right;color:#2a6;">'
                    f'{t} <b>:Toi</b></p>')
        self.view.append(html)
        self.view.verticalScrollBar().setValue(
            self.view.verticalScrollBar().maximum())

    # -- envoi ---------------------------------------------------------
    def on_send(self):
        if self._thinking:
            return
        msg = self.input.text().strip()
        if not msg:
            return
        self.input.clear()
        self._append("Toi", msg)
        self.history.append(("user", msg))

        first_today = not wrote_today(self.record)
        self.record = mark_written_today(self.record)
        if first_today:
            self.celebrate_time = 5.0
            self._update_header()

        self._thinking = True
        self.send_btn.setEnabled(False)
        reply = self.brain.reply(msg)
        QTimer.singleShot(600, lambda: self._show_reply(reply, first_today))

    def _show_reply(self, reply, first_today):
        self._append("Minou", reply)
        if first_today:
            streak = current_streak(self.record)
            self._append("Minou", f"(Youpi, tu as écrit aujourd'hui ! 🎉 "
                                   f"Série : {streak} j 🔥)")
        self.send_btn.setEnabled(True)
        self._thinking = False

    def check_daily_reminder(self):
        if wrote_today(self.record):
            return
        if self.record.get("last_reminder") != date.today().isoformat():
            self.record["last_reminder"] = date.today().isoformat()
            save_state(self.record)
            send_notification()

    # -- attraper Minou avec la souris pour le déplacer ----------------
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._press_pos = e.globalPos()
            self._drag_off = e.globalPos() - self.frameGeometry().topLeft()
            self._moved = False

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            if not self._moved and (
                    e.globalPos() - self._press_pos).manhattanLength() > 6:
                self._moved = True
            if self._moved:
                self._dragging = True
                self.move(e.globalPos() - self._drag_off)

    def mouseReleaseEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
        self._dragging = False
        if not self._moved and not self.chatting:
            self._enter_chat()              # un simple clic ouvre la boîte
        elif not self.chatting:
            self.tx, self.ty = self.x(), self.y()
            self.pause_left = 2.5

    def contextMenuEvent(self, e):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Quitter Minou", QtWidgets.QApplication.quit)
        menu.exec_(e.globalPos())

    # -- promenade -----------------------------------------------------
    def _interacting(self):
        return (self.chatting or self.underMouse()
                or self.input.hasFocus() or self._dragging)

    def _new_target(self):
        scr = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.tx = random.randint(scr.x(), scr.x() + scr.width() - self.width())
        self.ty = random.randint(scr.y(), scr.y() + scr.height() - self.height())
        self.pause_left = random.uniform(2.5, 6.0)

    def tick(self):
        self.frame += 1
        dt = FRAME_MS / 1000.0
        if self.celebrate_time > 0:
            self.celebrate_time -= dt

        self.walk = False
        if not self._interacting():
            dx = self.tx - self.x()
            dy = self.ty - self.y()
            dist = math.hypot(dx, dy)
            if dist > 3 and self.pause_left <= 0:
                step = min(DRIFT_SPEED, dist)
                self.move(int(self.x() + dx / dist * step),
                          int(self.y() + dy / dist * step))
                if abs(dx) > 1:
                    self.facing = 1 if dx > 0 else -1
                self.walk = True
            else:
                if self.pause_left > 0:
                    self.pause_left -= dt
                elif dist <= 3:
                    self._new_target()

        self.idle_time = 0.0 if self.walk else self.idle_time + dt
        self.update()

    # -- dessin --------------------------------------------------------
    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)

        cx = self.width() / 2
        p.setPen(Qt.NoPen)

        # le cou qui relie la boîte à la tête du chat (seulement quand on papote)
        if self.chatting:
            neck_top = self.box.geometry().bottom()
            p.setBrush(QtGui.QColor(240, 168, 188))
            p.drawRoundedRect(QtCore.QRectF(cx - 5, neck_top - 4, 10, 16), 4, 4)

        # ombre + chat
        cat_y = self.height() - 14
        p.setBrush(QtGui.QColor(0, 0, 0, 30))
        p.drawEllipse(QPointF(cx, cat_y + 4), 16 * CAT_SCALE * 0.5, 4.5 * CAT_SCALE * 0.5)
        p.save()
        p.translate(cx, cat_y)
        p.scale(CAT_SCALE * self.facing, CAT_SCALE)
        self._draw_cat(p)
        p.restore()

        if self.celebrate_time > 0:
            self._draw_hearts(p, cx, cat_y)

    def _draw_hearts(self, p, cx, cat_y):
        p.save()
        f = p.font()
        f.setPointSizeF(12)
        p.setFont(f)
        t = 5.0 - self.celebrate_time
        for i in range(3):
            phase = t * 1.4 + i * 0.7
            rise = (phase % 2.0) / 2.0
            x = cx + (i - 1) * 18 + math.sin(phase * 3) * 4
            y = cat_y - 60 - rise * 30
            p.setOpacity(max(0.0, 1.0 - rise))
            p.drawText(QPointF(x, y), "💛")
        p.setOpacity(1.0)
        p.restore()

    def _draw_cat(self, p):
        sad = self.mood == "sad"
        walking = self.walk
        sleeping = (self.idle_time > 9.0) and not self._interacting()

        body = QtGui.QColor(78, 80, 92) if sad else QtGui.QColor(70, 70, 78)
        belly = QtGui.QColor(225, 220, 210)
        pink = QtGui.QColor(240, 150, 165)
        white = QtGui.QColor(250, 250, 250)
        black = QtGui.QColor(30, 30, 34)
        p.setPen(Qt.NoPen)

        # queue
        self.tail_phase += 0.25 if walking else (0.04 if sad else 0.08)
        swing = math.sin(self.tail_phase) * (6 if walking else (1.5 if sad else 3))
        droop = 6 if sad else 0
        tail = QtGui.QPainterPath()
        tail.moveTo(-13, -10)
        tail.cubicTo(-22, -14 + droop, -24, -24 + swing + droop, -16, -30 + swing + droop)
        pen = QtGui.QPen(body, 5)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.drawPath(tail)
        p.setPen(Qt.NoPen)

        # corps + ventre
        p.setBrush(body)
        p.drawRoundedRect(QtCore.QRectF(-15, -22, 26, 22), 11, 11)
        p.setBrush(belly)
        p.drawRoundedRect(QtCore.QRectF(-8, -14, 14, 14), 6, 6)

        # pattes
        p.setBrush(body)
        if walking:
            wob = math.sin(self.frame * 0.6) * 3
            p.drawRoundedRect(QtCore.QRectF(-13, -6 - wob, 6, 8), 3, 3)
            p.drawRoundedRect(QtCore.QRectF(3, -6 + wob, 6, 8), 3, 3)
        else:
            p.drawRoundedRect(QtCore.QRectF(-12, -6, 6, 6), 3, 3)
            p.drawRoundedRect(QtCore.QRectF(2, -6, 6, 6), 3, 3)

        # tête
        hcx, hcy = 6, -26
        p.setBrush(body)
        if sad:
            self._ear(p, hcx, hcy, (-9, -3), (-14, -6), (-3, -7))
            self._ear(p, hcx, hcy, (9, -3), (14, -6), (3, -7))
        else:
            self._ear(p, hcx, hcy, (-9, -4), (-12, -14), (-2, -8))
            self._ear(p, hcx, hcy, (9, -4), (12, -14), (2, -8))
            p.setBrush(pink)
            p.drawEllipse(QtCore.QPointF(hcx - 7.5, hcy - 8), 1.6, 2.6)
            p.drawEllipse(QtCore.QPointF(hcx + 7.5, hcy - 8), 1.6, 2.6)

        p.setBrush(body)
        p.drawEllipse(QtCore.QPointF(hcx, hcy), 11, 10)

        if sleeping:
            pen = QtGui.QPen(black, 1.4)
            pen.setCapStyle(Qt.RoundCap)
            p.setPen(pen)
            p.drawArc(QtCore.QRectF(hcx - 7, hcy - 2, 5, 4), 0, -180 * 16)
            p.drawArc(QtCore.QRectF(hcx + 2, hcy - 2, 5, 4), 0, -180 * 16)
            p.setPen(Qt.NoPen)
        else:
            p.setBrush(white)
            p.drawEllipse(QtCore.QPointF(hcx - 4, hcy - 1), 2.6, 3.0)
            p.drawEllipse(QtCore.QPointF(hcx + 4, hcy - 1), 2.6, 3.0)
            p.setBrush(black)
            look_y = 1.2 if sad else -1
            look_x = 1.0 if self.facing > 0 else 0.4
            p.drawEllipse(QtCore.QPointF(hcx - 4 + look_x, hcy + look_y), 1.3, 1.7)
            p.drawEllipse(QtCore.QPointF(hcx + 4 + look_x, hcy + look_y), 1.3, 1.7)
            if sad:
                pen = QtGui.QPen(black, 1.0)
                pen.setCapStyle(Qt.RoundCap)
                p.setPen(pen)
                p.drawLine(QPointF(hcx - 7, hcy - 5), QPointF(hcx - 2, hcy - 3))
                p.drawLine(QPointF(hcx + 7, hcy - 5), QPointF(hcx + 2, hcy - 3))
                p.drawArc(QtCore.QRectF(hcx - 2.5, hcy + 5, 5, 4), 0, 180 * 16)
                p.setPen(Qt.NoPen)
                if (self.frame // 40) % 2 == 0:
                    p.setBrush(QtGui.QColor(120, 180, 240))
                    p.drawEllipse(QtCore.QPointF(hcx - 5.5, hcy + 3), 1.2, 1.8)

        p.setBrush(pink)
        p.drawEllipse(QtCore.QPointF(hcx, hcy + 3), 1.4, 1.1)

        pen = QtGui.QPen(QtGui.QColor(210, 210, 210), 0.8)
        p.setPen(pen)
        for dyw in (1.5, 4):
            p.drawLine(QPointF(hcx - 5, hcy + dyw), QPointF(hcx - 13, hcy + dyw - 1))
            p.drawLine(QPointF(hcx + 5, hcy + dyw), QPointF(hcx + 13, hcy + dyw - 1))
        p.setPen(Qt.NoPen)

        if sleeping:
            p.save()
            p.scale(self.facing, 1)
            p.setPen(QtGui.QPen(QtGui.QColor(120, 120, 200)))
            f = p.font()
            f.setPointSizeF(7)
            f.setBold(True)
            p.setFont(f)
            zwob = (self.frame // 12) % 3
            p.drawText(QtCore.QPointF(self.facing * 14, -38 - zwob * 2), "z")
            p.drawText(QtCore.QPointF(self.facing * 19, -44 - zwob * 2), "Z")
            p.restore()

    def _ear(self, p, hcx, hcy, base, tip, inner):
        path = QtGui.QPainterPath()
        path.moveTo(hcx + base[0], hcy + base[1])
        path.lineTo(hcx + tip[0], hcy + tip[1])
        path.lineTo(hcx + inner[0], hcy + inner[1])
        path.closeSubpath()
        p.drawPath(path)


def main():
    if os.environ.get("XDG_SESSION_TYPE") == "wayland" and "QT_QPA_PLATFORM" not in os.environ:
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    pet = MinouPet()
    pet.show()
    print("🐱 Minou se promène ! Clique droit sur lui -> Quitter, ou Ctrl+C ici.")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
