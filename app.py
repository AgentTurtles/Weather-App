from flask import Flask, render_template, request, redirect, url_for, session
from weather import main as get_weather
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Mock data for forecast and popular cities
MOCK_FORECAST = [
    {'date': 'Tomorrow', 'icon': '10d', 'temp': 23, 'desc': 'light rain'},
    {'date': 'Day After', 'icon': '01d', 'temp': 25, 'desc': 'clear sky'},
    {'date': 'In 3 Days', 'icon': '04d', 'temp': 21, 'desc': 'broken clouds'},
]
MOCK_POPULAR_CITIES = [
    {'city': 'Lahore', 'icon': '01d', 'temp': 28, 'desc': 'clear sky'},
    {'city': 'Karachi', 'icon': '02d', 'temp': 30, 'desc': 'few clouds'},
    {'city': 'Islamabad', 'icon': '10d', 'temp': 24, 'desc': 'rain'},
]

@app.route('/', methods=["GET", "POST"])
def index():
    data = None
    forecast = None
    popular_cities = None
    if request.method == "POST":
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data = get_weather(city, state, country)
        forecast = MOCK_FORECAST
        popular_cities = MOCK_POPULAR_CITIES
        # Store data and location in session and redirect
        session['weather_data'] = data
        session['forecast'] = forecast
        session['popular_cities'] = popular_cities
        session['city'] = city
        session['state'] = state
        session['country'] = country
        return redirect(url_for('index'))
    # On GET, check if data is in session
    if 'weather_data' in session:
        data = session.pop('weather_data')
        forecast = session.pop('forecast', None)
        popular_cities = session.pop('popular_cities', None)
        city = session.pop('city', None)
        state = session.pop('state', None)
        country = session.pop('country', None)
    else:
        city = state = country = None
    return render_template('index.html', data=data, forecast=forecast, popular_cities=popular_cities, city=city, state=state, country=country)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/location')
def location():
    # This endpoint can be used to receive geolocation data from the browser
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    # You can use lat/lon to fetch nearby cities' weather in the future
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)