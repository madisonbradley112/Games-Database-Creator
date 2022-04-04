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

    sql_file = open("tables.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    conn.commit()
    return


def scrape_file():
    """
    Scrapes a Steam games XML file from the web.
    :return: None
    """

    print("Your Steam ID is found here in your steam profile link: steamcommunity.com/id/**YourIDHere**/")
    steam_id = input("Please enter your Steam ID: ")
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
        hours_recorded = None

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


def scrape_prices():
    get_ids = """
              SELECT gid FROM games;
              """

    res = cursor.execute(get_ids)
    res = list(res)
    # setting up gid string of all games
    process = True
    for i in range(0, len(res), 100):
        process_100 = res[i:i + 100]
        gids = ""
        for gid in process_100:
            gids = gids + str(gid[0]) + ","

        gids = gids[:-1]
        url = "http://store.steampowered.com/api/appdetails?appids=" + gids + "&cc=us&filters=price_overview"
        print(url)


def main():
    connect("personalDB.sqlite")
    scrape_file()
    parse_file()
    sys.stdout = sys.__stdout__

    scrape_prices()


if __name__ == "__main__":
    main()