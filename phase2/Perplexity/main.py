from ui.main_window import MainWindow
import tkinter as tk


def main() -> None:
    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
