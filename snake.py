import tkinter as tk
from tkinter import messagebox
import random

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
MOVE_DELAY = 120

COLORS = {
    "Стандартный": "green",
    "Инь": "black",
    "Янь": "white",
    "Инь-Янь": ["black", "white"],
}

score = 0
unlocked_skins = {"Стандартный": True, "Инь": False, "Янь": False, "Инь-Янь": False}
selected_skin = "Стандартный"

snake = []
snake_dir = "Right"
food = None
game_running = False

root = tk.Tk()
root.title("Змейка")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

buttons = []

def draw_checkered_background():
    canvas.delete("bg")
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, WIDTH, BLOCK_SIZE):
            fill = "#FFEBCC" if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0 else "#FFD699"
            canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE, fill=fill, outline="", tags="bg")

def clear_buttons():
    global buttons
    for btn in buttons:
        canvas.delete(btn)
    buttons = []

def show_main_menu():
    canvas.delete("all")
    draw_checkered_background()
    clear_buttons()
    draw_score()

    def btn(text, y, cmd):
        b = canvas.create_rectangle(200, y, 400, y+40, fill="lightgray", tags="button")
        t = canvas.create_text(300, y+20, text=text, fill="black", font=("Arial", 14), tags="button")
        canvas.tag_bind(b, "<Button-1>", lambda e: cmd())
        canvas.tag_bind(t, "<Button-1>", lambda e: cmd())
        buttons.extend([b, t])

    btn("Играть", 100, start_game)
    btn("Магазин", 160, show_shop)
    btn("Выбор цвета", 220, show_color_select)
    btn("Достижения", 280, show_achievements)

def draw_score():
    canvas.delete("score")
    canvas.create_text(10, 10, anchor="nw", text=f"Очки: {score}", font=("Arial", 12, "bold"), tags="score")

def show_shop():
    canvas.delete("all")
    draw_checkered_background()
    clear_buttons()
    draw_score()

    canvas.create_text(300, 30, text="🛍 Магазин", font=("Arial", 18, "bold"))

    def buy(skin, cost):
        global score
        if unlocked_skins[skin]:
            messagebox.showinfo("Магазин", f"{skin} уже куплен.")
            return
        if score >= cost:
            score -= cost
            unlocked_skins[skin] = True
            messagebox.showinfo("Магазин", f"{skin} разблокирован!")
            show_shop()
        else:
            messagebox.showwarning("Магазин", "Недостаточно очков!")

    def btn(text, y, command):
        b = canvas.create_rectangle(180, y, 420, y+35, fill="lightgray", tags="button")
        t = canvas.create_text(300, y+17, text=text, fill="black", tags="button")
        canvas.tag_bind(b, "<Button-1>", lambda e: command())
        canvas.tag_bind(t, "<Button-1>", lambda e: command())
        buttons.extend([b, t])

    btn("Купить Инь (50)", 80, lambda: buy("Инь", 50))
    btn("Купить Янь (50)", 125, lambda: buy("Янь", 50))

    cond_yin = "✅" if unlocked_skins["Инь"] else "❌"
    cond_yang = "✅" if unlocked_skins["Янь"] else "❌"

    canvas.create_text(300, 180, text=f"Купить Инь-Янь (150)", font=("Arial", 12))
    canvas.create_text(300, 205, text=f"Условие: Инь {cond_yin}, Янь {cond_yang}", font=("Arial", 10))
    btn("Купить Инь-Янь", 230, lambda: buy("Инь-Янь", 150) if unlocked_skins["Инь"] and unlocked_skins["Янь"] else messagebox.showwarning("Магазин", "Сначала купи Инь и Янь!"))

    btn("Назад", 300, show_main_menu)

def show_color_select():
    canvas.delete("all")
    draw_checkered_background()
    clear_buttons()
    draw_score()

    canvas.create_text(300, 30, text="🎨 Выбор цвета", font=("Arial", 18, "bold"))

    def btn(skin, y):
        status = "✅" if unlocked_skins[skin] else "❌ Заблокирован"
        b = canvas.create_rectangle(180, y, 420, y+35, fill="lightgray", tags="button")
        t = canvas.create_text(300, y+17, text=f"{skin} ({status})", fill="black", tags="button")

        def select():
            global selected_skin
            if unlocked_skins[skin]:
                selected_skin = skin
                messagebox.showinfo("Выбор цвета", f"{skin} выбран!")
            else:
                messagebox.showwarning("Выбор цвета", f"{skin} ещё не разблокирован.")

        canvas.tag_bind(b, "<Button-1>", lambda e: select())
        canvas.tag_bind(t, "<Button-1>", lambda e: select())
        buttons.extend([b, t])

    y = 80
    for skin in COLORS:
        btn(skin, y)
        y += 45

    btn("Назад", y + 10, show_main_menu)

def show_achievements():
    messagebox.showinfo("Достижения", "Пока нет достижений...")

def start_game():
    global snake, food, snake_dir, game_running
    canvas.delete("all")
    draw_checkered_background()
    clear_buttons()
    draw_score()
    snake.clear()
    snake.append([100, 100])
    snake_dir = "Right"
    spawn_food()
    game_running = True
    move_snake()

def spawn_food():
    global food
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if [x, y] not in snake:
            food = [x, y]
            break

def move_snake():
    global score, game_running
    if not game_running:
        return

    head = snake[-1]
    dx, dy = 0, 0
    if snake_dir == "Up": dy = -BLOCK_SIZE
    elif snake_dir == "Down": dy = BLOCK_SIZE
    elif snake_dir == "Left": dx = -BLOCK_SIZE
    elif snake_dir == "Right": dx = BLOCK_SIZE

    new_head = [head[0] + dx, head[1] + dy]

    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        game_running = False
        show_main_menu()
        return

    snake.append(new_head)

    if new_head == food:
        score += 1
        spawn_food()
    else:
        snake.pop(0)

    canvas.delete("snake")
    draw_checkered_background()
    draw_score()
    canvas.create_rectangle(food[0], food[1], food[0]+BLOCK_SIZE, food[1]+BLOCK_SIZE, fill="red", tag="snake")

    for i, segment in enumerate(snake):
        color = COLORS[selected_skin][i % 2] if selected_skin == "Инь-Янь" else COLORS[selected_skin]
        canvas.create_rectangle(segment[0], segment[1], segment[0]+BLOCK_SIZE, segment[1]+BLOCK_SIZE, fill=color, tag="snake")

    root.after(MOVE_DELAY, move_snake)

def change_dir(event):
    global snake_dir
    key = event.keysym
    if key in ["Up", "Down", "Left", "Right"]:
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if snake_dir != opposites[key]:
            snake_dir = key

root.bind("<KeyPress>", change_dir)
show_main_menu()
root.mainloop()
