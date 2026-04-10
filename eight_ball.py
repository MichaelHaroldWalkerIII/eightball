import random
import time
import tkinter as tk
from tkinter import font

try:
    from winsdk.windows.devices.sensors import Accelerometer
except Exception:
    Accelerometer = None

SENSOR_THRESH = 2.8
SENSOR_COOLDOWN = 0.7

responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]

class Magic8BallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic 8-Ball")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        main = tk.Frame(root, bg="#1a1a2e")
        main.pack(padx=20, pady=20)
        
        title = tk.Label(main, text="Magic 8-Ball", font=("Helvetica", 20, "bold"),
                         fg="#fff", bg="#1a1a2e")
        title.pack(pady=(0, 10))
        
        self.canvas = tk.Canvas(main, width=300, height=300, bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.ball_center = (150, 150)
        cx, cy = self.ball_center
        
        # Outer black sphere
        self.ball = self.canvas.create_oval(30, 30, 270, 270, fill="#111", outline="#222", width=3)
        
        # Inner dark circle (liquid)
        self.inner = self.canvas.create_oval(55, 55, 245, 245, fill="#0a0a0a", outline="#1a1a1a", width=2)
        
        # Blue triangular window
        tri_size = 75
        self.triangle = self.canvas.create_polygon(
            cx, cy - tri_size * 0.8,
            cx - tri_size * 0.9, cy + tri_size * 0.5,
            cx + tri_size * 0.9, cy + tri_size * 0.5,
            fill="#0a3d62", outline="#1a5a82", width=2
        )
        
        # Faint "8" behind
        self.eight = self.canvas.create_text(cx, cy - 25, text="8", font=("Helvetica", 36, "bold"),
                                             fill="#0a3d62")
        
        # Answer text
        self.answer_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.answer_text = self.canvas.create_text(cx, cy + 20, text="", font=self.answer_font,
                                                    fill="#fff", width=110, justify="center")
        
        self.instruct = tk.Label(main, text="Ask a yes/no question and shake the ball",
                                  font=("Helvetica", 11), fg="#aaa", bg="#1a1a2e")
        self.instruct.pack(pady=(5, 10))
        
        self.entry = tk.Entry(main, font=("Helvetica", 12), width=35,
                              bg="#2a2a4a", fg="#fff", insertbackground="#fff",
                              relief="flat", bd=8)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.shake())
        self.entry.focus_set()
        
        self.shake_btn = tk.Button(main, text="SHAKE", font=("Helvetica", 14, "bold"),
                                    bg="#0a3d62", fg="#fff", activebackground="#1a5a82",
                                    activeforeground="#fff", relief="flat", padx=30, pady=8,
                                    cursor="hand2", command=self.shake)
        self.shake_btn.pack(pady=12)
        
        self.shaking = False
        self._last_shake = 0
        self._init_sensor()
    
    def _init_sensor(self):
        self._sensor = None
        if not Accelerometer:
            return
        try:
            self._sensor = Accelerometer.get_default()
            if self._sensor:
                self._sensor.report_interval = 50
                self._sensor.add_reading_changed(self._on_accel)
        except Exception:
            self._sensor = None
    
    def _on_accel(self, sender, args):
        r = args.reading
        mag = (r.acceleration_x ** 2 + r.acceleration_y ** 2 + r.acceleration_z ** 2) ** 0.5
        now = time.time()
        if mag > SENSOR_THRESH and now - self._last_shake > SENSOR_COOLDOWN:
            self._last_shake = now
            self.root.after(0, self.shake)
    
    def shake(self):
        if self.shaking:
            return
        
        question = self.entry.get().strip()
        if not question:
            self.instruct.config(text="You must ask a question!", fg="#ff6b6b")
            self.root.after(1200, lambda: self.instruct.config(text="Ask a yes/no question and shake the ball", fg="#aaa"))
            return
        
        self.shaking = True
        self.shake_btn.config(state="disabled")
        self.instruct.config(text="Shaking...", fg="#aaa")
        self.canvas.itemconfig(self.answer_text, text="")
        
        offsets = [(8, -6), (-10, 7), (6, 9), (-7, -5), (4, -8), (-3, 5), (0, 0)]
        delay = 50
        
        def animate(i=0):
            if i < len(offsets):
                dx, dy = offsets[i]
                self.canvas.move(self.ball, dx, dy)
                self.canvas.move(self.inner, dx, dy)
                self.canvas.move(self.triangle, dx, dy)
                self.canvas.move(self.eight, dx, dy)
                self.canvas.move(self.answer_text, dx, dy)
                self.root.after(delay, lambda: animate(i + 1))
            else:
                answer = random.choice(responses)
                self.canvas.itemconfig(self.answer_text, text=answer)
                self.instruct.config(text="The Magic 8-Ball has spoken.", fg="#4ade80")
                self.shake_btn.config(state="normal")
                self.shaking = False
                self.entry.delete(0, "end")
        
        animate()

if __name__ == "__main__":
    root = tk.Tk()
    Magic8BallGUI(root)
    root.mainloop()
