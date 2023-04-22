import json
import joblib
import pyttsx3
import wolframalpha
from selenium import webdriver
from gtts import gTTS
import speech_recognition as sr
from TTS.api import TTS


class LoadEntities:
    def __init__(self, credentials_path, config_path,
                 speaker):
        self.config = json.load(open(config_path, "r"))
        self.credentials = json.load(open(credentials_path, "r"))

        self.speaker = speaker
        print(self.config)
        print(self.credentials)
        self.load_speaker()
        print("Speaker loaded! :", self.speaker)
        self.wlf_alpha_client = wolframalpha.Client(
            self.credentials["wolfram-alpha"])
        print("loaded wolfram-alpha client")
        self.speech_recognizer = sr.Recognizer()
        self.options = webdriver.ChromeOptions()

    def load_speaker(self):
        if self.speaker == "pyttsx":
            self.engine = pyttsx3.init()
            self.voice_list = self.engine.getProperty('voices')
            self.set_configurations()
        elif self.speaker == "gtts":
            self.engine = gTTS
        else:
            self.engine = TTS(TTS.list_models()[0])

    def set_configurations(self):
        self.engine.setProperty(
            'voices', self.voice_list[self.config[self.speaker]["voice_type"]].id)
        self.engine.setProperty(
            'rate', self.config[self.speaker]["voice_speed"])
