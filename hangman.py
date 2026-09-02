"""
CodeAlpha Python Programming Internship - Task 1
Project: Hangman Game (Mystery Word Challenge • Paper-Cut Edition)
Author: CodeAlpha Intern
Tech Stack: Python 3, Tkinter (Standard Library Only)
"""

import math
import os
import random
import tkinter as tk
from typing import Dict, List, Optional, Set

# ==============================================================================
# EXACT COLOR PALETTE (From Visual Reference)
# ==============================================================================
COLORS = {
    # Canvas & Backdrops
    "bg_sky": "#C8EEF8",          # Sky blue main backdrop
    "bg_bubble": "#A7E3F5",       # Soft circle decals
    "paper_card": "#E6F5FA",      # Soft inner card fill
    "paper_card_shadow": "#AFDCEB",
    
    # 2.5D Stacked Button Colors (Cream Base + Jewel Faces)
    "cream_shadow": "#FFF7E6",    # Distinct warm cream 3D underlay
    
    "play_face": "#7A0066",       # Deep magenta plum
    "easy_face": "#067A3A",       # Rich forest green
    "med_face": "#8B2E00",        # Warm burnt rust
    "hard_face": "#5A3A0A",       # Deep bronze/brown
    "purple_face": "#541B80",     # Mystery hint purple
    
    # Interactive States
    "key_active": "#1C3144",      # Dark slate keyboard face
    "key_correct": "#067A3A",     # Correct guessed letter face
    "key_wrong": "#D3E4EA",       # Disabled key face
    "key_wrong_txt": "#8FA6AF",
    
    # Typography
    "txt_yellow": "#F9F871",      # Bright lemon-yellow button text
    "txt_white": "#FFFFFF",
    "txt_dark": "#24506A",        # Deep slate text for labels/stats
    
    # Game Artwork
    "gallows": "#24506A",
    "hang_rope": "#8B2E00",
    "hang_figure": "#7A0066"
}

FONTS = {
    "title_hero": ("Helvetica", 32, "bold"),
    "title_md": ("Helvetica", 20, "bold"),
    "title_sm": ("Helvetica", 14, "bold"),
    "btn_lg": ("Helvetica", 18, "bold"),
    "btn_md": ("Helvetica", 13, "bold"),
    "btn_sm": ("Helvetica", 10, "bold"),
    "word_tile": ("Helvetica", 24, "bold"),
    "body_bold": ("Helvetica", 11, "bold"),
    "body": ("Helvetica", 10, "normal"),
    "caption": ("Helvetica", 9, "bold"),
    "key": ("Helvetica", 11, "bold")
}

# ==============================================================================
# EXACT 5 PREDEFINED WORDS
# ==============================================================================
WORD_DATA: Dict[str, List[Dict[str, str]]] = {
    "EASY": [
        {
            "word": "PYTHON",
            "category": "Popular Programming Language",
            "fact": "Named after Monty Python's Flying Circus, not the snake!"
        },
        {
            "word": "NETWORK",
            "category": "Interconnected Computer Systems",
            "fact": "A collection of nodes sharing data and resources securely."
        }
    ],
    "MEDIUM": [
        {
            "word": "DATABASE",
            "category": "Organized Collection of Data",
            "fact": "Structured digital storehouse for records, tables, and files."
        },
        {
            "word": "SECURITY",
            "category": "Protection of Systems & Networks",
            "fact": "Safeguards digital infrastructure from cyber threats."
        }
    ],
    "HARD": [
        {
            "word": "ALGORITHM",
            "category": "Step-by-Step Logic Blueprint",
            "fact": "The foundational algorithm recipe guiding software execution."
        }
    ]
}


