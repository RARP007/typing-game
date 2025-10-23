"""
    Kode ini saya buat dengan 2 tujuan, yaitu untuk mengatasi kecepatan mengetik
siswa yang lambat serta untuk mengasah kemampuan logika saya. Banyak siswa jurusan
RPL, TKJ, IT, dan sejenisnya memiliki kecepatan mengetik yang lambat (termasuk
saya dan semua teman sekelas saya), dari sanalah saya terpikirkan untuk membuat
sebuah game dengan tema typing. Logika dalam game ini saya buat manual tanpa
menggunakan AI, baru setelah itu saya rapikan dengan bantuan AI agar sesui dengan
OOP yang terstruktur.
"""

import pygame
import random
import math

# =============================================================================
# Inisialisasi Pygame
# =============================================================================
pygame.init()
pygame.display.set_caption("Typing Run")

# =============================================================================
# Konstanta & Data Game (LENGKAP)
# =============================================================================

# --- Pengaturan Layar & Font ---
WIDTH, HEIGHT = 1365, 720
FPS = 60

# --- Warna ---
COLOR_BACKGROUND = (60, 60, 60)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN_BRIGHT = (0, 255, 0)
COLOR_GREEN_INPUT = (0, 210, 0)
COLOR_GREY_LIGHT = (230, 230, 230)
COLOR_GREY_MEDIUM = (130, 130, 130)
COLOR_GREY_DARK = (50, 50, 50)
COLOR_GOLD = (255, 215, 0)
COLOR_BLUE = (50, 50, 255)
COLOR_BLUE_DARK = (30, 30, 180)
COLOR_BLUE_BORDER = (20, 250, 250)
COLOR_GREY_COMING_SOON = (200, 200, 200)

# --- Data Petunjuk ---
COMING_SOON = {
    "1": {"t": "Coming soon:", "y": 15},  # Typo 'Cooming' diperbaiki
    "2": {"t": "-Update visual", "y": 65},
    "3": {"t": "-Mode hardcore", "y": 115},
    "4": {"t": "-Lebih banyak", "y": 165},
    "5": {"t": " kata/frasa/kalimat", "y": 215}
}

# --- Data Game ---
BEST_SCORES = {
    "huruf": {"p": 0, "y": 200, "t": "Huruf"},
    "kata": {"p": 0, "y": 500, "t": "Kata"},
    "frasa": {"p": 0, "y": 800, "t": "Frasa"},
    "kalimat": {"p": 0, "y": 1100, "t": "Kalimat"}
}

LEVEL_CHOICES = {
    "1": {"a": list("huruf"), "b": 150, "c": "huruf", "d": "HURUF"},
    "2": {"a": list("kata"), "b": 220, "c": "kata", "d": "KATA"},
    "3": {"a": list("frasa"), "b": 285, "c": "frasa", "d": "FRASA"},
    "4": {"a": list("kalimat"), "b": 355, "c": "kalimat", "d": "KALIMAT"}
}

KEY_MAP = {
    pygame.K_q: "q", pygame.K_w: "w", pygame.K_e: "e", pygame.K_r: "r",
    pygame.K_t: "t", pygame.K_y: "y", pygame.K_u: "u", pygame.K_i: "i",
    pygame.K_o: "o", pygame.K_p: "p", pygame.K_a: "a", pygame.K_s: "s",
    pygame.K_d: "d", pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h",
    pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", pygame.K_z: "z",
    pygame.K_x: "x", pygame.K_c: "c", pygame.K_v: "v", pygame.K_b: "b",
    pygame.K_n: "n", pygame.K_m: "m", pygame.K_SPACE: " "
}

SOAL = {
    "huruf": {str(i): [chr(96 + i)] for i in range(1, 27)},
    "kata": {
        "1": list("kabel"), "2": list("sinar"), "3": list("login"), "4": list("layar"),
        "5": list("cepat"), "6": list("rumah"), "7": list("dasar"), "8": list("modem"),
        "9": list("suara"), "10": list("cetak"), "11": list("kipas"), "12": list("pesan"),
        "13": list("kilau"), "14": list("tidur"), "15": list("angka"), "16": list("token"),
        "17": list("warna"), "18": list("tutup"), "19": list("panas"), "20": list("gerak")
    },
    "frasa": {
        "1": list("data aman"), "2": list("login cepat"), "3": list("kabel rusak"),
        "4": list("angin segar"), "5": list("lampu mati"), "6": list("layar penuh"),
        "7": list("waktu habis"), "8": list("meja bulat"), "9": list("server baru"),
        "10": list("pintu buka"), "11": list("tangan kanan"), "12": list("bola jatuh"),
        "13": list("suhu panas"), "14": list("api kecil"), "15": list("jalan jalan"),
        "16": list("awan tipis"), "17": list("suara keras"), "18": list("roda berputar"),
        "19": list("jam rusak"), "20": list("bunga segar")
    },
    "kalimat": {
        "1": list("aku tekan tombol hijau"),
        "2": list("angin sore membawa debu"),
        "3": list("server utama mulai sibuk"),
        "4": list("ibu menata bunga segar"),
        "5": list("layar laptop mulai redup"),
        "6": list("anak kecil bermain bola"),
        "7": list("lampu kamar padam lagi"),
        "8": list("aku simpan file penting"),
        "9": list("data user tersimpan aman"),
        "10": list("mereka duduk di taman"),
        "11": list("tikus kecil berlari cepat"),
        "12": list("guru memanggil nama saya"),
        "13": list("komputer mulai restart"),
        "14": list("kursi kayu terasa dingin"),
        "15": list("aku coba login ulang")
    }
}


