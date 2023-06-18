import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description, due_date, priority, category, dependencies=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = False
        self.dependencies = dependencies or []

class TaskManagementApp:
    def __init__(self):
        self.tasks = []
        self.categories = []
        
        self.root = tk.Tk()
        self.root.title("Academic Task Management")
        
        # Create GUI elements and layout
        self.create_widgets()
        
        # Initialize database connection
        self.conn = sqlite3.connect("task_manager.db")
        self.create_table()
        
        # Load tasks from the database
        self.load_tasks_from_database()
        
        # Check due date notifications every 24 hours
        self.root.after(86400000, self.check_due_date_notifications)
        
        self.root.mainloop()

    def create_widgets(self):
        # Create and position GUI elements
        
        # Create task list treeview
        self.task_tree = ttk.Treeview(self.root, columns=("Title", "Due Date", "Priority", "Category"))
        self.task_tree.heading("#0", text="Status")
        self.task_tree.column("#0", width=50)
        self.task_tree.heading("Title", text="Title")
        self.task_tree.column("Title", width=150)
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.column("Due Date", width=100)
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.column("Priority", width=100)
        self.task_tree.heading("Category", text="Category")
        self.task_tree.column("Category", width=100)
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the task list
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.task_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Create buttons for adding, editing, and marking tasks as complete
        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack(pady=10)
        
        edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_button.pack(pady=5)
        
        complete_button = tk.Button(self.root, text="Mark Complete", command=self.mark_complete)
        complete_button.pack(pady=5)
        
        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack(pady=5)
        
        complete_all_button = tk.Button(self.root, text="Complete All", command=self.complete_all_tasks)
        complete_all_button.pack(pady=5)
        
        # Create category dropdown menu
        self.category_var = tk.StringVar()
        self.category_var.set("All")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, "All", *self.categories, command=self.filter_tasks)
        self.category_menu.pack(pady=10)
        
        # Create sorting buttons
        sort_label = tk.Label(self.root, text="Sort by:")
        sort_label.pack(pady=5)
        
        sort_frame = tk.Frame(self.root)
        sort_frame.pack()
        
        sort_button_title = tk.Button(sort_frame, text="Title", command=lambda: self.sort_tasks("title"))
        sort_button_title.pack(side=tk.LEFT, padx=5)
        
        sort_button_due_date = tk.Button(sort_frame, text="Due Date", command=lambda: self.sort_tasks("due_date"))
        sort_button_due_date.pack(side=tk.LEFT, padx=5)
        
        sort_button_priority = tk.Button(sort_frame, text="Priority", command=lambda: self.sort_tasks("priority"))
        sort_button_priority.pack(side=tk.LEFT, padx=5)
        
        sort_button_category = tk.Button(sort_frame, text="Category", command=lambda: self.sort_tasks("category"))
        sort_button_category.pack(side=tk.LEFT, padx=5)
        
        # Create search functionality
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_tasks)
        search_button.pack(side=tk.LEFT)
        
    def create_table(self):
        # Create tasks table in the database if it doesn't exist
        self.conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                            (title TEXT, description TEXT, due_date TEXT, priority INTEGER, category TEXT, completed INTEGER, dependencies TEXT)''')
        self.conn.commit()
        
    def load_tasks_from_database(self):
        # Clear existing tasks
        self.tasks = []
        
        # Clear task list treeview
        self.task_tree.delete(*self.task_tree.get_children())
        
        # Load tasks from the database
        cursor = self.conn.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        
        for row in rows:
            title, description, due_date_str, priority, category, completed, dependencies_str = row
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            dependencies = dependencies_str.split(',') if dependencies_str else []
            task = Task(title, description, due_date, priority, category, dependencies)
            task.completed = bool(completed)
            self.tasks.append(task)
            self.insert_task_into_tree(task)
            
            # Update categories list
            if category not in self.categories:
                self.categories.append(category)
        
        # Refresh category menu
        menu = self.category_menu["menu"]
        menu.delete(0, "end")
        self.category_var.set("All")
        menu.add_command(label="All", command=lambda: self.filter_tasks("All"))
        for category in self.categories:
            menu.add_command(label=category, command=lambda c=category: self.filter_tasks(c))
            
    def insert_task_into_tree(self, task):
        # Insert a task into the task list treeview
        completed_status = "✓" if task.completed else ""
        self.task_tree.insert("", "end", text=completed_status, values=(task.title, task.due_date, task.priority, task.category))
        
    def add_task(self):
        # Function to handle adding a new task
        
        # Create a new window for task entry
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Task")
        
        # Create labels and entry fields for task details
        title_label = tk.Label(add_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()
        
        description_label = tk.Label(add_window, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()
        
        due_date_label = tk.Label(add_window, text="Due Date (YYYY-MM-DD):")
        due_date_label.pack()
        due_date_entry = tk.Entry(add_window)
        due_date_entry.pack()
        
        priority_label = tk.Label(add_window, text="Priority:")
        priority_label.pack()
        priority_entry = tk.Entry(add_window)
        priority_entry.pack()
        
        category_label = tk.Label(add_window, text="Category:")
        category_label.pack()
        category_entry = tk.Entry(add_window)
        category_entry.pack()
        
        dependencies_label = tk.Label(add_window, text="Dependencies (comma-separated):")
        dependencies_label.pack()
        dependencies_entry = tk.Entry(add_window)
        dependencies_entry.pack()
        
        def save_task():
            # Save the task to the database and update the task list
            title = title_entry.get()
            description = description_entry.get()
            due_date_str = due_date_entry.get()
            priority = int(priority_entry.get())
            category = category_entry.get()
            dependencies = dependencies_entry.get().split(',')
            
            if not title:
                messagebox.showerror("Error", "Please enter a title for the task.")
                return
            
            if not due_date_str:
                messagebox.showerror("Error", "Please enter a due date for the task.")
                return
            
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid due date format. Please use the format YYYY-MM-DD.")
                return
            
            task = Task(title, description, due_date, priority, category, dependencies)
            self.tasks.append(task)
            self.insert_task_into_tree(task)
            self.save_task_to_database(task)
            self.filter_tasks(self.category_var.get())
            
            add_window.destroy()
            
        save_button = tk.Button(add_window, text="Save", command=save_task)
        save_button.pack(pady=10)
        
    def edit_task(self):
        # Function to handle editing a task
        
        # Get the selected task from the task list
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to edit.")
            return
        
        task_index = int(selected_item[0][1:]) - 1
        task = self.tasks[task_index]
        
        # Create a new window for task editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        
        # Create labels and entry fields for task details
        title_label = tk.Label(edit_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(edit_window)
        title_entry.insert(tk.END, task.title)
        title_entry.pack()
        
        description_label = tk.Label(edit_window, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(edit_window)
        description_entry.insert(tk.END, task.description)
        description_entry.pack()
        
        due_date_label = tk.Label(edit_window, text="Due Date (YYYY-MM-DD):")
        due_date_label.pack()
        due_date_entry = tk.Entry(edit_window)
        due_date_entry.insert(tk.END, task.due_date.strftime("%Y-%m-%d"))
        due_date_entry.pack()
        
        priority_label = tk.Label(edit_window, text="Priority:")
        priority_label.pack()
        priority_entry = tk.Entry(edit_window)
        priority_entry.insert(tk.END, str(task.priority))
        priority_entry.pack()
        
        category_label = tk.Label(edit_window, text="Category:")
        category_label.pack()
        category_entry = tk.Entry(edit_window)
        category_entry.insert(tk.END, task.category)
        category_entry.pack()
        
        dependencies_label = tk.Label(edit_window, text="Dependencies (comma-separated):")
        dependencies_label.pack()
        dependencies_entry = tk.Entry(edit_window)
        dependencies_entry.insert(tk.END, ','.join(task.dependencies))
        dependencies_entry.pack()
        
        def save_task():
            # Save the edited task to the database and update the task list
            new_title = title_entry.get()
            new_description = description_entry.get()
            new_due_date_str = due_date_entry.get()
            new_priority = int(priority_entry.get())
            new_category = category_entry.get()
            new_dependencies = dependencies_entry.get().split(',')
            
            if not new_title:
                messagebox.showerror("Error", "Please enter a title for the task.")
                return
            
            if not new_due_date_str:
                messagebox.showerror("Error", "Please enter a due date for the task.")
                return
            
            try:
                new_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid due date format. Please use the format YYYY-MM-DD.")
                return
            
            task.title = new_title
            task.description = new_description
            task.due_date = new_due_date
            task.priority = new_priority
            task.category = new_category
            task.dependencies = new_dependencies
            
            self.update_task_in_database(task)
            self.update_task_in_tree(task_index)
            self.filter_tasks(self.category_var.get())
            
            edit_window.destroy()
            
        save_button = tk.Button(edit_window, text="Save", command=save_task)
        save_button.pack(pady=10)
        
    def mark_complete(self):
        # Function to handle marking a task as complete
        
        # Get the selected task from the task list
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to mark as complete.")
            return
        
        task_index = int(selected_item[0][1:]) - 1
        task = self.tasks[task_index]
        
        if task.completed:
            messagebox.showerror("Error", "Task is already marked as complete.")
            return
        
        # Mark the task as complete and update the task list
        task.completed = True
        self.update_task_in_database(task)
        self.update_task_in_tree(task_index)
        
    def delete_task(self):
        # Function to handle deleting a task
        
        # Get the selected task from the task list
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to delete.")
            return
        
        task_index = int(selected_item[0][1:]) - 1
        task = self.tasks[task_index]
        
        # Confirm the deletion with the user
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this task?")
        if not confirm:
            return
        
        # Delete the task from the database and update the task list
        self.delete_task_from_database(task)
        self.delete_task_from_tree(task_index)
        
    def complete_all_tasks(self):
        # Function to handle completing all tasks
        
        # Confirm with the user
        confirm = messagebox.askyesno("Confirm Complete All", "Are you sure you want to mark all tasks as complete?")
        if not confirm:
            return
        
        # Mark all tasks as complete and update the task list
        for task in self.tasks:
            task.completed = True
            self.update_task_in_database(task)
            self.update_task_in_tree(self.tasks.index(task))
        
    def save_task_to_database(self, task):
        # Save a task to the database
        dependencies_str = ','.join(task.dependencies)
        self.conn.execute("INSERT INTO tasks (title, description, due_date, priority, category, completed, dependencies) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (task.title, task.description, task.due_date.strftime("%Y-%m-%d"), task.priority, task.category, int(task.completed), dependencies_str))
        self.conn.commit()
        
    def update_task_in_database(self, task):
        # Update a task in the database
        dependencies_str = ','.join(task.dependencies)
        self.conn.execute("UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ?, category = ?, completed = ?, dependencies = ? WHERE rowid = ?",
                          (task.title, task.description, task.due_date.strftime("%Y-%m-%d"), task.priority, task.category, int(task.completed), dependencies_str, self.tasks.index(task) + 1))
        self.conn.commit()
        
    def delete_task_from_database(self, task):
        # Delete a task from the database
        self.conn.execute("DELETE FROM tasks WHERE rowid = ?", (self.tasks.index(task) + 1,))
        self.conn.commit()
        
    def update_task_in_tree(self, task_index):
        # Update a task in the task list treeview
        task = self.tasks[task_index]
        completed_status = "✓" if task.completed else ""
        self.task_tree.item(f"#{task_index + 1}", text=completed_status, values=(task.title, task.due_date, task.priority, task.category))
        
    def delete_task_from_tree(self, task_index):
        # Delete a task from the task list treeview
        self.task_tree.delete(f"#{task_index + 1}")
        
    def filter_tasks(self, category):
        # Filter tasks based on the selected category
        
        self.task_tree.delete(*self.task_tree.get_children())
        
        if category == "All":
            for task in self.tasks:
                self.insert_task_into_tree(task)
        else:
            for task in self.tasks:
                if task.category == category:
                    self.insert_task_into_tree(task)
                    
    def sort_tasks(self, sort_key):
        # Sort tasks based on the selected sort key
        
        self.tasks.sort(key=lambda x: getattr(x, sort_key.lower()))
        self.task_tree.delete(*self.task_tree.get_children())
        
        for task in self.tasks:
            self.insert_task_into_tree(task)
            
    def search_tasks(self):
        # Search tasks based on the entered search term
        
        search_term = self.search_entry.get().lower()
        
        self.task_tree.delete(*self.task_tree.get_children())
        
        for task in self.tasks:
            if search_term in task.title.lower() or search_term in task.description.lower():
                self.insert_task_into_tree(task)
                
    def check_due_date_notifications(self):
        # Check for due date notifications
        
        today = datetime.now().date()
        
        for task in self.tasks:
            if not task.completed and task.due_date == today:
                messagebox.showinfo("Due Date Notification", f"The task '{task.title}' is due today!")
                
        # Schedule the next check after 24 hours
        self.root.after(86400000, self.check_due_date_notifications)
        
        
if __name__ == "__main__":
    app = TaskManagementApp()