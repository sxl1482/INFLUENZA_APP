import pandas as pd
import plotly.express as px
import streamlit as st
import spacy

st.title("Monitoring Influenza Activity Worldwide")

# Load the dataset
df = pd.read_csv(r'C:/Users/priya/Downloads/VIW_FNT.csv')
min_year = df['ISO_YEAR'].min()

# Load an NLP model
nlp = spacy.load("en_core_web_sm")

# Function to answer questions
def answer_question(question, dataset):
    # Process the question using NLP
    doc = nlp(question)

    # Identify keywords or entities in the question
    keywords = [token.text for token in doc if token.is_alpha]

    # Match keywords to dataset columns
    relevant_columns = [col for col in dataset.columns if any(keyword.lower() in col.lower() for keyword in keywords)]

    # Retrieve data from the dataset based on the relevant columns
    answers = dataset[relevant_columns]

    # Generate a response
    response = answers.head().to_string(index=False)  # You can customize this based on your dataset structure

    return response

page_bg_img = f"""
<style>
  body {{
    background-image: url("https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 180%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
    opacity: 0.7; 
  }}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

col1, col2 = st.columns([0.2, 0.8])

with col1:
    plot_type = st.selectbox("Select Plot Type:", ['Time Series', 'Scatter Plot', 'Bar Plot', 'Pie Chart'])
    selected_year = st.selectbox("Select Year:", range(2023, min_year - 1, -1))
    selected_continent = st.selectbox("Select Continent:", df['WHOREGION'].unique())
    selected_variant = st.selectbox("Select Virus Variant:", ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'AOTHER_SUBTYPE_DETAILS', 'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B', 'INF_ALL', 'INF_NEGATIVE', 'ILI_ACTIVITY', 'ADENO', 'BOCA', 'HUMAN_CORONA', 'METAPNEUMO', 'PARAINFLUENZA', 'RHINO'])
    start_month = st.selectbox("Select Start Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())
    end_month = st.selectbox("Select End Month:", df['ISO_WEEKSTARTDATE'].dt.strftime('%B').unique())
    start_date = pd.to_datetime(f'{selected_year}-{start_month}-01')
    end_date = pd.to_datetime(f'{selected_year}-{end_month}-01') + pd.DateOffset(days=31)

    if plot_type in ['Time Series', 'Scatter Plot']:
        selected_countries = st.multiselect("Select Countries:", df[df['WHOREGION'] == selected_continent]['COUNTRY_AREA_TERRITORY'].unique())
        df_filtered = df[(df['ISO_YEAR'] == selected_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date) & (df['COUNTRY_AREA_TERRITORY'].isin(selected_countries))]
    else:
        df_filtered = df[(df['ISO_YEAR'] == selected_year) & (df['WHOREGION'] == selected_continent) & (df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date)]

with col2:
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
        fig = px.bar(top_10_countries, x='COUNTRY_AREA_TERRITORY', y=selected_variant, labels={'value': 'Count'}, title=f'Top 10 Countries for Influenza {selected_variant} in {selected_continent} ({selected_year})', template='plotly_dark')
        st.plotly_chart(fig)

    elif plot_type == 'Pie Chart':
        pie_chart_data = df_filtered.groupby(['COUNTRY_AREA_TERRITORY'])[selected_variant].sum().reset_index()
        top_20_countries = pie_chart_data.nlargest(20, selected_variant)
        fig = px.pie(top_20_countries, names='COUNTRY_AREA_TERRITORY', values=selected_variant, title=f'Top 20 Countries for Influenza {selected_variant} in {selected_continent} ({selected_year})')
        st.plotly_chart(fig)

# User's question input
user_question = st.text_input("Ask a question about the dataset:")
if user_question:
    answer = answer_question(user_question, df)
    st.write("Answer:")
    st.write(answer)
