import requests

# Player Tag P888QU8L0



def get_player_details(player_tag, authorization_key):
    headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer {}'.format(authorization_key)


}
    response = requests.get('https://api.clashofclans.com/v1/players/%23{}'.format(player_tag), headers = headers)
    player_json = response.json()
    #print(player_json)
    return player_json
    


def decode(json_file):
    try:
        if json_file['reason']:
            if json_file['reason'] == 'notFound':
                return "Player not found\nPlease enter valid player tag in the format\n/player <playertag>"
            if json_file['reason'] == 'accessDenied.invalidIp':
                return "We are having some connectivity issues\nPlease try again later"


    except:
        try:
            league_name = json_file['league']['name']
        except:
            league_name = 'Unranked'
        clan_name = json_file['clan'].get('name', '<No clan>')
        clan_tag = '%23{}'.format((json_file['clan'].get('tag', '%23'*9)[1:]))
        clan_lvl = json_file['clan'].get('clanLevel', '--')
        clan_role = json_file.get('role', '')
        return ('*Player Name:* {}\n*Player Tag:* %23{}\n*Town Hall:* {}\n*League:* {}\n*Player level:* {}\n*Trophies:* {}/{}\n*Clan Name:* {}\n*Clan Tag:* {}\n*Clan level:* {}\
            \n*Role:* {}\n*War Stars:* {}\n*Attacks Won:* {}\n*Defense Won:* {}\n*Builder Hall:* {}\n*Versus Trophies:* {}/{}\n*Versus Battle won:* {}\n*Troops Donated:* {}\
                \n*Troops recieved:* {}').format(json_file['name'], json_file['tag'][1:].upper(), json_file['townHallLevel'], league_name, json_file['expLevel'], \
                    json_file['trophies'], json_file['bestTrophies'], clan_name, clan_tag, clan_lvl, clan_role, \
                        json_file['warStars'], json_file['attackWins'], json_file['defenseWins'], json_file['builderHallLevel'], json_file['versusTrophies'], json_file['bestVersusTrophies'], json_file['versusBattleWins'], json_file['donations'], json_file['donationsReceived'])

def decode_legend(json_file):
    try:
        return "✨"*3 + "*Legend*" + "✨"*3 + "\n\nLegend Trophies: {}\nPrevious Season:\n  Trophies: {}\n  Rank: {}\
        \nBest Season:\n  {}\n  Trophies: {}\n  Rank: {}\nCurrent Season:\n  Trophies: {}".format(json_file['legendStatistics']['legendTrophies'], \
            json_file['legendStatistics']['previousSeason']['trophies'], json_file['legendStatistics']['previousSeason']['rank'], \
                json_file['legendStatistics']['bestSeason']['id'], json_file['legendStatistics']['bestSeason']['trophies'], json_file['legendStatistics']['bestSeason']['rank'], \
                    json_file['legendStatistics']['currentSeason']['trophies'])
    except:
        return ""

def decode_heroes(json_file):
    result = ''
    try:
        if json_file['heroes']:
            result = '*Heroes:*\n'
        for hero in json_file['heroes']:
            if hero['level'] == hero['maxLevel']:
                result += "  {}: level {}/{}🔥\n".format(hero['name'], hero['level'], hero['maxLevel'])
            else:
                result += "  {}: level {}/{}\n".format(hero['name'], hero['level'], hero['maxLevel'])
        return result
    except:
        return ''
    

def decode_spells(json_file):
    result = ''
    try:
        if json_file['spells']:
            result = '*Spells:*\n'
        for spell in json_file['spells']:
            if spell['level'] == spell['maxLevel']:
                result += "  {}: level {}/{}🔥\n".format(spell['name'], spell['level'], spell['maxLevel'])
            else:
                result += "  {}: level {}/{}\n".format(spell['name'], spell['level'], spell['maxLevel'])
        return result
    except:
        return ''
    
def decode_troops(json_file):
    result = ''
    try:
        if json_file['troops']:
            result = '*Troops:*\n'
        for troop in json_file['troops']:
            if troop['level'] == troop['maxLevel']:
                result += "  {}: level {}/{}🔥\n".format(troop['name'], troop['level'], troop['maxLevel'])
            else:
                result += "  {}: level {}/{}\n".format(troop['name'], troop['level'], troop['maxLevel'])
        return result
    except:
        return ''


#print(decode(get_player_details('P888QU8L0')))
#print(decode_legend(get_player_details('P888QU8L0')))
#print(decode_heroes(get_player_details('P888QU8L0')))
#print(decode_spells(get_player_details('P888QU8L0')))
#print(decode_troops(get_player_details('P888QU8L0')))