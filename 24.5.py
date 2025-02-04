import tkinter as tk
from tkinter import messagebox
from threading import Thread


def brackets(listic):
    result = []
    text = False

    for i in listic:
        if i == '(':
            text = True
        elif i == ')':
            text = False
        elif not text:
            result.append(i)
    return "".join(result)
def work():
    global entry_listic
    listic = entry_listic.get()

    if not listic:
        messagebox.showwarning("", "Напишіть текст!")
        return
    new = brackets(listic)
    res_label.config(text=f"Результат: {new}")


def main():
    global root, entry_listic, res_label, cal_btn

    root = tk.Tk()
    root.title("Видалення тексту у дужках")

    tk.Label(root, text="Введіть текст з дужками:").pack()

    entry_listic = tk.Entry(root)
    entry_listic.pack()

    res_label = tk.Label(root, text="Результат:")
    res_label.pack()

    cal_btn = tk.Button(root, text="Очистити", command=work)
    cal_btn.pack()

    root.mainloop()


if __name__ == "__main__":
    app = Thread(target=main)
    app.start()
    app.join()
