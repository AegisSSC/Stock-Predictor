
#Backtest the overall performance of the model over a given interval of time
#

#Gathers information to import in for testing
def read_data(timescale):
        pass 

#Formula used to calculate the total value of all stocks in a portfolio at a given time
def calculate_position(portfolio):
    position = 0
    for stock in portfolio:
        value_of_stock = portfolio[stock]['Price'] * portfolio[stock]['Number of Shares to Buy']
        position += value_of_stock
    return position

#Formula used to calculate the change in value of a portfolio between two points in time
#Returns the difference between the two points in time for a portfolio
def calculate_change_in_position(position_x, position_y):
    return (position_y-position_x, ((position_y-position_x)/position_x))


#Formula used to calculate the change in value of a given stock between two points in time
#Returns the difference between the two points in time for a stock
def calculate_change_in_stock(stock_x, stock_y):
    return stock_y-stock_x

#main function
def BackTest():
    #read in data for a given timeframe
    data = read_data()

    position = []

    #for every interval in the timeframe (each instance in the timeframe should be a "step" for the interval)
    for interval in timescale:
        #calculate total position of the portfolio
        position[interval] = calculate_position()
        #calculate total change in each stock

        #show the best performing stocks

        #show the worst performing stocks
    