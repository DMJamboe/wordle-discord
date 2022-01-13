from discord import User
from discord import DMChannel
from datetime import datetime
from datetime import timezone
from enum import Enum, auto
from wordmanager import WordManager

class Guess(Enum):
    WRONG = auto(),
    WRONGPOS = auto(),
    RIGHTPOS = auto()

    def getEmoji(guess: "Guess") -> str:
        if guess == Guess.WRONG:
            return "⬛"
        if guess == Guess.WRONGPOS:
            return "🟨"
        if guess == Guess.RIGHTPOS:
            return "🟩"


class Game:
    def __init__(self, user: User, word: str, maxRounds: int):
        self.user: User = user
        self.word: str = word
        self.startTime: datetime = datetime.now()
        self.maxRounds: int = maxRounds
        self.guesses: list[str] = []

    def isLost(self) -> bool:
        return len(self.guesses) >= self.maxRounds and self.word not in self.guesses

    def makeGuess(self, guess: str) -> "optional[list[Guess]]":
        if len(guess) != len(self.word):
            return None

        guessValidity = []
        for index, letter in enumerate([char for char in guess]):
            if self.word[index] == letter:
                guessValidity.append(Guess.RIGHTPOS)
            elif letter in self.word:
                guessValidity.append(Guess.WRONGPOS)
            else:
                guessValidity.append(Guess.WRONG)

        self.guesses.append(guess)
        return guessValidity

class GameManager:
    active_games: list[Game] = []

    @staticmethod
    def getGame(user: User) -> "optional[User]":
        userGames = list(filter(lambda game: game.user == user, GameManager.active_games))
        return userGames[0]

    @staticmethod
    def hasGame(user: User) -> bool:
        userGames = list(filter(lambda game: game.user == user, GameManager.active_games))
        return len(userGames) > 0

    @staticmethod
    async def createGame(user: User, daily: bool = False) -> "Optional[User]":
        if GameManager.hasGame(user):
            return None
        else:
            newgame = Game(user, WordManager.getRandomWord(), 5)
            GameManager.active_games.append(newgame)
            dmchannel = user.dm_channel
            if dmchannel is None:
                dmchannel = await user.create_dm()
            await dmchannel.send("Game started\nUse `!guess <word>` to make a guess\nWord: " + newgame.word)
            return newgame

    @staticmethod
    def gameEnd(game: Game):
        GameManager.active_games.remove(game)