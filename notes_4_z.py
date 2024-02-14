# выполненное четвертое задание
# вывод заметок в порядке уменьшения их длины (то есть сначала самые короткие)
def display_notes():
    import os
    notes = [note for note in os.listdir() if note.endswith(".txt")]
    print(notes)
    sorted_notes = sorted(notes, key=len)
    print(sorted_notes)

display_notes()








