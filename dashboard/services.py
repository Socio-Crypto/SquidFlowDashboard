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

    "Flipside: "

    sql_query = f"""
        SELECT 
        'Ethereum' as source,
        date(l.BLOCK_TIMESTAMP) as  date ,
        DECODED_LOG:destinationChain as destination,
            sum(AMOUNT_USD) as USD_AMOUNT,
            avg(AMOUNT_USD) as avg_AMOUNT,
        
        count (distinct DECODED_LOG:refundAddress) as senders,
        concat (source,'->',destination) as direction,
        sum(USD_AMOUNT)over(partition by direction order by date rows between unbounded preceding and current row) as cum_USD_AMOUNT,
        sum(senders)over(partition by direction order by date rows between unbounded preceding and current row) as cum_senders
        FROM ethereum.core.fact_decoded_event_logs l 
        inner join ethereum.core.ez_token_transfers t on t.tx_hash = l.tx_hash
        
        WHERE l.tx_hash in (
        SELECT tx_hash
        FROM ethereum.core.fact_token_transfers
        WHERE to_address ILIKE ('0xce16f69375520ab01377ce7b88f5ba8c48f8d666')
        )

        and destination is not null   and  l.BLOCK_TIMESTAMP >= '2023-02-01'
        group by 2,3,direction       
    """
    return get_result_from_query(sql_query)
    
