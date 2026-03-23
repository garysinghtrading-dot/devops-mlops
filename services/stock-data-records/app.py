from flask import Flask, render_template, request, redirect
from HandleTradeService import TradeService

app = Flask(__name__)
trade_service = TradeService()

@app.route("/")
def landing():
    user = "demo_user"
    user_id = trade_service.get_user_id(user)
    positions = trade_service.get_positions(user_id)
    return render_template("landing.html", user=user, positions=positions)

@app.route("/update", methods=["POST"])
def update():
    user_id = trade_service.get_user_id("demo_user")

    ticker = request.form["ticker"]
    action = request.form["action"]
    qty = int(request.form["quantity"])
    price = float(request.form["price"])

    if action == "sell":
        error = trade_service.sell_stock_fifo(user_id, ticker, qty, price)
        if error:
            return error
    else:
        trade_service.buy_stock(user_id, ticker, qty, price)

    return redirect("/")
