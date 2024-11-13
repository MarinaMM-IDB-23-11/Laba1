import xml.etree.ElementTree as ET

from typing import Union


class AudioFile:
    def __init__(self, name_file: str, author: str, duration: int, file: str):
        self.name_file: str = name_file
        self.author: str = author
        self.duration: int = duration  # the duration of the file playback in minutes
        self.file: str = file  # audio simulation

    def to_dict(self) -> dict[str, any]:  # converting an object to JSON format
        return {
            "type": "AudioFile",
            "name_file": self.name_file,
            "author": self.author,
            "duration": self.duration,
            "file": self.file
        }

    def to_xml(self) -> ET.Element:  # translation to XML format
        audio_elem: ET.Element = ET.Element("AudioFile")
        ET.SubElement(audio_elem, "name_file").text = self.name_file
        ET.SubElement(audio_elem, "author").text = self.author if self.author else ""
        ET.SubElement(audio_elem, "duration").text = str(self.duration)
        ET.SubElement(audio_elem, "file").text = self.file
        return audio_elem


class AudioEditor:  # CRUD
    def __init__(self):
        self.audio_files: list[Union[AudioFile, Effects]] = []

    def create_audio_file(self, audiofile: AudioFile) -> None:  # create
        self.audio_files.append(audiofile)

    def read_audio_file(self, name_file: str) -> None:  # read by name
        for af in self.audio_files:
            if af.name_file == name_file:  # Another class is responsible for the "playback" of the file
                print(f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")
                break
        print("No such audiofile.")

    def read_all_audio_files(self) -> None:  # read all files
        if not self.audio_files:  # Checking for audio files
            print("No audio files available.")
            return
        for af in self.audio_files:
            print(f"Name: {af.name_file}. Author: {af.author}. Duration: {af.duration} minutes")

    def update_audio_file(self, name_file: str) -> None:  # update
        for af in self.audio_files:
            if af.name_file == name_file:
                af.name_file = input("Enter the name of the audio: ")
                af.author = input("Enter the author`s name: ")
                return
        print("No such audiofile.")

    def delete_audio_file(self, name_file: str) -> None:  # delete
        for af in self.audio_files:
            if af.name_file == name_file:
                self.audio_files.remove(af)
                return
        print("No such audiofile.")


class Effects(AudioFile):  # here you can apply an audio effect to a file
    def __init__(self, name_file: str, author: str, duration: int, file: str, effect: str):
        super().__init__(name_file, author, duration, file)
        self.effect: str = effect

    def to_dict(self) -> dict[str, any]:  # converting an object to JSON format
        return {
            "type": "Effect",
            "name_file": self.name_file,
            "author": self.author,
            "duration": self.duration,
            "file": self.file,
            "effect": self.effect
        }

    def to_xml(self) -> ET.Element:  # translation to XML format
        effect_elem: ET.Element = super().to_xml()
        ET.SubElement(effect_elem, "effect").text = self.effect
        return effect_elem
