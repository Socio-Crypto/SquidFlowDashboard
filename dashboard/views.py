# import json
# import os

from django.shortcuts import render
from django.views.generic import View
from collections import Counter
import requests

# from operator import itemgetter
# import pandas as pd

from .services import (
    get_network_data, 
    get_source_chain_based_on_date, 
    get_destination_chain_based_on_date, 
    get_leader_board,
    get_leader_board_based_on_destination
    )


def get_data_from_the_graph(name, tokensQuery):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name
    data_dic = []

    
    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}
    response = None
    while not response or response.status_code != 200:
        try:
            response = requests.post(APIURL, headers=headers, json=query)
        except:
            pass

    # Get the response data as a dictionary
    data = response.json()['data']

    for item in data['tokenStats']:
            data_dic.append({
                'source': item['sourceChain'].lower(),
                'target': item['destinationChain'].lower(),
                'value': int(item['volume']) / 10**6,
            })
    
    return data_dic


def get_data_from_tokenstatbydates(name, tokensQuery, chain):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name

   
    data_dic = []

    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}

    response = None
    while not response or response.status_code != 200:
        try:
            response = requests.post(APIURL, headers=headers, json=query)
        except:
            pass


    # Get the response data as a dictionary
    data = response.json()['data']

    for item in data['tokenStatByDates']:
            data_dic.append({
                'date': item['date'],
                chain: item[chain].lower(),
                'value': int(item['volume']) / 10**6,
            })
    
    return data_dic


def get_data_addressstats(name, tokensQuery, chain):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name

   
    data_dic = []

    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}

    response = None
    while not response or response.status_code != 200:
        try:
            response = requests.post(APIURL, headers=headers, json=query)
        except:
            pass


    # Get the response data as a dictionary
    data = response.json()['data']

    for item in data['addressStats']:
            data_dic.append({
                'user': item['user_address'],
                # chain: item[chain],
                item[chain].lower(): int(item['volume']) / 10**6,
            })
    
    return data_dic


def aggregate_dictionary(data):
    sum_dict = {}
    for item in data:
        for key, value in item.items():
            if key in sum_dict:
                sum_dict[key] += value
            else:
                sum_dict[key] = value

    return sum_dict


def group_by_chain(data, chain_s):
    
    from operator import itemgetter

    # Sort the data by date and chain.
    data.sort(key=itemgetter('date', chain_s))

    # Create an empty dictionary to hold the aggregated values.
    date_chain_totals = {}

    # Iterate through each row of the data and sum the values for each date and chain.
    for row in data:
        date, chain, value = row['date'], row[chain_s], row['value']
        if date not in date_chain_totals:
            date_chain_totals[date] = {}
        if chain not in date_chain_totals[date]:
            date_chain_totals[date][chain] = {'value': 0, 'cum': 0}
        date_chain_totals[date][chain]['value'] += value
        date_chain_totals[date][chain]['cum'] += value

    result = [] 
    for date in date_chain_totals:
        for chain_s, reto_totals in date_chain_totals[date].items():
            row = {'date': date, 'chain': chain_s, 'value': reto_totals['value'], 'cum': reto_totals['cum']}
            result.append(row)
    
    return result


