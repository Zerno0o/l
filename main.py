import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator
from collections import defaultdict

def self():
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        self.words = {
        "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
        "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
        "hard": ["технология", "университет", "информация", "произношение", "воображение"]}
        self.scores = defaultdict(int)
        self.current_level = 'easy'
        self.lives = 3
        self.recognizer = sr.Recognizer()
         
    
    def select_level(self):
        self.speak("\nВыберите уровень сложности:")
        self.speak("1 - Легкий")
        self.speak("2 - Средний")
        self.speak("3 - Сложный")
        
        
        choice = self.listen()
        if '1' in choice or 'легк' in choice:
            self.current_level = 'easy'
        elif '2' in choice or 'средн' in choice:
            self.current_level = 'medium'
        elif '3' in choice or 'сложн' in choice:
            self.current_level = 'hard'
        else:
            self.speak("Неверный ввод, попробуйте снова.")
        return True
    duration = 5  # секунды записи
    sample_rate = 44100

    print("Говори...")
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

wav.write("output.wav", sample_rate, recording)
print("Запись завершена, теперь распознаём...")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

    def play_round(self):
        if not self.words[self.current_level]:
            self.speak("В этом уровне больше нет слов для изучения!")
            return True
        
        word, translation = random.choice(list(self.words[self.current_level].items()))
        
        self.speak(f"\nПереведите слово: {word}")
        self.speak("Повторите слово после сигнала")
        
        user_translation = self.listen()
        
        if user_translation and translation.lower() in user_translation:
            self.speak("Правильно! 👍")
            self.scores[self.current_level] += 1
            del self.words[self.current_level][word]
        else:
            self.speak(f"Неверно. Правильный перевод: '{translation}'")
            self.lives -= 1
            self.speak(f"У вас осталось {self.lives} жизней")
        
        return self.lives > 0
    
    def show_stats(self):
        self.speak("\nВаши результаты:")
        for level, score in self.scores.items():
            self.speak(f"{level.capitalize()}: {score} правильных ответов")
    
    def run(self):
        self.speak("Добро пожаловать в голосовую игру для изучения языков!")
        self.speak("Попробуйте перевести слова с английского на русский.")
        self.speak("У вас есть 3 жизни. После 3 ошибок игра закончится.")
        
        while True:
            if not self.select_level():
                break
            
            self.speak(f"\nУровень: {self.current_level.capitalize()}")
            if not self.play_round():
                self.speak("\nИгра окончена! Вы исчерпали все жизни.")
                break
            
            cont = self.listen()
            if 'нет' in cont or 'хватит' in cont or 'стоп' in cont:
                break
        
        self.show_stats()
        self.speak("Спасибо за игру! До свидания!")
