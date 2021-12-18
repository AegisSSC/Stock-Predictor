import numpy as np
import pandas as pd 
import requests
import xlsxwriter
import math

#Aquire and API Token
#IEX Cloud API Token 
#secrets.py file is to hide private information
from secrets import IEX_CLOUD_API_TOKEN

OUTFOLDER = str('output-files/Basic_Portfolio')
INFOLDER = str('stock-data')

def scrape_data():
    #Get information from the S&P500
    stocks = pd.read_csv( INFOLDER + '/sp_500_stocks.csv')
    type(stocks)
    print(stocks)
    my_columns = ['Symbol', 'Stock Price', 'Market Capitalization', 'Number of Stocks to Buy']

    symbol_groups = list(chunks(stocks['Symbol'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    final_dataframe = pd.DataFrame(columns= my_columns)
    
    for symbol_string in symbol_strings:
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            final_dataframe = final_dataframe.append(
                pd.Series([
                        symbol,
                        data[symbol]['quote']['latestPrice'],
                        data[symbol]['quote']['marketCap'],
                        'N/A'], 
                        index=my_columns), 
                        ignore_index=True)
    return final_dataframe



def write_output(final_dataframe):
    #Write the data output 
    writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
    final_dataframe.to_excel(writer, sheet_name='Recommended Trades', index = False)
    
    
    #freeCodeCamp Colors
    background_color = '#0a0a23'
    font_color = '#ffffff'

    string_format = writer.book.add_format(
            {
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    dollar_format = writer.book.add_format(
            {
                'num_format':'$0.00',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    integer_format = writer.book.add_format(
            {
                'num_format':'0',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )
        
    writer.sheets['Recommended Trades'].set_column('A1', 'Symbol', string_format)
    writer.sheets['Recommended Trades'].set_column('B1', 'Stock Price', dollar_format)
    writer.sheets['Recommended Trades'].set_column('C1', 'Market Capitalization', dollar_format)
    writer.sheets['Recommended Trades'].set_column('D1', 'Number of Shares to Buy', integer_format)

    column_formats = { 
                    'A': ['Ticker', string_format],
                    'B': ['Price', dollar_format],
                    'C': ['Market Capitalization', dollar_format],
                    'D': ['Number of Shares to Buy', integer_format]
                    }
    for column in column_formats.keys():
        writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
        writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], string_format)

    #save the spreadsheet
    writer.save()


def calculate_position(final_dataframe, portfolio_size):
    
    #calculate the total amount that you can spend per company
    position_size = portfolio_size/len(final_dataframe.index)

    #for every company listed, determine how many shares you can purchase with the amount allocated per company
    for i in range(0, len(final_dataframe)):
        final_dataframe.loc[i, 'Number of Stocks to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])
    print(final_dataframe)

    return final_dataframe

#Use a batch API Call
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def main():

    final_dataframe = scrape_data()
    
    portfolio_size = input('Enter the value of your portfolio  ')

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That is not a number! \n Please try again:")
        portfolio_size = input('Enter the value of your portfolio:  ')
        val = float(portfolio_size)

    #Calculate the total number of shares to buy of all of the given stocks. 
    final_dataframe = calculate_position(final_dataframe, val)


    #Export the information to csv and excel documents
    final_dataframe.to_csv( OUTFOLDER + '/CSVRecommended_Trades.csv')
    final_dataframe.to_excel(OUTFOLDER +"/XLSXRecommended_trades.xlsx")
    # write_output(final_dataframe)

if __name__ == "__main__":
    main()
   