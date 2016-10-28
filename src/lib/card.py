#!/usr/bin/python3

class Card:
    'Represents a simplified card in Magic the Gathering.'

    ## Construct a Magic the Gathering Card where the input variables are of the
    ## form:
    ##  name = a string representing the card name
    ##  colors = a dictionary of 'color -> bool', where the colors are
    ##           white, blue, black, red, green and colorless. If a card is of
    ##           a given color then the boolean is true.
    ##  rarity = the card's rarity (common, uncommon, rare)
    ##  rank = the card's rank relative to the others in its set 
    ##  number = the card's number in the set
    def __init__(self, name, colors, rarity, rank, number):
        self.name = name
        self.colors = dict(colors) ## Makeing a deep copy here
        self.rarity = rarity
        self.rank = rank
        self.number = number

    def __str__(self):
        toString = '{\n name: ' + str(self.name)
        toString += '\n' + ' rarity: ' + self.rarity
        toString += '\n' + ' colors: ' 

        if self.colors['White'] == True:
            toString += 'W'
        if self.colors['Blue'] == True:
            toString += 'U'
        if self.colors['Black'] == True:
            toString += 'B'
        if self.colors['Red'] == True:
            toString += 'R'
        if self.colors['Green'] == True:
            toString += 'G'
        if self.colors['Colorless'] == True:
            toString += 'C'

        toString += '\n' + ' rank: ' + str(self.rank)
        toString += '\n' + ' number: ' + str(self.number) + '\n' + '}'
        return toString
