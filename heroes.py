# Special thanks:
# 
# Scott Rome for tutorial on how to parse HTML tables in Python with BS
# https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
# https://github.com/srome
# https://twitter.com/_srome
#

# built-in
import json
import random
import os

# pip
import bs4

# mine
import web_document

class Heroes(object):
    def __init__(self):
        self.heroes = None

        self._heroes_filename = "heroes.json"

        if os.path.isfile(self._heroes_filename):
            file_mode = "r+"
        else:
            file_mode = "w+"
        self._heroes_file = open(self._heroes_filename, file_mode)

        # this might change sometime & that's when the program will break
        self._wiki_link = "https://dota2.gamepedia.com/Table_of_hero_attributes"
        self._wiki_table_class = "wikitable"

        self.get_list()

    def _download_list(self):
        document = web_document.WebDocument(self._wiki_link)
        contents = document.get_contents()

        self.heroes = self._format_list(contents)
        json.dump(self.heroes, self._heroes_file, sort_keys=True, indent=4)

    def _format_list(self, html):

        page = bs4.BeautifulSoup(html, "html.parser")
        hero_table = page.find('table', class_=self._wiki_table_class)
        tbody = hero_table.find('tbody')
        hero_rows = tbody.find_all('tr')

        heroes = []

        for row in hero_rows:
            hero_column = row.find('td') # get first column

            if hero_column == None: # header row
                continue

            column_text = hero_column.get_text()
            hero_name = column_text.strip()

            heroes.append(hero_name)

        return(heroes)

    def get_list(self):
        try:
            self.heroes = json.load(self._heroes_file)
        except json.decoder.JSONDecodeError:
            self._download_list()

    def get_random(self):
        random_hero = random.choice(self.heroes)

        return(random_hero)