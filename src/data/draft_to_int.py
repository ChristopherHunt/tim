
from app.draft_scraper import *
from data.kaladesh import *
from lib.pack_generator import PackGenerator
import glob
import sys
import re


def clean_pack(pack):
    clean_pack = []
    for card in pack:
        clean = card.strip()
        if 'Gonti, Lord of Luxuty' in clean:
            clean = '--> Gonti, Lord of Luxury'
        clean_pack.append(clean)
    return clean_pack


def grab_pack(lines, pack_num):
    grabbing_pack = False
    rnd = []
    picks = []
    i = 0
    for line in lines:
        i += 1
        if 'Pack ' + pack_num in line:
            grabbing_pack = True
            continue
        if grabbing_pack and line == '\n':
            grabbing_pack = False
            rnd.append(clean_pack(picks))
            picks = []
        if grabbing_pack and i == len(lines):
            # print (line)
            # input()
            picks.append(line)
            rnd.append(clean_pack(picks))
        if grabbing_pack:
            picks.append(line)
    return rnd


def strip_picked_and_prepend(round_picks):
    # pass
    new_rnd = []
    for rnd in round_picks:
        rnd_tmp = []
        pick = []
        for card in rnd:
            # iterate over list to find card with the arrow
            if '--> ' in card:
                pick = card[4:]
                rnd_tmp.append(pick)
            else:
                rnd_tmp.append(card)

        # prepend the card to the front of the list
        rnd_tmp = [pick] + rnd_tmp

        # add to new_rnd list
        new_rnd.append(rnd_tmp)
    return new_rnd


def main():
    pk = PackGenerator('/home/jon/repos/tim/src/data/kaladesh/kaladesh.json', \
                '/home/jon/repos/tim/src/data/kaladesh/kaladesh_pick_order.txt')

    files = glob.glob('/home/jon/repos/tim/src/data/kaladesh/scraped_drafts/*')
    for f in files:
        print ('filename: ', f)
        rnd_picks = []
        with open(f, 'r') as file_in:
            lines = [line for line in file_in.readlines()]
            rnd1 = grab_pack(lines, '1')
            new_rnd1 = strip_picked_and_prepend(rnd1)
            rnd_picks.append(new_rnd1)
            rnd2 = grab_pack(lines, '2')
            new_rnd2 = strip_picked_and_prepend(rnd2)
            rnd_picks.append(new_rnd2)
            rnd3 = grab_pack(lines, '3')
            new_rnd3 = strip_picked_and_prepend(rnd3)
            rnd_picks.append(new_rnd3)

        # strip last piece of filename
        last = f.split('/')[-1]
        print ('last: ' , last)

        filename = 'draft_data/' + last + '_num_picks.txt'
        with open(filename, 'a') as file_out:
            for num_rnd in rnd_picks:       # the first of 1,2,3 round
                for all_rnd in num_rnd:     # all 1-15 picks for this round
                    # convert all picks to numbers
                    t = pk.convert_card_names_to_card_nums(all_rnd)
                    # convert all numbers to a comma separated string
                    s = ','.join([str(i) for i in t])
                    # write the string to file
                    file_out.write(s + '\n')


if __name__ == '__main__':
    main()
