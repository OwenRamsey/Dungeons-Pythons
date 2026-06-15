# Owen Ramsey
# database functions
# April 6 2026

import sqlite3

# connect to game database function
def connect():
    return sqlite3.connect('game.db')

# create tables function
def createTables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    # creaate player table
    cur.execute('''  CREATE TABLE IF NOT EXISTS players (playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        baseAttack INTEGER,
                                        hp INTEGER,
                                        maxHp INTEGER,
                                        exp INTEGER,
                                        level INTEGER)
                                        ''')
    # create progress table
    cur.execute('''  CREATE TABLE IF NOT EXISTS saves (saveID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        playerID INTEGER,
                                        floor INTEGER,
                                        room INTEGER,
                                        eventText TEXT,
                                        FOREIGN KEY(playerID) REFERENCES
                                        players(playerID))
                                        ''')
    conn.commit()
    conn.close()


# create a new player function
def createPlayer(player):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute('''INSERT INTO players (baseAttack, hp, maxHp, exp, level)
                    VALUES (?, ?, ?, ?, ?)    ''',
                    (player.getBaseAttack(), player.getHp(), player.getMaxHp(), player.getExp(), player.getLevel()))
    
    # set playerID to the last row id
    playerID = cur.lastrowid
    
    conn.commit()
    conn.close()

    # return the playerID
    return playerID

# read player based on id
def readPlayer(playerID):
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM players WHERE playerID = ?', (playerID,))
    return cur.fetchone()

# update player
def updatePlayer(playerID, player):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute('''
    UPDATE players
    SET baseAttack = ?, 
    hp = ?, 
    maxHp = ?, 
    exp = ?, 
    level = ?
    WHERE playerID = ?
    ''', (player.getBaseAttack(), player.getHp(), player.getMaxHp(), player.getExp(), player.getLevel(), playerID))

    conn.commit()
    conn.close()

# delete player
def deletePlayer(playerID):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute(''' DELETE FROM players 
                WHERE playerID = ?
                ''', (playerID,))
    conn.commit()
    conn.close()

# create save
def createSave(playerID, floor, room, eventText):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute('''
    INSERT INTO saves (playerID, floor, room, eventText)
    VALUES (?, ?, ?, ?)
    ''', (playerID, floor, room, eventText))

    conn.commit()
    conn.close()

# read save
def readSave(playerID):
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT * FROM saves WHERE playerID = ?', (playerID,))
    return cur.fetchone()

# update save
def updateSave(playerID, floor, room, eventText):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute('''
    UPDATE saves
    SET floor = ?, 
    room = ?,
    eventText = ?
    WHERE playerID = ?
    ''', (floor, room, eventText, playerID))

    conn.commit()
    conn.close()

# delete save
def deleteSave(playerID):
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute('DELETE FROM saves WHERE playerID = ?', (playerID,))

    conn.commit()
    conn.close()

# check if there  are any saves
def checkForSaves():
    conn = connect()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM saves')
    count = cur.fetchone()[0]
    conn.close()
    if count > 0:
        return True
    
    return False

# function to get the last playerID
def getLastPlayerID():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT playerID FROM saves ORDER BY saveID DESC LIMIT 1')
    lastPlayer = cur.fetchone()
    conn.close()
    return lastPlayer[0]