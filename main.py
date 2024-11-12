from Base_CRUD import AudioEditor
from Functional import UserInterface

if __name__ == "__main__":
    editor = AudioEditor()
    work = UserInterface(editor)
    work.run()
