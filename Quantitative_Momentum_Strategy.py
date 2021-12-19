import numpy as np 
import pandas as pd 
import requests
import xlsxwriter
import math
from scipy import stats
from statistics import mean

OUTFOLDER = str('output-files/Momentum_Strategy/')
INFOLDER = str('stock-data')

# stocks = pd.read_csv(INFOLDER + '/sp_500_stocks.csv')
from secrets import IEX_CLOUD_API_TOKEN

# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   

###################################################################################################
## Create a dataframe for simple momentum stock evaluation
# Input:            stocks; a dataframe that contains all of the symbols for the stocks we evaluate
# Output:           final_dataframe; a dataframe that has the requested information for each stock
# Precondition:     IEX is active, Computer is Connected to the Internet, API Key is valid
# Postcondition:    final_dataframe = pd.DataFrame()
# General Workflow: 
#                   Breaks the list of stock symbols into smaller sublists
#                   Batch API calls from each sublist 
#                   Appends parsed response from api to final result
#                   Returns final result
###################################################################################################
def create_dataframe(stocks):      
    #split into substrings for API Batch calls        
    symbol_groups = list(chunks(stocks['Symbol'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))
    #     print(symbol_strings[i])

    #create the returning dataframe
    my_columns = ['Symbol', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']
    final_dataframe = pd.DataFrame(columns = my_columns)

    #Batch API Call to get the data
    for symbol_string in symbol_strings:
    #     print(symbol_strings)
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            final_dataframe = final_dataframe.append(
                                            pd.Series([symbol, 
                                                    data[symbol]['quote']['latestPrice'],
                                                    data[symbol]['stats']['year1ChangePercent'],
                                                    'N/A'
                                                    ], 
                                                    index = my_columns), 
                                            ignore_index = True)
    
    return final_dataframe

## Removing Low-Momentum Stocks
# The investment strategy that we're building seeks to identify the 50 highest-momentum stocks in the S&P 500.
# Because of this, the next thing we need to do is remove all the stocks in our DataFrame that fall below this momentum threshold. 
# We'll sort the DataFrame by the stocks' one-year price return, and drop all stocks outside the top 50.
###################################################################################################
# Remove all Low Momentum Stocks from the data set
# Input:            starting_dataframe; a dataframe that needs to have the low momentum stocks removed
#                   sort_request; a column that the dataframe needs to be sorted by
#                   remaining_rows; a value that represents the number of rows in the new dataframe
# Output:           final_dataframe; a dataframe that does not have any low momentum stocks
# Preconditions:    
# Postconditions:   
# General Workflow:
#                   Sort the data frame
#                   Create a new dataframe, with the remaining X number of rows
###################################################################################################
def remove_Low_Momentum_Stocks(starting_dataframe, sort_request, remaining_rows):
    starting_dataframe.sort_values(sort_request, ascending = False, inplace = True, ignore_index = True)
    final_dataframe = starting_dataframe.iloc[:(remaining_rows + 1)]
    return final_dataframe


def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the value of your portfolio: ")

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio: ")
        val = float(portfolio_size)
    
    return val

###################################################################################################
# Calculate the total number of shares of each stock from a given portfolio size
# Input:            portfolio_size; the numerical representation of the buying power
#                   starting_dataframe; a dataframe that needs the number of shares of each stock calculated
# Output:           final_dataframe; a dataframe that has the number of shares per stock calculated
# Preconditions:    
# Postconditions:   
# General Workflow:
#                   Calculate the position size for each stock
#                   Calculate the total number of possible shares from each stock
###################################################################################################
def calculate_position(portfolio_size, final_dataframe):
    position_size = float(portfolio_size) / len(final_dataframe)
    for i in range(0, len(final_dataframe['Symbol'])):
        final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])
    return final_dataframe


