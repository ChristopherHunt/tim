import json
from os import listdir
from os.path import isfile, join

## Enter directory of drafts dump
path_of_drafts = './training_drafts'

## Open each draft file and scrape the lines beginning with '--> '
def scrape_drafts(files):
    drafted_decks = []
    # open the text file
    print len(files)
    for item in files:
        with open(path_of_drafts + '/' + item, 'r') as file_in:
            deck = []
            for line in file_in.readlines():
                if line[:4] == '--> ':
                    card = line[4:]
                    deck.append(card)
        drafted_decks.append(deck)
    return drafted_decks

def to_json_dump(to_dump):
    json.dumps(to_dump)

## Gets list of files in "path_of_drafts"
## Scrape drafts for cards picked
## Send to NN...? Come back to this.
def main():
    files = [f for f in listdir(path_of_drafts) if isfile(join(path_of_drafts, f))]
    to_dump = scrape_drafts(files)
    to_json_dump(to_dump)

if __name__ == '__main__':
    main()
