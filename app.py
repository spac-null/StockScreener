from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json as json_lib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockscreener.db'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

with open('etoro_stocks_filtered.json', 'r') as f:
    data = json.load(f)
stocks = data['stocks']

# Train ML model
df = pd.DataFrame(stocks)
df = df.dropna(subset=['peRatio-TTM', 'beta', 'dividendYield', 'marketCapitalization', 'returnYearToDate'])
X = df[['peRatio-TTM', 'beta', 'dividendYield', 'marketCapitalization']]
y = df['returnYearToDate']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Model MSE: {mean_squared_error(y_test, model.predict(X_test))}")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', stocks=stocks[:50])

  # Show first 50

@app.route('/screen', methods=['POST'])
def screen():
    criteria = request.json
    filtered = stocks
    if 'peRatio_max' in criteria and criteria['peRatio_max']:
        filtered = [s for s in filtered if s.get('peRatio-TTM') and s['peRatio-TTM'] < float(criteria['peRatio_max'])]
    if 'dividendYield_min' in criteria and criteria['dividendYield_min']:
        filtered = [s for s in filtered if s.get('dividendYield') and s['dividendYield'] > float(criteria['dividendYield_min'])]
    if 'marketCap_min' in criteria and criteria['marketCap_min']:
        min_mc = float(criteria['marketCap_min']) * 1e9
        filtered = [s for s in filtered if s.get('marketCapitalization') and s['marketCapitalization'] > min_mc]
    if 'ytd_min' in criteria and criteria['ytd_min']:
        filtered = [s for s in filtered if s.get('returnYearToDate') and s['returnYearToDate'] > float(criteria['ytd_min'])]
    if 'sector' in criteria and criteria['sector']:
        filtered = [s for s in filtered if s.get('internalIndustryId') and criteria['sector'] in s.get('internalIndustryId', '')]  # Approximate
    return jsonify(filtered[:100])

@app.route('/export', methods=['POST'])
def export():
    criteria = request.json
    filtered = stocks
    # Same filters as above
    if 'peRatio_max' in criteria and criteria['peRatio_max']:
        filtered = [s for s in filtered if s.get('peRatio-TTM') and s['peRatio-TTM'] < float(criteria['peRatio_max'])]
    if 'dividendYield_min' in criteria and criteria['dividendYield_min']:
        filtered = [s for s in filtered if s.get('dividendYield') and s['dividendYield'] > float(criteria['dividendYield_min'])]
    if 'marketCap_min' in criteria and criteria['marketCap_min']:
        min_mc = float(criteria['marketCap_min']) * 1e9
        filtered = [s for s in filtered if s.get('marketCapitalization') and s['marketCapitalization'] > min_mc]
    if 'ytd_min' in criteria and criteria['ytd_min']:
        filtered = [s for s in filtered if s.get('returnYearToDate') and s['returnYearToDate'] > float(criteria['ytd_min'])]
    if 'sector' in criteria and criteria['sector']:
        filtered = [s for s in filtered if s.get('internalIndustryId') and criteria['sector'] in s.get('internalIndustryId', '')]
    # Create CSV
    import csv
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Symbol', 'PE', 'Yield', 'YTD', 'Market Cap'])
    for s in filtered[:100]:
        writer.writerow([s.get('internalInstrumentDisplayName'), s.get('internalSymbolFull'), s.get('peRatio-TTM'), s.get('dividendYield'), s.get('returnYearToDate'), s.get('marketCapitalization')])
    return output.getvalue(), 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=screened_stocks.csv'}

@app.route('/backtest', methods=['POST'])
def backtest():
    data = request.json
    symbol = data.get('symbol')
    stock = next((s for s in stocks if s.get('internalSymbolFull') == symbol), None)
    if not stock:
        return jsonify({'error': 'Stock not found'})
    # Simple backtest: assume buy now, simulate based on returnYearToDate
    ytd_return = stock.get('returnYearToDate', 0)
    simulated_return = ytd_return / 100  # As decimal
    initial_investment = 10000
    final_value = initial_investment * (1 + simulated_return)
    return jsonify({'symbol': symbol, 'initial': initial_investment, 'final': final_value, 'return': simulated_return * 100})

@app.route('/optimize', methods=['POST'])
def optimize():
    criteria = request.json
    filtered = stocks
    # Apply filters
    if 'peRatio_max' in criteria and criteria['peRatio_max']:
        filtered = [s for s in filtered if s.get('peRatio-TTM') and s['peRatio-TTM'] < float(criteria['peRatio_max'])]
    if 'dividendYield_min' in criteria and criteria['dividendYield_min']:
        filtered = [s for s in filtered if s.get('dividendYield') and s['dividendYield'] > float(criteria['dividendYield_min'])]
    if 'marketCap_min' in criteria and criteria['marketCap_min']:
        min_mc = float(criteria['marketCap_min']) * 1e9
        filtered = [s for s in filtered if s.get('marketCapitalization') and s['marketCapitalization'] > min_mc]
    if 'ytd_min' in criteria and criteria['ytd_min']:
        filtered = [s for s in filtered if s.get('returnYearToDate') and s['returnYearToDate'] > float(criteria['ytd_min'])]
    # Select top 5 by YTD return
    top5 = sorted(filtered, key=lambda s: s.get('returnYearToDate', 0), reverse=True)[:5]
    # Equal weight portfolio
    weights = [0.2] * 5
    expected_return = sum(w * s.get('returnYearToDate', 0) for w, s in zip(weights, top5))
    avg_beta = sum(s.get('beta', 1) for s in top5) / 5
    risk_score = avg_beta * 100  # Simple risk
    return jsonify({'portfolio': [{'symbol': s['internalSymbolFull'], 'weight': w, 'return': s.get('returnYearToDate')} for w, s in zip(weights, top5)], 'expected_return': expected_return, 'risk_score': risk_score})

@app.route('/premium')
def premium():
    # Placeholder for Stripe checkout
    return "Premium feature: Unlimited screens for $9.99/month. Integrate Stripe here."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symbol = data.get('symbol')
    stock = next((s for s in stocks if s.get('internalSymbolFull') == symbol), None)
    if not stock or not all(k in stock for k in ['peRatio-TTM', 'beta', 'dividendYield', 'marketCapitalization']):
        return jsonify({'error': 'Insufficient data'})
    features = [[stock['peRatio-TTM'], stock['beta'], stock['dividendYield'], stock['marketCapitalization']]]
    predicted = model.predict(features)[0]
    return jsonify({'symbol': symbol, 'predicted_ytd_return': predicted})

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    email = data.get('email')
    symbol = data.get('symbol')
    # Placeholder: send email
    print(f"Alert set for {email}: {symbol} price changes")
    return jsonify({'message': 'Alert set (demo)'})

@app.route('/realtime', methods=['POST'])
def realtime():
    data = request.json
    symbol = data.get('symbol')
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get('currentPrice', 'N/A')
        return jsonify({'symbol': symbol, 'price': price})
    except:
        return jsonify({'error': 'Failed to fetch'})

@app.route('/chart', methods=['POST'])
def chart():
    data = request.json
    symbol = data.get('symbol')
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='1y')
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(title=f'{symbol} 1Y Chart')
        return json_lib.dumps(fig, cls=PlotlyJSONEncoder)
    except:
        return jsonify({'error': 'Failed to fetch'})

if __name__ == '__main__':
    app.run(debug=True)