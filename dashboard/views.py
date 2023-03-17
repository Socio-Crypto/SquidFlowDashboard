import json
import os
from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from graphqlclient import GraphQLClient
from collections import Counter

from .services import get_wallet_activity


def get_data_from_the_graph(name, tokensQuery):
    """
    https://thegraph.com/en/
    """
    APIURL = 'https://api.thegraph.com/subgraphs/name/kidacrypto/' + name

   
    client = GraphQLClient(APIURL)
    data = client.execute(tokensQuery)
    data_dic = []

    for item in json.loads(data)['data']['tokenStats']:
            data_dic.append({
                'source': item['sourceChain'],
                'target': item['destinationChain'],
                'value': int(item['volume']) / 10**6,
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
        flipside = get_wallet_activity()
        
        links.extend(fantom)
        links.extend(moonbeam)
        links.extend(celo)
        links.extend(flipside)

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
        
        labels.extend(labels_source)
        labels.extend(labels_target)
        unique_labels = set(labels)

        
        for label in unique_labels:
            nodes.append({
                "label_short": label, 
                "label": label,
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
            if nodes[i]['label'] in labels_source_count:
                nodes[i]['count_out'] = labels_source_count[nodes[i]['label']]
                nodes[i]['value_out'] = agg_source_val[nodes[i]['label']]
            if nodes[i]['label'] in labels_target_count:
                nodes[i]['count_in'] = labels_target_count[nodes[i]['label']]
                nodes[i]['value_in'] = agg_target_val[nodes[i]['label']]
            
          
        
        print(labels_source_val)
        context = {
            'links': links,
            'nodes': nodes,
        }

        return render(request, 'dashboard.html', context=context)


class DashboardView1(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard_1.html', context=context)
