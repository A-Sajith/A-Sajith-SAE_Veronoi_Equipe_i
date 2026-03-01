import tkinter as tk

class PointListView(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg='white')
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.items = []

    def clear(self):
        for _, _, frame in self.items:
            frame.destroy()
        self.items.clear()

    def add_point(self, color: str, text: str):
        frame = tk.Frame(self.scrollable_frame, bg='white')
        frame.pack(fill=tk.X, padx=2, pady=1)

        color_canvas = tk.Canvas(frame, width=20, height=20, bg='white', highlightthickness=0)
        color_canvas.create_oval(2, 2, 18, 18, fill=color, outline='black')
        color_canvas.pack(side=tk.LEFT, padx=2)

        label = tk.Label(frame, text=text, bg='white', anchor='w')
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.items.append((color, text, frame))