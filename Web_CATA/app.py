from flask import Flask, render_template, request
# from flask import current_app as app
import datetime
from plotlydash.Dash_RSI import create_dashboard_rsi
from plotlydash.Dash_SMA import create_dashboard_sma
from plotlydash.Dash_VWAP import create_dashboard_vwap

app = Flask(__name__, instance_relative_config=False)

with app.app_context():
    app = create_dashboard_rsi(app)
    app = create_dashboard_sma(app)
    app = create_dashboard_vwap(app)



@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/stocks", methods = ["GET", "POST"])
def page_stocks():

    entry_content = "AAPL"

    if request.method == "POST":
        entry_content = request.form.get("ticker")
        print(entry_content)

    return render_template("stocks.html", ticker = entry_content)


# @app.route("/backtest", methods = ["GET", "POST"])
# def page_backtest():
#     return render_template("backtest.html")



if __name__ == "__main__":
    app.run(debug=True)