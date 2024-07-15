"""Gemini API example"""
import argparse
import datetime
import threading
from enum import Enum

import requests


class LogLevel(Enum):
    """
    An enumeration representing different log levels.

    Log levels are used to categorize log messages based on their severity or importance.
    This class defines the following log levels:

    - CRITICAL: Indicates a critical error or system failure.
    - ERROR: Indicates an error condition that should be addressed.
    - WARN: Indicates a warning condition that may require attention.
    - INFO: Indicates an informational message for tracking the application flow.
    - DEBUG: Indicates a debug message for detailed debugging information.

    These log levels can be used in a logging system to filter and handle log messages
    based on their importance or severity.
    """
    CRITICAL = 'CRITICAL'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'


BASE_URL = 'https://api.gemini.com'
DEFAULT_TIMEOUT = 10
DEFAULT_CURRENCY = 'ALL'
DEFAULT_STANDARD_DEVIATION = 1.0
DEFAULT_LOG_LEVEL = LogLevel.INFO.value


def get_currency_pairs(debug=False):
    """
    Retrieves a list of available currency pairs from the Gemini Symbols API.

    Args:
        debug (bool): If True, logs additional information about the API call.

    Returns:
        list: A list of currency pairs as strings.
    """
    endpoint = f'{BASE_URL}/v1/symbols'
    response = requests.get(endpoint, timeout=DEFAULT_TIMEOUT)
    if response.status_code == 200:
        pairs = response.json()
        if debug:
            print(f'API call: {endpoint}')
            print(f'Response: {pairs}')
        return pairs
    else:
        if debug:
            print(f'API call: {endpoint}')
            print(f'Error: {response.status_code} - {response.text}')
        return []


def get_ticker_data(currency_pair, debug=False):
    """
    Retrieves the current pricing information for a given currency pair from the Gemini Ticker API.

    Args:
        currency_pair (str): The currency pair to retrieve ticker information for.
        debug (bool): If True, logs additional information about the API call.

    Returns:
        dict: A dictionary containing the ticker information for the specified currency pair.
    """
    endpoint = f'{BASE_URL}/v2/ticker/{currency_pair}'
    response = requests.get(endpoint, timeout=DEFAULT_TIMEOUT)
    if response.status_code == 200:
        ticker_data = response.json()
        if debug:
            print(f'API call: {endpoint}')
            print(f'Response: {ticker_data}')
        return ticker_data
    else:
        if debug:
            print(f'API call: {endpoint}')
            print(f'Error: {response.status_code} - {response.text}')
        return {}


def calculate_standard_deviation(prices, debug=False):
    """
    Calculates the standard deviation of a list of prices.

    Args:
        prices (list): A list of prices as strings.
        debug (bool): If True, logs additional information about the calculation.

    Returns:
        float: The standard deviation of the prices.
    """
    prices = [float(price) for price in prices]
    mean = sum(prices) / len(prices)
    squared_diffs = [(price - mean) ** 2 for price in prices]
    variance = sum(squared_diffs) / len(prices)
    standard_deviation = variance ** 0.5
    if debug:
        print(f'Prices: {prices}')
        print(f'Mean: {mean}')
        print(f'Variance: {variance}')
        print(f'Standard Deviation: {standard_deviation}')
    return standard_deviation


def process_currency_pair(currency_pair, deviation, log_level, debug=False):
    """
    Processes a currency pair and prints a message to STDOUT if the standard deviation for the last 24 hours
    exceeds the specified deviation threshold.

    Args:
        currency_pair (str): The currency pair being processed.
        deviation (float): The standard deviation threshold.
        log_level (str): The logging level.
        debug (bool): If True, logs additional information about the calculation and condition checking.

    Returns:
        None
    """
    # Get price data for the last 24 hours
    ticker_data = get_ticker_data(currency_pair, debug)
    # Exit if no data is available for the currency pair
    if not ticker_data or 'changes' not in ticker_data:
        if debug:
            print(f'No data available for {currency_pair}')
        return
    standard_deviation = calculate_standard_deviation(ticker_data['changes'], debug)
    if standard_deviation > deviation:
        # Calculate the average price for the last 24 hours
        average_price = format(sum([float(price) for price in ticker_data['changes']]) / len(ticker_data['changes']), '.2f')
        # Calculate the price change between open and close
        price_change = format(float(ticker_data['close']) - float(ticker_data['open']), '.2f')

        alert_data = {'timestamp': f'{datetime.datetime.now(datetime.UTC).isoformat()}', 'level': log_level,
            'trading_pair': currency_pair, 'deviation': True,
            'data': {'last_price': f'{ticker_data["close"]}', 'average': f'{average_price}',
                'change': f'{price_change}', 'sdev': f'{standard_deviation}'}}
        print(alert_data)


def check_currency(currency=DEFAULT_CURRENCY, deviation=DEFAULT_STANDARD_DEVIATION, log_level=DEFAULT_LOG_LEVEL,
                   debug=False):
    """
    Checks if the standard deviation for a currency using hourly values for the last 24 hours exceeds the specified deviation threshold.

    Args:
        currency (str): The currency pair to check, or 'ALL' to check all available currency pairs.
        deviation (float): The standard deviation threshold.
        log_level (str): The log level to use for logging.
        debug (bool): If True, logs additional information about the API calls and calculations.

    Returns:
        None
    """
    # Get current list of available currency pairs
    available_pairs = get_currency_pairs(debug)
    # Exit if no currency pairs are available
    if not available_pairs:
        print('No currency pairs available.')
        return
    # Reset list for a single currency pair
    if currency != 'ALL':
        if currency not in available_pairs:
            print(f'Invalid currency pair: {currency}')
            return
        available_pairs = [currency]
    # Create a thread for each currency pair
    threads = []
    for pair in available_pairs:
        thread = threading.Thread(target=process_currency_pair, args=(pair, deviation, log_level, debug))
        threads.append(thread)
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Log an alert if the standard deviation for a currency using hourly values for the last 24 hours exceeds the standard deviation threshold.')
    parser.add_argument('-c', '--currency', type=str, default='ALL', required=False,
                        help='Currency trading pair, or ALL')
    parser.add_argument('-d', '--deviation', type=float, default=1.0, required=False,
                        help='Standard deviation threshold, default is 1.0')
    parser.add_argument('-l', '--log-level', type=str, default='INFO', required=False,
                        choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], help='Log level, default is INFO')
    parser.add_argument('--debug', type=bool, default=False, required=False, help='Debug mode, default is False')
    args = parser.parse_args()
    check_currency(currency=args.currency, deviation=args.deviation, log_level=args.log_level, debug=args.debug)
