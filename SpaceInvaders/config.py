from pathlib import Path


# ==================================================
# PATH
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

HIGH_SCORE_FILE = DATA_DIR / "highscore.txt"


# ==================================================
# IMAGE PATH
# ==================================================

BACKGROUND_IMAGE = IMAGES_DIR / "background.png"
PLAYER_IMAGE = IMAGES_DIR / "player.png"
ENEMY_IMAGE = IMAGES_DIR / "enemy.png"
BULLET_IMAGE = IMAGES_DIR / "bullet.png"
ICON_IMAGE = IMAGES_DIR / "ufo.png"


# ==================================================
# SOUND PATH
# ==================================================

BACKGROUND_SOUND = SOUNDS_DIR / "background.wav"
LASER_SOUND = SOUNDS_DIR / "laser.wav"
EXPLOSION_SOUND = SOUNDS_DIR / "explosion.wav"


# ==================================================
# SCREEN
# ==================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60


# ==================================================
# GAME STATE
# ==================================================

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
STATE_HIGH_SCORE = "HIGH_SCORE"


# ==================================================
# LEVEL
# ==================================================

# Mỗi 100 điểm tăng 1 level
LEVEL_SCORE_STEP = 100


# ==================================================
# PLAYER
# ==================================================

PLAYER_SPEED = 5
PLAYER_LIVES = 3

PLAYER_START_X = 370
PLAYER_START_Y = 480

# Thời gian bất tử sau khi mất máu (milliseconds)
PLAYER_INVINCIBLE_TIME = 1200


# ==================================================
# ENEMY
# ==================================================

ENEMY_COUNT = 6

ENEMY_SPEED = 4
ENEMY_DROP_DISTANCE = 40

ENEMY_MIN_Y = 50
ENEMY_MAX_Y = 150

GAME_OVER_Y = 440


# ==================================================
# BULLET
# ==================================================

BULLET_SPEED = 10

# Thời gian giữa 2 lần bắn (milliseconds)
SHOOT_COOLDOWN = 300


# ==================================================
# SCORE
# ==================================================

NORMAL_ENEMY_SCORE = 10


# ==================================================
# COLORS
# ==================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)