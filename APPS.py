import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Monitoring Influenza Activity Worldwide")

page_bg = '''
<style>
body {
  background-image: url("https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
  opacity: 0.7;
  font-color: white;
}
</style>
'''
st.markdown(page_bg, unsafe_allow_html=True)
df = pd.read_csv(r'https://raw.githubusercontent.com/Gill817/INFLUENZA_APP/main/VIW_FNT.csv')
min_year = df['ISO_YEAR'].min()

df['ISO_WEEKSTARTDATE'] = pd.to_datetime(df['ISO_WEEKSTARTDATE'])

st.sidebar.title("Options")

plot_type = st.sidebar.selectbox("Select Plot Type:", ['Time Series', 'Scatter Plot', 'Bar Plot', 'Pie Chart'])
selected_start_year = st.sidebar.selectbox("Select Start Year:", range(2023, min_year - 1, -1))
selected_end_year = st.sidebar.selectbox("Select End Year:", range(2023, min_year - 1, -1))
selected_continent = st.sidebar.selectbox("Select Continent:", df['WHOREGION'].unique())
selected_variant = st.sidebar.selectbox("Select Virus Variant:", ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'AOTHER_SUBTYPE_DETAILS', 'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B', 'INF_ALL', 'INF_NEGATIVE', 'ILI_ACTIVITY', 'ADENO', 'BOCA', 'HUMAN_CORONA', 'METAPNEUMO', 'PARAINFLUENZA', 'RHINO'])
start_month = st.sidebar.selectbox("Select Start Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())
end_month = st.sidebar.selectbox("Select End Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())
start_date = pd.to_datetime(f'{selected_start_year}-{start_month}-01')
end_date = pd.to_datetime(f'{selected_end_year}-{end_month}-01') + pd.DateOffset(days=31)

if plot_type in ['Time Series', 'Scatter Plot']:
    selected_countries = st.sidebar.multiselect("Select Countries:", df[df['WHOREGION'] == selected_continent]['COUNTRY_AREA_TERRITORY'].unique())
    df_filtered = df[(df['ISO_YEAR'] >= selected_start_year) & (df['ISO_YEAR'] <= selected_end_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date) & (df['COUNTRY_AREA_TERRITORY'].isin(selected_countries))]
else:
    df_filtered = df[(df['ISO_YEAR'] >= selected_start_year) & (df['ISO_YEAR'] <= selected_end_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date)]

if plot_type == 'Time Series':
    time_series_data = df_filtered.groupby(['ISO_WEEKSTARTDATE', 'COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
    fig = px.line(time_series_data, x='ISO_WEEKSTARTDATE', y=selected_variant, color='COUNTRY_AREA_TERRITORY', labels={'ISO_WEEKSTARTDATE': 'Time', 'value': 'Count'}, title=f'Influenza {selected_variant} Over Time in {selected_continent}', template='plotly_dark')
    st.plotly_chart(fig)

elif plot_type == 'Scatter Plot':
    scatter_plot_data = df_filtered.groupby(['ISO_WEEKSTARTDATE', 'COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
    fig = px.scatter(scatter_plot_data, x='ISO_WEEKSTARTDATE', y=selected_variant, color='COUNTRY_AREA_TERRITORY', labels={'ISO_WEEKSTARTDATE': 'Time', 'value': 'Count'}, title=f'Influenza {selected_variant} Scatter Plot in {selected_continent}', template='plotly_dark')
    st.plotly_chart(fig)

elif plot_type == 'Bar Plot':
    bar_plot_data = df_filtered.groupby(['COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
    top_10_countries = bar_plot_data.nlargest(10, selected_variant)
    fig = px.bar(top_10_countries, x='COUNTRY_AREA_TERRITORY', y=selected_variant, labels={'value': 'Count'}, title=f'Top 10 Countries for Influenza {selected_variant} in {selected_continent} ({selected_start_year} - {selected_end_year})', template='plotly_dark')
    st.plotly_chart(fig)

elif plot_type == 'Pie Chart':
    pie_chart_data = df_filtered.groupby(['COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
    top_20_countries = pie_chart_data.nlargest(20, selected_variant)
    fig = px.pie(top_20_countries, names='COUNTRY_AREA_TERRITORY', values=selected_variant, title=f'Top 20 Countries for Influenza {selected_variant} in {selected_continent} ({selected_start_year} - {selected_end_year})')
    st.plotly_chart(fig)


