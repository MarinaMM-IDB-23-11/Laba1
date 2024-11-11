import json
import xml.etree.ElementTree as ET
from typing import Union
from xml.dom import minidom

from Base_CRUD import AudioEditor, AudioFile, Effects

class JSONSerializer:
    def __init__(self, editor: AudioEditor):
        self.json_editor = editor

    def save_to_json(self, filename: str) -> None: #serialization
        with open(filename, 'w') as json_file:
            json.dump([audio.to_dict() for audio in self.json_editor.audio_files], json_file, indent=4)

    def load_from_json(self, filename: str) -> AudioEditor: #deserialization
        with open(filename, 'r') as json_file:
            audio_files_data: list[dict[str, any]] = json.load(json_file)

            for data in audio_files_data:
                # Deleting the "type" field before creating the object
                audio_type: Union[str, None] = data.pop("type", None)  # We delete the "type", if there is one

                if audio_type == "Effect":
                    audio_file = Effects(**data)  # Creating an Effect object
                else:
                    audio_file = AudioFile(**data)
                self.json_editor.create_audio_file(audio_file)
        return self.json_editor

class XMLSerializer:
    def __init__(self, editor: AudioEditor):
        self.xml_editor = editor

    def save_to_xml(self, filename: str) -> None: #serialization
        root = ET.Element("AudioFilesXML.xml")

        for audio in self.xml_editor.audio_files:
            root.append(audio.to_xml())

        # Creating a tree
        pretty_xml = self.prettify(root)

        # We write it to a file
        with open(filename, "w", encoding='utf-8') as f:
            f.write(pretty_xml)

    def load_from_xml(self, filename: str) -> AudioEditor: #deserialization
        tree = ET.parse(filename)
        root = tree.getroot()

        for audio_elem in root.findall('AudioFile'):
            if audio_elem.find('effect') is not None:
                audio_file = Effects(
                    name_file=audio_elem.find('name_file').text,
                    author=audio_elem.find('author').text or None,
                    duration=int(audio_elem.find('duration').text),
                    file=audio_elem.find('file').text,
                    effect=audio_elem.find('effect').text
                )
            else:
                audio_file = AudioFile(
                    name_file=audio_elem.find('name_file').text,
                    author=audio_elem.find('author').text or None,
                    duration=int(audio_elem.find('duration').text),
                    file=audio_elem.find('file').text
                )
            self.xml_editor.create_audio_file(audio_file)
        return self.xml_editor

    @staticmethod
    def prettify(elem: ET.Element) -> str:
        """Format XML with indentation."""
        # Converting an element to a string
        rough_string = ET.tostring(elem, 'utf-8')
        # Parse the string and create a beautiful output
        repairs = minidom.parseString(rough_string)
        return repairs.toprettyxml(indent="  ")