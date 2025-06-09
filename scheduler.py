import tkinter as tk
from tkinter import messagebox
from datetime import date
import json
import os
from collections import defaultdict

DATA_FILE = 'todos.json'
current_lang = 'kor'  # 기본 언어를 한국어로 고정

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

def delete_by_date(date_to_delete):
    global todos
    todos = [todo for todo in todos if todo['date'] != date_to_delete]
    save_todos(todos)
    update_list()

def update_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    # 날짜별 그룹화
    grouped = defaultdict(list)
    for i, todo in enumerate(todos):
        grouped[todo['date']].append((i, todo))

    for date_text in sorted(grouped):
        date_frame = tk.Frame(list_frame)
        date_label = tk.Label(date_frame, text=f"{date_text}")
        date_label.pack(side="left")

        tk.Button(date_frame, 
                  text="해당 날짜 일정 삭제", 
                  command=lambda d=date_text: delete_by_date(d)).pack(side="left", padx=5)
        date_frame.pack(anchor="w", pady=(10, 0))

        for i, todo in grouped[date_text]:
            status = "☑️" if todo['done'] else "⬜"
            task_frame = tk.Frame(list_frame)
            task_label = tk.Label(task_frame, text=f"{status} {todo['text']}", anchor="w")
            task_label.pack(side="left")

            tk.Button(task_frame, text="완료", command=lambda i=i: toggle_done(i)).pack(side="left", padx=5)
            tk.Button(task_frame, text="삭제", command=lambda i=i: delete_todo(i)).pack(side="left")

            task_frame.pack(fill="x", anchor="w")

# GUI
root = tk.Tk()
root.title("일정 보드")

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

date_entry = tk.Entry(root, width=20)
date_entry.insert(0, date.today().isoformat())
date_entry.pack(pady=5)

btn_frame = tk.Frame(root)
tk.Button(btn_frame, text="일정 추가", command=add_todo).pack(side="left", padx=5)
btn_frame.pack(pady=5)

list_frame = tk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=10, pady=10)

todos = load_todos()
update_list()

root.mainloop()
