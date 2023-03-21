import json
import os

from django.shortcuts import render
from django.views.generic import View
from collections import Counter
import requests

from operator import itemgetter
# import pandas as pd

from .services import (
    get_network_data, 
    get_source_chain_based_on_date, 
    get_destination_chain_based_on_date, 
    get_leader_board
    )


def get_data_from_the_graph(name, tokensQuery):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name
    data_dic = []

    
    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}

    response = requests.post(APIURL, headers=headers, json=query)

    # Get the response data as a dictionary
    # data = response.json()['data']

    # for item in data['tokenStats']:
    #         data_dic.append({
    #             'source': item['sourceChain'].lower(),
    #             'target': item['destinationChain'].lower(),
    #             'value': int(item['volume']) / 10**6,
    #         })
    
    return data_dic


def get_data_from_tokenstatbydates(name, tokensQuery, chain):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name

   
    data_dic = []

    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}

    response = requests.post(APIURL, headers=headers, json=query)

    # Get the response data as a dictionary
    # data = response.json()['data']

    # for item in data['tokenStatByDates']:
    #         data_dic.append({
    #             'date': item['date'],
    #             chain: item[chain].lower(),
    #             'value': int(item['volume']) / 10**6,
    #         })
    
    return data_dic


def get_data_addressstats(name, tokensQuery, chain):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name

   
    data_dic = []

    headers = {'Content-Type': 'application/json'}
    query = {'query': tokensQuery}

    response = requests.post(APIURL, headers=headers, json=query)

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


def group_by_chain(data, chain):
    
    data.sort(key=itemgetter('date', chain))
#     df = pd.DataFrame(data)

#     # groupby date and chain and sum the value column
#     result = df.groupby(['date', chain])['value'].sum().reset_index()
#     result['cum'] = result['value'].cumsum()
#     return result.to_dict('records')


def get_data_of_source_chain():
    # tokensQuery = """
    #         query {
    #            tokenStatByDates {
    #                 date
    #                 volume
    #                 sourceChain
    #             }
    #         }
    #         """
    # fantom = group_by_chain(get_data_from_tokenstatbydates('fantom-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    # moonbeam = group_by_chain(get_data_from_tokenstatbydates('moonbeam-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    # celo = group_by_chain(get_data_from_tokenstatbydates('celo-squid-protocol', tokensQuery, 'sourceChain'), 'sourceChain')
    # flipside = get_source_chain_based_on_date()
    # data = []
    # data = fantom + moonbeam + celo + flipside

    # return data
    pass


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
    # data = fantom + moonbeam + celo + flipside

    return data


def group_by_user(data, chain):
    
    # df = pd.DataFrame(data)
    # # groupby user and sourceChain and sum the value column
    # result = df.groupby(['user'])[chain].sum().reset_index()
    # return result.to_dict('records')
    pass

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
    # data = fantom + moonbeam + celo + flipside

    # data_df = pd.DataFrame(data)
    # data_df.fillna(value=0, inplace=True)

    # grouped_df = data_df.groupby('user').sum().reset_index()
    # list_of_dicts = grouped_df.to_dict(orient='records')

    # for item in list_of_dicts:
    #     total = sum([v for k, v in item.items() if k != 'user' and k != 'total_volume'])
    #     item['total_volume'] = total

    # sorted_list = sorted(list_of_dicts, key=lambda x: x['total_volume'], reverse=True)

    # return sorted_list


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
        
        links = fantom + moonbeam + celo + flipside

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
            
          
        
        data_of_source_chain = get_data_of_source_chain()
        data_of_destination_chain = get_data_of_destination_chain()

        leaderboard = get_users_data()
        context = {
            'links': links,
            'nodes': sorted(nodes, key=lambda x: x['id']),
            'data_of_source_chain': data_of_source_chain,
            'data_of_destination_chain': data_of_destination_chain,
            'leaderboard': leaderboard,
        }

        return render(request, 'dashboard.html', context=context)


class DashboardView1(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard_1.html', context=context)
