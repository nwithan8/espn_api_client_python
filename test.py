from index import ESPN

espn = ESPN()
print(espn)

# index test
football = espn.Sport('football')
print(football)
golf = espn.Sport('golf')
print(golf)


# sport test
cfb = football.League('cfb')
print(cfb)
rory = golf.Player('6798')
print(rory)


# league test
sec = cfb.Conference(8)
print(sec)
natty = cfb.Game('401135295')
print(natty)
burrow = cfb.Player('3915511')
print(burrow)
lsu = cfb.Team('99')
print(lsu)
cfbteams = cfb.getTeams()
print(cfbteams)
cfbrankings = cfb.getRankings()
print(cfbrankings)
cfbnews = cfb.getNews()
print(cfbnews)


# player test
rory.updatePlayerInfo()
roryteamnull = rory.getPlayerTeam()
print(roryteamnull)
rorysummarynull = rory.getPlayerStatsSummary()
print(rorysummarynull)
rorystatsfull = rory.getPlayerFullStats()
print(rorystatsfull)

burrow.updatePlayerInfo()
burrowlsu = burrow.getPlayerTeam()
print(burrowlsu)
burrowsummary = burrow.getPlayerStatsSummary()
print(burrowsummary)
burrowstatsfull = burrow.getPlayerFullStats()
print(burrowstatsfull)


# team test
lsu.makeTeam()
lsusched = lsu.getTeamSchedule()
print(lsusched)
lsusched = lsu.schedule
print(lsusched)
lsuconf = lsu.getTeamConference()
print(lsuconf)
lsuconf = lsu.conference
print(lsuconf)
lsuroster = lsu.getTeamRoster()
print(lsuroster)
lsuroster = lsu.roster
print(lsuroster)


# conference test
secteams = sec.getTeams()
print(secteams)


# game test
natty.makeGame()
nattyteams = natty.getTeams()
print(nattyteams)
nattyscore = natty.getScore()
print(nattyscore)
nattyscore = natty.score
print(nattyscore)
nattyprob = natty.getGameProbability()
print(nattyprob)
nattyprob = natty.winProbability
print(nattyprob)
nattyodds = natty.getGameOdds()
print(nattyodds)
nattyspread = natty.spread
print(nattyspread)
nattyou = natty.overUnder
print(nattyou)

"""
cfb = football.League('cfb')
sec = cfb.Conference(8)
teams = sec.getTeams()
games = cfb.getCurrentGames()
game = games[0]
game.makeGame()
teams = game.getTeams()
print(teams['awayTeam'].teamID)
"""

"""
for team in teams:
    team.makeTeam()
    print(team.mascot)
    for player in team.roster[0]['players']: # offense
        player.updatePlayerInfo()
        print('{} {}'.format(player.firstName, player.lastName))
"""
