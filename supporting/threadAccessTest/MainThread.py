import threading
from ChildThread import childThread

weWantThisVariableToChange = [1, 2]
print(f'before childThread is run: {weWantThisVariableToChange}')

childThreadThread = childThread(weWantThisVariableToChange)
childThreadThread.start()
childThreadThread.join()

print(f'after childThread is run: {weWantThisVariableToChange}')

weWantThisVariableToChange[0] = 'change'
weWantThisVariableToChange[1] = 'me back'

print(f'just updated this from main: {weWantThisVariableToChange}')

childThreadThreadAgain = childThread(weWantThisVariableToChange)
childThreadThreadAgain.start()
childThreadThreadAgain.join()

print(f'after childThread is run again: {weWantThisVariableToChange}')






