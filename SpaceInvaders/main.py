import sys

import pygame

from game import Game


def main():
    pygame.init()

    try:
        game = Game()

        game.run()

    except FileNotFoundError as error:

        # Thiếu ảnh / âm thanh trong thư mục assets/
        print(
            f"Không tìm thấy file asset: {error.filename}\n"
            "Hãy kiểm tra thư mục assets/images và assets/sounds "
            "(xem đường dẫn trong config.py)."
        )

        sys.exit(1)

    finally:

        pygame.quit()


if __name__ == "__main__":
    main()
