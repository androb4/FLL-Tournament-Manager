import database

raknings = []

def updateRankings():
    global rankings
    rankings = database.getTeams()
    rankings = sorted(rankings, key=lambda tup: tup[1], reverse=True)
    database.updateRankings(rankings)
