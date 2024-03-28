import requests
import json

def main():
    # Specify the URL of the API endpoint you want to query
    api_url = "https://overfast-api.tekrop.fr/players/SherdyShark-1475/stats/career"
    api_url2 = "https://overfast-api.tekrop.fr/players/MiniMartian-11891/stats/career"

    # Specify the query parameter and its value
    params = {
        "gamemode": "competitive"
    }
    params2 = {
        "gamemode": "competitive"
    }

    try:
        # Perform a GET request to the API endpoint with the specified parameters
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (JSON format)
            print("Response Content:")
            dict1 = response.json()
            #print(json.dumps(dict1["all-heroes"], indent=4))
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
    except Exception as e:
        # Print an error message if an exception occurred during the request
        print(f"Error: {e}")

    try:
        # Perform a GET request to the API endpoint with the specified parameters
        response2 = requests.get(api_url2, params=params2)

        # Check if the request was successful (status code 200)
        if response2.status_code == 200:
            # Print the response content (JSON format)
            print("Response2 Content:")
            dict2 = response2.json()
            #print(json.dumps(dict2["all-heroes"], indent=4))
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response2.status_code}")
    except Exception as e:
        # Print an error message if an exception occurred during the request
        print(f"Error: {e}")
    
    hero = 'ana'
    players = {'player1': {} , 'player2': {}}
    for key in dict1[hero]:
        for elm in dict1[hero][key]:
            if 'avg_per_10_min' in elm:
                players['player1'][elm]=(dict1[hero][key][elm])

    for key in dict2[hero]:
        for elm in dict2[hero][key]:
            if 'avg_per_10_min' in elm:
                players['player2'][elm]=(dict2[hero][key][elm])
    print(json.dumps(players, indent=4))
   
    common_keys = set(players['player1'].keys()) & set(players['player2'].keys())
    outstring = f"{'Player1':>50} {'Player2':>20}\n"
    print(outstring)
    for key in common_keys: 
        value_width = 50 - len(key)
        outstring += f"{key}: {players['player1'][key]:>{value_width}} {players['player2'][key]:>20}\n"

def get_player_stats(player):
    # Specify the URL of the API endpoint you want to query
    api_url = f"https://overfast-api.tekrop.fr/players/{player}/stats/career"

    # Specify the query parameter and its value
    params = {
        "gamemode": "competitive"
    }

    try:
        # Perform a GET request to the API endpoint with the specified parameters
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (JSON format)
            rtv = response.json()
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
    except Exception as e:
        # Print an error message if an exception occurred during the request
        print(f"Error: {e}")
    return rtv

def compare_by_hero(name1, name2, hero = 'all-heroes'):
    player1 = get_player_stats(name1)
    player2 = get_player_stats(name2)
    players = {'player1': {} , 'player2': {}}

    p1_playtime = round(player1[hero]['game']['time_played'] / 3600,2)
    p2_playtime = round(player2[hero]['game']['time_played'] / 3600,2)
    try:
        p1_winrate = round(player1[hero]['game']['games_won'] / player1[hero]['game']['games_played'] * 100,2)
    except:
        p1_winrate = 0
    try:
        p2_winrate = round(player2[hero]['game']['games_won'] / player2[hero]['game']['games_played'] * 100,2)
    except:
        p2_winrate = 0
    for key in player1[hero]:
        for elm in player1[hero][key]:
            if 'avg_per_10_min' in elm:
                players['player1'][elm]=(player1[hero][key][elm])

    for key in player2[hero]:
        for elm in player2[hero][key]:
            if 'avg_per_10_min' in elm:
                players['player2'][elm]=(player2[hero][key][elm])
    #print(json.dumps(players, indent=4))

    common_keys = list(set(players['player1'].keys()) & set(players['player2'].keys()))
    common_keys.sort()
    value_width = 50 - len(f"Hero name {hero}")
    outstring = f"Hero name: {hero} {name1:>{value_width}} {name2:>15}\n"
    value_width = 50 - len(f"Playtime(h)")
    outstring += f"Playtime(h): {p1_playtime:>{value_width}} {p2_playtime:>15}\n"
    value_width = 50 - len(f"Winrate")
    outstring += f"Winrate: {p1_winrate:>{value_width}} {p2_winrate:>15}\n"
    for key in common_keys: 
        value_width = 50 - len(key)
        outstring += f"{key}: {players['player1'][key]:>{value_width}} {players['player2'][key]:>15}\n"
    #print(outstring)
    return outstring

def get_player_summary(player):
     # Specify the URL of the API endpoint you want to query
    api_url = f"https://overfast-api.tekrop.fr/players/{player}/stats/summary"

    # Specify the query parameter and its value
    params = {
        "gamemode": "competitive"
    }

    try:
        # Perform a GET request to the API endpoint with the specified parameters
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (JSON format)
            roles = response.json()['roles']
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
    except Exception as e:
        # Print an error message if an exception occurred during the request
        print(f"Error: {e}")
        return
    
    api_url = f"https://overfast-api.tekrop.fr/players/{player}/summary"

    try:
        # Perform a GET request to the API endpoint with the specified parameters
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (JSON format)
            ranks_raw = response.json()['competitive']['pc']
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
    except Exception as e:
        # Print an error message if an exception occurred during the request
        print(f"Error: {e}")
        return
    

    tank_rank = ranks_raw.get('tank')
    damage_rank = ranks_raw.get('damage')
    support_rank = ranks_raw.get('support')

    tank_str = ""
    if tank_rank:
        tank_str = str(tank_rank.get('division', '') + ' ' + str(tank_rank.get('tier', '')))

    damage_str = ""
    if damage_rank:
        damage_str = str(damage_rank.get('division', '') + ' ' + str(damage_rank.get('tier', '')))

    support_str = ""
    if support_rank:
        support_str = str(support_rank.get('division', '') + ' ' + str(support_rank.get('tier', '')))

    ranks = {
        "tank": tank_str,
        "damage": damage_str,
        "support": support_str
    }

    role_names = ['tank','damage','support']
    summary = {}
    for role_name in role_names:
        role_summary = {'time played(h)' : round(roles[role_name]['time_played'] / 3600,2),
                        'winrate' : roles[role_name]['winrate'],
                        'games_played' : roles[role_name]['games_played'],
                        'games_won' : roles[role_name]['games_won'],
                        'games_lost' : roles[role_name]['games_lost'],
                        'kda' : roles[role_name]['kda'], 
                        "eliminations": roles[role_name]['average']['eliminations'],
                        "deaths": roles[role_name]['average']['deaths'],
                        "assists": roles[role_name]['average']['assists'],
                        "damage": roles[role_name]['average']['damage'],
                        "healing": roles[role_name]['average']['healing']
                        }
        summary[role_name] = role_summary
    
    value_width = (25 - len('Roles'))
    outstring = f"Player Name: {player}\n\nRoles: {'tank':>{value_width}} {'damage':>15} {'support':>15}\n"
    value_width = (25 - len('rank'))
    outstring += f"Rank: {ranks['tank']:>{value_width}} {ranks['damage']:>15} {ranks['support']:>15}\n"

    for key in summary['tank'].keys(): 
        value_width = 25 - len(key)
        outstring += f"{key}: {summary['tank'][key]:>{value_width}} {summary['damage'][key]:>15} {summary['support'][key]:>15}\n"

    rtv = str(outstring)
    return rtv

if __name__ == "__main__":
    #compare_by_hero('SherdyShark-1475','TwisterF5-1368',hero='sigma')

    print(get_player_summary('BunnySage-1508'))