# =============================================================================
# Kelas Utama Game (Context)
# =============================================================================

class Game:
    """Kelas utama yang mengelola state, data bersama, dan game loop."""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Typing Run")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Memuat Font & Data Bersama
        self.load_shared_data()

        # Variabel Status UI Bersama
        self.reset_shared_ui_state()
        
        # Inisialisasi State Awal
        self.current_state = LobbyState(self)

    def load_shared_data(self):
        """Memuat aset yang akan digunakan di banyak state."""
        self.FONT_LG = pygame.font.SysFont(None, 100)
        self.FONT_MD = pygame.font.SysFont(None, 50)
        self.FONT_SM = pygame.font.SysFont(None, 25)
        
        # Data persisten
        self.BEST_SCORES = BEST_SCORES
        self.SOAL = SOAL
        self.KEY_MAP = KEY_MAP
        self.LEVEL_CHOICES = LEVEL_CHOICES
        self.COMING_SOON = COMING_SOON

    def reset_shared_ui_state(self):
        """Mereset variabel UI yang digunakan di semua state."""
        self.current_input_list = []
        self.help_panel_animation = None
        self.help_panel_left_x = -500
        self.help_panel_right_x = 1370
        self.show_overlay = False
        self.show_wrong_input = False
        self.idle_timer = 0
        self.cursor_blink_on = True
        self.cursor_blink_timer = 1
        self.cursor_color = COLOR_GREEN_BRIGHT

    def switch_state(self, new_state):
        """Metode untuk transisi ke state (layar) baru."""
        # Reset UI input/overlay saat pindah layar
        self.show_wrong_input = False
        self.current_input_list = []
        self.current_state = new_state

    def run(self):
        """Game loop utama."""
        while self.running:
            # 1. Dapatkan semua event
            events = pygame.event.get()

            # 2. Update status UI bersama (cursor, panel, dll.)
            self.update_common_state()
            
            # 3. Delegasikan event handling ke state yang aktif
            self.current_state.handle_events(events)
            
            # 4. Delegasikan update logic ke state yang aktif
            self.current_state.update()
            
            # 5. Gambar (Draw)
            self.screen.fill(COLOR_BACKGROUND)  # Bersihkan layar
            self.current_state.draw(self.screen) # State aktif menggambar
            self.draw_common_ui(self.screen)    # UI bersama (input, overlay, petunjuk)
            
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

    def update_common_state(self):
        """Update logic yang berjalan di semua state (panel, kursor)."""
        # --- Logika Animasi Panel Petunjuk (Help Panel) ---
        if not self.help_panel_left_x >= 0 and self.idle_timer >= 600 and not self.help_panel_animation == "aktif":
            self.help_panel_animation = "aktif"
        else:
            self.idle_timer += 1

        if self.help_panel_animation == "aktif":
            self.help_panel_left_x += 20
            self.help_panel_right_x -= 20
            self.show_overlay = True
            if self.help_panel_left_x >= 0:
                self.help_panel_animation = None
        elif self.help_panel_animation == "mati":
            self.help_panel_left_x -= 20
            self.help_panel_right_x += 20
            self.show_overlay = False
            if self.help_panel_left_x <= -500:
                self.help_panel_animation = None
                
        # --- Logika Kursor Berkedip ---
        if self.cursor_blink_on:
            self.cursor_blink_timer -= 1
            self.cursor_color = COLOR_GREEN_BRIGHT
            if self.cursor_blink_timer <= 0:
                self.cursor_blink_on = False
        elif not self.cursor_blink_on:
            self.cursor_blink_timer += 1
            self.cursor_color = COLOR_BACKGROUND
            if self.cursor_blink_timer >= 30:
                self.cursor_blink_on = True

    def handle_common_events(self, event):
        """Memproses event yang sama di semua state (input teks, F1)."""
        # Reset idle timer, kursor, dan pesan error setiap ada input
        self.idle_timer = 0
        self.cursor_blink_timer = 30
        self.cursor_blink_on = True
        self.show_wrong_input = False

        if event.key in self.KEY_MAP:
            self.current_input_list.append(self.KEY_MAP[event.key])
        elif event.key == pygame.K_BACKSPACE and self.current_input_list:
            self.current_input_list.pop()
        elif event.key == pygame.K_DELETE:
            self.current_input_list = []
        
        # Tombol F1 untuk Petunjuk
        elif event.key == pygame.K_F1:
            if not self.help_panel_left_x >= 0 and not self.help_panel_animation == "aktif":
                self.help_panel_animation = "aktif"
            elif not self.help_panel_left_x <= -500 and not self.help_panel_animation == "mati":
                self.help_panel_animation = "mati"

    def draw_common_ui(self, screen):
        """Menggambar elemen UI yang ada di semua state."""
        
        # Tentukan apakah input line harus digambar
        draw_input = isinstance(self.current_state, (LobbyState, ResultState)) or \
                     (isinstance(self.current_state, GameState) and self.current_state.game_mode != "huruf")
        
        if draw_input:
            self.draw_input_line(screen, self.cursor_color)

        if self.show_overlay or self.show_wrong_input:
            self.overlay_layar(screen)
        
        if self.show_wrong_input:
            self.wrong_input_feedback(screen)
        
        # Panel petunjuk (menggunakan nama kelas state untuk menentukan teks)
        self.draw_petunjuk(screen, self.current_state.state_name)

    # --- Fungsi Helper UI (sebelumnya fungsi global) ---

    def draw_input_line(self, screen, cursor_color_param):
        screen.fill(COLOR_BACKGROUND, (0, 0, 0, 0))
        input_text = "".join(self.current_input_list)
        cursor_text_surface = self.FONT_LG.render(input_text + "|", True, cursor_color_param)
        screen.blit(cursor_text_surface, (100, 425))
        input_text_surface = self.FONT_LG.render(input_text, True, COLOR_GREEN_BRIGHT)
        screen.blit(input_text_surface, (100, 425))
        screen.blit(self.FONT_LG.render(">", True, COLOR_GREEN_BRIGHT), (50, 425))

    def overlay_layar(self, screen):
        overlay_surface = pygame.Surface((WIDTH, HEIGHT))
        overlay_surface.set_alpha(150)
        overlay_surface.fill(COLOR_GREY_DARK)
        screen.blit(overlay_surface, (0, 0))

    def wrong_input_feedback(self, screen):
        screen.fill(COLOR_BACKGROUND, (0, 0, 0, 0))
        text = self.FONT_LG.render("Salah input!", True, COLOR_RED)
        screen.blit(text, text.get_rect(center=(700, 300)))

    def draw_petunjuk(self, screen, state_name):
        # Menggambar panel dasar
        pygame.draw.rect(screen, COLOR_GREY_LIGHT, (self.help_panel_left_x, 305, 500, 300))
        pygame.draw.rect(screen, COLOR_BLUE_BORDER, ((self.help_panel_left_x - 15), 305, 515, 300), 10)
        pygame.draw.rect(screen, COLOR_GREY_LIGHT, (self.help_panel_right_x, 305, 500, 300))
        pygame.draw.rect(screen, COLOR_BLUE_BORDER, (self.help_panel_right_x, 305, 515, 300), 10)

        # Menggambar teks spesifik berdasarkan state_name
        # (Fungsi ini identik dengan di file asli Anda, hanya menggunakan self.FONT, dll.)
        if state_name == "lobby":
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 25), 530, 100, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 15), 530, 100, 50), border_radius=10)
            screen.blit(self.FONT_MD.render(">reset", True, COLOR_GREEN_INPUT), ((self.help_panel_left_x + 15), 480))
            screen.blit(self.FONT_MD.render(">menu", True, COLOR_GREEN_INPUT), ((self.help_panel_right_x + 25), 480))
            screen.blit(self.FONT_MD.render("[!] MENU", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 325))
            screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_left_x + 55), 540))
            screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_right_x + 65), 540))
            screen.blit(self.FONT_MD.render("[!] RESET SCORE", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 325))
            screen.blit(self.FONT_SM.render("Ketik 'menu' lalu tekan 'Enter' untuk pergi ke MENU.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
            screen.blit(self.FONT_SM.render("Ketik 'reset' lalu tekan 'Enter' untuk mereset score.", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 380))
       
        elif state_name == "menu":
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 25), 510, 50, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 125), 510, 50, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 75), 510, 50, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 75), 450, 50, 50), border_radius=10)
            pygame.draw.polygon(screen, COLOR_WHITE, [((self.help_panel_right_x + 55), 515), ((self.help_panel_right_x + 55), 525), ((self.help_panel_right_x + 45), 520)])
            pygame.draw.polygon(screen, COLOR_WHITE, [((self.help_panel_right_x + 145), 515), ((self.help_panel_right_x + 145), 525), ((self.help_panel_right_x + 155), 520)])
            pygame.draw.polygon(screen, COLOR_WHITE, [((self.help_panel_left_x + 95), 465), ((self.help_panel_left_x + 105), 465), ((self.help_panel_left_x + 100), 455)])
            pygame.draw.polygon(screen, COLOR_WHITE, [((self.help_panel_left_x + 95), 515), ((self.help_panel_left_x + 105), 515), ((self.help_panel_left_x + 100), 525)])
            screen.blit(self.FONT_MD.render("[!] BACK OR NEXT", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 325))
            screen.blit(self.FONT_MD.render("[!] CHOISE", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 325))
            screen.blit(self.FONT_SM.render("Left", True, COLOR_BLACK), ((self.help_panel_right_x + 35), 560))
            screen.blit(self.FONT_SM.render("Right", True, COLOR_BLACK), ((self.help_panel_right_x + 128), 560))
            screen.blit(self.FONT_SM.render("Up", True, COLOR_BLACK), ((self.help_panel_left_x + 90), 431))
            screen.blit(self.FONT_SM.render("Down", True, COLOR_BLACK), ((self.help_panel_left_x + 76), 560))
            screen.blit(self.FONT_SM.render("Tekan 'Left' untuk kembali ke LOBBY dan", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
            screen.blit(self.FONT_SM.render("tekan 'Right' untuk memainkan mode yang dipilih.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 400))
            screen.blit(self.FONT_SM.render("Tekan 'Up' dan 'Down' untuk mengganti pilihan mode.", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 380))
        
        elif state_name == "game":
            game_mode = self.current_state.game_mode # Ambil game_mode dari state game
            if game_mode == "huruf":
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 25), 530, 50, 50), border_radius=10)
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 85), 530, 50, 50), border_radius=10)
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 145), 530, 50, 50), border_radius=10)
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 205), 530, 50, 50), border_radius=10)
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 265), 530, 50, 50), border_radius=10)
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 15), 530, 100, 50), border_radius=10)
                screen.blit(self.FONT_SM.render("Q", True, COLOR_WHITE), ((self.help_panel_right_x + 35), 540))
                screen.blit(self.FONT_SM.render("W", True, COLOR_WHITE), ((self.help_panel_right_x + 95), 540))
                screen.blit(self.FONT_SM.render("E", True, COLOR_WHITE), ((self.help_panel_right_x + 155), 540))
                screen.blit(self.FONT_SM.render("R", True, COLOR_WHITE), ((self.help_panel_right_x + 215), 540))
                screen.blit(self.FONT_SM.render("T", True, COLOR_WHITE), ((self.help_panel_right_x + 275), 540))
                screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_left_x + 55), 540))
                screen.blit(self.FONT_MD.render("[!] STARTING GAME", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 325))
                screen.blit(self.FONT_MD.render("[!] PLAYING GAME", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 325))
                screen.blit(self.FONT_SM.render("Tekan tombol sesuai huruf yang muncul di layar.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
                screen.blit(self.FONT_SM.render("Tekan tombol 'Enter' untuk memulai game.", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 380))
            else:
                pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 15), 530, 100, 50), border_radius=10)
                screen.blit(self.FONT_MD.render(">start_", True, COLOR_GREEN_INPUT), ((self.help_panel_left_x + 15), 480))
                screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_left_x + 55), 540))
                screen.blit(self.FONT_MD.render("[!] STARTING GAME", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 325))
                screen.blit(self.FONT_MD.render("[!] PLAYING GAME", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 325))
                screen.blit(self.FONT_SM.render("Ketik 'Start' lalu tekan 'Enter' untuk memulai game.", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 380))
                if game_mode == "kata":
                    screen.blit(self.FONT_SM.render("Ketik kata yang muncul di layar, lalu tekan 'Enter'.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
                    screen.blit(self.FONT_SM.render("Ketik sebanyak mungkin dalam waktu 30 detik!", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 420))
                elif game_mode == "frasa":
                    screen.blit(self.FONT_SM.render("Ketik frasa yang muncul di layar, lalu tekan 'Enter'.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
                    screen.blit(self.FONT_SM.render("Ketik sebanyak mungkin dalam waktu 30 detik!", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 420))
                elif game_mode == "kalimat":
                    screen.blit(self.FONT_SM.render("Ketik kalimat yang muncul di layar, lalu tekan 'Enter'.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
                    screen.blit(self.FONT_SM.render("Ketik kalimat di layar sebanyak 3 kali secepat mungkin!", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 420))
        
        elif state_name == "result":
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_right_x + 25), 530, 100, 50), border_radius=10)
            pygame.draw.rect(screen, COLOR_GREY_DARK, ((self.help_panel_left_x + 15), 530, 100, 50), border_radius=10)
            screen.blit(self.FONT_MD.render("[!] MENU", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 325))
            screen.blit(self.FONT_MD.render("[!] LOBBY", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 325))
            screen.blit(self.FONT_MD.render(">lobby", True, COLOR_GREEN_INPUT), ((self.help_panel_left_x + 15), 480))
            screen.blit(self.FONT_MD.render(">menu", True, COLOR_GREEN_INPUT), ((self.help_panel_right_x + 25), 480))
            screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_left_x + 55), 540))
            screen.blit(self.FONT_SM.render("Enter", True, COLOR_WHITE), ((self.help_panel_right_x + 65), 540))
            screen.blit(self.FONT_SM.render("Ketik 'menu' lalu tekan 'Enter' untuk langsung ke MENU.", True, COLOR_BLACK), ((self.help_panel_right_x + 20), 380))
            screen.blit(self.FONT_SM.render("Ketik 'lobby' lalu tekan 'Enter' untuk langsung ke LOBBY.", True, COLOR_BLACK), ((self.help_panel_left_x + 10), 380))


