from Base_CRUD import AudioFile, AudioEditor, Effects
from JSON_and_XML import JSONSerializer, XMLSerializer


class Playlist:  #Tracks are played here
    def __init__(self, editor_zero: AudioEditor):
        self.editor: AudioEditor = editor_zero

    def play_audiofile(self, name_file: str) -> None:  #plays the selected audio file by name
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                print(af.file)
                break
        print("No such audiofile.")

    def play_all(self) -> None:
        for af in self.editor.audio_files:
            print(af.file)


class Cropping:  #this is where the audio file is cropped
    def __init__(self, editor_zero: AudioEditor):
        self.editor: AudioEditor = editor_zero

    def crop(self, name_file: str) -> str:
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                result: str = af.file.split("-", 1)[-1]
                return result  #before "la-la-la", after "la-la"


class Continuation:  #here you can "continue" the audio
    def __init__(self, editor_zero: AudioEditor):
        self.editor: AudioEditor = editor_zero

    def proceed(self, name_file: str) -> str:
        for af in self.editor.audio_files:
            if af.name_file == name_file:
                verse: str = af.file.split("-", 1)[0]
                result: str = af.file + "-" + verse
                return result  #before "Uc-Uc", after "Uc-Uc-Uc"
        print("No such audiofile.")


class Mix:  #You can mix audio files here
    def __init__(self, editor_zero: AudioEditor):
        self.editor: AudioEditor = editor_zero

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
                    if af1.duration == af2.duration:
                        verse1: str = af1.file.split("-", 1)[0]
                        verse2: str = af2.file.split("-", 1)[0]
                        result: str = verse1 + "-" + verse2
                        while count != af1.duration - 1:
                            result += "-" + result
                            count += 1
                        return result  #before "La-La" and "Uc-Uc", after "La-Uc-La-Uc"
                    else:
                        return ""


class UserInterface:
    def __init__(self, editor_zero: AudioEditor):
        self.editor: AudioEditor = editor_zero
        self.playlist: Playlist = Playlist(self.editor)
        self.cropping: Cropping = Cropping(self.editor)
        self.continuation: Continuation = Continuation(self.editor)
        self.mix: Mix = Mix(self.editor)

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
        print("9. Update the audio file")
        print("10. Exit")

    @staticmethod
    def counting_the_duration(file: str) -> int:
        duration: int = file.count("-") + 1
        return duration

    def upload_audiofiles(self) -> None:
        while True:
            choice: str = input("Upload files from JSON(press 1) or XML (press 2)? ")
            if choice == "1":
                jsoneditor: JSONSerializer = JSONSerializer(self.editor)
                self.editor: AudioEditor = jsoneditor.load_from_json("AudiofilesJSON.json")
                break
            elif choice == "2":
                xml_editor: XMLSerializer = XMLSerializer(self.editor)
                self.editor: AudioEditor = xml_editor.load_from_xml("AudiofilesXML.xml")
                break
            else:
                print("Invalid number, try again.")

    def save_to_files(self) -> None:
        json_serializer: JSONSerializer = JSONSerializer(self.editor)
        json_serializer.save_to_json("AudiofilesJSON.json")

        xml_serializer: XMLSerializer = XMLSerializer(self.editor)
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
                name_file: str = input("Enter the name of the file you want to delete: ")
                self.editor.delete_audio_file(name_file)

            elif choice == "3":
                name_file: str = input("Enter the name of the file you want to list: ")
                self.playlist.play_audiofile(name_file)

            elif choice == "4":
                self.playlist.play_all()

            elif choice == "5":
                name_file: str = input("Enter the name of the file you want to crop: ")
                cropped_data: str = self.cropping.crop(name_file)
                if cropped_data:  # We check that the pruning was successful
                    # Creating a new audio file with cropped data
                    for af in self.editor.audio_files:
                        if af.name_file == name_file:
                            new_duration: int = self.counting_the_duration(
                                cropped_data)  # Recalculating the new duration
                            cropped_audio_file: AudioFile = AudioFile(af.name_file, af.author, new_duration,
                                                                      cropped_data)
                            self.editor.delete_audio_file(af.name_file)
                            self.editor.create_audio_file(cropped_audio_file)  # Adding a new file to self.editor
                            break
                else:
                    print("Cropping failed or audio file not found.")

            elif choice == "6":
                name_file: str = input("Enter the name of the file you want to continue: ")
                continuation_data: str = self.continuation.proceed(name_file)
                if continuation_data:
                    for af in self.editor.audio_files:
                        if af.name_file == name_file:
                            new_duration: int = self.counting_the_duration(continuation_data)
                            continuation_audio_file: AudioFile = AudioFile(af.name_file, af.author, new_duration,
                                                                           continuation_data)
                            self.editor.delete_audio_file(af.name_file)
                            self.editor.create_audio_file(continuation_audio_file)
                            break
                else:
                    print("Continuation failed or audio file not found.")

            elif choice == "7":
                name_file1: str = input("Enter the name of the file 1: ")
                name_file2: str = input("Enter the name of the file 2: ")

                while True:
                    choice_mix: str = input(
                        "If you want to connect two audio files, enter 1. If you want to mix them, enter 2 "
                        "(WARNING: The remix function only works with files of the same duration). ")
                    if choice_mix == "1":
                        connect_data: str = self.mix.connect(name_file1, name_file2)
                        if connect_data:
                            new_duration: int = self.counting_the_duration(connect_data)
                            name_file: str = input("Enter the name of the audio file: ")
                            author: str = input("Enter the author of the audio file: ")
                            connect_audio_file: AudioFile = AudioFile(name_file, author, new_duration, connect_data)
                            self.editor.create_audio_file(connect_audio_file)
                        else:
                            print("Connect failed or audio file not found.")
                        break
                    elif choice_mix == "2":
                        remix_data: str = self.mix.remix(name_file1, name_file2)
                        if remix_data:
                            new_duration: int = self.counting_the_duration(remix_data)
                            name_file: str = input("Enter the name of the audio file: ")
                            author: str = input("Enter the author of the audio file: ")
                            remix_audio_file: AudioFile = AudioFile(name_file, author, new_duration, remix_data)
                            self.editor.create_audio_file(remix_audio_file)
                        else:
                            print("Remix failed or audio file not found.")
                        break
                    else:
                        print("Invalid number, try again.")

            elif choice == "8":
                name_file: str = input("Write the name of the file to which you want to add the effect: ")
                effect: str = input("Write the name of the effect to which you want to add: ")
                for af in self.editor.audio_files:
                    if isinstance(af, AudioFile) and af.name_file == name_file:
                        effect_audiofile: Effects = Effects(af.name_file, af.author, af.duration, af.file, effect)
                        self.editor.delete_audio_file(name_file)
                        self.editor.create_audio_file(effect_audiofile)
                        break
                print("Sorry, there may not be a suitable file or file with that name.")

            elif choice == "9":
                name_file: str = input("Enter the name of the file you want to update: ")
                self.editor.update_audio_file(name_file)

            elif choice == "10":
                break

            else:
                print("Invalid number, try again.")
            self.save_to_files()


if __name__ == "__main__":
    editor = AudioEditor()
    work = UserInterface(editor)
    work.run()
