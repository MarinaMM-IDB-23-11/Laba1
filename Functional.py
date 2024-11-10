from Base_CRUD import AudioFile, AudioEditor

class Playlist:  #Tracks are played here
    def __init__(self, audio: AudioEditor):
        self.editor: list[AudioFile] = audio.audio_files

    def play_audiofile(self, name_file: str) -> None:  #plays the selected audio file by name
        for af in self.editor:
            if af.name_file == name_file:
                print(af.file)
                break

    def play_all(self) -> None:
        for af in self.editor:
            print(af.file)


class Cropping:  #this is where the audio file is cropped
    def __init__(self, audio: AudioEditor):
        self.editor: list[AudioFile] = audio.audio_files

    def crop(self, name_file: str) -> str:
        for af in self.editor:
            if af.name_file == name_file:
                result: str = af.file.split("-", 1)[-1]
                return result #before "la-la-la", after "la-la"


class Continuation:  #here you can "continue" the audio
    def __init__(self, audio: AudioEditor):
        self.editor: list[AudioFile] = audio.audio_files

    def proceed(self, name_file: str) -> str:
        for af in self.editor:
            if af.name_file == name_file:
                verse: str = af.file.split("-", 1)[0]
                result: str = af.file + "-" + verse
                return result #before "Uc-Uc", after "Uc-Uc-Uc"


class Mix:  #You can mix audio files here
    def __init__(self, audio: AudioEditor):
        self.editor: list[AudioFile] = audio.audio_files

    def connect(self, name_file1: str, name_file2: str) -> str:  #just by combining them
        for af1 in self.editor:
            for af2 in self.editor:
                if af1.name_file == name_file1 and af2.name_file == name_file2:
                    result: str = af1.file + "-" + af2.file
                    return result  #before "La-La" and "Uc-Uc", after "La-La-Uc-Uc"

    def remix(self, name_file1: str, name_file2: str) -> str:  #or making a remix
        count: int = 0  #WARNING: The remix function only works with files of the same duration
        for af1 in self.editor:
            for af2 in self.editor:
                if af1.name_file == name_file1 and af2.name_file == name_file2:
                    verse1: str = af1.file.split("-", 1)[0]
                    verse2: str = af2.file.split("-", 1)[0]
                    result: str = verse1 + "-" + verse2
                    while count != af1.duration - 1:
                        result += "-" + result
                        count += 1
                    return result  #before "La-La" and "Uc-Uc", after "La-Uc-La-Uc"

class Effects(AudioFile):
    def __init__(self, name_file: str, author: str, duration: int, file: str, effect: str):
        super().__init__(name_file, author, duration, file)
        self.effect = effect