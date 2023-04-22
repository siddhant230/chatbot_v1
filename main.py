import os
import time
import warnings
import wikipedia
from gtts import gTTS
import speech_recognition as sr
from TTS.api import TTS
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
import nltk

from loader import LoadEntities
from chatbot import ChatModel

warnings.filterwarnings('ignore')


class ChatBot(LoadEntities):
    def __init__(self,
                 credentials_path="configs/credentials.json",
                 config_path="configs/config.json",
                 model_path="models/generic",
                 speaker="tts"):
        super(ChatBot, self).__init__(
            credentials_path, config_path,
            speaker)
        if speaker == "pyttsx":
            self.speed = self.config[speaker]["voice_speed"]
        nltk.download('punkt')
        self.chat_model = ChatModel(model_path)
        print("All files imported!")

    def weather(self, commands):
        query = ' '.join(commands)
        self.speak("Searching for {}".format(query))
        result = self.wlf_alpha_client.query(query)
        opt = next(result.results).text
        self.speak(opt)

    def play_song(self, commands):
        id = 'https://www.soundcloud.com/search/sounds?q='
        driver = webdriver.Chrome(options=self.options)
        name = '%20'.join(commands[1:])
        print(id+name)
        driver.get(id+name)
        try:
            driver.find_element(By.CLASS_NAME, 'search__empty')
            self.speak('No such song found sir,Try again...')
            driver.quit()
        except:
            button = driver.find_element(By.XPATH,
                                         '//*[@id="content"]/div/div/div[3]/div/div/div/ul/li[1]/div/div/div/div[2]/div[1]/div/div/div[1]')

            button.click()

    def search_command(commands):
        print(commands)
        if 'joke' in commands:
            query = 'tell me a joke'
            result = client.query(query)
            opt = next(result.results).text
            print(opt)
            opt = opt.split('(')[0]
        else:
            speak('searching...')
            if 'what' not in commands:
                query = ' '.join(commands[1:])
            else:
                query = ' '.join(commands)
            try:
                try:
                    "BOT : Sure Sir!\nSearching for {}".format(query)
                    speak("Searching for {}".format(query))
                    result = client.query(query)
                    opt = next(result.results).text
                    speak("Here is what I found\nInternet says...")
                    speak(opt)
                except:
                    result = wikipedia.summary(query, sentences=3)
                    speak("Here is what I found\nAccording to Wikipedia...")
                    speak(result)
            except:
                browser = webdriver.Chrome(options=options)
                speak("Here is what I found on Google...")
                browser.get("https://www.google.com/search?q=" +
                            query + "&start=" + str(10 * 0))

    def run_command(self, commands):
        self.speak('Opening {}'.format(' '.join(commands[1:])))
        driver = webdriver.Chrome(options=self.options)
        site = commands[-1]
        desc = " ".join(commands[:-2])
        url = 'https://www.{}.com'.format(site)
        print(url)
        driver.get(url)
        time.sleep(200)

    def search_command(self, commands):
        if 'joke' in commands:
            query = 'tell me a joke'
            result = self.wlf_alpha_client.query(query)
            opt = next(result.results).text
            self.speak(opt)
            opt = opt.split('(')[0]
        else:
            self.speak('searching...')
            if 'what' not in commands:
                query = ' '.join(commands[1:])
            else:
                query = ' '.join(commands)
            try:
                try:
                    "BOT : Sure Sir!\nSearching for {}".format(query)
                    self.speak("Searching for {}".format(query))
                    result = self.wlf_alpha_client.query(query)
                    opt = next(result.results).text
                    self.speak("Here is what I found\nInternet says...")
                    self.speak(opt)
                except:
                    result = wikipedia.summary(query, sentences=3)
                    self.speak(
                        "Here is what I found\nAccording to Wikipedia...")
                    self.speak(result)
            except:
                browser = webdriver.Chrome(options=self.options)
                self.speak("Here is what I found on Google...")
                browser.get("https://www.google.com/search?q=" +
                            query + "&start=" + str(10 * 0))

    def speak(self, text):
        print('BOT : '+text)
        if self.speaker == "pyttsx":
            self.engine.say(text)
            self.engine.runAndWait()
        elif self.speaker == "gtts":
            gtts_obj = self.engine(text=text, lang="en",
                                   slow=False, tld="com.au")
            gtts_obj.save("test.mp3")
            playsound('test.mp3')
            os.remove("test.mp3")
        else:
            self.engine.tts_to_file(
                text=text, speaker=self.engine.speakers[5],
                language=self.engine.languages[0], file_path="test.mp3")
            playsound('test.mp3')
            os.remove("test.mp3")

    def listen(self):
        transcription = ""
        tolerance = 5
        while transcription == "":
            if tolerance <= 0:
                break
            tolerance += 1
            with sr.Microphone() as source:
                time.sleep(1)
                self.speech_recognizer.adjust_for_ambient_noise(
                    source, duration=1)

                self.speak('How can I help?')
                audio = self.speech_recognizer.listen(source)
                try:
                    transcription = self.speech_recognizer.recognize_google(
                        audio)
                    print(transcription)
                    # self.speak("I think you said " + transcription)
                except:
                    error_message = "I can't understand what you said sir,Please try again..."
                    self.speak(error_message)
        if transcription != "":
            self.perform_actions(transcription)
        if "quit" in transcription:
            return True
        return False

    def perform_actions(self, text):
        print('YOU : {}'.format(text))
        commands = text.split(' ')
        for i in range(len(commands)):
            commands[i] = commands[i].lower()
        if 'speak' in commands and 'fast' in commands:
            self.speak('Speeding myself up!!')
            self.speed = min(600, 50+self.speed)
            self.engine.setProperty('rate', self.speed)
        # elif ('email' in commands and 'write' in commands) or neg == -1:
        #     write_email(commands)
        elif 'speak' in commands and 'slow' in commands:
            self.speak('Slowing myself down!!')
            self.speed = max(50, abs(50-self.speed))
            self.engine.setProperty('rate', self.speed)
        elif 'speech' in commands and 'reset' in commands:
            self.speak(
                f'resetting my speed to {self.config[self.speaker]["voice_speed"]}')
            self.speed = self.config[self.speaker]["voice_speed"]
            self.engine.setProperty('rate', self.speed)
        elif 'wait' in commands:
            self.speak('I am waiting...')
            time.sleep(5)
            self.speak('I waited for 5 seconds...')
        elif 'fuck' in commands:
            self.speak('denge pel khatam ho jayga khel...')
            self.speak(
                'Please atleast talk good, kharaab to apki shakal bhi hai...(#offence Intended)')
        elif 'weather' in commands:
            self.weather(commands)
        elif 'play' in commands:
            self.play_song(commands)
        elif 'open' in commands or 'run' in commands:
            self.run_command(commands)
        elif 'search' in commands or 'joke' in commands:
            self.search_command(commands)
        else:
            if "quit" in text:
                text = "bye"
            response = self.chat_model.reply(text)
            self.speak(response)


if __name__ == "__main__":
    chat_obj = ChatBot(speaker="pyttsx")
    chat_obj.speak("Hi there! I am Steve")

    quit = False
    while not quit:
        quit = chat_obj.listen()
