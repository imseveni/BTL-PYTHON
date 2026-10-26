# PHÂN CÔNG DỰ ÁN SPACE INVADERS BẰNG PYTHON / PYGAME

## 1. Mục tiêu dự án

Nhóm gồm **5 thành viên**, cùng xây dựng một game **Space Invaders** bằng **Python + Pygame**.

Repo tham khảo:

- `attreyabhatt/Space-Invaders-Pygame`

Mục tiêu của nhóm **không phải chỉ clone lại code mẫu**, mà sẽ:

- Giữ gameplay cơ bản của Space Invaders.
- Tổ chức lại code theo hướng rõ ràng, dễ đọc, dễ chia việc.
- Áp dụng OOP ở mức vừa phải.
- Mỗi thành viên có một phần code chính tương đối độc lập.
- Hạn chế nhiều người sửa cùng một file để tránh conflict Git.
- Có một số chức năng mở rộng vừa sức, không quá khó.
- Có thể trình bày rõ vai trò của từng thành viên khi demo hoặc vấn đáp.

---

# 2. Gameplay cơ bản dự kiến

Người chơi điều khiển một phi thuyền ở phía dưới màn hình.

Nhiệm vụ:

- Di chuyển sang trái / phải.
- Bắn đạn lên phía trên.
- Tiêu diệt enemy.
- Nhận điểm khi tiêu diệt enemy.
- Enemy di chuyển qua lại và tiến dần xuống phía dưới.
- Nếu enemy xuống quá thấp hoặc người chơi hết mạng thì Game Over.
- Có nhiều level với độ khó tăng dần.

Điều khiển gợi ý:

| Phím | Chức năng |
|---|---|
| `LEFT` / `A` | Di chuyển trái |
| `RIGHT` / `D` | Di chuyển phải |
| `SPACE` | Bắn |
| `P` | Pause |
| `R` | Restart khi Game Over |
| `ESC` | Thoát |

---

# 3. Nguyên tắc chia việc

Để công bằng, mỗi thành viên đều phải có:

1. **Một module logic chính**
2. **Code OOP**
3. **Kiểm thử module của mình**
4. **Viết tài liệu / README cho phần mình làm**
5. **Tạo branch riêng**
6. **Tạo Pull Request trước khi merge**
7. **Có ít nhất một phần chức năng có thể demo độc lập**

Không chia theo kiểu:

- Một người chỉ làm âm thanh.
- Một người chỉ tìm ảnh.
- Một người làm gần hết gameplay.

Thay vào đó, mỗi người đều phải có phần code đủ lớn để khi giảng viên hỏi có thể tự giải thích.

---

# 4. Cấu trúc project đề xuất

```text
SpaceInvaders/
│
├── main.py
├── game.py
├── config.py
│
├── entities/
│   ├── __init__.py
│   ├── player.py
│   ├── enemy.py
│   ├── bullet.py
│   └── powerup.py
│
├── managers/
│   ├── __init__.py
│   ├── enemy_manager.py
│   ├── bullet_manager.py
│   └── sound_manager.py
│
├── ui/
│   ├── __init__.py
│   ├── menu.py
│   ├── hud.py
│   └── game_over.py
│
├── utils/
│   ├── __init__.py
│   └── collision.py
│
├── data/
│   └── highscore.txt
│
├── assets/
│   ├── images/
│   │   ├── player.png
│   │   ├── enemy.png
│   │   ├── bullet.png
│   │   ├── background.png
│   │   └── ...
│   │
│   └── sounds/
│       ├── background.wav
│       ├── laser.wav
│       ├── explosion.wav
│       └── ...
│
├── requirements.txt
└── README.md
```

Không bắt buộc phải đúng 100% cấu trúc này, nhưng nên giữ nguyên tư tưởng:

> **Mỗi chức năng lớn nằm ở một module riêng, không dồn toàn bộ game vào `main.py`.**

---

# 5. PHÂN CÔNG CHI TIẾT CHO 5 THÀNH VIÊN

---

# THÀNH VIÊN 1 — GAME CORE + GAME STATE + LEVEL SYSTEM

## Vai trò chính

Phụ trách bộ khung của toàn bộ game và là người tích hợp các module.

## File phụ trách chính

```text
main.py
game.py
config.py
```

## Công việc chi tiết

### 1. Khởi tạo game

Thiết lập:

- `pygame.init()`
- Kích thước màn hình
- Caption
- Icon
- FPS
- Clock
- Background cơ bản

