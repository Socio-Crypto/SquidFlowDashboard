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


def get_wallet_activity():

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
    