# =============================================================================
# Kelas State Dasar (Template)
# =============================================================================

class State:
    """Kelas dasar untuk semua state (layar) game."""
    def __init__(self, game):
        self.game = game
        self.state_name = "base"

    def handle_events(self, events):
        """Memproses input untuk state ini."""
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                # Kirim event ke handler bersama di kelas Game
                self.game.handle_common_events(event)
                # Jalankan handler spesifik milik state ini
                self.handle_specific_event(event)

    def handle_specific_event(self, event):
        """Metode ini akan di-override oleh kelas turunan."""
        pass

    def update(self):
        """Update logika untuk state ini (akan di-override)."""
        pass

    def draw(self, screen):
        """Gambar state ini ke layar (akan di-override)."""
        pass
    
    def choose_random_soal_for_mode(self, mode):
        """Fungsi helper yang bisa diakses oleh state turunan."""
        if mode in self.game.SOAL:
            mode_soal_dict = self.game.SOAL[mode]
            random_key = random.choice(list(mode_soal_dict.keys()))
            return mode_soal_dict[random_key]
        return None

# =============================================================================
# Kelas State Spesifik (Layar Game)
# =============================================================================

class LobbyState(State):
    """State untuk layar Lobby (Best Scores)."""
    def __init__(self, game):
        super().__init__(game)
        self.state_name = "lobby"

    def handle_specific_event(self, event):
        if event.key == pygame.K_RETURN:
            input_str = "".join(self.game.current_input_list)
            if input_str == "menu":
                self.game.switch_state(MenuState(self.game))
            elif input_str == "reset":
                for score_data in self.game.BEST_SCORES.values():
                    score_data["p"] = 0
                self.game.current_input_list = []
            else:
                self.game.show_wrong_input = True
    
    def draw(self, screen):
        # (Logika dari 'draw_lobby' dipindah ke sini)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (850, 620, 515, 85), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 605, 350, 100), 0)
        pygame.draw.rect(screen, COLOR_BLUE, (0, 0, WIDTH, 300), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 100, WIDTH, 200), 10)
        pygame.draw.rect(screen, COLOR_GOLD, (0, 0, WIDTH, 100), 0)
        pygame.draw.rect(screen, COLOR_BLACK, (870, 640, 50, 50), border_radius=10)
        
        screen.blit(self.game.FONT_SM.render("F1", True, COLOR_WHITE), (888, 650))
        screen.blit(self.game.FONT_MD.render("Tekan F1 untuk petunjuk.", True, COLOR_WHITE), (930, 650))
        screen.blit(self.game.FONT_LG.render("LOBBY", True, COLOR_GREY_LIGHT), (50, 625))
        screen.blit(self.game.FONT_LG.render("Best Score", True, COLOR_WHITE), (475, 20))

        for mode_data in self.game.BEST_SCORES.values():
            text = self.game.FONT_MD.render(mode_data["t"], True, COLOR_WHITE)
            point = self.game.FONT_MD.render(str(mode_data["p"]), True, COLOR_WHITE)
            ctext = text.get_rect(center=(mode_data["y"], 175))
            cpoint = point.get_rect(center=(mode_data["y"], 225))
            screen.blit(text, ctext)
            screen.blit(point, cpoint)


