import streamlit as st
import pandas as pd
import plost
import requests

API_KEY = 'pwQi epcp p6Gs nTxg zbN7 Znjt' # Set your API key here

#st.set_page_config(layout="wide")
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
def get_token(username, password):
    response = requests.post( 'http://project2dashboard.local/wp-json/jwt-auth/v1/token', data={'username': username, 'password': password}, headers={'X-API-KEY': API_KEY}
)
    if response.status_code == 200:
        return response.json()['token']
    else:
        return None

def verify_token(token):
    response = requests.post(
    'http://project2dashboard.local/wp-json/jwt-auth/v1/token/validate',
    headers={'Authorization': f'Bearer {token}', 'X-API-KEY': API_KEY}
    )
    return response.status_code == 200

def main():
    st.write("This is the main page of the application.") # Your main code goes here

    


    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    st.sidebar.header('Dashboard `version 2`')
    
    st.sidebar.subheader('Heat map parameter')
    time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 
    
    st.sidebar.subheader('Donut chart parameter')
    donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))
    
    st.sidebar.subheader('Line chart parameters')
    plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
    plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
    
    st.sidebar.markdown('''
    ---
    Created with ❤️ by [Data Professor](https://youtube.com/dataprofessor/).
    ''')
    
    
    # Row A
    st.markdown('### Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
    
    # Row B
    seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
    stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')
    
    c1, c2 = st.columns((7,3))
    with c1:
        st.markdown('### Heatmap')
        plost.time_hist(
        data=seattle_weather,
        date='date',
        x_unit='week',
        y_unit='day',
        color=time_hist_color,
        aggregate='median',
        legend=None,
        height=345,
        use_container_width=True)
    with c2:
        st.markdown('### Donut chart')
        plost.donut_chart(
            data=stocks,
            theta=donut_theta,
            color='company',
            legend='bottom', 
            use_container_width=True)

# Row C
st.markdown('### Line chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)


    #Check if the user is already logged in
    if 'token' in st.session_state and verify_token(st.session_state['token']):
        main() # Call the main function
    else:
# Show the login form
        col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.write("")

    with col2:
        with st.form(key='login_form'):
            st.title("Please log in")
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submit_button = st.form_submit_button(label='Log in')
    
            if submit_button:
                token = get_token(username, password)
                if token and verify_token(token):
                    st.session_state['token'] = token  # We store the token in the session state
                    st.experimental_rerun()  # Reload the page so that the login form disappears
                else:
                    st.error('Access denied')

    with col3:
        st.write("")

