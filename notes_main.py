from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout


import json


app = QApplication([])


'''Notes in json'''
notes = {
    "Welcome!" : {
        "text" : "This is the best note taking app in the world!",
        "tags" : ["good", "instructions"]
    }
}
with open("notes_data.json", "w") as file:
    json.dump(notes, file, ensure_ascii=False)




'''Application interface'''
#application window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)


#application window widgets
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')


button_note_create = QPushButton('Create note') #a window appears with the field "Enter note name"
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()
button_add = QPushButton('Add to note')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')


#arranging widgets by layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


'''Application functionality'''
def show_note():
    #get the text from the note with the title highlighted and display it in the edit field
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])

def add_notes():
    notes_name, result = QInputDialog.getText(notes_win, "Create Note", "Note name:")
    if result and notes_name != "":
        notes[notes_name] = {"text" : "", "tags" : []}
        list_notes.addItem(notes_name)
        list_tags.addItems(notes[notes_name]["tags"])
        print(notes)

def delete_notes():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print("No notes selected")

def save_notes():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print("No notes selected")

def add_tags():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys = True)
            print(notes)
        else:
            print("tag name already in use")
    else:
        print("no notes selected")

def delete_tags():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["tags"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print("no tags selected")

def search_tags():
    tag = field_tag.text() 
    if button_search.text() == "Search notes by tag" and tag:
        filtered_notes = {}
        for key in notes:
            if tag in notes[key]["tags"]:
                filtered_notes[key] = notes[key]
        button_search.setText("Reset Search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(filtered_notes)
    elif button_search.text() == "Reset Search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_search.setText("Search notes by tag")

'''Run the application'''
#connecting event handling
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_notes)
button_note_del.clicked.connect(delete_notes)
button_note_save.clicked.connect(save_notes)
button_add.clicked.connect(add_tags)
button_del.clicked.connect(delete_tags)
button_search.clicked.connect(search_tags)
#run the application 
notes_win.show()


with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


app.exec_()

