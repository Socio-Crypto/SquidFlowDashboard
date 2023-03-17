from shroomdk import ShroomDK
import itertools
from datetime import datetime
import json


def get_result_from_query(sql_query):
    
    sdk = ShroomDK('0aa823ca-fc7c-485a-9412-4d96b04e54be')
    result = sdk.query(sql_query)

    activity_data = {}
    if result.records is not None:
        activity_data = result.records
    return activity_data


def get_network_data():

    "Flipside: https://app.flipsidecrypto.com/velocity/queries/5647f303-2168-4ba9-b4ea-159919dde4a4"

    sql_query = f"""
       select 
        source_chain as source,
        destination_chain as target,
        sum(amount) as value
        from axelar.core.EZ_SQUID
        WHERE  destination_chain in ('ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam')
        group by 1,2
    """
    return get_result_from_query(sql_query)
    

def get_source_chain_based_on_date():

    "Flipside: https://api.flipsidecrypto.com/api/v2/queries/f451f2cc-62d0-429c-b9f5-59a81ab5881a/data/latest"

    sql_query ="""
        select 
        to_varchar(block_timestamp::timestamp, 'yyyy/mm/dd') as date,
        source_chain as sourceChain,
        --destination_chain as target,
        sum(amount) as value,
        sum(value)over(partition by sourceChain order by date) as cum
        from axelar.core.EZ_SQUID
        WHERE  destination_chain in ('ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam')
        AND date >= '2022-12-01'
        group by 1,2 
    """

    return get_result_from_query(sql_query)

def get_destination_chain_based_on_date():

    "Flipside: https://api.flipsidecrypto.com/api/v2/queries/61e13bdb-89df-46dd-b373-77869e852872/data/latest"

    sql_query ="""
        select 
        to_varchar(block_timestamp::timestamp, 'yyyy/mm/dd') as date,
        --source_chain as source,
        destination_chain as destinationChain,
        sum(amount) as value,
        sum(value)over(partition by destinationChain order by date) as cum
        from axelar.core.EZ_SQUID
        WHERE  destination_chain in ('ethereum', 'avalanche', 'binance', 'arbitrum', 'polygon', 'celo', 'fantom', 'moonbeam')
        AND date >= '2022-12-01'
        group by 1,2
        
    """

    return get_result_from_query(sql_query)