class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mystery Word Challenge • Paper-Cut Hangman")
        self.geometry("860x650")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_sky"])

        # Statistics State
        self.stats = {
            "games_played": 0,
            "wins": 0,
            "best_score": 0
        }

        # Game State
        self.selected_difficulty: str = "EASY"
        self.current_word_data: Optional[Dict[str, str]] = None
        self.secret_word: str = ""
        self.guessed_letters: Set[str] = set()
        self.mistakes: int = 0
        self.max_mistakes: int = 6
        self.score: int = 100
        self.game_over: bool = False
        
        # Hints (Free, -10, -20)
        self.hint1_used: bool = False
        self.hint2_used: bool = False
        self.hint3_used: bool = False
        self.hint_display_text: str = "Need a clue? Tap a boost below!"

        # Confetti
        self.confetti_particles: List[Dict] = []
        self.confetti_anim_id: Optional[str] = None

        # Bind physical keyboard
        self.bind("<Key>", self.handle_physical_key)

        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=860,
            height=650,
            bg=COLORS["bg_sky"],
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.show_home_screen()

    # ==========================================================================
    # SOUND & SCREEN SHAKE FEEDBACK
    # ==========================================================================
    def play_sound(self, sound_type: str):
        try:
            if os.name == "nt":
                import winsound
                if sound_type == "click":
                    winsound.Beep(1200, 30)
                elif sound_type == "correct":
                    winsound.Beep(1600, 60)
                elif sound_type == "wrong":
                    winsound.Beep(400, 90)
                elif sound_type == "win":
                    winsound.Beep(1100, 70)
                    winsound.Beep(1500, 100)
                elif sound_type == "lose":
                    winsound.Beep(350, 150)
            else:
                print('\a', end='', flush=True)
        except Exception:
            pass

    def trigger_screen_shake(self, count=4):
        if count <= 0:
            self.canvas.place(x=0, y=0)
            return
        dx = random.choice([-5, 5, -3, 3])
        dy = random.choice([-3, 3, -2, 2])
        self.canvas.place(x=dx, y=dy)
        self.after(25, lambda: self.trigger_screen_shake(count - 1))

    # ==========================================================================
    # 2.5D VECTOR PAPER-CUT DRAWING HELPERS
    # ==========================================================================
    def draw_rounded_rect(self, x1: float, y1: float, x2: float, y2: float, radius: float = 16, **kwargs) -> int:
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_paper_button(self, tag: str, x: float, y: float, width: float, height: float,
                          label: str, sublabel: Optional[str] = None,
                          face_color: str = COLORS["play_face"],
                          text_color: str = COLORS["txt_yellow"],
                          command=None, radius: float = 14,
                          offset_x: float = 10, offset_y: float = 12,
                          enabled: bool = True) -> None:
        """Draws a paper-cut stacked button with a cream base and jewel-toned face."""
        cream_bg = COLORS["cream_shadow"] if enabled else COLORS["key_wrong"]
        top_color = face_color if enabled else COLORS["key_wrong"]
        lbl_color = text_color if enabled else COLORS["key_wrong_txt"]

        shadow_tag = f"{tag}_shadow"
        face_tag = f"{tag}_face"
        text_tag = f"{tag}_text"
        full_tag = tag

        # Cream Shadow Underlay
        self.draw_rounded_rect(
            x + offset_x, y + offset_y,
            x + width + offset_x, y + height + offset_y,
            radius=radius, fill=cream_bg, outline="",
            tags=(full_tag, shadow_tag)
        )
        # Main Colored Face
        self.draw_rounded_rect(
            x, y, x + width, y + height,
            radius=radius, fill=top_color, outline="",
            tags=(full_tag, face_tag)
        )

        # Centered Text
        if sublabel:
            self.canvas.create_text(
                x + width / 2, y + (height / 2) - 8,
                text=label, font=FONTS["btn_md"], fill=lbl_color,
                tags=(full_tag, text_tag)
            )
            self.canvas.create_text(
                x + width / 2, y + (height / 2) + 10,
                text=sublabel, font=FONTS["caption"], fill=lbl_color,
                tags=(full_tag, text_tag)
            )
        else:
            self.canvas.create_text(
                x + width / 2, y + (height / 2),
                text=label, font=FONTS["btn_lg"], fill=lbl_color,
                tags=(full_tag, text_tag)
            )

        if enabled and command:
            def on_press(e):
                self.canvas.move(face_tag, offset_x * 0.5, offset_y * 0.5)
                self.canvas.move(text_tag, offset_x * 0.5, offset_y * 0.5)

            def on_release(e):
                self.canvas.move(face_tag, -offset_x * 0.5, -offset_y * 0.5)
                self.canvas.move(text_tag, -offset_x * 0.5, -offset_y * 0.5)
                self.play_sound("click")
                command()

            self.canvas.tag_bind(full_tag, "<Button-1>", on_press)
            self.canvas.tag_bind(full_tag, "<ButtonRelease-1>", on_release)
            self.canvas.tag_bind(full_tag, "<Enter>", lambda e: self.config(cursor="hand2"))
            self.canvas.tag_bind(full_tag, "<Leave>", lambda e: self.config(cursor=""))

    def draw_background_bubbles(self):
        """Draws floating sky bubbles matching the reference SVG."""
        bubbles = [
            (120, 90, 42),
            (730, 85, 38),
            (110, 480, 32),
            (750, 490, 28),
            (430, 20, 22),
            (440, 610, 26)
        ]
        for cx, cy, r in bubbles:
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=COLORS["bg_bubble"], outline=""
            )

    # ==========================================================================
    # SCREEN 1: HOME MENU (Matching Reference SVG Layout)
    # ==========================================================================
    def show_home_screen(self) -> None:
        self.canvas.delete("all")
        if self.confetti_anim_id:
            self.after_cancel(self.confetti_anim_id)
            self.confetti_anim_id = None

        self.draw_background_bubbles()

        # Title / Subtitle
        self.canvas.create_text(430, 65, text="HANGMAN", font=FONTS["title_hero"], fill=COLORS["play_face"])
        self.canvas.create_text(430, 105, text="MYSTERY WORD CHALLENGE", font=FONTS["title_sm"], fill=COLORS["txt_dark"])

        # Main Play Button (Plum Face + Cream Shadow)
        self.draw_paper_button(
            tag="main_play_btn",
            x=285, y=140, width=290, height=82,
            label="▶  PLAY",
            face_color=COLORS["play_face"],
            text_color=COLORS["txt_yellow"],
            command=self.start_new_game,
            radius=18,
            offset_x=12, offset_y=14
        )

        # Section Label
        self.canvas.create_text(430, 270, text="DIFFICULTY SELECTION", font=FONTS["body_bold"], fill=COLORS["txt_dark"])

        # 3 Difficulty Cards (Easy / Medium / Hard)
        diff_cards = [
            ("EASY", "2 Words", 65, COLORS["easy_face"]),
            ("MEDIUM", "2 Words", 325, COLORS["med_face"]),
            ("HARD", "1 Word", 585, COLORS["hard_face"])
        ]

        for mode, sub, x_pos, face_c in diff_cards:
            is_active = (self.selected_difficulty == mode)
            tag = f"home_diff_{mode}"
            
            # Highlight selected difficulty
            display_title = f"✓ {mode}" if is_active else mode
            self.draw_paper_button(
                tag=tag,
                x=x_pos, y=305, width=210, height=75,
                label=display_title,
                sublabel=sub,
                face_color=face_c if is_active else COLORS["key_active"],
                text_color=COLORS["txt_yellow"] if is_active else COLORS["txt_white"],
                command=lambda m=mode: self.set_difficulty(m),
                radius=14,
                offset_x=10, offset_y=12
            )

        # Statistics Bottom Line
        win_rate = int((self.stats["wins"] / self.stats["games_played"] * 100)) if self.stats["games_played"] > 0 else 0
        stats_summary = f"Games: {self.stats['games_played']}   •   Wins: {self.stats['wins']}   •   Win Rate: {win_rate}%   •   Best Score: {self.stats['best_score']}"
        
        # Stats Pill Card
        self.draw_rounded_rect(160, 485, 700, 535, radius=14, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(155, 480, 695, 530, radius=14, fill=COLORS["paper_card"], outline="")
        self.canvas.create_text(425, 505, text=stats_summary, font=FONTS["body_bold"], fill=COLORS["txt_dark"])

        self.canvas.create_text(430, 595, text="CodeAlpha Python Internship Task 1 • Standard 6-Mistake Rule", font=FONTS["caption"], fill=COLORS["txt_dark"])

    def set_difficulty(self, mode: str) -> None:
        self.selected_difficulty = mode
        self.show_home_screen()

    # ==========================================================================
    # GAME SESSION INITIALIZATION
    # ==========================================================================
    def start_new_game(self) -> None:
        pool = WORD_DATA[self.selected_difficulty]
        self.current_word_data = random.choice(pool)
        self.secret_word = self.current_word_data["word"].upper()
        
        self.guessed_letters = set()
        self.mistakes = 0
        self.score = 100
        self.game_over = False
        
        self.hint1_used = False
        self.hint2_used = False
        self.hint3_used = False
        self.hint_display_text = "Hints are ready! Hint 1 is 100% FREE."
        
        self.show_game_screen()

    # ==========================================================================
    # SCREEN 2: GAMEPLAY SCREEN
    # ==========================================================================
    def show_game_screen(self) -> None:
        self.canvas.delete("all")
        self.draw_background_bubbles()

        # Top Bar: Menu / Score / Mistakes
        self.draw_rounded_rect(44, 24, 824, 84, radius=14, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(40, 20, 820, 80, radius=14, fill=COLORS["paper_card"], outline="")

        # Home Button
        self.draw_paper_button(
            tag="game_home_btn",
            x=55, y=28, width=90, height=44,
            label="⌂ MENU",
            face_color=COLORS["play_face"],
            text_color=COLORS["txt_yellow"],
            command=self.show_home_screen,
            radius=10,
            offset_x=4, offset_y=4
        )

        # Mode Badge
        diff_colors = {
            "EASY": COLORS["easy_face"],
            "MEDIUM": COLORS["med_face"],
            "HARD": COLORS["hard_face"]
        }
        self.canvas.create_text(220, 50, text=f"MODE: {self.selected_difficulty}", font=FONTS["btn_md"], fill=diff_colors[self.selected_difficulty])

        # Current Score
        self.canvas.create_text(420, 50, text=f"SCORE: {self.score}", font=FONTS["title_sm"], fill=COLORS["txt_dark"])

        # Mistakes Indicator (Max 6)
        self.canvas.create_text(605, 50, text=f"MISTAKES: {self.mistakes}/{self.max_mistakes}", font=FONTS["body_bold"], fill=COLORS["play_face"] if self.mistakes >= 4 else COLORS["txt_dark"])
        for i in range(self.max_mistakes):
            dot_color = COLORS["play_face"] if i < self.mistakes else COLORS["cream_shadow"]
            self.canvas.create_oval(715 + (i * 16), 42, 728 + (i * 16), 56, fill=dot_color, outline="")

        # Left Card: Hangman Figure
        self.draw_rounded_rect(44, 104, 354, 434, radius=18, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(40, 100, 350, 430, radius=18, fill=COLORS["paper_card"], outline="")
        self.draw_hangman_figure(195, 270)

        # Left Card: 3 Hint Buttons (X-Factor)
        self.draw_rounded_rect(44, 454, 354, 624, radius=18, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(40, 450, 350, 620, radius=18, fill=COLORS["paper_card"], outline="")
        self.canvas.create_text(195, 470, text="MYSTERY BOOSTS", font=FONTS["caption"], fill=COLORS["txt_dark"])
        self.canvas.create_text(195, 495, text=self.hint_display_text, font=FONTS["body"], fill=COLORS["txt_dark"], width=290, justify="center")

        # Hint 1: Free
        self.draw_paper_button(
            tag="h1_btn",
            x=50, y=530, width=90, height=48,
            label="HINT 1", sublabel="FREE",
            face_color=COLORS["easy_face"],
            text_color=COLORS["txt_yellow"],
            command=self.use_hint_1 if not self.hint1_used else None,
            enabled=not self.hint1_used,
            radius=10,
            offset_x=4, offset_y=4
        )

        # Hint 2: -10
        self.draw_paper_button(
            tag="h2_btn",
            x=150, y=530, width=90, height=48,
            label="HINT 2", sublabel="-10 PTS",
            face_color=COLORS["med_face"],
            text_color=COLORS["txt_yellow"],
            command=self.use_hint_2 if not self.hint2_used else None,
            enabled=not self.hint2_used,
            radius=10,
            offset_x=4, offset_y=4
        )

        # Hint 3: -20
        self.draw_paper_button(
            tag="h3_btn",
            x=250, y=530, width=90, height=48,
            label="HINT 3", sublabel="-20 PTS",
            face_color=COLORS["purple_face"],
            text_color=COLORS["txt_yellow"],
            command=self.use_hint_3 if not self.hint3_used else None,
            enabled=not self.hint3_used,
            radius=10,
            offset_x=4, offset_y=4
        )

        # Right Top Card: Mystery Word Paper Tiles
        self.draw_rounded_rect(384, 104, 824, 244, radius=18, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(380, 100, 820, 240, radius=18, fill=COLORS["paper_card"], outline="")
        self.canvas.create_text(600, 125, text="MYSTERY WORD TILES", font=FONTS["caption"], fill=COLORS["txt_dark"])
        self.render_word_tiles(600, 175)

        # Right Bottom Card: On-Screen Virtual Keyboard
        self.draw_rounded_rect(384, 264, 824, 624, radius=18, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(380, 260, 820, 620, radius=18, fill=COLORS["paper_card"], outline="")
        self.canvas.create_text(600, 285, text="CHOOSE A LETTER (OR TYPE ON KEYBOARD)", font=FONTS["caption"], fill=COLORS["txt_dark"])
        self.render_paper_keyboard(395, 310)

    # ==========================================================================
    # HANGMAN ARTWORK (Progressive 6 Stages)
    # ==========================================================================
    def draw_hangman_figure(self, cx: float, cy: float) -> None:
        """Draws stylized gallows and character in deep plum tones."""
        # Gallows Scaffold
        self.canvas.create_line(cx - 90, cy + 90, cx + 50, cy + 90, width=8, fill=COLORS["gallows"], capstyle="round")
        self.canvas.create_line(cx - 50, cy + 90, cx - 50, cy - 110, width=8, fill=COLORS["gallows"], capstyle="round")
        self.canvas.create_line(cx - 50, cy - 110, cx + 40, cy - 110, width=8, fill=COLORS["gallows"], capstyle="round")
        self.canvas.create_line(cx - 20, cy - 110, cx - 50, cy - 80, width=6, fill=COLORS["gallows"], capstyle="round")
        self.canvas.create_line(cx + 40, cy - 110, cx + 40, cy - 75, width=4, fill=COLORS["hang_rope"], capstyle="round")

        # STAGE 1: Head
        if self.mistakes >= 1:
            self.canvas.create_oval(cx + 20, cy - 75, cx + 60, cy - 35, width=4, outline=COLORS["hang_figure"], fill=COLORS["cream_shadow"])
            self.canvas.create_oval(cx + 29, cy - 58, cx + 33, cy - 54, fill=COLORS["hang_figure"])
            self.canvas.create_oval(cx + 47, cy - 58, cx + 51, cy - 54, fill=COLORS["hang_figure"])
            if self.mistakes < 6:
                self.canvas.create_arc(cx + 33, cy - 50, cx + 47, cy - 40, start=190, extent=160, style="arc", width=2, outline=COLORS["hang_figure"])
            else:
                self.canvas.create_line(cx + 34, cy - 44, cx + 46, cy - 44, width=2, fill=COLORS["hang_figure"])

        # STAGE 2: Torso
        if self.mistakes >= 2:
            self.canvas.create_line(cx + 40, cy - 35, cx + 40, cy + 20, width=5, fill=COLORS["hang_figure"], capstyle="round")

        # STAGE 3: Left Arm
        if self.mistakes >= 3:
            self.canvas.create_line(cx + 40, cy - 20, cx + 15, cy + 5, width=4, fill=COLORS["hang_figure"], capstyle="round")

        # STAGE 4: Right Arm
        if self.mistakes >= 4:
            self.canvas.create_line(cx + 40, cy - 20, cx + 65, cy + 5, width=4, fill=COLORS["hang_figure"], capstyle="round")

        # STAGE 5: Left Leg
        if self.mistakes >= 5:
            self.canvas.create_line(cx + 40, cy + 20, cx + 20, cy + 65, width=4, fill=COLORS["hang_figure"], capstyle="round")

        # STAGE 6: Right Leg
        if self.mistakes >= 6:
            self.canvas.create_line(cx + 40, cy + 20, cx + 60, cy + 65, width=4, fill=COLORS["hang_figure"], capstyle="round")

    # ==========================================================================
    # MYSTERY WORD TILES
    # ==========================================================================
    def render_word_tiles(self, center_x: float, center_y: float):
        n = len(self.secret_word)
        tile_w, tile_h, gap = 38, 48, 8
        total_w = n * (tile_w + gap) - gap
        start_x = center_x - (total_w / 2)

        for i, char in enumerate(self.secret_word):
            tx = start_x + i * (tile_w + gap)
            ty = center_y - (tile_h / 2)

            # Cream drop shadow underlay
            self.draw_rounded_rect(tx + 4, ty + 4, tx + tile_w + 4, ty + tile_h + 4, radius=8, fill=COLORS["cream_shadow"], outline="")

            if char in self.guessed_letters:
                # Revealed Green Tile
                self.draw_rounded_rect(tx, ty, tx + tile_w, ty + tile_h, radius=8, fill=COLORS["easy_face"], outline="")
                self.canvas.create_text(tx + tile_w / 2, ty + tile_h / 2, text=char, font=FONTS["word_tile"], fill=COLORS["txt_yellow"])
            else:
                # Blank Tile
                self.draw_rounded_rect(tx, ty, tx + tile_w, ty + tile_h, radius=8, fill=COLORS["paper_card"], outline="")
                self.canvas.create_text(tx + tile_w / 2, ty + tile_h / 2 + 4, text="_", font=FONTS["title_md"], fill=COLORS["txt_dark"])

    # ==========================================================================
    # KEYBOARD RENDERING
    # ==========================================================================
    def render_paper_keyboard(self, start_x: float, start_y: float):
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        btn_w, btn_h, pad = 36, 42, 6

        for r_idx, row in enumerate(rows):
            row_w = len(row) * (btn_w + pad) - pad
            row_start_x = start_x + (415 - row_w) / 2
            
            for c_idx, char in enumerate(row):
                bx = row_start_x + c_idx * (btn_w + pad)
                by = start_y + r_idx * (btn_h + 16)
                tag = f"key_{char}"

                if char in self.guessed_letters:
                    if char in self.secret_word:
                        # Correct Guess
                        self.draw_paper_button(
                            tag=tag, x=bx, y=by, width=btn_w, height=btn_h,
                            label=char, face_color=COLORS["easy_face"], text_color=COLORS["txt_yellow"],
                            enabled=False, radius=8, offset_x=3, offset_y=3
                        )
                    else:
                        # Wrong Guess
                        self.draw_paper_button(
                            tag=tag, x=bx, y=by, width=btn_w, height=btn_h,
                            label=char, face_color=COLORS["key_wrong"], text_color=COLORS["key_wrong_txt"],
                            enabled=False, radius=8, offset_x=2, offset_y=2
                        )
                else:
                    # Active Key
                    self.draw_paper_button(
                        tag=tag, x=bx, y=by, width=btn_w, height=btn_h,
                        label=char, face_color=COLORS["key_active"], text_color=COLORS["txt_yellow"],
                        command=lambda l=char: self.process_guess(l),
                        radius=8, offset_x=4, offset_y=4
                    )

    # ==========================================================================
    # GUESS PROCESSING & SCREEN JUICE
    # ==========================================================================
    def handle_physical_key(self, event: tk.Event) -> None:
        if self.game_over:
            return
        char = event.char.upper()
        if char.isalpha() and len(char) == 1:
            self.process_guess(char)

    def process_guess(self, letter: str) -> None:
        if self.game_over or letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            self.score += 10
            self.play_sound("correct")
        else:
            self.mistakes += 1
            self.score = max(0, self.score - 10)
            self.play_sound("wrong")
            self.trigger_screen_shake()

        all_revealed = all(char in self.guessed_letters for char in self.secret_word)
        
        if all_revealed:
            self.handle_game_end(won=True)
        elif self.mistakes >= self.max_mistakes:
            self.handle_game_end(won=False)
        else:
            self.show_game_screen()

    # ==========================================================================
    # HINT MECHANICS
    # ==========================================================================
    def use_hint_1(self) -> None:
        if self.hint1_used or self.game_over or not self.current_word_data:
            return
        self.hint1_used = True
        cat = self.current_word_data.get("category", "General Tech")
        self.hint_display_text = f"Category: '{cat}'"
        self.show_game_screen()

    def use_hint_2(self) -> None:
        if self.hint2_used or self.game_over or not self.secret_word:
            return
        self.hint2_used = True
        self.score = max(0, self.score - 10)
        self.hint_display_text = f"Starts with '{self.secret_word[0]}'"
        self.show_game_screen()

    def use_hint_3(self) -> None:
        if self.hint3_used or self.game_over or not self.secret_word:
            return
        self.hint3_used = True
        self.score = max(0, self.score - 20)
        
        unrevealed = [c for c in self.secret_word if c not in self.guessed_letters]
        if unrevealed:
            reveal_char = random.choice(unrevealed)
            self.hint_display_text = f"Revealed letter '{reveal_char}'!"
            self.process_guess(reveal_char)
        else:
            self.hint_display_text = "All letters already uncovered!"
            self.show_game_screen()

    # ==========================================================================
    # RESULT OVERLAYS & ANIMATION
    # ==========================================================================
    def handle_game_end(self, won: bool) -> None:
        self.game_over = True
        self.stats["games_played"] += 1
        
        if won:
            self.score += 50
            self.stats["wins"] += 1
            if self.score > self.stats["best_score"]:
                self.stats["best_score"] = self.score
            self.play_sound("win")
            self.show_win_screen()
        else:
            self.play_sound("lose")
            self.show_loss_screen()

    def spawn_confetti(self):
        self.confetti_particles = []
        colors = [COLORS["easy_face"], COLORS["med_face"], COLORS["play_face"], COLORS["txt_yellow"], COLORS["purple_face"]]
        for _ in range(50):
            self.confetti_particles.append({
                "x": random.randint(40, 820),
                "y": random.randint(-60, 40),
                "vy": random.uniform(3.0, 6.5),
                "vx": random.uniform(-1.5, 1.5),
                "sz": random.randint(6, 12),
                "color": random.choice(colors)
            })

    def animate_confetti(self):
        if not self.game_over or self.mistakes >= self.max_mistakes:
            return
        self.canvas.delete("confetti")
        for p in self.confetti_particles:
            p["y"] += p["vy"]
            p["x"] += p["vx"]
            if p["y"] > 650:
                p["y"] = -10
                p["x"] = random.randint(40, 820)
            
            self.canvas.create_oval(
                p["x"], p["y"], p["x"] + p["sz"], p["y"] + p["sz"],
                fill=p["color"], outline="", tags="confetti"
            )
        self.confetti_anim_id = self.after(35, self.animate_confetti)

    def show_win_screen(self) -> None:
        self.canvas.delete("all")
        self.draw_background_bubbles()

        self.spawn_confetti()
        self.animate_confetti()

        # Result Card
        self.draw_rounded_rect(204, 64, 684, 584, radius=24, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(200, 60, 680, 580, radius=24, fill=COLORS["paper_card"], outline="")

        # Banner
        self.draw_rounded_rect(240, 85, 640, 150, radius=16, fill=COLORS["easy_face"], outline="")
        self.canvas.create_text(440, 118, text="★ VICTORY! ★", font=FONTS["title_md"], fill=COLORS["txt_yellow"])

        self.canvas.create_text(440, 185, text="YOU CRACKED THE MYSTERY!", font=FONTS["title_sm"], fill=COLORS["txt_dark"])
        self.canvas.create_text(440, 225, text=f"THE WORD WAS: {self.secret_word}", font=FONTS["title_hero"], fill=COLORS["easy_face"])

        # Fact Card
        fact_text = self.current_word_data.get("fact", "") if self.current_word_data else ""
        self.draw_rounded_rect(234, 274, 644, 394, radius=14, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(230, 270, 640, 390, radius=14, fill=COLORS["bg_sky"], outline="")
        self.canvas.create_text(435, 295, text="DID YOU KNOW?", font=FONTS["caption"], fill=COLORS["txt_dark"])
        self.canvas.create_text(435, 325, text=fact_text, font=FONTS["body"], fill=COLORS["txt_dark"], width=380, justify="center")
        self.canvas.create_text(435, 365, text=f"FINAL SCORE: {self.score} PTS", font=FONTS["title_sm"], fill=COLORS["txt_dark"])

        # Replay & Home Buttons
        self.draw_paper_button(
            tag="win_replay_btn",
            x=240, y=430, width=185, height=56,
            label="PLAY AGAIN",
            face_color=COLORS["easy_face"],
            text_color=COLORS["txt_yellow"],
            command=self.start_new_game,
            radius=14,
            offset_x=6, offset_y=6
        )

        self.draw_paper_button(
            tag="win_home_btn",
            x=455, y=430, width=185, height=56,
            label="MAIN MENU",
            face_color=COLORS["play_face"],
            text_color=COLORS["txt_yellow"],
            command=self.show_home_screen,
            radius=14,
            offset_x=6, offset_y=6
        )

    def show_loss_screen(self) -> None:
        self.canvas.delete("all")
        if self.confetti_anim_id:
            self.after_cancel(self.confetti_anim_id)
            self.confetti_anim_id = None
        self.draw_background_bubbles()

        # Result Card
        self.draw_rounded_rect(204, 64, 684, 584, radius=24, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(200, 60, 680, 580, radius=24, fill=COLORS["paper_card"], outline="")

        # Banner
        self.draw_rounded_rect(240, 85, 640, 150, radius=16, fill=COLORS["play_face"], outline="")
        self.canvas.create_text(440, 118, text="GAME OVER", font=FONTS["title_md"], fill=COLORS["txt_yellow"])

        self.canvas.create_text(440, 185, text="THE HANGMAN WAS COMPLETED!", font=FONTS["title_sm"], fill=COLORS["txt_dark"])
        self.canvas.create_text(440, 225, text=f"THE WORD WAS: {self.secret_word}", font=FONTS["title_hero"], fill=COLORS["play_face"])

        # Overview Card
        fact_text = self.current_word_data.get("fact", "") if self.current_word_data else ""
        self.draw_rounded_rect(234, 274, 644, 394, radius=14, fill=COLORS["cream_shadow"], outline="")
        self.draw_rounded_rect(230, 270, 640, 390, radius=14, fill=COLORS["bg_sky"], outline="")
        self.canvas.create_text(435, 295, text="OVERVIEW", font=FONTS["caption"], fill=COLORS["txt_dark"])
        self.canvas.create_text(435, 325, text=fact_text, font=FONTS["body"], fill=COLORS["txt_dark"], width=380, justify="center")
        self.canvas.create_text(435, 365, text=f"FINAL SCORE: {self.score} PTS", font=FONTS["title_sm"], fill=COLORS["txt_dark"])

        # Replay & Home Buttons
        self.draw_paper_button(
            tag="loss_replay_btn",
            x=240, y=430, width=185, height=56,
            label="TRY AGAIN",
            face_color=COLORS["med_face"],
            text_color=COLORS["txt_yellow"],
            command=self.start_new_game,
            radius=14,
            offset_x=6, offset_y=6
        )

        self.draw_paper_button(
            tag="loss_home_btn",
            x=455, y=430, width=185, height=56,
            label="MAIN MENU",
            face_color=COLORS["play_face"],
            text_color=COLORS["txt_yellow"],
            command=self.show_home_screen,
            radius=14,
            offset_x=6, offset_y=6
        )


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()