## Building a Better (and More Realistic) Momentum Strategy
#
# Real-world quantitative investment firms differentiate between "high quality" and "low quality" momentum stocks:
#
# * High-quality momentum stocks show "slow and steady" outperformance over long periods of time
# * Low-quality momentum stocks might not show any momentum for a long time, and then surge upwards.
#
# The reason why high-quality momentum stocks are preferred is because low-quality momentum can often be cause by short-term news that is unlikely to be repeated in the future (such as an FDA approval for a biotechnology company).
#
# To identify high-quality momentum, we're going to build a strategy that selects stocks from the highest percentiles of: 
#
# * 1-month price returns
# * 3-month price returns
# * 6-month price returns
# * 1-year price returns
#
# Let's start by building our DataFrame. You'll notice that I use the abbreviation `hqm` often. It stands for `high-quality momentum`.
###################################################################################################
## Create a dataframe for High Quality Momentum stock evaluation
# Input:            stocks; a dataframe that contains all of the symbols for the stocks we evaluate
# Output:           final_dataframe; a dataframe that has the requested information for each stock
# Precondition:     IEX is active, Computer is Connected to the Internet, API Key is valid
# Postcondition:    final_dataframe = pd.DataFrame()
# General Workflow: 
#                   Breaks the list of stock symbols into smaller sublists
#                   Batch API calls from each sublist 
#                   Appends parsed response from api to final result
#                   Returns final result
###################################################################################################
def get_hqm_dataframe(stocks):
    symbol_groups = list(chunks(stocks['Symbol'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))
    #     print(symbol_strings[i])

    hqm_columns = [
                    'Symbol', 
                    'Price', 
                    'Number of Shares to Buy', 
                    'One-Year Price Return', 
                    'One-Year Return Percentile',
                    'Six-Month Price Return',
                    'Six-Month Return Percentile',
                    'Three-Month Price Return',
                    'Three-Month Return Percentile',
                    'One-Month Price Return',
                    'One-Month Return Percentile',
                    'HQM Score'
                    ]

    hqm_dataframe = pd.DataFrame(columns = hqm_columns)

    for symbol_string in symbol_strings:
    #     print(symbol_strings)
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            hqm_dataframe = hqm_dataframe.append(
                                            pd.Series([symbol, 
                                                    data[symbol]['quote']['latestPrice'],
                                                    'N/A',
                                                    data[symbol]['stats']['year1ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month6ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month3ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month1ChangePercent'],
                                                    'N/A',
                                                    'N/A'
                                                    ], 
                                                    index = hqm_columns), 
                                            ignore_index = True)
            
    return hqm_dataframe


def calculate_HQM_Score(hqm_dataframe, time_periods):
    for row in hqm_dataframe.index:
        momentum_percentiles = []
        for time_period in time_periods:
            momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
        hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)
    return hqm_dataframe


## Calculating Momentum Percentiles
# 
# We now need to calculate momentum percentile scores for every stock in the universe. More specifically, we need to calculate percentile scores for the following metrics for every stock:
# 
# * `One-Year Price Return`
# * `Six-Month Price Return`
# * `Three-Month Price Return`
# * `One-Month Price Return`
def Momentum_Percentiles(hqm_dataframe):
    time_periods = [
                    'One-Year',
                    'Six-Month',
                    'Three-Month',
                    'One-Month'
                    ]

    for row in hqm_dataframe.index:
        for time_period in time_periods:
            hqm_dataframe.loc[row, f'{time_period} Return Percentile'] =  stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100

    # Print each percentile score to make sure it was calculated properly
    # for time_period in time_periods:
        # print(hqm_dataframe[f'{time_period} Return Percentile'])

    hqm_dataframe = calculate_HQM_Score(hqm_dataframe, time_periods)
    return hqm_dataframe


def Calculate_HQM_Stocks(stocks):
    #Get the size of the portfolio
    portfolio_size = portfolio_input()
    print('Your portfolio is valued at: $' + str(portfolio_size))

    hqm_dataframe = get_hqm_dataframe(stocks)
    # print(hqm_dataframe)
    hqm_dataframe = Momentum_Percentiles(hqm_dataframe)
    hqm_dataframe = remove_Low_Momentum_Stocks(hqm_dataframe, 'HQM Score', 50)
    # hqm_dataframe.sort_values(by = 'HQM Score', ascending = False, inplace = True, ignore_index = True)
    # hqm_dataframe = hqm_dataframe.iloc[:51]
    # print(hqm_dataframe)

    hqm_dataframe = calculate_position(portfolio_size, hqm_dataframe)
    hqm_dataframe.to_csv( OUTFOLDER + '/high-quality-momentum/HQM_Recommended_Trades.csv')
    hqm_dataframe.to_excel(OUTFOLDER +"/high-quality-momentum/HQM_Recommended_trades.xlsx")
    print("Finished High Qualtiy Momentum.\n")


def Calculate_Simple_Momentum_Stocks(stocks):
    #create the dataframe
    sm_dataframe = create_dataframe(stocks)

    #remove low performance stocks
    remove_Low_Momentum_Stocks(sm_dataframe,'One-Year Price Return', 50)

    #determine the portfolio size
    portfolio_size = portfolio_input()
    print('Your portfolio is: $' + str(portfolio_size))

    #calculate the total positions for the client
    sm_dataframe = calculate_position(portfolio_size, sm_dataframe)
    
    #output the results to a csv file
    sm_dataframe.to_csv( OUTFOLDER + '/simple-momentum/Momentum_Recommended_Trades.csv')
    sm_dataframe.to_excel(OUTFOLDER +"/simple-momentum/Momentum_Recommended_trades.xlsx")
    print("Finished Calcuating Simple Momentum.\n")




def main():
    print("Loading in stock information.")
    stocks = pd.read_csv(INFOLDER + '/sp_500_stocks.csv')
    print("Finished Loading in stock information.\n")
    print("Calculating Simple Momentum Stocks")    
    Calculate_Simple_Momentum_Stocks(stocks)
    print("Calculating High Quality Momentum Stocks")    
    Calculate_HQM_Stocks(stocks)

    

if __name__ == "__main__":
    main()