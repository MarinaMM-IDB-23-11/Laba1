import xml.etree.ElementTree as ET

from typing import Union

class AudioFile:
    def __init__(self, name_file: str, author: str, duration: int, file: str):
        self.name_file = name_file
        self.author = author
        self.duration = duration #the duration of the file playback in minutes
        self.file = file #audio simulation

    def to_dict(self) -> dict[str, any]:
        return {
            "type": "AudioFile",
            "name_file": self.name_file,
            "author": self.author,
            "duration": self.duration,
            "file": self.file
        }

    def to_xml(self) -> ET.Element:
        audio_elem = ET.Element("AudioFile")
        ET.SubElement(audio_elem, "name_file").text = self.name_file
        ET.SubElement(audio_elem, "author").text = self.author if self.author else ""
        ET.SubElement(audio_elem, "duration").text = str(self.duration)
        ET.SubElement(audio_elem, "file").text = self.file
        return audio_elem

class AudioEditor: #CRUD
    def __init__(self):
        self.audio_files: list[Union[AudioFile, Effects]] = []

    def create_audio_file(self, audiofile: AudioFile) -> None: #create
        self.audio_files.append(audiofile)

    def read_audio_file(self, name_file: str) -> None: #read by name
        for af in self.audio_files:
            if af.name_file == name_file: #Another class is responsible for the "playback" of the file
                print (f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")
                break

    def read_all_audio_files(self) -> None: #read all files
        for af in self.audio_files:
            print(f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")

    def update_audio_file(self, name_file: str) -> None: #update
        for af in self.audio_files:
            if af._name_file == name_file:
                af._name_file = input("Enter the name of the audio: ")
                af._author = input("Enter the author`s name: ")

    def delete_audio_file(self, name_file: str) -> None: #delete
        for af in self.audio_files:
            if af.name_file == name_file:
                self.audio_files.remove(af)
                break

class Effects(AudioFile):
    def __init__(self, name_file: str, author: str, duration: int, file: str, effect: str):
        super().__init__(name_file, author, duration, file)
        self.effect = effect

    def to_dict(self) -> dict [str, any]:
        return {
            "type": "Effect",
            "name_file": self.name_file,
            "author": self.author,
            "duration": self.duration,
            "file": self.file,
            "effect": self.effect
        }

    def to_xml(self) -> ET.Element:
        effect_elem = super().to_xml()
        ET.SubElement(effect_elem, "effect").text = self.effect
        return effect_elem