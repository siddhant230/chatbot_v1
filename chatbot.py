import json
import joblib
import random
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer


class ChatModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.load_chat_models()
        self.stemmer = LancasterStemmer()
        print("Chatbot model loaded successfully")

    def load_chat_models(self):
        with open(f'{self.model_path}/intents2.json') as f:
            self.data = json.load(f)
        self.model = joblib.load(f'{self.model_path}/chat_bot.pkl')
        self.words = joblib.load(f'{self.model_path}/words.pkl')
        self.labels = joblib.load(f'{self.model_path}/labels.pkl')

    def bag_of_words(self, text):
        bag = [0 for _ in range(len(self.words))]

        s_words = nltk.word_tokenize(text)
        s_words = [self.stemmer.stem(w.lower()) for w in s_words]

        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1
        return bag

    def reply(self, text_inp):
        res = 'I am sorry, I cannot answer that...'
        result = self.model.predict([self.bag_of_words(text_inp)])
        result_ind = np.argmax(result)
        tag = self.labels[result_ind]
        for tg in self.data['intents']:
            if tg['tag'] == tag:
                res = tg['responses']
        response = random.choice(res)
        return response