Ví dụ:

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
```

Các thông số chung nên đưa vào `config.py`.

---

### 2. Xây dựng class `Game`

Dự kiến:

```python
class Game:
    def __init__(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def reset(self):
        pass

    def run(self):
        pass
```

`main.py` nên càng ngắn càng tốt.

Ví dụ:

```python
from game import Game

game = Game()
game.run()
```

---

### 3. Quản lý trạng thái game

Các trạng thái:

```text
MENU
PLAYING
PAUSED
GAME_OVER
```

Có thể dùng:

```python
self.state = "MENU"
```

Luồng:

```text
MENU
  ↓
PLAYING
  ↓
PAUSED
  ↓
PLAYING
  ↓
GAME_OVER
  ↓
RESTART
```

Người 1 chịu trách nhiệm chuyển trạng thái đúng.

---

### 4. Game Loop

Game Loop phải xử lý theo thứ tự:

```text
Nhận sự kiện
    ↓
Update logic
    ↓
Xử lý collision / trạng thái
    ↓
Vẽ màn hình
    ↓
Update display
```

Ví dụ:

```python
while self.running:
    self.handle_events()
    self.update()
    self.draw()
```

---

### 5. Pause / Resume

Phím gợi ý:

```text
P
```

Khi pause:

- Enemy không di chuyển.
- Bullet không di chuyển.
- Player không di chuyển.
- Hiện chữ `PAUSED`.

---

### 6. Restart game

Khi Game Over:

```text
R → chơi lại
ESC → thoát
```

Restart phải reset:

- Score
- Level
- Player lives
- Player position
- Enemy
- Bullet
- Game state

---

### 7. Level System

Ví dụ:

| Level | Enemy | Speed |
|---|---:|---:|
| 1 | 6 | 2 |
| 2 | 8 | 2.5 |
| 3 | 10 | 3 |
| 4 | 12 | 3.5 |

Có thể tăng level theo:

```text
Score
```

Ví dụ:

```python
level = score // 100 + 1
```

Hoặc:

```text
Tiêu diệt toàn bộ enemy
→ Level mới
```

---

## Người 1 cần phối hợp với ai?

Phải thống nhất interface với tất cả thành viên.

Ví dụ:

```python
player.update()
player.draw(screen)

enemy_manager.update()
enemy_manager.draw(screen)

bullet_manager.update()
bullet_manager.draw(screen)
```

Người 1 **không nên sửa trực tiếp code của thành viên khác**, trừ khi đang xử lý tích hợp sau khi trao đổi.

---

## Tiêu chí hoàn thành

- [ ] Game khởi động được.
- [ ] Game loop ổn định.
- [ ] Có MENU / PLAYING / PAUSED / GAME_OVER.
- [ ] Restart hoạt động.
- [ ] Có ít nhất 3 level.
- [ ] Các module khác được gọi đúng.
- [ ] Không dồn toàn bộ logic vào `main.py`.
- [ ] Có test thủ công các trạng thái game.
- [ ] Có tài liệu mô tả Game Loop.

---

# THÀNH VIÊN 2 — PLAYER SYSTEM + INPUT + LIFE + POWER-UP

## Vai trò chính

Phụ trách toàn bộ logic của người chơi.

## File phụ trách

```text
entities/player.py
entities/powerup.py
```

---

## 1. Xây dựng class `Player`

Dự kiến:

```python
class Player:
    def __init__(self):
        self.x = 370
        self.y = 480
        self.speed = 5
        self.lives = 3

    def update(self):
        pass

    def draw(self, screen):
        pass
```

Thuộc tính gợi ý:

```python
self.image
self.x
self.y
self.speed
self.lives
self.rect
self.has_shield
```

---

## 2. Di chuyển Player

Phím:

```text
LEFT / A
RIGHT / D
```

Player phải:

- Di chuyển mượt.
- Không đi ra ngoài màn hình.
- Dừng khi thả phím.

Ví dụ giới hạn:

```python
self.x = max(0, min(self.x, SCREEN_WIDTH - PLAYER_WIDTH))
```

---

## 3. Input

Có thể viết:

```python
def handle_input(self, keys):
    pass
```

Không nên để toàn bộ logic input của Player nằm trong `game.py`.

---

## 4. Hệ thống mạng sống

Ví dụ:

```python
self.lives = 3
```

Khi bị trúng:

```text
Lives 3
  ↓
Lives 2
  ↓
Lives 1
  ↓
Game Over
```

Cần có:

```python
def take_damage(self):
    pass
```

---

## 5. Trạng thái bất tử ngắn sau khi bị trúng — ý tưởng nên làm

Đây là tính năng không quá khó.

Sau khi mất một mạng:

```text
Player bất tử 1–2 giây
```

Để tránh:

```text
Enemy chạm player
→ mất cả 3 mạng ngay lập tức
```

Có thể dùng thời gian:

```python
pygame.time.get_ticks()
```

---

## 6. Power-up đơn giản

Chỉ cần chọn **1 hoặc 2 loại**, không cần làm quá nhiều.

### Gợi ý 1 — Shield

Nhặt Shield:

```text
Player có khiên
```

Lần tiếp theo bị trúng:

```text
Mất Shield
Không mất mạng
```

---

### Gợi ý 2 — Speed Boost

Trong 5 giây:

```text
speed = 8
```

Sau đó trở về:

```text
speed = 5
```

---

### Gợi ý 3 — Double Shot

Khi bắn:

```text
2 viên đạn
```

thay vì:

```text
1 viên đạn
```

Phần bắn thực tế cần phối hợp với thành viên 4.

---

## 7. Respawn Player

Khi mất mạng:

```text
Đưa Player về vị trí ban đầu
```

Ví dụ:

```python
self.x = SCREEN_WIDTH // 2
```

---

## Tiêu chí hoàn thành

- [ ] Có class `Player`.
- [ ] Di chuyển trái / phải.
- [ ] Không ra ngoài màn hình.
- [ ] Có lives.
- [ ] Có `take_damage()`.
- [ ] Có respawn.
- [ ] Có bất tử tạm thời.
- [ ] Có ít nhất 1 power-up.
- [ ] Có test giới hạn màn hình.
- [ ] Có tài liệu giải thích Player.

---

# THÀNH VIÊN 3 — ENEMY SYSTEM + ENEMY MANAGER + DIFFICULTY

## Vai trò chính

Phụ trách toàn bộ enemy.

## File phụ trách

```text
entities/enemy.py
managers/enemy_manager.py
```

---

## 1. Xây dựng class `Enemy`

Dự kiến:

```python
class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        pass

    def draw(self, screen):
        pass
```

Thuộc tính:

```python
self.image
self.x
self.y
self.speed
self.health
self.score
self.rect
```

---

## 2. Enemy Movement

Gameplay cơ bản:

```text
→ → → → →
          ↓
← ← ← ← ←
↓
→ → → → →
```

Khi enemy chạm biên:

- Đổi hướng.
- Đi xuống một đoạn.

---

## 3. Enemy Manager

Không để `game.py` chứa hàng loạt list riêng lẻ.

Nên có:

```python
class EnemyManager:
    def __init__(self):
        self.enemies = []
```

Các hàm:

```python
spawn_enemies()
update()
draw()
remove_enemy()
reset()
```

---

## 4. Spawn Enemy

Ví dụ tạo theo hàng:

```text
E E E E E E
E E E E E E
```

Có thể dùng vòng lặp:

```python
for row in range(...):
    for col in range(...):
        ...
```

---

## 5. Nhiều loại enemy

Không cần quá phức tạp.

### Normal Enemy

```text
HP: 1
Speed: bình thường
Score: 10
```

### Fast Enemy

```text
HP: 1
Speed: nhanh
Score: 20
```

### Tank Enemy

```text
HP: 2 hoặc 3
Speed: chậm
Score: 30
```

Có thể dùng kế thừa:

```python
class FastEnemy(Enemy):
    pass
```

Nhưng nếu nhóm thấy kế thừa khó, có thể dùng thuộc tính `enemy_type`.

---

## 6. Difficulty tăng theo Level

Ví dụ:

```text
Level cao
→ nhiều enemy hơn
→ enemy nhanh hơn
```

Không nên tăng quá mạnh.

Ví dụ:

```python
speed = 2 + level * 0.3
```

---

## 7. Enemy xuống quá thấp

Nếu:

```python
enemy.y > LIMIT_Y
```

thì báo cho Game:

```text
GAME OVER
```

Hoặc gây damage cho Player tùy cách nhóm thiết kế.

---

## 8. Enemy bắn đạn — ý tưởng mở rộng vừa phải

Có thể làm nếu còn thời gian.

Mỗi khoảng:

```text
1.5 – 3 giây
```

một enemy ngẫu nhiên bắn xuống.

Không cần AI phức tạp.

Chỉ cần:

```python
random.choice(enemies)
```

Sau đó tạo enemy bullet.

Phải phối hợp với thành viên 4.

---

## Tiêu chí hoàn thành

- [ ] Có class `Enemy`.
- [ ] Có `EnemyManager`.
- [ ] Spawn được nhiều enemy.
- [ ] Enemy đổi hướng khi chạm biên.
- [ ] Enemy đi xuống.
- [ ] Có ít nhất 2 loại enemy.
- [ ] Difficulty tăng theo level.
- [ ] Game phát hiện enemy xuống quá thấp.
- [ ] Có test spawn và movement.
- [ ] Có tài liệu giải thích enemy system.

---

# THÀNH VIÊN 4 — BULLET + COMBAT + COLLISION + SCORE

## Vai trò chính

Phụ trách toàn bộ hệ thống chiến đấu.

## File phụ trách

```text
entities/bullet.py
managers/bullet_manager.py
utils/collision.py
```

---

## 1. Xây dựng class `Bullet`

Dự kiến:

```python
class Bullet:
    def __init__(self, x, y, direction=-1):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction

    def update(self):
        self.y += self.speed * self.direction
```

---

## 2. Hỗ trợ nhiều viên đạn

Không sử dụng kiểu:

```python
bullet_state = "ready"
```

cho toàn bộ game.

Nên dùng:

```python
bullets = []
```

Khi bắn:

```python
bullets.append(Bullet(...))
```

---

## 3. Bullet Manager

Dự kiến:

```python
class BulletManager:
    def __init__(self):
        self.bullets = []

    def shoot(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def remove_outside_bullets(self):
        pass
```

---

## 4. Giới hạn tốc độ bắn

Nếu giữ `SPACE`, không nên bắn hàng trăm viên mỗi giây.

Có thể dùng cooldown:

```text
300 ms / viên
```

Ví dụ:

```python
shoot_cooldown = 300
```

---

## 5. Collision

Nên dùng:

```python
pygame.Rect
```

Ví dụ:

```python
if bullet.rect.colliderect(enemy.rect):
    ...
```

Các collision cần xử lý:

```text
Player Bullet ↔ Enemy
Enemy ↔ Player
Enemy Bullet ↔ Player
Power-up ↔ Player
```

Tùy feature thực tế mà triển khai.

---

## 6. Damage

Ví dụ:

```python
enemy.health -= bullet.damage
```

Nếu:

```python
enemy.health <= 0
```

thì:

- Xóa enemy.
- Cộng điểm.
- Phát explosion.
- Có thể random rơi power-up.

---

## 7. Score System

Gợi ý:

| Enemy | Điểm |
|---|---:|
| Normal | 10 |
| Fast | 20 |
| Tank | 30 |

Không hard-code quá nhiều nơi.

Nên để:

```python
enemy.score
```

Sau đó:

```python
score += enemy.score
```

---

## 8. Combo — ý tưởng mở rộng vừa phải

Ví dụ:

```text
Tiêu diệt liên tục trong thời gian ngắn
→ Combo x2
```

Có thể đơn giản:

```text
3 enemy liên tục
→ +10 bonus
```

Nếu thấy khó có thể bỏ.

---

## 9. Explosion effect đơn giản

Không nhất thiết phải animation phức tạp.

Có thể:

- Hiện ảnh explosion trong thời gian ngắn.
- Hoặc chỉ phát sound + hiệu ứng nhỏ.

---

## Tiêu chí hoàn thành

- [ ] Có class `Bullet`.
- [ ] Bắn nhiều bullet.
- [ ] Có cooldown.
- [ ] Bullet bị xóa khi ra màn hình.
- [ ] Collision chính xác.
- [ ] Enemy mất HP.
- [ ] Enemy chết được.
- [ ] Score hoạt động.
- [ ] Có test collision.
- [ ] Có tài liệu giải thích combat.

---

# THÀNH VIÊN 5 — UI + HUD + SOUND + HIGH SCORE

## Vai trò chính

Phụ trách trải nghiệm người dùng và dữ liệu điểm cao.

## File phụ trách

```text
ui/menu.py
ui/hud.py
ui/game_over.py
managers/sound_manager.py
data/highscore.txt
```

---

## 1. Main Menu

Menu tối thiểu:

```text
SPACE INVADERS

PLAY
HIGH SCORE
QUIT
```

Có thể điều khiển bằng:

```text
↑
↓
ENTER
```

Nếu làm button chuột phức tạp thì không bắt buộc.

---

## 2. HUD trong game

Hiển thị:

```text
Score
Lives
Level
```

Ví dụ:

```text
Score: 150        Lives: 2        Level: 3
```

---

## 3. Pause UI

Khi pause:

```text
PAUSED

Press P to continue
```

---

## 4. Game Over UI

Hiển thị:

```text
GAME OVER

Score: 250
High Score: 600

R - Restart
ESC - Exit
```

---

## 5. Sound Manager

Không nên gọi:

```python
pygame.mixer.Sound(...)
```

ở nhiều file.

Nên gom vào:

```python
class SoundManager:
    def play_shoot(self):
        pass

    def play_explosion(self):
        pass

    def play_music(self):
        pass

    def stop_music(self):
        pass
```

---

## 6. Âm thanh cần có

Tối thiểu:

```text
Background Music
Shoot
Explosion
```

Có thể thêm:

```text
Game Over
Power-up
Button Select
```

nếu còn thời gian.

---

## 7. High Score

Lưu high score bằng file:

```text
data/highscore.txt
```

Đọc:

```python
with open("data/highscore.txt", "r") as f:
    high_score = int(f.read())
```

Ghi:

```python
with open("data/highscore.txt", "w") as f:
    f.write(str(high_score))
```

Phải xử lý trường hợp:

```text
File chưa tồn tại
File rỗng
```

---

## 8. Có thể thêm Settings nhỏ

Nếu còn thời gian:

```text
Music: ON / OFF
Sound: ON / OFF
```

Không cần làm menu settings quá phức tạp.

---

## Tiêu chí hoàn thành

- [ ] Có Main Menu.
- [ ] Có HUD.
- [ ] Có Pause UI.
- [ ] Có Game Over UI.
- [ ] Sound Manager hoạt động.
- [ ] Có background music.
- [ ] Có shoot/explosion sound.
- [ ] High Score được lưu.
- [ ] High Score vẫn còn sau khi tắt game.
- [ ] Có tài liệu giải thích UI + file I/O.

---

# 6. BẢNG TỔNG HỢP PHÂN CÔNG

| Thành viên | Module | Chức năng chính | Branch |
|---|---|---|---|
| Người 1 | Game Core | Game Loop, State, Level, Restart, Integration | `feature/game-core` |
| Người 2 | Player | Movement, Input, Lives, Respawn, Power-up | `feature/player` |
| Người 3 | Enemy | Enemy, Spawn, Movement, Difficulty | `feature/enemy` |
| Người 4 | Combat | Bullet, Collision, Damage, Score | `feature/combat` |
| Người 5 | UI/System | Menu, HUD, Sound, High Score | `feature/ui-system` |

---

# 7. CÁC INTERFACE CẦN THỐNG NHẤT TRƯỚC KHI CODE

Đây là phần rất quan trọng.

Các thành viên cần thống nhất tên hàm trước để code song song.

---

## Player

Nên có:

```python
player.update()
player.draw(screen)
player.take_damage()
player.reset()
```

Thuộc tính tối thiểu:

```python
player.rect
player.lives
player.x
player.y
```

---

## Enemy

Nên có:

```python
enemy.update()
enemy.draw(screen)
enemy.take_damage(damage)
```

Thuộc tính:

```python
enemy.rect
enemy.health
enemy.score
```

---

## Enemy Manager

Nên có:

```python
enemy_manager.spawn_enemies()
enemy_manager.update()
enemy_manager.draw(screen)
enemy_manager.reset()
```

---

## Bullet Manager

Nên có:

```python
bullet_manager.shoot(x, y)
bullet_manager.update()
bullet_manager.draw(screen)
bullet_manager.reset()
```

---

## Sound Manager

Nên có:

```python
sound_manager.play_shoot()
sound_manager.play_explosion()
sound_manager.play_music()
```

---

## UI

Nên có:

```python
hud.draw(screen, score, lives, level)
menu.draw(screen)
game_over.draw(screen, score, high_score)
```

---

# 8. CÁC Ý TƯỞNG MỞ RỘNG PHÙ HỢP, KHÔNG QUÁ KHÓ

Không cần làm tất cả.

Nên chọn khoảng **3–5 ý tưởng**.

---

## Ý tưởng 1 — Nhiều Level

Độ khó:

```text
Dễ
```

Mỗi level:

```text
Enemy nhiều hơn
Enemy nhanh hơn
```

Đây là feature rất nên làm.

---

## Ý tưởng 2 — Nhiều loại Enemy

Độ khó:

```text
Dễ → Trung bình
```

Ví dụ:

```text
Normal
Fast
Tank
```

Khác nhau về:

```text
HP
Speed
Score
```

---

## Ý tưởng 3 — Player có 3 mạng

Độ khó:

```text
Dễ
```

Hiển thị:

```text
Lives: 3
```

Khi mất hết:

```text
GAME OVER
```

---

## Ý tưởng 4 — Shield Power-up

Độ khó:

```text
Trung bình
```

Enemy chết có xác suất:

```text
10%
```

rơi Shield.

Player nhặt:

```text
Chặn 1 lần damage
```

---

## Ý tưởng 5 — Speed Boost

Độ khó:

```text
Trung bình
```

Nhặt power-up:

```text
Player chạy nhanh hơn 5 giây
```

---

## Ý tưởng 6 — Double Shot

Độ khó:

```text
Trung bình
```

Thay vì:

```text
    |
    |
```

bắn:

```text
|       |
|       |
```

trong một khoảng thời gian.

---

## Ý tưởng 7 — Enemy bắn lại

Độ khó:

```text
Trung bình
```

Một enemy ngẫu nhiên:

```text
↓ bắn xuống
```

Player phải né.

---

## Ý tưởng 8 — High Score

Độ khó:

```text
Dễ
```

Dùng file:

```text
highscore.txt
```

Ưu điểm:

- Có File I/O.
- Dễ trình bày.
- Game thú vị hơn.

---

## Ý tưởng 9 — Pause

Độ khó:

```text
Dễ
```

Nhấn:

```text
P
```

Game dừng.

---

## Ý tưởng 10 — Màn hình Menu

Độ khó:

```text
Dễ → Trung bình
```

```text
PLAY
HIGH SCORE
QUIT
```

---

## Ý tưởng 11 — Boss đơn giản

Độ khó:

```text
Trung bình
```

Không cần AI phức tạp.

Ví dụ Level 5:

```text
BOSS

HP: 20
Di chuyển trái / phải
```

Boss có thể bắn chậm.

Nếu nhóm thiếu thời gian thì bỏ feature này.

---

## Ý tưởng 12 — Random Background

Độ khó:

```text
Dễ
```

Mỗi level đổi background hoặc màu nền.

---

## Ý tưởng 13 — Combo Score

Độ khó:

```text
Trung bình
```

Ví dụ:

```text
3 enemy liên tục
→ BONUS +20
```

---

## Ý tưởng 14 — Difficulty Selection

Độ khó:

```text
Dễ → Trung bình
```

Menu:

```text
EASY
NORMAL
HARD
```

Khác nhau về:

```text
Enemy Speed
Enemy Count
Lives
```

---

# 9. FEATURE NÊN CHỌN CHO PHIÊN BẢN ĐẦU

Để tránh dự án quá lớn, phiên bản đầu chỉ cần:

```text
Player Movement
Shooting
Enemy Movement
Collision
Score
3 Lives
Game Over
Restart
3 Levels
Main Menu
Sound
High Score
```

Sau khi tất cả chạy ổn mới làm thêm.

---

# 10. FEATURE NÊN LÀM THÊM NẾU CÒN THỜI GIAN

Ưu tiên theo thứ tự:

```text
1. Shield
2. Multiple Enemy Types
3. Enemy Shooting
4. Double Shot
5. Boss
```

Không nên làm Boss trước khi gameplay cơ bản ổn định.

---

# 11. GIT WORKFLOW CHO NHÓM

## Branch chính

```text
main
```

Chỉ chứa code:

```text
đã test
đã review
chạy được
```

Không code trực tiếp trên `main`.

---

## Branch từng người

```text
feature/game-core
feature/player
feature/enemy
feature/combat
feature/ui-system
```

---

# 12. QUY TRÌNH CODE

Ví dụ thành viên Player:

```bash
git checkout main
git pull origin main
```

Tạo branch:

```bash
git checkout -b feature/player
```

Sau khi code:

```bash
git add .
git commit -m "feat: implement player movement"
git push origin feature/player
```

Sau đó tạo:

```text
Pull Request
```

từ:

```text
feature/player
```

vào:

```text
main
```

---

# 13. QUY TẮC COMMIT

Không nên:

```text
update
fix
code moi
sua code
abc
```

Nên:

```text
feat: implement player movement
feat: add enemy manager
feat: add multiple bullets
fix: prevent player moving outside screen
fix: remove bullet after leaving screen
docs: add enemy module documentation
refactor: move sound logic to sound manager
```

---

# 14. QUY TẮC PULL REQUEST

Trong Pull Request ghi:

```text
## Chức năng

- Thêm Player class
- Thêm movement
- Thêm boundary check

## Đã test

- LEFT
- RIGHT
- Border left
- Border right

## File thay đổi

- entities/player.py
```

Không merge nếu:

```text
Game không chạy
Có conflict chưa xử lý
Code chưa test
```

---

# 15. CÁCH HẠN CHẾ CONFLICT

Không để nhiều người cùng sửa:

```text
main.py
game.py
```

trong thời gian dài.

Ví dụ:

```text
Người 2 → player.py
Người 3 → enemy.py
Người 4 → bullet.py
```

Người 1 chỉ kết nối sau.

Nếu cần sửa file người khác:

```text
Trao đổi trước
```

Không tự ý sửa rồi push.

---

# 16. CHECKLIST TRƯỚC KHI MERGE

Mỗi thành viên tự kiểm tra:

- [ ] Code chạy không lỗi.
- [ ] Không còn `print()` debug không cần thiết.
- [ ] Không dùng đường dẫn tuyệt đối.
- [ ] Không hard-code asset sai thư mục.
- [ ] Không commit file rác.
- [ ] Đã test chức năng chính.
- [ ] Đã cập nhật tài liệu.
- [ ] Đã pull `main` mới nhất.
- [ ] Không còn conflict.

---

# 17. QUY ƯỚC CODE

## Tên class

```python
Player
Enemy
Bullet
Game
EnemyManager
SoundManager
```

---

## Tên hàm / biến

Dùng:

```python
snake_case
```

Ví dụ:

```python
player_speed
enemy_count
shoot_bullet()
check_collision()
```

---

## Không nên

```python
a
b
x1
tmp2
abc
```

trừ biến vòng lặp đơn giản.

---

# 18. QUẢN LÝ ASSET

Không để:

```text
player.png
enemy.png
laser.wav
```

lẫn với file Python ở thư mục gốc.

Nên:

```text
assets/images/
assets/sounds/
```

Ví dụ:

```python
pygame.image.load("assets/images/player.png")
```

---

# 19. REQUIREMENTS.TXT

Tạo:

```text
requirements.txt
```

Nội dung:

```text
pygame
```

Cài bằng:

```bash
pip install -r requirements.txt
```

---

# 20. KẾ HOẠCH LÀM THEO GIAI ĐOẠN

## Giai đoạn 1 — Khung game

Mục tiêu:

- Cửa sổ game chạy.
- Các class được tạo.
- Import giữa các module không lỗi.

Người 1 làm:

```text
Game Core
```

Các thành viên khác tạo skeleton module.

Ví dụ:

```python
class Player:
    def update(self):
        pass
```

---

## Giai đoạn 2 — Gameplay cơ bản

Hoàn thành:

```text
Player movement
Enemy movement
Bullet
Collision
Score
```

Kết thúc giai đoạn này:

> Game phải chơi được dù chưa đẹp.

---

## Giai đoạn 3 — Hệ thống game

Thêm:

```text
Lives
Level
Game Over
Restart
Menu
High Score
Sound
```

---

## Giai đoạn 4 — Feature mở rộng

Chọn:

```text
Shield
Enemy Type
Enemy Shooting
Double Shot
Boss
```

---

## Giai đoạn 5 — Hoàn thiện

Cả nhóm:

- Test game.
- Sửa bug.
- Cân bằng tốc độ.
- Kiểm tra asset.
- Hoàn thiện README.
- Chuẩn bị demo.
- Chuẩn bị câu hỏi vấn đáp.

---

# 21. ĐỀ XUẤT MỐC HOÀN THÀNH

Có thể chia theo buổi / tuần.

## Mốc 1

Hoàn thành skeleton:

```text
main.py
game.py
player.py
enemy.py
bullet.py
```

---

## Mốc 2

Game chơi được:

```text
Player
Enemy
Shoot
Collision
Score
```

---

## Mốc 3

Game hoàn chỉnh:

```text
Lives
Level
Menu
Game Over
Restart
Sound
High Score
```

---

## Mốc 4

Thêm feature:

```text
Power-up
Enemy Type
Enemy Shooting
...
```

---

# 22. CÁCH TEST TỪNG MODULE

## Player

Test:

```text
Đi trái
Đi phải
Chạm biên
Mất mạng
Respawn
```

---

## Enemy

Test:

```text
Spawn đủ số lượng
Chạm biên
Đổi hướng
Đi xuống
Tăng speed
```

---

## Bullet

Test:

```text
Bắn
Cooldown
Ra khỏi màn hình
Trúng enemy
Không trúng enemy
```

---

## UI

Test:

```text
Menu
Pause
Score
Lives
Game Over
Restart
```

---

## High Score

Test:

```text
Không có file
Có file
Score mới thấp hơn
Score mới cao hơn
Restart game
Tắt game rồi mở lại
```

---

# 23. PHẦN MỖI THÀNH VIÊN PHẢI VIẾT TRONG README / BÁO CÁO

Mỗi thành viên chuẩn bị tối thiểu:

```text
1. Module của mình làm gì?
2. Class chính là gì?
3. Các thuộc tính chính?
4. Các hàm chính?
5. Luồng xử lý?
6. Khó khăn gặp phải?
7. Cách test?
8. Đóng góp cá nhân?
```

---

# 24. GỢI Ý CÂU HỎI VẤN ĐÁP

## Người 1

- Game Loop là gì?
- `pygame.event.get()` dùng để làm gì?
- Tại sao phải giới hạn FPS?
- State game hoạt động thế nào?
- Restart reset những gì?

---

## Người 2

- Player được di chuyển như thế nào?
- Tại sao phải giới hạn tọa độ?
- `pygame.Rect` dùng để làm gì?
- Lives được quản lý ra sao?
- Power-up hoạt động như thế nào?

---

## Người 3

- Enemy đổi hướng bằng cách nào?
- Vì sao cần Enemy Manager?
- Spawn enemy như thế nào?
- Difficulty tăng theo level ra sao?
- Khác biệt giữa các enemy type?

---

## Người 4

- Bullet được lưu ở đâu?
- Tại sao dùng list bullet?
- Collision được kiểm tra ra sao?
- Cooldown để làm gì?
- Score cập nhật ở đâu?

---

## Người 5

- HUD là gì?
- `pygame.font` dùng như thế nào?
- `pygame.mixer` dùng làm gì?
- High score được lưu ra sao?
- Nếu file high score không tồn tại thì xử lý thế nào?

---

# 25. DEFINITION OF DONE — KHI NÀO DỰ ÁN ĐƯỢC COI LÀ HOÀN THÀNH?

Dự án được xem là hoàn thành khi:

- [ ] Game chạy được bằng `python main.py`.
- [ ] Không crash trong gameplay bình thường.
- [ ] Player di chuyển được.
- [ ] Player bắn được.
- [ ] Enemy di chuyển được.
- [ ] Bullet giết được enemy.
- [ ] Có Score.
- [ ] Có Lives.
- [ ] Có Game Over.
- [ ] Có Restart.
- [ ] Có ít nhất 3 Level.
- [ ] Có Main Menu.
- [ ] Có Sound.
- [ ] Có High Score.
- [ ] Có ít nhất 2–3 feature mở rộng.
- [ ] Code được chia module rõ ràng.
- [ ] Mỗi thành viên có branch / commit riêng.
- [ ] README đầy đủ.
- [ ] Cả 5 thành viên đều giải thích được phần mình làm.

---

# 26. PHƯƠNG ÁN FEATURE ĐƯỢC KHUYẾN NGHỊ

Nếu nhóm muốn một bản vừa đẹp vừa không quá khó, đề xuất:

## Bắt buộc

```text
Player Movement
Multiple Bullets
Enemy Movement
Collision
Score
3 Lives
Level System
Pause
Restart
Main Menu
Game Over
Sound
High Score
```

## Làm thêm

```text
Normal Enemy
Fast Enemy
Tank Enemy
Shield Power-up
Enemy Shooting
```

## Nếu còn nhiều thời gian

```text
Double Shot
Boss
Difficulty Selection
Combo
```

---

# 27. LƯU Ý QUAN TRỌNG

Không nên cố làm quá nhiều feature ngay từ đầu.

Thứ tự đúng nên là:

```text
Game chạy được
      ↓
Gameplay cơ bản ổn
      ↓
Code rõ ràng
      ↓
Ít bug
      ↓
Sau đó mới thêm feature
```

Một game có:

```text
10 feature nhưng nhiều bug
```

sẽ kém hơn một game có:

```text
5 feature nhưng chạy ổn định
```

---

# 28. MỤC TIÊU CUỐI CÙNG CỦA NHÓM

Sản phẩm cuối không chỉ cần "chạy được", mà phải thể hiện được:

- Biết sử dụng Python.
- Biết sử dụng Pygame.
- Biết chia class / module.
- Biết xử lý event.
- Biết collision.
- Biết quản lý object bằng list.
- Biết đọc / ghi file.
- Biết làm việc nhóm với Git.
- Biết chia branch.
- Biết tạo Pull Request.
- Biết giải thích phần code của bản thân.

Đây cũng là lý do dự án được chia thành 5 module lớn thay vì cả nhóm cùng sửa một file `main.py`.
