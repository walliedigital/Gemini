# Gemini Challenge

This project is part of the Gemini Challenge to find currency pairs that exceed a standard deviation threshold.

## Setup and Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/walliedigital/Gemini.git
    cd Gemini
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Available Command-Line Arguments

The script `main.py` accepts several command-line arguments to control its behavior. Here is a list of available
arguments:

- `--currency`: Currency pair to evaluate like `btcusd` or `ethgusd`; uses all available currency pairs if `currency` is
  not set or set to `ALL`
- `--deviation`: Standard deviation of prices in the past 24 hours must exceed this value; default value is `1.0`
- `--log-level`: Specifies the log level for the script. Possible values are `DEBUG`, `INFO`, `WARNING`, `ERROR`,
  and `CRITICAL`; default is `INFO`
- `--debug`: When included, additional details are written to STDOUT

> [!IMPORTANT]
> Logging has not been enabled

## CLI Help Content

```
usage: main.py [-h] [-c CURRENCY] [-d DEVIATION] [-l {CRITICAL,ERROR,WARN,INFO,DEBUG}] [--debug DEBUG]

Log an alert if the standard deviation for a currency using hourly values for the last 24 hours exceeds the standard deviation threshold.

options:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
                        Currency trading pair, or ALL
  -d DEVIATION, --deviation DEVIATION
                        Standard deviation threshold, default is 1.0
  -l {CRITICAL,ERROR,WARN,INFO,DEBUG}, --log-level {CRITICAL,ERROR,WARN,INFO,DEBUG}
                        Log level, default is INFO
  --debug DEBUG         Debug mode, default is False
```

## Usage Examples

1. **Run the script with no arguments set will check all of the currency pairs for a standard deviation above 1.0:**
    ```sh
    python main.py
    ```

2. **Run the script for a specific trading pair:**
    ```sh
    python main.py --c etheur
    ```

## Sample Output

```json
{
  'timestamp': '2024-07-15T19:46:02.408916+00:00',
  'level': 'INFO',
  'trading_pair': 'etheur',
  'deviation': True,
  'data': {
    'last_price': '2930.05',
    'average': '3046.46',
    'change': '-185.17',
    'sdev': '53.974868635975675'
  }
}

```

## Code Overview

### Main Script

The main script (`main.py`) processes command-line arguments and logs messages based on the specified log level.

### Gemini public APIs being used:

- https://api.gemini.com/v1/symbols
- https://api.gemini.com/v2/ticker/:currency_pair

## Dependencies

- `requests==2.32.3`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

