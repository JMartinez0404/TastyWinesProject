import sqlite3


def main():
    name = input('Enter your name: ')
    welcome(name)
    print('Option 1: Add a wine')
    print('Option 2: Show wines')
    print('Option 3: Search wines\n')
    valid_option = False
    while not valid_option:
        selection = input('What would you like to do: ')
        print()
        if menu_option(selection):
            valid_option = True


def welcome(name):
    print(f'----Welcome to TastyWines {name}!----\n')


def menu_option(selection):
    try:
        selection = int(selection)
        if selection == 1:
            add_wine()
        elif selection == 2:
            show_wines()
        elif selection == 3:
            search_wines()
    except ValueError:
        print('You did not enter a valid selection. Try again.\n')
        return False

    return True


def add_wine():
    not_correct = True
    wine = Wine()

    while not_correct:
        name = input('What is the name of the wine: ')
        print(f'You entered {name}.\n')
        if input('Is that correct (y/n): ').lower() == 'y':
            wine.name(name)
            not_correct = False

    rating = int(input('\nRate the wine from 1-10: '))
    wine.rating(rating)
    if rating == 10:
        print('Wow that\'s an amazing wine! Get some more!')
    elif rating > 7:
        print('That\'s a good wine!')
    elif rating > 4:
        print('Pretty good but not the best.')
    elif rating > 2:
        print('Eh, maybe you should try something else.')
    else:
        print('Never...again...')
    print()

    rev_choice = input(f'Do you want to add a review for {wine.name()} (y/n): ')
    print()
    if rev_choice.lower() == 'y':
        rev_confirm = 'y'
        while rev_confirm.lower() == 'y':
            review = input(f'What do you want to say about {wine.name()}: ')
            print()
            rev_confirm = input(f'You wrote: "{review}"\nDo you want to edit the review? (y/n) ')
            if rev_confirm.lower() == 'n':
                wine.review(review)
                print('Good. Your review has been saved.\n')
    else:
        print('Maybe next time :)\n')

    print(f'This is the wine you added: \n{wine}\n')


def show_wines():
    # implement this when you add the database
    # pseudo-code
    # ask user what details they want to print
    # print names only, or details, or rating, etc
    # print wines and selected details
    print('UNDER CONSTRUCTION')


def search_wines():
    # implement this when you add the database
    # might be worthwhile parsing words and returning results that match at least one word
    print('UNDER CONSTRUCTION')


class Wine:
    def __init__(self, **kwargs):
        self._name = kwargs['name'] if 'name' in kwargs else 'No Name Given'
        self._rating = kwargs['rating'] if 'rating' in kwargs else 0
        self._review = kwargs['review'] if 'review' in kwargs else 'No Review Given'

    def name(self, n=None):
        if n:
            self._name = n
        return self._name

    def rating(self, ra=None):
        if ra:
            self._rating = ra
        return self._rating

    def review(self, re=None):
        if re:
            self._review = re
        return self._review

    def __str__(self):
        return f'This wine is named {self.name()} and has a rating of {self.rating()}. You wrote "{self.review()}"'


if __name__ == '__main__':
    main()
