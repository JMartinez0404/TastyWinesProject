import sqlite3
# current bugs:
# - can't insert text with apostrophes because the characters aren't escaped


def main():
    con = sqlite3.connect('winereviewsdb.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS reviews(
                        name text NOT NULL,
                        rating integer NOT NULL,
                        review text NOT NULL
                );''')
    name = input('Enter your name: ')
    welcome(name)
    print('Option 1: Add a wine')
    print('Option 2: Show wines')
    print('Option 3: Search wines\n')
    valid_option = False
    while not valid_option:
        selection = input('What would you like to do: ')
        print()
        if menu_option(int(selection), con, cur):
            valid_option = True
    con.close()


def welcome(name: str):
    '''
    :param name:
    :return:
    '''
    print(f'----Welcome to TastyWines {name}!----\n')


def menu_option(selection: int, con, cur) -> bool:
    try:
        if selection == 1:
            add_wine(cur)
        elif selection == 2:
            show_wines(cur)
        elif selection == 3:
            search_wines(cur)
    except ValueError:
        print('You did not enter a valid selection. Try again.\n')
        return False
    con.commit()
    return True


def add_wine(cur):
    not_correct = True
    wine = Wine()

    while not_correct:
        name = input('What is the name of the wine: ')
        print(f'You entered {name}.\n')
        if input('Is that correct (y/n): ').lower() == 'y':
            wine.name(name.lower())
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
                review = review.replace('\'', '')  # band-aids apostrophe issue for now
                print(review)
                wine.review(review)
                print('Good. Your review has been saved.\n')
    else:
        print('Maybe next time :)\n')

    print(f'This is the wine you added: \n{wine}\n')
    cur.execute(f'''INSERT INTO reviews
                    VALUES ('{wine.name()}', {wine.rating()}, '{wine.review()}');''')


def show_wines(cur):
    exit_select = False
    options = (1, 2, 0)
    while exit_select is False:
        print('''   1 - All Details\n   2 - Only Wine Names\n   0 - Exit''')
        selection = int(input('What would you like to do: '))
        if selection not in options:
            print('You did not select a valid option.')
            continue
        elif selection == 1:
            print('REVIEWED WINES:')
            for row in cur.execute('SELECT * from reviews;'):
                print(f'  {row[0]}: {row[1]}\n   {row[2]}\n')
        elif selection == 2:
            for row in cur.execute('SELECT name from reviews;'):
                print(f'{row[0]}')
            print()
        elif selection == 0:
            exit_select = True


def search_wines(cur):
    exit_select = False
    options = (1, 2, 0)
    while exit_select is False:
        print('''   1 - Search by Name\n   2 - Search by Rating\n   0 - Exit''')
        selection = int(input('What would you like to do: '))
        if selection not in options:
            print('You did not select a valid option.\n')
            continue
        elif selection == 1:
            name_search = input('Enter name: ')
            name_search = name_search.lower()
            is_there = False
            for row in cur.execute('SELECT name FROM reviews'):
                if is_there is False and name_search == row[0]:
                    rev = cur.execute(f'SELECT * FROM reviews WHERE name = \'{name_search}\';').fetchall()[0]
                    print(f'  {rev[0]}: {rev[1]}\n   {rev[2]}\n')
                    is_there = True
            if is_there is False:
                print('That wine is not in the list.\n')
        elif selection == 2:
            rating_search = int(input('Enter rating: '))
            is_there = False
            for row in cur.execute('SELECT rating FROM reviews'):
                if is_there is False and rating_search == row[0]:
                    for rev in cur.execute(f'SELECT * FROM reviews WHERE rating = \'{rating_search}\';').fetchall():
                        print(f'  {rev[0]}: {rev[1]}\n   {rev[2]}\n')
                    is_there = True
            if is_there is False:
                print(f'There are no wines with a rating of {rating_search} in the list.\n')
        elif selection == 0:
            exit_select = True


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