class MenuState(State):
    """State untuk layar Menu (Pilih Level)."""
    def __init__(self, game):
        super().__init__(game)
        self.state_name = "menu"
        self.selected_menu_index = 1 # Variabel 'a' lama, sekarang lokal
    
    def update(self):
        # Menu tidak menggunakan input teks, jadi selalu kosongkan
        self.game.current_input_list = []

    def handle_specific_event(self, event):
        if event.key == pygame.K_RIGHT:
            chosen_level = self.game.LEVEL_CHOICES[str(self.selected_menu_index)]
            # Buat state game baru dan kirim data level
            new_game_state = GameState(self.game, chosen_level["c"], chosen_level["d"])
            self.game.switch_state(new_game_state)
        elif event.key == pygame.K_LEFT:
            self.game.switch_state(LobbyState(self.game))
        elif event.key == pygame.K_DOWN and not self.selected_menu_index >= 4:
            self.selected_menu_index += 1
        elif event.key == pygame.K_UP and not self.selected_menu_index <= 1:
            self.selected_menu_index -= 1
        elif event.key not in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_F1):
            # Cek agar F1 tidak memicu 'salah input'
            if event.key != pygame.K_F1:
                self.game.show_wrong_input = True

    def draw(self, screen):
        # (Logika dari 'draw_menu' dipindah ke sini)
        pilihan = self.game.FONT_LG.render("Pilih Level Berikut!", True, COLOR_WHITE)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 605, 350, 100), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 0, WIDTH, 430), 0)
        pygame.draw.rect(screen, COLOR_BLUE_DARK, (340, 0, 680, 430), 0)
        pygame.draw.rect(screen, COLOR_GOLD, (340, 0, 680, 90), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (340, 0, 680, 430), 10)
        
        highlight_y = self.game.LEVEL_CHOICES[str(self.selected_menu_index)]["b"] - 20
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, highlight_y, WIDTH, 40), 0)
        
        screen.blit(self.game.FONT_LG.render("MENU", True, COLOR_GREY_LIGHT), (70, 625))
        screen.blit(pilihan, pilihan.get_rect(center=(680, 50)))

        for item in self.game.COMING_SOON.values():
            screen.blit(self.game.FONT_MD.render(item["t"], True, COLOR_GREY_COMING_SOON), (15, item["y"]))
        
        for level_data in self.game.LEVEL_CHOICES.values():
            sp = self.game.FONT_MD.render(level_data["c"], True, COLOR_WHITE)
            screen.blit(sp, sp.get_rect(center=(680, level_data["b"])))


