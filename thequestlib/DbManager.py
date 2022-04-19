import sqlite3
from thequestlib import DATABASE_FILE, HIGHSCORE_HEADER1, HIGHSCORE_HEADER2, HIGHSCORE_HEADER3
import sqlite3

def getScores():
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("""
            SELECT name, points
            FROM highscores
            ORDER BY points DESC
            LIMIT 10;
            """)
    topscores = cur.fetchall()
    con.close()
    text = []
    text.append(HIGHSCORE_HEADER1)
    text.append(HIGHSCORE_HEADER2)
    text.append(HIGHSCORE_HEADER2)
    text.append(HIGHSCORE_HEADER3)
    i = 1
    for score in topscores:
        text.append("{:0>2}.......................{}...........{:0>10}".format(i, score[0], score[1]))
        i += 1
    text.append("")
    text.append("")
    text.append("press space to return to main menu")
    return [text, topscores]


def addScore(name, points):
    con = sqlite3.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("""
                INSERT INTO highscores (name, points)
                VALUES (?,?)
                """, [name, points])
    con.commit()
    con.close()
        