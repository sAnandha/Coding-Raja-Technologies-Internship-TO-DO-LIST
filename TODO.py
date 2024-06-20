from tkinter import *
from tkinter import ttk

class Todo:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List')
        self.root.geometry('800x500+300+150')
        self.root.resizable(True, True)

        self.label = Label(self.root, text='To-Do List Application',
                           font=('sans-serif', 25), width=10, bd=5, bg='orange', fg='black')
        self.label.pack(side='top', fill=BOTH)

        self.left_frame = Frame(self.root)
        self.left_frame.pack(side=LEFT, padx=20, pady=20, fill=Y)


        self.right_frame = Frame(self.root)
        self.right_frame.pack(side=LEFT, padx=20, pady=20, expand=True, fill=BOTH)

        self.label2 = Label(self.left_frame, text='Add Task',
                            font=('sans-serif', 20, 'bold'), width=10, bd=5, bg='orange', fg='black')
        self.label2.grid(row=0, column=0, pady=10)

        self.text = Text(self.left_frame, height=2, width=30, font=('ariel', 10, 'bold'))
        self.text.grid(row=1, column=0, pady=10)

        self.priority_label = Label(self.left_frame, text='Priority',
                                    font=('ariel', 20, 'bold'), width=10, bd=5, bg='orange', fg='black')
        self.priority_label.grid(row=2, column=0, pady=10)

        self.priority = ttk.Combobox(self.left_frame, values=["None", "Low", "Medium", "High"], font=('ariel', 10))
        self.priority.grid(row=3, column=0, pady=10)
        self.priority.current(0)

        self.add_button = Button(self.left_frame, text="Add", font=('sarif', 20, 'bold', 'italic'),
                                 width=10, bd=5, bg='orange', fg='black', command=self.add)
        self.add_button.grid(row=4, column=0, pady=10)

        self.delete_button = Button(self.left_frame, text="Delete", font=('sarif', 20, 'bold', 'italic'),
                                    width=10, bd=5, bg='orange', fg='black', command=self.delete)
        self.delete_button.grid(row=5, column=0, pady=10)

        self.label3 = Label(self.right_frame, text='Tasks',
                            font=('ariel', 20, 'bold'), width=10, bd=5, bg='orange', fg='black')
        self.label3.pack(pady=10)

        self.main_text = Listbox(self.right_frame, height=15, bd=5, font=("ariel", 14, "italic"))
        self.main_text.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.right_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.main_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.main_text.yview)

        self.load_tasks()

    def add(self):
        task = self.text.get(1.0, END).strip()
        priority = self.priority.get()
        if task:
            tasks = self.get_all_tasks()
            if priority != "None":
                tasks.append(f"{task} ({priority})")
            else:
                tasks.append(task)
            tasks.sort(key=lambda x: ('None' in x, 'Low' in x, 'Medium' in x, 'High' in x))
            self.update_listbox(tasks)
            self.save_tasks(tasks)
            self.text.delete(1.0, END)

    def delete(self):
        selected_task = self.main_text.curselection()
        if selected_task:
            tasks = self.get_all_tasks()
            tasks.pop(selected_task[0])
            self.update_listbox(tasks)
            self.save_tasks(tasks)

    def get_all_tasks(self):
        return [self.main_text.get(idx)[3:] for idx in range(self.main_text.size())]

    def update_listbox(self, tasks):
        self.main_text.delete(0, END)
        for index, task in enumerate(tasks, 1):
            self.main_text.insert(END, f"{index}. {task}")

    def save_tasks(self, tasks):
        with open('data.txt', 'w') as file:
            for task in tasks:
                file.write(f"{task}\n")

    def load_tasks(self):
        try:
            with open('data.txt', 'r') as file:
                tasks = file.readlines()
                tasks.sort(key=lambda x: ('None' in x, 'Low' in x, 'Medium' in x, 'High' in x))
                self.update_listbox([task.strip() for task in tasks])
        except FileNotFoundError:
            pass

def main():
    root = Tk()
    ui = Todo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
