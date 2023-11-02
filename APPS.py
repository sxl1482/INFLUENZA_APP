import pandas as pd
import plotly.express as px
import streamlit as st
import requests  # Add this line to import the 'requests' module
import io



# Loading the data
def filter_and_fix_lines(text):
  lines = text.split("\n")
  filtered_lines = []
  for line in lines:
    fields = line.split(",")
    if len(fields) == 41:  # Adjust the field count as needed
      filtered_lines.append(line)
    else:
      # Handle or fix the problematic line as needed
      # For example, you can split the line and fill missing fields with empty values
      fields.extend([''] * (41 - len(fields)))  # Fill missing fields
      filtered_lines.append(','.join(fields))
  return "\n".join(filtered_lines)

# Download the CSV file and apply the filtering function
raw_csv_url = 'https://github.com/Gill817/INFLUENZA_APP/blob/e9139f50b7829322aec9df7b55fbe7129052336c/VIW_FNT.csv'
response = requests.get(raw_csv_url)
if response.status_code == 200:
  filtered_text = filter_and_fix_lines(response.text)
  df = pd.read_csv(io.StringIO(filtered_text))

# Rename the 'ISOYEAR' column to 'ISO_YEAR'
df.columns = df.columns.str.replace('ISOYEAR', 'ISO_YEAR')

# Strip leading and trailing whitespace from column names
df.columns = df.columns.str.strip()

# Get the minimum year
min_year = df['ISO_YEAR'].min()

# Convert date columns to datetime format as usual
df['ISO_WEEKSTARTDATE'] = pd.to_datetime(df['ISO_WEEKSTARTDATE'])

# Define the app layout
st.title("Influenza Data Analysis")

# Create two columns
col1, col2 = st.columns(2)

# Place user options in the left column
with col1:
    plot_type = st.radio("Select Plot Type:", ['Time Series', 'Scatter Plot', 'Bar Plot', 'Pie Chart'])
    selected_year = st.selectbox("Select Year:", range(2023, min_year - 1, -1))
    selected_continent = st.selectbox("Select Continent:", df['WHOREGION'].unique())
    selected_variant = st.selectbox("Select Virus Variant:", ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'AOTHER_SUBTYPE_DETAILS', 'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B', 'INF_ALL', 'INF_NEGATIVE', 'ILI_ACTIVITY', 'ADENO', 'BOCA', 'HUMAN_CORONA', 'METAPNEUMO', 'PARAINFLUENZA', 'RHINO'])
    start_month = st.selectbox("Select Start Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())
    end_month = st.selectbox("Select End Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())

    # Filter the data based on selected options
    start_date = pd.to_datetime(f'{selected_year}-{start_month}-01')
    end_date = pd.to_datetime(f'{selected_year}-{end_month}-01') + pd.DateOffset(days=31)

    if plot_type in ['Time Series', 'Scatter Plot']:
        # Allow user to select multiple countries
        selected_countries = st.multiselect("Select Countries:", df[df['WHOREGION'] == selected_continent]['COUNTRY_AREA_TERRITORY'].unique())
        df_filtered = df[(df['ISO_YEAR'] == selected_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date) & (df['COUNTRY_AREA_TERRITORY'].isin(selected_countries))]
    else:
        df_filtered = df[(df['ISO_YEAR'] == selected_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date)]

# Place the plot in the right column
with col2:
    if plot_type == 'Time Series':
        # Group the data by 'ISO_WEEKSTARTDATE' and calculate the sum of the selected variant to generate the graph
        time_series_data = df_filtered.groupby(['ISO_WEEKSTARTDATE', 'COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
        # Create an interactive time series plot
        fig = px.line(time_series_data, x='ISO_WEEKSTARTDATE', y=selected_variant, color='COUNTRY_AREA_TERRITORY', labels={'ISO_WEEKSTARTDATE': 'Time', 'value': 'Count'}, title=f'Influenza {selected_variant} Over Time in {selected_continent}', template='plotly_dark')
        st.plotly_chart(fig)

    elif plot_type == 'Scatter Plot':
        # Group the data by 'ISO_WEEKSTARTDATE' and calculate the sum of the selected variant to generate the graph
        scatter_plot_data = df_filtered.groupby(['ISO_WEEKSTARTDATE', 'COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
        # Create a scatter plot
        fig = px.scatter(scatter_plot_data, x='ISO_WEEKSTARTDATE', y=selected_variant, color='COUNTRY_AREA_TERRITORY', labels={'ISO_WEEKSTARTDATE': 'Time', 'value': 'Count'}, title=f'Influenza {selected_variant} Scatter Plot in {selected_continent}', template='plotly_dark')
        st.plotly_chart(fig)

    elif plot_type == 'Bar Plot':
        # Group the data by 'COUNTRY_AREA_TERRITORY' and calculate the sum of the selected variant to generate the bar plot
        bar_plot_data = df_filtered.groupby(['COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
        # Select the top 10 countries
        top_10_countries = bar_plot_data.nlargest(10, selected_variant)
        # Create a bar plot for the top 10 countries
        fig = px.bar(top_10_countries, x='COUNTRY_AREA_TERRITORY', y=selected_variant, labels={'value': 'Count'}, title=f'Top 10 Countries for Influenza {selected_variant} in {selected_continent} ({selected_year})', template='plotly_dark')
        st.plotly_chart(fig)

    elif plot_type == 'Pie Chart':
        # Group the data by 'COUNTRY_AREA_TERRITORY' and calculate the sum of the selected variant to generate the pie chart
        pie_chart_data = df_filtered.groupby(['COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
        # Select the top 20 countries
        top_20_countries = pie_chart_data.nlargest(20, selected_variant)
        # Create a pie chart for the top 20 countries
        fig = px.pie(top_20_countries, names='COUNTRY_AREA_TERRITORY', values=selected_variant, title=f'Top 20 Countries for Influenza {selected_variant} in {selected_continent} ({selected_year})')
        st.plotly_chart(fig)
