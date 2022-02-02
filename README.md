###################################################################################################
# Stock-Predictor
 

###################################################################################################
# Quantitive_Momentum_Strategy



###################################################################################################
def create_dataframe(stocks):      
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


###################################################################################################
def calculate_position(portfolio_size, final_dataframe):
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





## Removing Low-Momentum Stocks
# The investment strategy that we're building seeks to identify the 50 highest-momentum stocks in the S&P 500.
# Because of this, the next thing we need to do is remove all the stocks in our DataFrame that fall below this momentum threshold. 
# We'll sort the DataFrame by the stocks' one-year price return, and drop all stocks outside the top 50.
###################################################################################################
def remove_Low_Momentum_Stocks(starting_dataframe, sort_request, remaining_rows):
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


# We'll sort the DataFrame by the stocks' one-year price return, and drop all stocks outside the top 50.

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
def get_hqm_dataframe(stocks):
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


## Calculating Momentum Percentiles
###################################################################################################
def Momentum_Percentiles(hqm_dataframe):
    # We now need to calculate momentum percentile scores for every stock in the universe. More specifically,
    #  we need to calculate percentile scores for the following metrics for every stock:
    # 
    # * `One-Year Price Return`
    # * `Six-Month Price Return`
    # * `Three-Month Price Return`
    # * `One-Month Price Return`
###################################################################################################
