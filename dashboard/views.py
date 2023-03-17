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


def get_data_from_the_graph(url):
    """
    https://thegraph.com/en/
    """
    APIURL = url

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

class DashboardView(View):

    def get(self, request):
        context = {}
        links = []
        nodes = []
        fantom = get_data_from_the_graph('https://api.thegraph.com/subgraphs/name/kidacrypto/fantom-squid-protocol')
        moonbeam = get_data_from_the_graph('https://api.thegraph.com/subgraphs/name/kidacrypto/moonbeam-squid-protocol')
        celo = get_data_from_the_graph('https://api.thegraph.com/subgraphs/name/kidacrypto/celo-squid-protocol')
        flipside = get_wallet_activity()
        
        links.extend(fantom)
        links.extend(moonbeam)
        links.extend(celo)
        links.extend(flipside)

        labels_source = []
        labels_target = []
        labels = []
        for item in links:
            labels_source.append(item['source'])
            labels_target.append(item['target'])
        labels.extend(labels_source)
        labels.extend(labels_target)
        unique_labels = set(labels)

        for label in unique_labels:
            nodes.append({
                "label_short": label, 
                "label": label,
                "value_in": 0,
                "value_out": 0,
            })

        labels_source_count = dict(Counter(labels_source))
        labels_target_count = dict(Counter(labels_target))
        for i in range(len(nodes)):
            if nodes[i]['label'] in labels_source_count:
                nodes[i]['value_out'] = labels_source_count[nodes[i]['label']]
            if nodes[i]['label'] in labels_target_count:
                nodes[i]['value_in'] = labels_target_count[nodes[i]['label']]
            
            
        
        
        context = {
            'links': links,
            'nodes': nodes,
        }

        return render(request, 'dashboard.html', context=context)


class DashboardView1(View):

    def get(self, request):
        context = {}
        
        return render(request, 'dashboard_1.html', context=context)
