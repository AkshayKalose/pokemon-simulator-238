from Tkinter import *
import threading

class GUI(threading.Thread):
    def __init__(self):
        self.ready = False
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def action(self, a):
        self.selectedAction = a

    def setPlayer(self, pokemonName, hp):
        self.playerPokemonName.set(pokemonName)
        self.playerPokemonHP.set(hp)

    def setOpponent(self, pokemonName, hp):
        self.opponentPokemonName.set(pokemonName)
        self.opponentPokemonHP.set(hp)

    def setActionText(self, action, text):
        self.actionText[action].set(text)

    def getAction(self):
        self.selectedAction = None
        while self.selectedAction is None:
            continue
        return self.selectedAction

    def waitUntilReady(self):
        while not self.ready:
            continue

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('Pokemon Simulator')
        self.root.geometry('500x500')

        self.opponentInfo = Frame(self.root).grid(row=0, column=0)
        Label(self.opponentInfo, text="Opponent's Pokemon: ").grid(row=0, column=0, sticky=W)
        self.opponentPokemonName = StringVar()
        Label(self.opponentInfo, textvariable=self.opponentPokemonName).grid(row=0, column=1, sticky=W)
        Label(self.opponentInfo, text="HP: ").grid(row=0, column=2, sticky=W)
        self.opponentPokemonHP = StringVar()
        Label(self.opponentInfo, textvariable=self.opponentPokemonHP).grid(row=0, column=3, sticky=W)

        self.playerInfo = Frame(self.root).grid(row=2, column=0)
        Label(self.playerInfo, text="Player's Pokemon: ").grid(row=2, column=0, sticky=W)
        self.playerPokemonName = StringVar()
        Label(self.playerInfo, textvariable=self.playerPokemonName).grid(row=2, column=1, sticky=W)
        Label(self.playerInfo, text="HP: ").grid(row=2, column=2, sticky=W)
        self.playerPokemonHP = StringVar()
        Label(self.playerInfo, textvariable=self.playerPokemonHP).grid(row=2, column=3, sticky=W)

        self.actions = Frame(self.root).grid(row=4, column=0, sticky=W)
        self.actionText = [StringVar() for _ in range(4)]
        Button(self.actions, textvariable=self.actionText[0], width=15, command=lambda: self.action(0)).grid(row=4, column=0, sticky=W)
        Button(self.actions, textvariable=self.actionText[1], width=15, command=lambda: self.action(1)).grid(row=4, column=1, sticky=W)
        Button(self.actions, textvariable=self.actionText[2], width=15, command=lambda: self.action(2)).grid(row=4, column=2, sticky=W)
        Button(self.actions, textvariable=self.actionText[3], width=15, command=lambda: self.action(3)).grid(row=4, column=3, sticky=W)

        self.ready = True
        self.root.mainloop()
