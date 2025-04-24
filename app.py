from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('pollution_by_country_2012_2025.csv')

@app.route('/')
def index():
    country1 = request.args.get('country1', '').strip()
    country2 = request.args.get('country2', '').strip()

    # Average pollution per year for bar chart
    year_avg = df.groupby('Year')['Pollution Index'].mean().reset_index()
    year_avg = year_avg.sort_values('Year')  # Ensure it's sorted by year

    # Trend line for first country
    country1_data = []
    if country1:
        country1_data = df[df['Country'].str.lower() == country1.lower()] \
                        .sort_values('Year')[['Year', 'Pollution Index']].to_dict(orient='records')

    # Trend line for second country
    country2_data = []
    if country2:
        country2_data = df[df['Country'].str.lower() == country2.lower()] \
                        .sort_values('Year')[['Year', 'Pollution Index']].to_dict(orient='records')

    return render_template('index.html',
                           year_data=year_avg.to_dict(orient='records'),
                           country1=country1,
                           country2=country2,
                           country1_data=country1_data,
                           country2_data=country2_data)

if __name__ == '__main__':
    app.run(debug=True)