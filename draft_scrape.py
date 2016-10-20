

def main():
    lst = [1,2,3,]
    # open the text file
    for item in lst:
        with open(item, 'r') as file_in:
            for line in file_in.readlines():
                if line[:4] == '--> ':
                    card = line[4:]
                    print (card)
    # scrape the card choices


if __name__ == '__main__':
  main()
