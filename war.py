import requests

# Clan Tag 229QQV8CY

def get_war_details(clan_tag, authorization_key):
    headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer {}'.format(authorization_key)
    }
    response = requests.get('https://api.clashofclans.com/v1/clans/%23{}/currentwar'.format(clan_tag), headers = headers)
    war_json = response.json()
    return war_json

def decode(json_file):
    try:
        if json_file['reason']:
            if json_file['reason'] == 'notFound':
                return "Clan not found\nPlease enter valid clan tag in the format\n/war <clantag>"
            if json_file['reason'] == 'accessDenied.invalidIp':
                return "We are having some connectivity issues\nPlease try again later"
            if json_file['reason'] == 'accessDenied':
                return "Failed to access war info\nClan warlog is private"
    except:
        endtime = json_file['endTime']
        return "Status: {}\n{} vs {}\nWar type: {}  vs  {}\nAttacks:   {}      {}\nStars:      {}      {}\nDestruction: {}%      {}%\nEnd time: {}/{}/{} {}".format(json_file['state'], json_file['clan']['name'], json_file['opponent']['name'], json_file['teamSize'], json_file['teamSize'], json_file['clan']['attacks'], json_file['opponent']['attacks'], json_file['clan']['stars'], json_file['opponent']['stars'], json_file['clan']['destructionPercentage'], json_file['opponent']['destructionPercentage'], endtime[6:8], endtime[4:6], endtime[:4], endtime[9:15])

def decode_members(json_file):
    try:
        result1 = '*Clan war details:*\n\n'
        result2 = ''
        for count in range(1, (int(json_file['teamSize']//2)+1)):
            for member in json_file['clan']['members']:
                if count == int(member['mapPosition']):
                    result1 += '{}. {}\n'.format(count, member['name'])
                    try:
                        result1 += '    ' +'❌'*(member['bestOpponentAttack']['stars']) + ' ({}%) by {}\n\n'.format(member['bestOpponentAttack']['destructionPercentage'], member['bestOpponentAttack']['attackerTag'][1:])
                    except:
                        result1 += "\n"

                    try:
                        result1 += "  Attacks left: {}\n".format(2 - len(member['attacks']))
                        for attacks in member['attacks']:
                            result1 += '  -Attacked ' + '⭐'*attacks['stars'] + ' ({}%) on {}\n'.format(attacks['destructionPercentage'], attacks['defenderTag'][1:])
                        result1 += "\n"
                    except:
                        result1 += "  Attacks left: 2\n\n"

        for count in range(int(json_file['teamSize']//2)+1, int(json_file['teamSize']+1)):
            for member in json_file['clan']['members']:
                if count == int(member['mapPosition']):
                    result2 += '{}. {}\n'.format(count, member['name'])
                    try:
                        result2 += '    ' +'❌'*(member['bestOpponentAttack']['stars']) + ' ({}%) by {}\n\n'.format(member['bestOpponentAttack']['destructionPercentage'], member['bestOpponentAttack']['attackerTag'][1:])
                    except:
                        result2 += "\n"

                    try:
                        result2 += "  Attacks left: {}\n".format(2 - len(member['attacks']))
                        for attacks in member['attacks']:
                            result2 += '  -Attacked ' + '⭐'*attacks['stars'] + ' ({}%) on {}\n'.format(attacks['destructionPercentage'], attacks['defenderTag'][1:])
                        result2 += "\n"
                    except:
                        result2 += "  Attacks left: 2\n\n"
        return result1, result2
    except:
        return ''

def decode_opp_members(json_file):
    try:
        result1 = '*Opponent clan war details:*\n\n'
        result2 = ''
        for count in range(1, (int(json_file['teamSize']//2)+1)):
            for member in json_file['opponent']['members']:
                if count == int(member['mapPosition']):
                    result1 += '{}. {}\n'.format(count, member['name'])
                    try:
                        result1 += '    ' +'🌟'*(member['bestOpponentAttack']['stars']) + ' ({}%) by {}\n\n'.format(member['bestOpponentAttack']['destructionPercentage'], member['bestOpponentAttack']['attackerTag'][1:])
                    except:
                        result1 += "\n"

                    try:
                        result1 += "  Attacks left: {}\n".format(2 - len(member['attacks']))
                        for attacks in member['attacks']:
                            result1 += '  -Attacked ' + '❌'*attacks['stars'] + ' ({}%) on {}\n'.format(attacks['destructionPercentage'], attacks['defenderTag'][1:])
                        result1 += "\n"
                    except:
                        result1 += "  Attacks left: 2\n\n"

        for count in range(int(json_file['teamSize']//2)+1, int(json_file['teamSize']+1)):
            for member in json_file['opponent']['members']:
                if count == int(member['mapPosition']):
                    result2 += '{}. {}\n'.format(count, member['name'])
                    try:
                        result2 += '    ' +'🌟'*(member['bestOpponentAttack']['stars']) + ' ({}%) by {}\n\n'.format(member['bestOpponentAttack']['destructionPercentage'], member['bestOpponentAttack']['attackerTag'][1:])
                    except:
                        result2 += "\n"

                    try:
                        result2 += "  Attacks left: {}\n".format(2 - len(member['attacks']))
                        for attacks in member['attacks']:
                            result2 += '  -Attacked ' + '❌'*attacks['stars'] + ' ({}%) on {}\n'.format(attacks['destructionPercentage'], attacks['defenderTag'][1:])
                        result2 += "\n"
                    except:
                        result2 += "  Attacks left: 2\n\n"

        return result1, result2
    except:
        return ''


#print(get_war_details('229QQV8CY', authorization_key))
#print(decode(get_war_details('229QQV8CY', authorization_key)))
#print(decode_members(get_war_details('229QQV8CY', authorization_key)))
#print(decode_opp_members(get_war_details('229QQV8CY', authorization_key)))