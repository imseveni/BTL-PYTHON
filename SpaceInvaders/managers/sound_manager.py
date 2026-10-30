from pygame import mixer

from config import (
    BACKGROUND_SOUND,
    LASER_SOUND,
    EXPLOSION_SOUND
)


class SoundManager:
    def __init__(self):

        self.shoot_sound = mixer.Sound(
            str(LASER_SOUND)
        )

        self.explosion_sound = mixer.Sound(
            str(EXPLOSION_SOUND)
        )

    # ==================================================
    # MUSIC
    # ==================================================

    def play_music(self):

        mixer.music.load(
            str(BACKGROUND_SOUND)
        )

        mixer.music.play(-1)

    # ==================================================
    # SHOOT
    # ==================================================

    def play_shoot(self):

        self.shoot_sound.play()

    # ==================================================
    # EXPLOSION
    # ==================================================

    def play_explosion(self):

        self.explosion_sound.play()

    # ==================================================
    # STOP MUSIC
    # ==================================================

    def stop_music(self):

        mixer.music.stop()