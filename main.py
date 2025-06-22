import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import os
from time import sleep

# Настройки аудио
duration = 5  # секунды записи
sample_rate = 44100

# Инициализация
recognizer = sr.Recognizer()
score = 0
mistakes = 0
max_mistakes = 3
highscore_file = "highscore.txt"

# Словарь слов по уровням сложности (русский: английский)
words = {
    "easy": {
        "яблоко": "apple",
        "кот": "cat",
        "собака": "dog",
        "дом": "house",
        "книга": "book",
        "солнце": "sun",
        "вода": "water"
    },
    "medium": {
        "огонь": "fire",
        "дерево": "tree",
        "город": "city",
        "работа": "work",
        "школа": "school",
        "учеба": "study",
        "деньги": "money"
    },
     "hard": {
        "достопримечательность": "attraction",
        "эксперимент": "experiment",
        "исследование": "research",
        "технология": "technology",
        "государство": "state",
        "окружающая среда": "environment",
        "взаимодействие": "interaction"
    }
}

def record_audio():
    """Запись аудио с микрофона"""
    print("Говорите сейчас...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return audio
def save_and_recognize(audio):
    """Сохраняет аудио и распознает речь"""
    temp_file = "temp.wav"
    wav.write(temp_file, sample_rate, audio)
    
    with sr.AudioFile(temp_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            print(f"Вы сказали: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Речь не распознана")
            return None
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def load_highscore():
    """Загружает рекорд из файла"""
    if os.path.exists(highscore_file):
        with open(highscore_file, 'r') as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(new_score):
    """Сохраняет новый рекорд"""
    with open(highscore_file, 'w') as f:
        f.write(str(new_score))

def select_level():
    """Выбор уровня сложности"""
    print("\nВыберите уровень сложности:")
    print("1 - Легкий (Easy)")
    print("2 - Средний (Medium)")
    print("3 - Сложный (Hard)")
    
    while True:
        choice = input("Ваш выбор (1-3): ")
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            print("Неверный ввод, попробуйте снова")

def play_game(level):
    global score, mistakes
    
    level_words = words[level]
    if not level_words:
        print("В этом уровне нет доступных слов!")
        return False

    # Выбираем случайное слово из выбранного уровня
    russian_word, correct_translation = random.choice(list(level_words.items()))
    
    print(f"\nПереведите слово: '{russian_word}'")
    print("Запись через 1 секунду...")
    sleep(1)
    
    # Записываем и распознаем ответ
    audio = record_audio()
    user_answer = save_and_recognize(audio)
    
    if user_answer is None:
        print("Попробуйте еще раз")
        return True
    
    # Проверяем ответ
    if user_answer == correct_translation:
        print("Правильно! 👍")
        score += 1
    else:
        print(f"Неверно. Правильный ответ: '{correct_translation}'")
        mistakes += 1
        print(f"Ошибок: {mistakes}/{max_mistakes}")
    
    print(f"Счет: {score}")
    return mistakes < max_mistakes

if __name__ == "__main__":
    print("Добро пожаловать в игру 'Переводчик'!")
    print(f"У вас есть {max_mistakes} попытки. После {max_mistakes} ошибок игра закончится.")
    
    highscore = load_highscore()
    print(f"Текущий рекорд: {highscore}")
    
    while True:
        level = select_level()
        print(f"\nВыбран уровень: {level.capitalize()}")
        
        # Сброс счетчиков для новой игры
        score = 0
        mistakes = 0

        while play_game(level):
            continue
        
        # Конец игры
        print("\nИгра окончена!")
        print(f"Ваш результат: {score}")
        
        if score > highscore:
            print("Новый рекорд! 🎉")
            save_highscore(score)
            highscore = score
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if play_again != 'да':
            break
    
    print("Спасибо за игру! До свидания!")
