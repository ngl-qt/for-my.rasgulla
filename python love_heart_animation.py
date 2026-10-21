import tkinter as tk
import math
import random

# Window
root = tk.Tk()
root.title("Love Heart Animation")
root.geometry("700x750")
root.configure(bg="#08030d")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=680,
    height=650,
    bg="#08030d",
    highlightthickness=0
)
canvas.pack(pady=10)

canvas.create_text(
    340, 35,
    text="LOVE HEART ANIMATION",
    fill="#ff9edb",
    font=("Arial", 23, "bold")
)
canvas.create_text(
    340, 75,
    text="MADE WITH LOVE",
    fill="#bd77b5",
    font=("Arial", 11)
)

# Heart curve
def heart(t, size=15):
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return 340 + x * size, 340 - y * size

# Background stars
stars = []
for i in range(65):
    x = random.randint(20, 660)
    y = random.randint(100, 620)
    star = canvas.create_oval(
        x, y, x + 2, y + 2,
        fill="#a94b91",
        outline=""
    )
    stars.append((star, x, y))

# Heart text particles
particles = []
for i in range(170):
    t = i * 2 * math.pi / 170
    x, y = heart(t, 12)
    text = canvas.create_text(
        x, y,
        text="I love you",
        fill="#ff9bd6",
        font=("Arial", 8, "bold")
    )
    particles.append((text, t, i * 0.13))

# Heart outline
outline = canvas.create_line(
    *[coordinate
      for i in range(301)
      for coordinate in heart(i * 2 * math.pi / 300, 12)],
    fill="#ff55bd",
    width=2,
    smooth=True
)

# Center heart
center = canvas.create_text(
    340, 340,
    text="♥",
    fill="#ff5bbd",
    font=("Arial", 38, "bold")
)

canvas.create_text(
    340, 590,
    text="I LOVE YOU ♥",
    fill="#ffc1e6",
    font=("Arial", 24, "bold")
)
canvas.create_text(
    340, 620,
    text="Click anywhere for a little magic",
    fill="#a86e9c",
    font=("Arial", 10)
)

time = 0
burst = []

def make_burst(event):
    for i in range(18):
        particle = canvas.create_text(
            event.x, event.y,
            text=random.choice(["♥", "✦", "♡"]),
            fill=random.choice(["#ff5bbd", "#ffc1e6", "#ff9edb", "#ff77cc"]),
            font=("Arial", random.randint(10, 18))
        )
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 7)
        burst.append([particle, angle, speed, 0])

def animate():
    global time
    time += 0.05

    # Animate particles on the heart
    for text, t, offset in particles:
        scale = 12 + 1.2 * math.sin(time * 2 + offset)
        x, y = heart(t + time * 0.3, scale)
        canvas.coords(text, x, y)

        # Soft color pulse
        alpha = (math.sin(time * 3 + offset) + 1) / 2
        color = f"#{int(255 - 40 * alpha):02x}{int(155 - 30 * alpha):02x}{int(214 - 20 * alpha):02x}"
        canvas.itemconfig(text, fill=color)

    # Twinkle stars
    for star, x, y in stars:
        if random.random() < 0.03:
            size = random.randint(1, 3)
            canvas.coords(star, x, y, x + size, y + size)
            canvas.itemconfig(star, fill=random.choice(["#a94b91", "#ff9edb", "#bd77b5", "#ffc1e6"]))

    # Animate burst particles
    for p in burst[:]:
        particle, angle, speed, life = p
        life += 1
        if life > 40:
            canvas.delete(particle)
            burst.remove(p)
            continue
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed - life * 0.08  # slight gravity
        canvas.move(particle, dx, dy)
        p[3] = life

    # Gentle center heart pulse
    pulse = 38 + 4 * math.sin(time * 3)
    canvas.itemconfig(center, font=("Arial", int(pulse), "bold"))

    root.after(30, animate)

# Bind click
canvas.bind("<Button-1>", make_burst)

# Start animation
animate()
root.mainloop()