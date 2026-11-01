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

# Player
PLAYER_IMAGE = IMAGES_DIR / "player_new.png"
PLAYER_DEFENSE_IMAGE = IMAGES_DIR / "player_defense.png"

# Enemy
NORMAL_ENEMY_IMAGE = IMAGES_DIR / "enemy_normal.png"
FAST_ENEMY_IMAGE = IMAGES_DIR / "enemy_fast.png"
TANK_ENEMY_IMAGE = IMAGES_DIR / "enemy_tank.png"

# Bullet
BULLET_IMAGE = IMAGES_DIR / "bullet.png"

# PowerUp
HEALTH_POWERUP_IMAGE = IMAGES_DIR / "health.png"
SHIELD_POWERUP_IMAGE = IMAGES_DIR / "shield.png"

# HUD
HEART_IMAGE = IMAGES_DIR / "heart_full.png"

# Icon
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

LEVEL_SCORE_STEP = 100


# ==================================================
# PLAYER
# ==================================================

PLAYER_SPEED = 5
PLAYER_LIVES = 3

PLAYER_START_X = 370
PLAYER_START_Y = 480

# milliseconds
PLAYER_INVINCIBLE_TIME = 1200

# Shield tồn tại 10 giây
PLAYER_DEFENSE_TIME = 5000


# ==================================================
# ENEMY - GENERAL
# ==================================================

ENEMY_COUNT = 5

ENEMY_SPEED = 4

ENEMY_DROP_DISTANCE = 40

ENEMY_MIN_Y = 50
ENEMY_MAX_Y = 150

GAME_OVER_Y = 440


# ==================================================
# ENEMY - DIFFICULTY
# ==================================================

MAX_ENEMIES = 10

# Mỗi level tăng tốc độ cơ bản
ENEMY_SPEED_INCREASE_PER_LEVEL = 0.4

# Mỗi level tăng thêm số lượng Enemy
ENEMY_COUNT_INCREASE_PER_LEVEL = 1


# ==================================================
# ENEMY - NORMAL
# ==================================================

NORMAL_ENEMY_SCORE = 10


# ==================================================
# ENEMY - FAST
# ==================================================

FAST_ENEMY_SCORE = 20

FAST_ENEMY_SPEED_MULTIPLIER = 1.35


# ==================================================
# ENEMY - TANK
# ==================================================

TANK_ENEMY_SCORE = 30

TANK_ENEMY_SPEED_MULTIPLIER = 0.75

TANK_ENEMY_HEALTH = 3


# ==================================================
# BULLET
# ==================================================

BULLET_SPEED = 10

SHOOT_COOLDOWN = 300

# ==================================================
# ENEMY BULLET
# ==================================================

ENEMY_BULLET_SPEED = 5

# Khoảng thời gian giữa 2 lần Enemy bắn
ENEMY_SHOOT_COOLDOWN = 1000

# Số đạn Enemy tối đa cùng tồn tại
MAX_ENEMY_BULLETS = 3

# ==================================================
# COLORS
# ==================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)