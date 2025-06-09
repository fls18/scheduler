import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
import json
import os

DATA_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

def add_todo():
    text = entry.get()
    date_text = date_entry.get()
    if text.strip() == '' or date_text.strip() == '':
        messagebox.showwarning("입력 오류", "할 일과 날짜를 모두 입력해주세요.")
        return
    todos.append({'text': text, 'date': date_text, 'done': False})
    save_todos(todos)
    entry.delete(0, tk.END)
    update_list()

def toggle_done(index):
    todos[index]['done'] = not todos[index]['done']
    save_todos(todos)
    update_list()

def delete_todo(index):
    todos.pop(index)
    save_todos(todos)
    update_list()

def update_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    for i, todo in enumerate(todos):
        status = "☑️" if todo['done'] else "⬜"
        item = f"[{status}] {todo['date']} - {todo['text']}"
        lbl = tk.Label(list_frame, text=item, anchor="w")
        lbl.pack(fill="x")

        btns = tk.Frame(list_frame)
        tk.Button(btns, text="완료", command=lambda i=i: toggle_done(i)).pack(side="left")
        tk.Button(btns, text="일정 삭제", command=lambda i=i: delete_todo(i)).pack(side="left")
        btns.pack(anchor="w")

# GUI 구성
root = tk.Tk()
root.title("일정 보드")

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

date_entry = tk.Entry(root, width=20)
date_entry.insert(0, date.today().isoformat())
date_entry.pack(pady=5)

tk.Button(root, text="일정 추가", command=add_todo).pack(pady=5)

list_frame = tk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=10, pady=10)

todos = load_todos()
update_list()

root.mainloop()