class GameState(State):
    """State untuk layar Game utama."""
    def __init__(self, game, game_mode, game_mode_display_text):
        super().__init__(game)
        self.state_name = "game"
        
        """Sebelumnya saya menggunakan variabel dengan nama random sebelum diganti oleh AI."""
        # Variabel 'atur', 'axas', 'kr', 'mulai', 'score', 'stack' lama
        # Sekarang menjadi instance variable milik state ini
        self.game_mode = game_mode
        self.game_mode_display_text = game_mode_display_text
        self.current_soal_list = None
        self.start_time = None
        self.current_score = 0
        self.current_stack = 0

    def handle_specific_event(self, event):
        input_list = self.game.current_input_list # shortcut
        
        # 1. Cek kondisi START GAME
        if event.key == pygame.K_RETURN and not self.start_time:
            input_str = "".join(input_list)
            if self.game_mode == "huruf":
                self.start_time = pygame.time.get_ticks()
                self.current_soal_list = self.choose_random_soal_for_mode(self.game_mode)
            elif input_str == "start" and self.game_mode != "huruf":
                self.start_time = pygame.time.get_ticks()
                self.current_soal_list = self.choose_random_soal_for_mode(self.game_mode)
                self.game.current_input_list = []
            else:
                self.game.show_wrong_input = True
        
        # 2. Cek kondisi INPUT BENAR (saat game berjalan)
        elif input_list == self.current_soal_list and self.start_time:
            if self.game_mode == "huruf":
                self.current_soal_list = self.choose_random_soal_for_mode(self.game_mode)
                self.current_score += 1
                self.game.current_input_list = [] # Mode huruf langsung reset
            elif event.key == pygame.K_RETURN:
                if self.game_mode in ("kata", "frasa"):
                    self.current_soal_list = self.choose_random_soal_for_mode(self.game_mode)
                    self.current_score += 1
                elif self.game_mode == "kalimat":
                    self.current_soal_list = self.choose_random_soal_for_mode(self.game_mode)
                    self.current_stack += 1
                self.game.current_input_list = []

        # 3. Cek kondisi INPUT SALAH (saat game berjalan)
        elif event.key == pygame.K_RETURN and input_list != self.current_soal_list:
            if self.start_time:
                self.game.show_wrong_input = True
        
        # 4. Mode huruf selalu reset input
        if self.game_mode == "huruf" and self.start_time:
             self.game.current_input_list = []

    def update(self):
        """Logika timer dan kondisi akhir game."""
        if self.start_time:
            waktu_game = 45 if self.game_mode == "kalimat" else 30
            waktu_berlalu_detik = (pygame.time.get_ticks() - self.start_time) // 1000
            waktu_tersisa = waktu_game - waktu_berlalu_detik

            waktu_habis = waktu_tersisa <= 0
            
            # Cek kondisi akhir
            if self.game_mode == "kalimat":
                if self.current_stack == 3 or waktu_habis:
                    sisa_waktu_valid = waktu_tersisa if not waktu_habis else 0
                    final_score = sisa_waktu_valid + self.current_stack
                    self.game.switch_state(ResultState(self.game, self.game_mode, final_score))
            elif waktu_habis:
                self.game.switch_state(ResultState(self.game, self.game_mode, self.current_score))

    def draw(self, screen):
        # (Logika dari 'draw_game' dipindah ke sini)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 605, 350, 100), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 0, WIDTH, 255), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (350, 670, 1265, 35), 0)
        
        mode_text = self.game.FONT_LG.render(self.game_mode_display_text, True, COLOR_GREY_LIGHT)
        score_text = self.game.FONT_MD.render(str(self.current_score), True, COLOR_WHITE)
        stack_text = self.game.FONT_MD.render(str(self.current_stack), True, COLOR_WHITE)
        screen.blit(mode_text, mode_text.get_rect(center=(175, 660)))

        if self.start_time:
            waktu_game = 45 if self.game_mode == "kalimat" else 30
            waktu_berlalu_detik = (pygame.time.get_ticks() - self.start_time) // 1000
            waktu_tersisa = waktu_game - waktu_berlalu_detik
            
            # Pastikan timer tidak negatif
            waktu_tampil = max(0, waktu_tersisa)
            timer_text = self.game.FONT_LG.render(str(waktu_tampil), True, COLOR_WHITE)
            screen.blit(timer_text, timer_text.get_rect(center=(1300, 330)))

        if self.game_mode and self.current_soal_list:
            soal_text = "".join(self.current_soal_list)
            screen.blit(self.game.FONT_LG.render(soal_text, True, COLOR_WHITE), (100, 80))
            
            if self.game_mode == "kalimat":
                screen.blit(stack_text, stack_text.get_rect(center=(1340, 689)))
            else:
                screen.blit(score_text, score_text.get_rect(center=(1340, 689)))
        else:
            if self.game_mode == "huruf":
                screen.blit(self.game.FONT_MD.render("Tekan tombol pada keyboard sesuai dengan huruf yang muncul di layar!", True, COLOR_WHITE), (50, 145))
                screen.blit(self.game.FONT_LG.render("Tekan tombol 'Enter' untuk mulai!", True, COLOR_WHITE), (50, 75))
            else:
                screen.blit(self.game.FONT_MD.render("Ketik apa yang muncul di layar lalu tekan 'Enter'!", True, COLOR_WHITE), (50, 145))
                screen.blit(self.game.FONT_LG.render("Ketik 'start' lalu 'Enter' untuk mulai!", True, COLOR_WHITE), (50, 75))


