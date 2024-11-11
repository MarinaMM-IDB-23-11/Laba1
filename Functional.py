from Base_CRUD import AudioFile, AudioEditor, Effects
from JSON_and_XML import JSONSerializer, XMLSerializer


class Playlist:  #Tracks are played here
    def __init__(self, editor_zero):
        self.editor = editor_zero

    def play_audiofile(self, name_file: str) -> None:  #plays the selected audio file by name
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                print(af.file)
                break

    def play_all(self) -> None:
        for af in self.editor.audio_files:
            print(af.file)


class Cropping:  #this is where the audio file is cropped
    def __init__(self, editor_zero):
        self.editor = editor_zero

    def crop(self, name_file: str) -> str:
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                result: str = af.file.split("-", 1)[-1]
                return result  #before "la-la-la", after "la-la"


class Continuation:  #here you can "continue" the audio
    def __init__(self, editor_zero):
        self.editor = editor_zero

    def proceed(self, name_file: str) -> str:
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                verse: str = af.file.split("-", 1)[0]
                result: str = af.file + "-" + verse
                return result  #before "Uc-Uc", after "Uc-Uc-Uc"


class Mix:  #You can mix audio files here
    def __init__(self, editor_zero):
        self.editor = editor_zero

    def connect(self, name_file1: str, name_file2: str) -> str:  #just by combining them
        for af1 in self.editor.audio_files:
            for af2 in self.editor.audio_files:
                if af1.name_file == name_file1 and af2.name_file == name_file2:
                    result: str = af1.file + "-" + af2.file
                    return result  #before "La-La" and "Uc-Uc", after "La-La-Uc-Uc"

    def remix(self, name_file1: str, name_file2: str) -> str:  #or making a remix
        count: int = 0  #WARNING: The remix function only works with files of the same duration
        for af1 in self.editor.audio_files:
            for af2 in self.editor.audio_files:
                if af1.name_file == name_file1 and af2.name_file == name_file2:
                    verse1: str = af1.file.split("-", 1)[0]
                    verse2: str = af2.file.split("-", 1)[0]
                    result: str = verse1 + "-" + verse2
                    while count != af1.duration - 1:
                        result += "-" + result
                        count += 1
                    return result  #before "La-La" and "Uc-Uc", after "La-Uc-La-Uc"


