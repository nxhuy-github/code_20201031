import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('My first app')
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first_column': [1,2,3,4],
    'second_column': [10,20,30,40]
}))

df = pd.DataFrame({
    'first_column': [1,2,3,4],
    'second_column': [10,20,30,40]
})

df

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a','b','c'])
st.line_chart(chart_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns=['a','b','c'])
    st.line_chart(chart_data)

"""
option = st.selectbox(
    'Which number do you like best?',
    df['first_column'])

'You selected: ', option
"""
option = st.sidebar.selectbox(
    'Which number do you like best?',
    df['first_column'])
'You selected: ', option

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration{i+1}')
    bar.progress(i+1)
    time.sleep(0.1)
"...and now we'are done!"































