import requests

# Clan Tag 229QQV8CY

def get_clan_details(clan_tag, authorization_key):
    headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer {}'.format(authorization_key)

}
    response = requests.get('https://api.clashofclans.com/v1/clans/%23{}'.format(clan_tag), headers = headers)
    clan_json = response.json()
    #print(clan_json)
    return clan_json

def decode(json_file):
    try:
        if json_file['reason']:
            if json_file['reason'] == 'notFound':
                return "Clan not found\nPlease enter valid clan tag in the format\n/clan <clantag>"
            if json_file['reason'] == 'accessDenied.invalidIp':
                return "We are having some connectivity issues\nPlease try again later"
    except:
        clan_tag = json_file['tag'][1:]
        return "*Clan Name:* {}\n*Clan tag:* %23{}\n*Clan Level:* {}\n*Description:* {}\n*Members:* {}\n*Type:* {}\n*Required Trophies:* {}\
            \n*Total Trophies:* {}\n*Total Versus Trophies:* {}\n*Clan Location:* {}\n*War wins:* {}\n*War win streak:* {}\n*War League:* {}".format(json_file['name'], clan_tag, json_file['clanLevel'], \
                json_file['description'], json_file['members'], json_file['type'], json_file['requiredTrophies'], json_file['clanPoints'], json_file['clanVersusPoints'], json_file['location']['name'], \
                    json_file['warWins'], json_file['warWinStreak'], json_file['warLeague']['name'])

def decode_members(json_file):
    result = ''
    count = 1
    leader = ''
    try:
        for member in json_file['memberList']:
            if member['role'] == 'leader':
                leader = member['name']
            result += "{}. *{} :*\n  -Tag: %23{}\n  -Role: {}\n  -League: {}\n\n".format(count, member['name'], member['tag'][1:], member['role'], member['league'].get('name', 'Not in any league'))
            count += 1
        return "*Leader:* " + leader + "\n\n" +result
    except:
        return ''


#print(decode(get_clan_details('229QQV8CY')))
#print(decode_members(get_clan_details('229QQV8CY')))