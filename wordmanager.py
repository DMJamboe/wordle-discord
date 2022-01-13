# manages word gen
import random

class WordManager:
    words = []
    loaded = False

    @staticmethod
    def loadWords(file: str):
        with open(file, "r+") as f:
            readwords = f.readlines()
            WordManager.words = [word.strip() for word in readwords]
        WordManager.loaded = True
    
    @staticmethod
    def getRandomWord() -> str:
        if not WordManager.loaded:
            WordManager.loadWords("words-five.txt")
        return random.choice(WordManager.words)
    
    def containsWord(word: str) -> bool:
        if not WordManager.loaded:
            WordManager.loadWords("words-five.txt")
        return word in WordManager.words