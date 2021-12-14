import numpy as np
import pandas as pd 
import requests
import xlsxwriter
import math

#Get information from the S&P500
stocks = pd.read_csv('sp_500_stocks.csv')
type(stocks)
print(stocks)

#Aquire and API Token
#IEX Cloud API Token 
#secrets.py file is to hide private information
from secrets import IEX_CLOUD_API_TOKEN

#Make your first API Call
symbol = 'AAPL'
api_url = 'https://sandbox.iexapis.com/'