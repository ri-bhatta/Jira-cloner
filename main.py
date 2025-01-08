from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import json
import os
import uuid

class TaskBoardApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = "tasks.json"
        self.columns = ["Not Started", "In Progress", "Done"]
        self.tasks = self.load_tasks()

    def build(self):
        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)

        self.column_widgets = {}
        for column in self.columns:
            column_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=10)
            column_layout.bind(minimum_height=column_layout.setter('height'))
            
            column_title = Label(text=column, size_hint_y=None, height=40, bold=True, font_size=18)
            column_layout.add_widget(column_title)
            
            scroll_view = ScrollView(size_hint=(1, None), height=600)
            scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
            scroll_view.add_widget(scroll_layout)
            column_layout.add_widget(scroll_view)
            
            add_button = Button(text="Add Task", size_hint_y=None, height=40)
            add_button.bind(on_release=lambda x, col=column: self.add_task_popup(col))
            column_layout.add_widget(add_button)

            main_layout.add_widget(column_layout)
            self.column_widgets[column] = scroll_layout
        
        self.display_tasks()
        return main_layout

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                tasks = json.load(file)
                # Ensure all tasks have a unique ID
                for column, task_list in tasks.items():
                    for task in task_list:
                        if "id" not in task:
                            task["id"] = str(uuid.uuid4())
                return tasks
        return {col: [] for col in self.columns}

    def save_tasks(self):
        with open(self.data_file, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task_popup(self, column_name):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        task_input = TextInput(hint_text="Task Description", multiline=False)
        popup_layout.add_widget(task_input)

        save_button = Button(text="Save")
        popup_layout.add_widget(save_button)

        popup = Popup(title=f"Add Task to {column_name}",
                      content=popup_layout,
                      size_hint=(0.8, 0.4))

        save_button.bind(on_release=lambda x: self.add_task(column_name, task_input.text, popup))
        popup.open()

    def add_task(self, column_name, task_text, popup):
        if not task_text:
            return

        task_data = {
            "id": str(uuid.uuid4()),
            "text": task_text,
        }
        self.tasks[column_name].append(task_data)
        self.save_tasks()
        self.display_tasks()
        popup.dismiss()

    def display_tasks(self):
        for column in self.columns:
            self.column_widgets[column].clear_widgets()
            for task in self.tasks[column]:
                task_label = Label(text=task["text"], size_hint_y=None, height=40, halign="left", valign="middle")
                task_label.bind(size=task_label.setter('text_size'))
                self.column_widgets[column].add_widget(task_label)

if __name__ == "__main__":
    TaskBoardApp().run()
