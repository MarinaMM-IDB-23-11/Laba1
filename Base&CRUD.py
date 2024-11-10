class AudioFile:
    def __init__(self, name_file: str, author: str, duration: int, file: str):
        self.name_file = name_file
        self.author = author
        self.duration = duration #the duration of the file playback in minutes
        self.file = file #audio simulation

class AudioEditor: #CRUD
    def __init__(self):
        self.audio_files = [] #type AudioFile

    def create_audio_file(self, audiofile): #create
        self.audio_files.append(audiofile)

    def read_audio_file(self, name_file: str): #read by name
        for af in self.audio_files:
            if af.name_file == name_file: #Another class is responsible for the "playback" of the file
                print (f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")
                break

    def read_all_audio_files(self): #read all files
        for af in self.audio_files:
            print(f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")

    def update_audio_file(self, name_file: str): #update
        for af in self.audio_files:
            if af._name_file == name_file:
                af._name_file = input("Enter the name of the audio: ")
                af._author = input("Enter the author`s name: ")

    def delete_audio_file(self, name_file: str): #delete
        for af in self.audio_files:
            if af.name_file == name_file:
                self.audio_files.remove(af)
                break




