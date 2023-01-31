import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='sales dashboard',
    layout='wide'
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
    io=r"C:\Users\Carlos\Downloads\supermarkt_sales.xlsx",
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df=get_data_from_excel()

st.sidebar.header('please filter here:')
city = st.sidebar.multiselect(
    'select the city:',
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    'select the customer type:',
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    'select the gender:',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

st.title('sales dashboard')
st.markdown('##')

total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(), 1)
star_rating = int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection['Total'].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('total sales:')
    st.subheader(f'US $ {total_sales:,}')
with middle_column:
    st.subheader('average rating:')
    st.subheader(f'{average_rating}')
with right_column:
    st.subheader('average sale per transaction:')
    st.subheader(f'US $ {average_sale_by_transaction}')

st.markdown('---')

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title='<b>sales by product</b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template='plotly_white'
)

fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
