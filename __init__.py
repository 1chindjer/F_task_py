import json
import datetime

class Note:
    def __init__(self, title, body):
        self.id = None
        self.title = title
        self.body = body
        self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp
        }

class NotesApp:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Note(note['title'], note['body']) for note in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open(self.filename, 'w') as file:
            json.dump([note.to_dict() for note in self.notes], file)

    def add_note(self, title, body):
        note = Note(title, body)
        note.id = len(self.notes) + 1
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.body = body
                note.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def list_notes(self, start_date=None, end_date=None):
        for note in self.notes:
            if start_date and end_date:
                note_date = datetime.datetime.strptime(note.timestamp, '%Y-%m-%d %H:%M:%S')
                if not (start_date <= note_date <= end_date):
                    continue
            print(f"ID: {note.id}\nTitle: {note.title}\nBody: {note.body}\nTimestamp: {note.timestamp}\n")

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                notes = []
                for note_data in data:
                    note = Note(note_data['title'], note_data['body'])
                    note.id = note_data['id']
                    note.timestamp = note_data['timestamp']
                    notes.append(note)
                return notes
        except (FileNotFoundError, json.JSONDecodeError):
            return []

if __name__ == "__main__":
    app = NotesApp()

    while True:
        command = input("Введите команду (add, edit, delete, list, exit): ")

        if command == "add":
            title = input("Введите заголовок заметки: ")
            body = input("Введите тело заметки: ")
            app.add_note(title, body)

        elif command == "edit":
            note_id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое тело заметки: ")
            app.edit_note(note_id, title, body)

        elif command == "delete":
            note_id = int(input("Введите ID заметки для удаления: "))
            app.delete_note(note_id)

        elif command == "list":
            filter_date = input("Хотите ли вы фильтровать по дате? (yes/no): ").strip().lower()
            if filter_date == "yes":
                try:
                    start_date_str = input("Введите начальную дату (YYYY-MM-DD): ").strip()
                    end_date_str = input("Введите конечную дату (YYYY-MM-DD): ").strip()
                    
                    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
                    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
                    end_date = end_date.replace(hour=23, minute=59, second=59)
                    
                    app.list_notes(start_date, end_date)
                except ValueError as e:
                    print(f"Ошибка в формате даты: {e}")
            else:
                app.list_notes()

        elif command == "exit":
            break

        else:
            print("Неизвестная команда!")
