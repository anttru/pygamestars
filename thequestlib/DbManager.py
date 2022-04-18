import sqlite3
from thequestlib import DATABASE_FILE, HIGHSCORE_HEADER
import sqlite3


class DbManager:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_FILE)
        self.cur = self.con.cursor()

class ScoreGetter(DbManager):
    def __init__(self):
        super().__init__()
        self.cur.execute("""
            SELECT name, points
            FROM highscores
            ORDER BY points DESC
            LIMIT 10;
            """)
        self.topscores = self.cur.fetchall()
        self.text = HIGHSCORE_HEADER
        self.con.close()

    def createtext(self):
        i = 1
        for score in self.topscores:
            self.text.append("{:0>2}.......................{}...........{:0>10}".format(i, score[0], score[1]))
            i += 1
        self.text.append("")
        self.text.append("")
        self.text.append("press space to return to main menu")
        return self.text
    
class ScoreAdder(DbManager):
    def __init__(self, name, points):
        super().__init__()
        self.cur.execute("""
                        INSERT INTO highscores (name, points)
                        VALUES (?,?)
                        """, [name, points])
        self.con.commit()
        self.con.close()
        