import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('startup_clean.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
st.set_page_config(layout='wide',page_title='Startup analysis')
def load_investor_details(investor):
    st.title(investor)

    investor_df = df[df['investors'].str.contains(investor, case=False, na=False, regex=False)]

    # Recent 5 investments
    st.subheader('Most Recent Investments')
    last5_df = investor_df.head(5)[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)

    # Biggest investments
    col1,col2=st.columns(2)
    with col1:
        biggest_investment = (
        investor_df
        .groupby('startup')['amount']
        .sum()
        .sort_values(ascending=False)
        .head(5)
        )
        # Pie chart
        st.subheader('Biggest investment')
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index,biggest_investment.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.1f%%")
        st.pyplot(fig1)
    with col1:
        st.subheader('Year Wise Investment')
        df['Year']=df['date'].dt.year
        Year_series=df[df['investors'].str.contains(investor)].groupby('Year')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.plot(Year_series.index,Year_series.values)
        st.pyplot(fig2)
# Sidebar
st.sidebar.title("Startup Funding Analysis")

options = st.sidebar.selectbox(
    'Select One',
    ['overall Analysis', 'startup-wise Analysis', 'investor-wise Analysis']
)

if options == 'overall Analysis':
    st.title("Overall Analysis of Startup Funding")

elif options == 'startup-wise Analysis':
    selected_startup = st.sidebar.selectbox(
        'Select Startup',
        sorted(df['startup'].dropna().unique().tolist())
    )

    btn1 = st.sidebar.button('Find startup details')

    if btn1:
        st.title(selected_startup)
        startup_df = df[df['startup'] == selected_startup]
        st.dataframe(startup_df)

else:
    investor_list = sorted(
        set(
            df['investors']
            .str.split(',')
            .sum()
        )
    )

    investor_list = [i.strip() for i in investor_list if i.strip() != '']

    selected_investor = st.sidebar.selectbox('Select Investor', investor_list)

    btn2 = st.sidebar.button('Find investor details')

    if btn2:
        load_investor_details(selected_investor)