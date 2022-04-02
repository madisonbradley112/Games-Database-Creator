import sys
from xml.etree import ElementTree as ET
import requests
import sqlite3

conn = None
cursor = None


def connect(path):
    """Connects to the sqlite db and initializes a cursor."""
    global conn, cursor

    conn = sqlite3.connect(path,
                           detect_types=sqlite3.PARSE_COLNAMES)  # allows us to use date-times
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    conn.commit()
    return


def scrape_file():
    """
    Scrapes a Steam games XML file from the web.
    :return: None
    """

    steam_id = "thefifthplanet"
    url = 'https://steamcommunity.com/id/' + steam_id + "/games?xml=1"

    response = requests.get(url)
    with open('games.xml', 'wb') as file:
        file.write(response.content)


def parse_file():
    """
    Takes an XML file and parses it, reading it into txt.
    :return:
    """
    global conn, cursor

    file = "games.xml"

    tree = ET.parse(file)

    games = tree.findall('.//game')

    insert_game = """
                     INSERT INTO games(gid, name, storelink)
                     VALUES (?, ?, ?);
                     """

    insert_hours = """
                            INSERT INTO hoursPlayed(gid, hours) VALUES (?, ?);
                           """

    for game in games:
        hours_recorded = 0

        for elem in game.iter():
            if elem.tag == "appID":
                app_id = elem.text
            elif elem.tag == "name":
                title = elem.text
            elif elem.tag == "storeLink":
                store_link = elem.text
            elif elem.tag == "hoursOnRecord":
                hours_recorded = elem.text

        cursor.execute(insert_game, (app_id, title, store_link))
        cursor.execute(insert_hours, (app_id, hours_recorded))

        conn.commit()


def main():
    connect("personalDB.sqlite")
    scrape_file()
    parse_file()
    sys.stdout.close()


if __name__ == "__main__":
    main()