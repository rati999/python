import sqlite3
import random
from texttable import Texttable

class AnimeDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY,
                name TEXT,
                sport TEXT,
                finished_airing INTEGER,
                rating REAL,
                seen INTEGER
            )
        ''')
        self.connection.commit()

    def insert_row(self, name, sport, finished_airing, rating, seen):
        self.cursor.execute('''
            INSERT INTO anime (name, sport, finished_airing, rating, seen)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, sport.lower(), finished_airing, rating, seen))
        self.connection.commit()

    def select_all(self):
        self.cursor.execute('SELECT * FROM anime')
        table = Texttable()
        table.set_deco(Texttable.VLINES | Texttable.HEADER)
        table.set_cols_align(["c"] * 6)
        table.header(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
        for row in self.cursor.fetchall():
            table.add_row(row)
        print(table.draw())

    def select_by_sport(self, sport):
        self.cursor.execute('SELECT * FROM anime WHERE sport = ?', (sport.lower(),))
        table = Texttable()
        table.set_deco(Texttable.VLINES | Texttable.HEADER)
        table.set_cols_align(["c"] * 6)
        table.header(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
        for row in self.cursor.fetchall():
            table.add_row(row)
        print(table.draw())

    def select_random(self):
        self.cursor.execute('SELECT * FROM anime WHERE finished_airing = 1 AND seen = 0')
        unwatched_anime = self.cursor.fetchall()
        if not unwatched_anime:
            print("An anime that has finished airing and is not seen by you could not be found.")
        else:
            random_anime = random.choice(unwatched_anime)
            print("Random anime you can watch:")
            table = Texttable()
            table.set_deco(Texttable.VLINES | Texttable.HEADER)
            table.set_cols_align(["c"] * 6)
            table.header(["ID", "Name", "Sport", "Finished Airing", "Rating", "Seen"])
            table.add_row(random_anime)
            print(table.draw())

    def mark_as_seen(self, anime_id):
        self.cursor.execute('UPDATE anime SET seen = 1 WHERE id = ?', (anime_id,))
        self.connection.commit()

    def delete_row(self, anime_id):
        self.cursor.execute('DELETE FROM anime WHERE id = ?', (anime_id,))
        self.connection.commit()

    def disconnect(self):
        self.connection.close()

def main():
    db_name = "anime_database.db"
    anime_db = AnimeDatabase(db_name)
    anime_db.connect()
    anime_db.create_table()

    while True:
        print("Choose an action:")
        print("1. Add anime")
        print("2. View all anime")
        print("3. Filter animes by sport")
        print("4. Choose random anime to watch")
        print("5. Mark anime as seen")
        print("6. Delete anime")
        print("7. Quit")

        choice = input(">>> Enter your choice: ")

        if choice == "1":
            name = input(">>>Enter name: ")
            sport = input(">>>Enter type of sport: ")
            finished_airing = input(">>>Is the anime finished? (y/n): ")
            if finished_airing.lower() == "y":
                finished_airing = 1
            else:
                finished_airing = 0
            rating = float(input(">>>Enter rating: "))
            seen = 0
            anime_db.insert_row(name, sport, finished_airing, rating, seen)
            print("\n")
            
        elif choice == "2":
            print("\n")
            anime_db.select_all()
            print("\n")

        elif choice == "3":
            sport = input("Enter type of sport: ")
            print("\n")
            anime_db.select_by_sport(sport)
            print("\n")

        elif choice == "4":
            print("\n")
            anime_db.select_random()
            print("\n")

        elif choice == "5":
            anime_id = input("Enter ID: ")
            anime_db.mark_as_seen(anime_id)
            print("\n")

        elif choice == "6":
            anime_id = input("Enter ID: ")
            anime_db.delete_row(anime_id)
            print("\n")

        elif choice == "7":
            anime_db.disconnect()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
