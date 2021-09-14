from PuzzleImporter import PuzzleImporter
from GA import GA
def main():
    # Use a breakpoint in the code line below to debug your script.
    puzzle = PuzzleImporter('Data/Easy-P4.csv')
    array = puzzle.open()
    GA(array)



# Bryndon can push

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/