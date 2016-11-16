from os import listdir
from os.path import isfile, join

## Enter directory of drafts dump
path_of_drafts = '../../data/kaladesh/scraped_drafts'

## Open each draft file and scrape the lines beginning with '--> '
def scrape_drafts(files):
    drafted_decks = []
    # open the text file
    # print len(files)
    for item in files:
        with open(path_of_drafts + '/' + item, 'r') as file_in:
            deck = []
            for line in file_in.readlines():
                if line[:4] == '--> ':
                    card = line[4:]
                    deck.append(card)
                if "------ KLD ------ " in line:
                    card = line
                    deck.append(card)
        drafted_decks.append(deck)
    return drafted_decks

## Write each drafted deck on a line in a text file.
def write_to_file(drafts):
    for draft in drafts:
        with open('all_drafts.txt', 'a') as file_in:
            for card in draft:
                if "------ KLD ------ " in card:
                    file_in.write('\n')
                    continue
                if (card[:3] != 'Bot'):
                    f_card = card.replace(' ', '_')
                    f_card = f_card.replace('\n', '')
                    # print(f_card)
                    file_in.write(f_card + ' ')
            file_in.write('\n')

## Gets list of files in "path_of_drafts"
## Scrape drafts for cards picked
## Send to NN...? Come back to this.
def main():
    files = [f for f in listdir(path_of_drafts) if isfile(join(path_of_drafts, f))]
    to_write = scrape_drafts(files)
    write_to_file(to_write)


if __name__ == '__main__':
    main()