class UserInterface:
    def __init__(self, editor_zero):
        self.editor = editor_zero
        self.playlist = Playlist(self.editor)
        self.cropping = Cropping(self.editor)
        self.continuation = Continuation(self.editor)
        self.mix = Mix(self.editor)

    @staticmethod
    def show_menu() -> None:
        print("1. Add an audio file")
        print("2. Delete the audio file ")
        print("3. Listen to one audio file")
        print("4. Listen to all audio files")
        print("5. Crop the audio file")
        print("6. Continue an audio file ")
        print("7. Mix audio files")
        print("8. Add an effect")
        print("9. Exit")

    @staticmethod
    def counting_the_duration(file: str) -> int:
        duration: int = file.count("-") + 1
        return duration

    def upload_audiofiles(self) -> None:
        print("Upload files from JSON(press 1) or XML (press 2)?")
        choice: str  = input()
        if choice == "1":
            jsoneditor = JSONSerializer(self.editor)
            self.editor = jsoneditor.load_from_json("AudiofilesJSON.json")
        elif choice == "2":
            xml_editor = XMLSerializer(self.editor)
            self.editor = xml_editor.load_from_xml("AudiofilesXML.xml")
        #self.editor.read_all_audio_files()

    def save_to_files(self) -> None:
        json_serializer = JSONSerializer(self.editor)
        json_serializer.save_to_json("AudiofilesJSON.json")

        xml_serializer = XMLSerializer(self.editor)
        xml_serializer.save_to_xml("AudiofilesXML.xml")

    def run(self):
        self.upload_audiofiles()
        self.show_menu()
        self.editor.read_all_audio_files()

        while True:
            choice: str = input("Choose an option: ")

            if choice == "1":
                name_file: str = input("Enter the name of the audio file: ")
                author: str = input("Enter the author of the audio file: ")
                file: str = input("Upload an audio file (Write, for example, la-la-la. "
                                  "Please use the '-' symbol to split your file into 'couplets'): ")
                duration: int = self.counting_the_duration(file)
                audiofile: AudioFile = AudioFile(name_file, author, duration, file)
                self.editor.create_audio_file(audiofile)

            elif choice == "2":
                name_file = input("Enter the name of the file you want to delete: ")
                self.editor.delete_audio_file(name_file)

            elif choice == "3":
                name_file = input("Enter the name of the file you want to list: ")
                self.playlist.play_audiofile(name_file)

            elif choice == "4":
                self.playlist.play_all()

            elif choice == "5":
                name_file = input("Enter the name of the file you want to crop: ")
                cropped_data = self.cropping.crop(name_file)
                if cropped_data:  # Проверяем, что обрезка прошла успешно
                    # Создаем новый аудиофайл с обрезанными данными
                    for af in self.editor.audio_files:
                        if af.name_file == name_file:
                            new_duration = self.counting_the_duration(cropped_data)  # Пересчитываем новую продолжительность
                            cropped_audio_file = AudioFile(af.name_file, af.author, new_duration, cropped_data)
                            self.editor.delete_audio_file(af.name_file)
                            self.editor.create_audio_file(cropped_audio_file)  # Добавляем новый файл в self.editor
                            break
                else:
                    pass #print("Cropping failed or audio file not found.")

            elif choice == "6":
                name_file = input("Enter the name of the file you want to continue: ")
                continuation_data = self.continuation.proceed(name_file)
                if continuation_data:  # Проверяем, что обрезка прошла успешно
                    # Создаем новый аудиофайл с обрезанными данными
                    for af in self.editor.audio_files:
                        if af.name_file == name_file:
                            new_duration = self.counting_the_duration(continuation_data)  # Пересчитываем новую продолжительность
                            continuation_audio_file = AudioFile(af.name_file, af.author, new_duration, continuation_data)
                            self.editor.delete_audio_file(af.name_file)
                            self.editor.create_audio_file(continuation_audio_file)  # Добавляем новый файл в self.editor
                            break
                else:
                    pass #print("Cropping failed or audio file not found.")

            elif choice == "7":
                name_file1 = input("Enter the name of the file 1: ")
                name_file2 = input("Enter the name of the file 2: ")
                choice_mix: str = input(
                    "If you want to connect two audio files, enter 1. If you want to mix them, enter 2. ")
                if choice_mix == "1":
                    connect_data = self.mix.connect(name_file1, name_file2)
                    new_duration = self.counting_the_duration(connect_data)
                    name_file: str = input("Enter the name of the audio file: ")
                    author: str = input("Enter the author of the audio file: ")
                    connect_audio_file = AudioFile(name_file, author, new_duration, connect_data)
                    self.editor.create_audio_file(connect_audio_file)
                elif choice_mix == "2":
                    remix_data: str = self.mix.remix(name_file1, name_file2)
                    new_duration = self.counting_the_duration(remix_data)
                    name_file: str = input("Enter the name of the audio file: ")
                    author: str = input("Enter the author of the audio file: ")
                    remix_audio_file = AudioFile(name_file, author, new_duration, remix_data)
                    self.editor.create_audio_file(remix_audio_file)
                else:
                    pass

            elif choice == "8":
                name_file = input("Write the name of the file to which you want to add the effect: ")
                effect: str = input("Write the name of the effect to which you want to add: ")
                for af in self.editor.audio_files:
                    if isinstance(af, AudioFile) and af.name_file == name_file:
                        effect_audiofile = Effects(af.name_file, af.author, af.duration, af.file, effect)
                        self.editor.delete_audio_file(name_file)
                        self.editor.create_audio_file(effect_audiofile)

            elif choice == "9":
                break
            else:
                pass
            self.save_to_files()


if __name__ == "__main__":
    editor = AudioEditor()
    work = UserInterface(editor)
    work.run()
