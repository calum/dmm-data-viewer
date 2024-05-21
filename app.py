from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import logging

app = Flask(__name__)
pio.templates.default = "plotly_white"  # Setting the default plotly template

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Try to load the data and log the first line
df = pd.read_csv('deadman_apocalypse.csv')
df['dateTime'] = pd.to_datetime(df['unixTime'], unit='s')
df.fillna(0, inplace=True)  # Replace all NaN values with 0
logging.info("First line of the CSV:")
logging.info(df.iloc[0])  # Log the first line of the dataframe

# Load item names
item_names_df = pd.read_csv('ItemID.csv')
item_names_df['itemId'] = pd.to_numeric(item_names_df['ID'])
logging.info("Item names CSV loaded successfully.")

# Merge item names into the main DataFrame on 'itemId'
try:
    df = pd.merge(df, item_names_df, on='itemId', how='left')
    logging.info("DataFrames merged successfully.")
except Exception as e:
    logging.error("Error merging DataFrames:", exc_info=True)

@app.route('/item-search', methods=['GET', 'POST'])
def item_search():
    items = df['Item Name'].dropna().unique().tolist()
    items.sort()
    if request.method == 'POST':
        item_name = request.form['item_name']
        return redirect(url_for('display_graph', item_name=item_name))
    return render_template('item_search.html', items=items)

@app.route('/display-graph', methods=['GET'])
def display_graph():
    item_name = request.args.get('item_name')
    if item_name:
        data_filtered = df[df['Item Name'] == item_name]
        # Filter the data to include only dates up to September 14th, 2023
        data_filtered = data_filtered[data_filtered['dateTime'] <= pd.Timestamp('2023-09-14')]
        
        if not data_filtered.empty:
            # Prepare the plot with two y-axes
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add line for avgHighPrice
            fig.add_trace(go.Scatter(x=data_filtered['dateTime'], y=data_filtered['avgHighPrice'],
                                     mode='lines', name='Average High Price', line=dict(color='blue')),
                          secondary_y=False)

            # Add line for avgLowPrice
            fig.add_trace(go.Scatter(x=data_filtered['dateTime'], y=data_filtered['avgLowPrice'],
                                     mode='lines', name='Average Low Price', line=dict(color='red')),
                          secondary_y=False)

            # Calculate the sum of highPriceVolume and lowPriceVolume and add as trace
            data_filtered['totalVolume'] = data_filtered['highPriceVolume'] + data_filtered['lowPriceVolume']
            fig.add_trace(go.Scatter(x=data_filtered['dateTime'], y=data_filtered['totalVolume'],
                                     mode='lines', name='Total Volume', line=dict(color='green'),
                                     visible='legendonly'),  # Make this trace toggleable but hidden by default
                          secondary_y=True)

            # Update axis labels
            fig.update_layout(title=f'Item Data Over Time for {item_name}',
                              xaxis_title='Date Time',
                              yaxis_title='Price',
                              legend_title='Legend')
            fig.update_yaxes(title_text='Volume', secondary_y=True)

            graph_html = fig.to_html(full_html=False)
            return render_template('display_graph.html', graph_html=graph_html, item_name=item_name)
        else:
            return "No data available for item: {}".format(item_name), 404
    else:
        return "Please select an item to view the graph.", 400


# Home route with multi-column filters and sorting
@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    per_page = 250
    start = (page - 1) * per_page
    end = start + per_page

    filtered_df = df.copy()

    if request.method == 'POST':
        # Apply filters
        for column in filtered_df.columns:
            if request.form.get(column):
                filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(request.form[column], case=False, na=False)]

        # Apply sorting
        sort_column = request.form.get('sort_column')
        sort_order = request.form.get('sort_order', 'asc')
        if sort_column:
            filtered_df = filtered_df.sort_values(by=sort_column, ascending=sort_order == 'asc')

    page_data_html = filtered_df.iloc[start:end].to_html(classes='data', header="true", index=False, escape=False).replace('\n', '')
    return render_template('index.html', tables=page_data_html, df_columns=filtered_df.columns.tolist(), page=page)

if __name__ == "__main__":
    app.run(debug=True)
