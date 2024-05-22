# OSRS Deadman Data Viewer

This is a Flask application that allows users to view and interact with data from the runelite DMM CSV file. The application provides functionality to search for specific items and visualize their data over time.

## Demo
https://calum.github.io/dmm-data-viewer/ 

## Features

- **Home Page:** Allows for filtering and sorting of data.
- **Item Search:** Enables users to search for an item and view a graph of its average high price, average low price, and total volume over time.

## Prerequisites

- Python 3.8+
- `pip` (Python package installer)

## Setup

### Clone the Repository

```bash
git clone https://github.com/calum/dmm-data-viewer.git
cd dmm-data-viewer
```

### Using `pipenv` (Recommended)

1. **Install `pipenv` if not already installed:**

    ```bash
    pip install pipenv
    ```

2. **Install dependencies:**

    ```bash
    pipenv install
    ```

3. **Activate the virtual environment:**

    ```bash
    pipenv shell
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

### Using `pip`

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the application:**

    ```bash
    python app.py
    ```

## Usage

### Item Search

1. Navigate to `/item-search` to use the item search functionality.
2. Start typing an item name and select from the autocomplete suggestions.
3. Click "Search" to view a graph of the item's data over time.

### Viewing Graphs

1. The graph will display:
    - **Average High Price** in blue.
    - **Average Low Price** in red.
    - **Total Volume** in green (initially hidden, can be toggled from the legend).