def get_data_of_source_chain():
    tokensQuery = """
            query {
               tokenStatByDates {
                    date
                    volume
                    sourceChain
                }
            }
            """
    fantom = group_by_chain(get_data_from_tokenstatbydates('fantom-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    moonbeam = group_by_chain(get_data_from_tokenstatbydates('moonbeam-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    celo = group_by_chain(get_data_from_tokenstatbydates('celo-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    flipside = get_source_chain_based_on_date()
    data = []
    data = fantom + moonbeam + celo + flipside

    return data


def get_data_of_destination_chain():
    tokensQuery = """
            query {
               tokenStatByDates {
                    date
                    volume
                    destinationChain
                }
            }
            """
    fantom = group_by_chain(get_data_from_tokenstatbydates('fantom-squid-protocol', tokensQuery, 'destinationChain'), 'destinationChain')
    moonbeam = group_by_chain(get_data_from_tokenstatbydates('moonbeam-squid-protocol', tokensQuery, 'destinationChain'), 'destinationChain')
    celo = group_by_chain(get_data_from_tokenstatbydates('celo-squid-protocol', tokensQuery, 'destinationChain'), 'destinationChain')
    flipside = get_destination_chain_based_on_date()
    data = []
    data = fantom + moonbeam + celo + flipside

    return data


def group_by_user(data, chain):
    
    user_totals = {}
    for row in data:
        user = row['user']
        chain_value = row[chain]
        if user not in user_totals:
            user_totals[user] = 0
        user_totals[user] += chain_value

    result = [{'user': user, chain: total} for user, total in user_totals.items()]
    
    return result


def get_users_data():
    
    tokensQuery = """
        query {
            addressStats {
                user_address
                volume
                sourceChain
            }
        }
    """
    
    fantom = group_by_user(get_data_addressstats('fantom-squid-protocol', tokensQuery, 'sourceChain'), 'fantom')
    moonbeam = group_by_user(get_data_addressstats('moonbeam-squid-protocol', tokensQuery, 'sourceChain'), 'moonbeam')
    celo = group_by_user(get_data_addressstats('celo-squid-protocol', tokensQuery, 'sourceChain'),'celo')
    flipside = get_leader_board()

    data = []
    data = fantom + moonbeam + celo + flipside

    required_keys = {'user', 'total_volume', 'ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam'}

    for d in data:
        if set(d.keys()) - required_keys:
            data.remove(d)
    # Iterate over the list of dictionaries
    for d in data:
        # Check if dictionary has all required keys
        if not required_keys.issubset(d.keys()):
            # Add missing keys with default value
            for key in required_keys - set(d.keys()):
                d[key] = 0  

    user_totals = {}

    # Iterate over the list of dictionaries
    for d in data:
        user = d['user']
        # Add user to the dictionary if it doesn't already exist
        if user not in user_totals:
            user_totals[user] = {}
        # Iterate over the keys in the dictionary and add to the corresponding summed value
        for k, v in d.items():
            if k != 'user':
                user_totals[user][k] = user_totals[user].get(k, 0) + v

    # Convert user_totals to a list of dictionaries
    list_of_dicts = [{'user': user, **user_totals[user]} for user in user_totals]
   

    for item in list_of_dicts:
        total = sum([v for k, v in item.items() if k != 'user' and k != 'total_volume'])
        item['total_volume'] = total

    sorted_list = sorted(list_of_dicts, key=lambda x: x['total_volume'], reverse=True)

    return sorted_list



def leader_board_destination():
    
    tokensQuery = """
        query {
            addressStats {
                user_address
                volume
                destinationChain
            }
        }
    """
    
    fantom = get_data_addressstats('fantom-squid-protocol', tokensQuery, 'destinationChain')
    moonbeam = get_data_addressstats('moonbeam-squid-protocol', tokensQuery, 'destinationChain')
    celo = get_data_addressstats('celo-squid-protocol', tokensQuery, 'destinationChain')
    flipside = get_leader_board_based_on_destination()

    data = []
    data = fantom + moonbeam + celo + flipside

    required_keys = {'user', 'total_volume', 'ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam'}

    for d in data:
        if set(d.keys()) - required_keys:
            data.remove(d)

    # Iterate over the list of dictionaries
    for d in data:
        # Check if dictionary has all required keys
        if not required_keys.issubset(d.keys()):
            # Add missing keys with default value
            for key in required_keys - set(d.keys()):
                d[key] = 0  

    grouped_data = {}

    for item in data:
        user = item['user']
        if user not in grouped_data:
            grouped_data[user] = item.copy()
        else:
            for key in item.keys():
                if key != 'user':
                    grouped_data[user][key] += item[key]

    grouped_data = list(grouped_data.values())

   

    for item in grouped_data:
        total = sum([v for k, v in item.items() if k != 'user' and k != 'total_volume'])
        item['total_volume'] = total

    sorted_list = sorted(grouped_data, key=lambda x: x['total_volume'], reverse=True)

    return sorted_list


class DashboardView(View):

    def get(self, request):
        context = {}
        links = []
        nodes = []
        tokensQuery = """
            query {
                tokenStats {
                    id
                    volume
                    symbol
                    sourceChain
                    destinationChain
                }
            }
            """
        fantom = get_data_from_the_graph('fantom-squid-protocol', tokensQuery)
        moonbeam = get_data_from_the_graph('moonbeam-squid-protocol', tokensQuery)
        celo = get_data_from_the_graph('celo-squid-protocol', tokensQuery)
        flipside = get_network_data()

        # fantom = [d for d in fantom if d.get('target') != 'kava']
        moonbeam = [d for d in moonbeam if d.get('target') != 'kava']
        # celo = [d for d in celo if d.get('target') != 'kava']


        links = fantom + moonbeam + celo + flipside
        
        required_keys = {'ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam'}
        for d in links:
            if d['source'] not in required_keys or d['target'] not in required_keys:
                links.remove(d)

        labels_source = []
        labels_target = []
        labels_source_val = []
        labels_target_val = []
        labels = []
        for item in links:
            labels_source.append(item['source'])
            labels_target.append(item['target'])
            labels_source_val.append({item['source']: item['value']})
            labels_target_val.append({item['target']: item['value']})
        
        labels = labels_source + labels_target
        unique_labels = set(labels)
        
        for label in unique_labels:
            nodes.append({
                "id_short": label, 
                "id": label,
                "value_in": 0,
                "value_out": 0,
                "count_in": 0,
                "count_out": 0,
                "total": 0,
                "net": 0
            })

        labels_source_count = dict(Counter(labels_source))
        labels_target_count = dict(Counter(labels_target))
          
        agg_source_val = aggregate_dictionary(labels_source_val)
        agg_target_val = aggregate_dictionary(labels_target_val)

        for i in range(len(nodes)):
            if nodes[i]['id'] in labels_source_count:
                nodes[i]['count_out'] = labels_source_count[nodes[i]['id']]
                nodes[i]['value_out'] = agg_source_val[nodes[i]['id']]
            if nodes[i]['id'] in labels_target_count:
                nodes[i]['count_in'] = labels_target_count[nodes[i]['id']]
                nodes[i]['value_in'] = agg_target_val[nodes[i]['id']]
            
        for i in range(len(nodes)):
            nodes[i]['total'] = nodes[i]['value_in'] + nodes[i]['value_out']
            nodes[i]['net'] = nodes[i]['value_in'] - nodes[i]['value_out']
        
        data_of_source_chain = get_data_of_source_chain()
        data_of_destination_chain = get_data_of_destination_chain()

        context = {
            'links': links,
            'nodes': sorted(nodes, key=lambda x: x['net'], reverse=True),
            'data_of_source_chain': data_of_source_chain,
            'data_of_destination_chain': data_of_destination_chain,
        }

        return render(request, 'dashboard.html', context=context)


class LeaderboardView(View):

    
    def get(self, request):
        context = {}
        leaderboard = get_users_data()
        leaderboard_destination_chain = leader_board_destination()
        context = {
            'leaderboard': leaderboard[:25],
            'leaderboard_destination_chain': leaderboard_destination_chain[:25],
        }

        return render(request, 'leaderboard.html', context=context)
