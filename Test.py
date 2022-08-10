import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Analyzing Big Basket Products')
st.caption('### This is an interactive dashboard which provides a comprehensive analysis of the products sold on Big Basket')

@st.cache(persist=True)
def load_data(nrows):
    df=pd.read_csv('BB.csv', nrows=nrows,index_col=0)
    df.dropna(axis=0,inplace=True)
    return df

df=load_data(27556)

st.subheader('Product Rating')

main_cat=st.selectbox('Select Main Category:',list(df['category'].unique()))
mask_1=df['category']==main_cat
sub_cat=st.selectbox('Select Sub Category:', list(df['sub_category'].where(mask_1,np.nan).dropna().unique()))


rating=st.slider('Rating Slider:',0.0,5.0,step=0.5,help='You can sort data by clicking on the columns')
if rating<5:
    st.markdown("Products Rated between %.2f⭐ and %.2f⭐" % (rating, (rating + 0.5) % 24))
else:
    st.markdown("Products Rated %.2f⭐" % (rating % 24))

mask=(df['rating']>=rating) & (df['rating']<(rating+0.5)) &(df['category']==main_cat) & (df['sub_category']==sub_cat)
st.write(df[['product','brand','sale_price','market_price']].where(mask,np.nan).dropna())
st.caption('Total Number of Products:')
st.write(df[['product','brand','sale_price','market_price']].where(mask,np.nan).dropna().shape[0])

pdf=df[['sale_price','market_price']].where(mask,np.nan).dropna()
fig=px.histogram(pdf,nbins=20,color_discrete_sequence=['#FF97FF','#FECB52'])
fig.update_xaxes(dtick=400)
fig.update_layout(bargap=0.2)
fig.update_layout(xaxis_title='Price(INR)',yaxis_title='No. of Products',legend_title="Prices",title="Sale Price and Market Price Histogram" )
st.write(fig)
pig=px.histogram(((df['market_price'].where(mask,np.nan).dropna()-df['sale_price'].where(mask,np.nan).dropna())*100)/df['market_price'].where(mask,np.nan).dropna(),nbins=20,color_discrete_sequence=['#FFA15A'])
pig.update_layout(xaxis_title='Discount(%)',yaxis_title='No. of Products',showlegend=False,title="Discount (%) Histogram")
pig.update_xaxes(dtick=5)
pig.update_layout(bargap=0.2)
st.write(pig)






