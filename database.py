import sqlite3 as sqlite

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

database = sqlite.connect('db.db')
cursor = database.cursor()
isInitialized = False


def createDtabase():
    if not checkTableExists(database, 'Matches'):
        scriptFile = open('./db/matches.sql', 'r')
        script = scriptFile.read()
        scriptFile.close()
        cursor.executescript(script)
    if not checkTableExists(database, 'TableNames'):
        scriptFile = open('./db/tables.sql', 'r')
        script = scriptFile.read()
        scriptFile.close()
        cursor.executescript(script)
    if not checkTableExists(database, 'Rankings'):
        scriptFile = open('./db/rankings.sql', 'r')
        script = scriptFile.read()
        scriptFile.close()
        cursor.executescript(script)
    global isInitialized
    isInitialized = True

def addTable(tableName):
    if not isInitialized:
        createDtabase()
    cursor.execute("INSERT INTO TableNames(tableName) VALUES (?);", (tableName,))
    database.commit()

def getTableNames():
    cursor.execute("SELECT * FROM TableNames")
    return cursor.fetchall()

def addMatch(matchNumber, matchTime, table1, table2, team1, team2):
    if not isInitialized:
        createDtabase()
    match = ((matchNumber, matchTime, table1, table2, team1, team2, False, -1, -1))
    cursor.executemany("INSERT INTO Matches VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (match,))
    database.commit()

def getMatchList():
    cursor.execute("SELECT * FROM Matches")
    return cursor.fetchall()

def editScore(data):
    cursor.execute("UPDATE Matches SET isScored=?, score1=?, score2=? WHERE id=?", (True, data['team1']['score'], data['team2']['score'], data['match']))
    database.commit()

def clearDatabase():
    cursor.execute("DROP TABLE IF EXISTS Matches")
    cursor.execute("DROP TABLE IF EXISTS TableNames")
    cursor.execute("DROP TABLE IF EXISTS Rankings")
    database.commit()
    global isInitialized
    isInitialized = False
