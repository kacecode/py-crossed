# PurpleState
# Word Search

import sys

# Unit class definition
class Unit:
    def __init__(self, y, x, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        tempString = self.value + " at: " + str(self.y) + ", " + str(self.x)
        return tempString
# END Unit class definition

# WordPuzzle class definition
class WordPuzzle:
    def __init__(self):
        self.puzzle = []

    def __str__(self):
        collector = ""
        for row in self.puzzle:
            for char in row:
                collector += char
            collector += "\n"
        return collector

    def setSize(self, size):
        self.size = size

    def buildPuzzle(self, row):
        temp = []
        for char in row:
            temp.append(char)
        self.puzzle.append(temp)

    def getUnit(self, y, x):
        try:
            tempUnit = Unit(y, x, self.puzzle[y][x])
            return tempUnit
        except IndexError:
            return None

    def substring(self, word, current, func):
        string = ""
        lastLoc = None
        for i in range(0, len(word)):
            temp = func(current, i)
            if temp is not None:
                string += temp.value
                lastLoc = (temp.y, temp.x)
            else:
                return False

        return (string, lastLoc)


    def NW(self, current, offset):
        return self.getUnit(current.y - offset, current.x - offset)            

    def N(self, current, offset):
        return self.getUnit(current.y - offset, current.x) 

    def NE(self, current, offset):
        return self.getUnit(current.y - offset, current.x + offset) 

    def E(self, current, offset):
        return self.getUnit(current.y, current.x + offset) 

    def SE(self, current, offset):
        return self.getUnit(current.y + offset, current.x + offset) 

    def S(self, current, offset):
        return self.getUnit(current.y + offset, current.x) 

    def SW(self, current, offset):
        return self.getUnit(current.y + offset, current.x - offset) 

    def W(self, current, offset):
        return self.getUnit(current.y, current.x - offset) 

    def find(self, word):
        functions = [self.NW, self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W]
        for row in range(0, self.size):
            for char in range (0, self.size):
                tempUnit = self.getUnit(row, char)
                
                for fun in functions:
                    holder = self.substring(word, tempUnit, fun)
                    if holder is not False and holder[0] == word:
                        return (True, {word: { "start": (tempUnit.y, tempUnit.x), "end": ( holder[1])}})

        return False; # Not found

        
# END WordPuzzle class definition

def getPuzzle(filePath):
    try:
        with open(filePath, "rU") as puzzleInput:
            puzzle = WordPuzzle()
            feed = puzzleInput.readline()
            feed = (feed.strip())
            puzzle.setSize(len(feed))
            puzzle.buildPuzzle(feed)

            for i in range(1, puzzle.size):
                puzzle.buildPuzzle(puzzleInput.readline().strip())

            tests = []
            dataReturned = True
            if feed == "":
                dataReturned = False
            
            while(dataReturned):
                feed = puzzleInput.readline()
                if feed == "":
                    dataReturned = False
                elif feed == "\n":
                    pass
                else:
                    tests.append(feed.strip())

            return (puzzle, tests)
    except IOError, e:
        print e

# !!! ENTRY POINT !!!
def main(argv = None):
    if argv is None:
        argv = sys.argv #get system passed arguments
        passedArgs = argv[1:] #strip execution call

        for arg in passedArgs: #loop passed args
            puzzle = getPuzzle(arg)
            print puzzle[0]

            for word in puzzle[1]:
                found = puzzle[0].find(word)
                if found is False:
                    print word, "not found"
                else:
                    print word, "found at", found[1][word]

            print "==============================="

if __name__ == '__main__':
        sys.exit(main())
