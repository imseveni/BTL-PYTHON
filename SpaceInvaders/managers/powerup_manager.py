from entities.powerup import PowerUp
from config import SCREEN_HEIGHT


class PowerUpManager:
    def __init__(self):

        self.powerups = []

    def spawn(
        self,
        image,
        x,
        y,
        power_type,
        speed=3
    ):

        powerup = PowerUp(
            image=image,
            x=x,
            y=y,
            power_type=power_type,
            speed=speed
        )

        self.powerups.append(
            powerup
        )

        return powerup

    def add(self, powerup):

        self.powerups.append(
            powerup
        )

    def update(self):

        for powerup in self.powerups:

            powerup.update()

        self.powerups = [
            powerup
            for powerup in self.powerups
            if not powerup.is_outside(
                SCREEN_HEIGHT
            )
        ]

    def draw(self, screen):

        for powerup in self.powerups:

            powerup.draw(
                screen
            )

    def remove(self, powerup):

        if powerup in self.powerups:

            self.powerups.remove(
                powerup
            )

    def reset(self):

        self.powerups.clear()