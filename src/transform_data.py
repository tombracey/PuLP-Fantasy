import pandas as pd
from pandasql import sqldf
from tabulate import tabulate

def transform_data():
    rt = pd.read_csv('data/rallings & thrasher notional 2019 results.csv')
    yg = pd.read_csv('data/yougov_final_mrp_poll.csv')
    
    query = '''SELECT rt.PA_Name AS Constituency,
        yg.WinnerGE2024 AS Winning_Party,
        ROUND((yg.Winner_margin/100) * (rt.turnout/100 * rt.electorate) + CASE WHEN yg.`2019v2024status` LIKE '%gain%' THEN rt.majority ELSE 0 END) AS Projected_Points, 
        rt.majority AS Price,
        CASE WHEN yg.`2019v2024status` LIKE '%gain%' THEN 'Attacker' ELSE 'Defender' END AS Position,
        rt.country_name AS Country
        FROM rt
        LEFT JOIN yg ON rt.ONS_Code LIKE yg.const;
        '''

    df = sqldf(query)
    
    df = df.dropna(subset=['Projected_Points'])

    df.to_markdown('data/transformed_data.md', index=False)

    list_of_dicts = df.to_dict(orient='records')

    return list_of_dicts

transform_data()





    # with open('transform_data_output.txt', 'w') as f:
    #     f.write(f'{df_query}')


