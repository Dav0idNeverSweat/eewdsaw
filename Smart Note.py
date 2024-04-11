from PyQt5.QtWidgets import QTextEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QListWidget, QLineEdit, QInputDialog, QListWidgetItem
from PyQt5.QtCore import Qt # alignment
from json import load, dump
from functools import partial

notes = dict()
notes_name = str()
notes_text = str()
notes_tag  = str()

def delete_note():
    global notes
    to_delete = note_list.selectedItems()[0]
    note_list.takeItem(note_list.row(to_delete))
    del notes[to_delete.text()]
    note_input.setText(str())

tags = list()


def add_tag():
    global notes, tags

    tag = add_tag_input.text()
    if not tag:
        tag = tag_list.selectedItems()[0].text()
    
    notes_name = note_list.selectedItems()[0].text()
    if not tag in notes[notes_name]['tags']:
        notes[notes_name]['tags'].append(tag)

    if not tag in tags:
        tag_list.addItem(tag)
        tags.append(tag)
    #else:
    #    for i in range(tag_list.count()):
    #        if tag_list.item(i).text() == tag:
    #            tag_list.setRowHidden(tag_list.row(tag_list.item(i)), False)

def untag():
    global notes
    tag = tag_list.selectedItems()[0]
    notes_name = note_list.selectedItems()[0].text()
    notes[notes_name]['tags'].remove(tag.text())
    tag_list.setRowHidden(tag_list.row(tag), True)

def show_note():
    global notes
    name = note_list.selectedItems()[0].text()
    content = notes[name]['text']
    note_input.setText(content)

    tags = notes[name]['text']
    for i in range(tag_list.count()):
        if not tag_list.item(i).text() in tags:
            tag_list.setRowHidden(tag_list.row(tag_list.item(i)), True)

def show_tag_list():
    for i in range(tag_list.count() - 1):
        tag_list.show(tag_list.item(i), False)

def create_notes_func():
    global notes_name, notes

    # click create note button
    notes_name, ok = QInputDialog.getText(window, 'Add note', 'Note name')
    if ok and notes_name and not notes_name in notes:
        notes[notes_name] = {'text' : '', 'tags' : []}
        item = QListWidgetItem(notes_name)
        note_list.addItem(item)
        note_list.setCurrentItem(item)
        note_input.setText('')

def save_note():
    global notes_name, notes_text, notes_tag

    if note_list.count() != 0:
        notes_name = note_list.currentItem().text()
        notes_text = note_input.toPlainText()
        notes[notes_name]['text'] = notes_text

        print(notes)

def closeEvent(self):
    global notes, tags
    with open('my_notes.json', 'w') as file:
        dump(notes, file)
    
    with open('my_tags.txt', 'w') as file:
        for tag in tags:
            file.write(tag + '\n')

def read_file():
    global notes
    try:
        file = open('filename.json', 'r')

        notes = load(file)
        for note in notes:
            note_list.addItem(note)
    except:
        print('File not found')
    
    try:
        with open('my_tags.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if '\n' in line:
                    line = line.strip('\n')
                tags.append(line)
                tag_list.addItem(line)              
    except:
        print('Tags file does not exist!')

def search_by_tag():
    global notes
    try:
        curr_tag = tag_list.selectedItems()[0].text()
    except:
        curr_tag = add_tag_input.text()
    for i in range(note_list.count()):
        curr_note = note_list.item(i)
        notes_name = curr_note.text()
        if not curr_tag in notes[notes_name]['tags']:
            note_list.setRowHidden(note_list.row(curr_note))

# Set application/window
app = QApplication([])
window = QWidget()
window.setFixedSize(900, 700)

main_Layout = QHBoxLayout()
window.setLayout(main_Layout)
window.setWindowTitle('Note programme')

left_side = QVBoxLayout()
close_note = QPushButton('Close Note')
left_side.addWidget(close_note)
note_input = QTextEdit()
note_input.setPlaceholderText('Write something...')
left_side.addWidget(note_input)
main_Layout.addLayout(left_side, stretch=2)

# Create right side GUI (1)
right_side = QVBoxLayout()
note_list_label = QLabel('List of notes')
note_list = QListWidget()
right_side.addWidget(note_list_label)
right_side.addWidget(note_list)

group_note_button = QHBoxLayout()
create_note_button = QPushButton('Create')
delete_note_button = QPushButton('Delete')
group_note_button.addWidget(create_note_button)
group_note_button.addWidget(delete_note_button)
right_side.addLayout(group_note_button)

save_note_button = QPushButton('Save note')
right_side.addWidget(save_note_button)

# Create right side GUI (2)
note_tag_label = QLabel('List of tags')
tag_list = QListWidget()
add_tag_input = QLineEdit()
add_tag_input.setPlaceholderText('Enter tag...')
right_side.addWidget(note_tag_label)
right_side.addWidget(tag_list)
right_side.addWidget(add_tag_input)

group_tag_button = QHBoxLayout()
add_to_note_button = QPushButton('Add to note')
untag_note_button = QPushButton('Untag from note')
group_tag_button.addWidget(add_to_note_button)
group_tag_button.addWidget(untag_note_button)
right_side.addLayout(group_tag_button)

search_note_button = QPushButton('Search note by tag')
right_side.addWidget(search_note_button)

# Add right side GUI (1-2) to main layout
main_Layout.addLayout(right_side, stretch=1)
create_note_button.clicked.connect(create_notes_func)
save_note_button.clicked.connect(save_note)
note_list.itemClicked.connect(show_note)
delete_note_button.clicked.connect(delete_note)
note_list.itemDoubleClicked.connect(show_note)
add_to_note_button.clicked.connect(add_tag)

# Show and run application
window.closeEvent = partial(closeEvent)
window.show()
app.exec()