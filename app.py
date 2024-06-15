import streamlit as st
import requests

# OpenWeatherMap API 키
API_KEY = '25db290fe10cde3402e11e8acb3d1827'

# 충남 아산시 탕정면의 위도와 경도
LAT = 36.7853
LON = 127.0089

# OpenWeatherMap API URL
url = f'http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'

def get_weather_data():
    response = requests.get(url)
    data = response.json()
    return data

def main():
    st.title("충남 아산시 탕정면 현재 온도")

    weather_data = get_weather_data()
    
    if weather_data and 'main' in weather_data:
        temp = weather_data['main']['temp']
        st.write(f"현재 온도: {temp}°C")
    else:
        st.write("날씨 데이터를 가져오는데 실패했습니다.")

if __name__ == "__main__":
    main()
