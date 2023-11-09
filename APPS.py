import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Monitoring Influenza Activity Worldwide")

page_bg_img = f"""
<style>
  body {{
    background-image: url("https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 180%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
    opacity: 0.7; /* Set the opacity to make the background transparent */
  }}
</style>
"""

# Inject the CSS style into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Loading the data
df = pd.read_csv(r'https://raw.githubusercontent.com/Gill817/INFLUENZA_APP/main/VIW_FNT.csv')
min_year = df['ISO_YEAR'].min()

# Convert date columns to datetime format as usual
df['ISO_WEEKSTARTDATE'] = pd.to_datetime(df['ISO_WEEKSTARTDATE'])



# Create two columns
col1, col2 = st.columns([0.2, 0.8])

# Place user options in the left column
with col1:
    plot_type = st.selectbox("Select Plot Type:", ['Time Series', 'Scatter Plot', 'Bar Plot', 'Pie Chart'])
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