class ResultState(State):
    """State untuk layar Hasil Skor."""
    def __init__(self, game, game_mode, final_score):
        super().__init__(game)
        self.state_name = "result"
        
        self.game_mode = game_mode
        self.final_score = final_score
        
        # Hitung tier & update best score saat state ini dibuat
        self.tier_text, self.tier_color, self.is_best = self.calculate_tier_and_update_score()

    def calculate_tier_and_update_score(self):
        """Menggabungkan logika tier dan update best score."""
        is_best = False
        tier_text = ""
        tier_color = COLOR_GREEN_BRIGHT
        score = self.final_score
        
        if self.game_mode == "huruf":
            if score > self.game.BEST_SCORES["huruf"]["p"]: 
                is_best = True
                self.game.BEST_SCORES["huruf"]["p"] = score
            if score >= 150: tier_text, tier_color = "!Professional!", (255, 255, 0)
            elif score >= 75: tier_text, tier_color = ">Advanced<", (255, 0, 255)
            elif score >= 35: tier_text, tier_color = "+Intermediate+", (0, 200, 200)
            else: tier_text, tier_color = "~Beginner~", (0, 175, 0)
                
        elif self.game_mode == "kata":
            if score > self.game.BEST_SCORES["kata"]["p"]:
                is_best = True
                self.game.BEST_SCORES["kata"]["p"] = score
            if score >= 35: tier_text, tier_color = "!Professional!", (255, 255, 0)
            elif score >= 20: tier_text, tier_color = ">Advanced<", (255, 0, 255)
            elif score >= 10: tier_text, tier_color = "+Intermediate+", (0, 200, 200)
            else: tier_text, tier_color = "~Beginner~", (0, 175, 0)
                
        elif self.game_mode == "frasa":
            if score > self.game.BEST_SCORES["frasa"]["p"]:
                is_best = True
                self.game.BEST_SCORES["frasa"]["p"] = score
            if score >= 20: tier_text, tier_color = "!Professional!", (255, 255, 0)
            elif score >= 12: tier_text, tier_color = ">Advanced<", (255, 0, 255)
            elif score >= 6: tier_text, tier_color = "+Intermediate+", (0, 200, 200)
            else: tier_text, tier_color = "~Beginner~", (0, 175, 0)
                
        elif self.game_mode == "kalimat":
            if score > self.game.BEST_SCORES["kalimat"]["p"]:
                is_best = True
                self.game.BEST_SCORES["kalimat"]["p"] = score
            if score >= 30: tier_text, tier_color = "!Professional!", (255, 255, 0)
            elif score >= 20: tier_text, tier_color = ">Advanced<", (255, 0, 255)
            elif score >= 10: tier_text, tier_color = "+Intermediate+", (0, 200, 200)
            else: tier_text, tier_color = "~Beginner~", (0, 175, 0)

        return tier_text, tier_color, is_best

    def handle_specific_event(self, event):
        if event.key == pygame.K_RETURN:
            input_str = "".join(self.game.current_input_list)
            # Tidak perlu update best score di sini, sudah dilakukan di __init__
            if input_str == "lobby":
                self.game.switch_state(LobbyState(self.game))
            elif input_str == "menu":
                self.game.switch_state(MenuState(self.game))
            else:
                self.game.show_wrong_input = True
                
    def draw(self, screen):
        # (Logika dari 'draw_result' dipindah ke sini)
        xall, yall = 850, 400
        radius_outer, radius_inner = 150, 60
        points = []
        
        for i in range(10):
            angle = -math.pi/2 + i * math.pi/5
            radius = radius_outer if i % 2 == 0 else radius_inner
            x = xall + radius * math.cos(angle)
            y = yall + radius * math.sin(angle)
            points.append((x, y))

        text_your_score = self.game.FONT_LG.render("Your score!", True, COLOR_WHITE)
        text_best_score = self.game.FONT_LG.render("Best score!", True, COLOR_GOLD)
        score_display = self.game.FONT_LG.render(str(self.final_score), True, COLOR_WHITE)

        if self.is_best:
            pygame.draw.polygon(screen, COLOR_GOLD, points)
            screen.blit(text_best_score, text_best_score.get_rect(center=(xall, (yall - 185))))
        else:
            screen.blit(text_your_score, text_your_score.get_rect(center=(xall, (yall - 185))))

        tier_surface = self.game.FONT_MD.render(self.tier_text, True, self.tier_color)
        screen.blit(tier_surface, tier_surface.get_rect(center=(xall, (yall + 150))))

        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 605, 350, 100), 0)
        pygame.draw.rect(screen, COLOR_GREY_MEDIUM, (0, 0, 350, 310), 0)
        pygame.draw.circle(screen, COLOR_BLUE, (xall, yall), 45, 0)
        screen.blit(score_display, score_display.get_rect(center=(xall, yall)))
        screen.blit(self.game.FONT_LG.render("SCORE", True, COLOR_GREY_LIGHT), (50, 625))


# =============================================================================
# Titik Masuk Program
# =============================================================================
if __name__ == "__main__":
    game_app = Game()
    game_app.run()

"""
    Saya harap dengan adanya projek ini maka saya akan lebih dekat dengan dunia programming.
Bukan hanya programmer yang bisa salin tempel, tapi juga programmer yang bisa berpikir
secara komputasional. Saya juga berharap supaya teman-teman sekelas saya (juga saya) dapat
mengasah kemampuan mengetiknya, terutama di era yang serba digital ini.
"""