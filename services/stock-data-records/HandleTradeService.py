import sqlite3

class TradeService:
    def __init__(self, db_path="records/demo.db"):
        self.db_path = db_path

    # -----------------------------
    # Internal DB helper
    # -----------------------------
    def _get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # -----------------------------
    # User helpers
    # -----------------------------
    def get_user_id(self, username):
        conn = self._get_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        return row["user_id"] if row else None

    # -----------------------------
    # Position helpers
    # -----------------------------
    def get_positions(self, user_id):
        """
        Returns a list of:
        {
            ticker: "CRM",
            total_shares: 100,
            avg_cost: 190.0
        }
        """
        conn = self._get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                ticker,
                SUM(quantity) AS total_shares,
                SUM(quantity * price) AS total_cost
            FROM trade_legs
            JOIN trades ON trades.trade_id = trade_legs.trade_id
            WHERE trades.user_id = ?
              AND asset_type = 'stock'
            GROUP BY ticker;
        """, (user_id,))

        rows = cur.fetchall()
        conn.close()

        positions = []
        for r in rows:
            if r["total_shares"] != 0:
                avg_cost = r["total_cost"] / r["total_shares"]
            else:
                avg_cost = 0

            positions.append({
                "ticker": r["ticker"],
                "total_shares": r["total_shares"],
                "avg_cost": round(avg_cost, 2)
            })

        return positions

    # -----------------------------
    # Buy helpers
    # -----------------------------
    def buy_stock(self, user_id, ticker, qty, price):
        conn = self._get_db()
        cur = conn.cursor()

        # Insert into trades
        cur.execute("""
            INSERT INTO trades (user_id, trade_type, action, date, ticker_symbol)
            VALUES (?, 'stock', 'buy', DATE('now'), ?)
        """, (user_id, ticker))

        trade_id = cur.lastrowid

        # Insert into trade_legs
        cur.execute("""
            INSERT INTO trade_legs (
                trade_id, asset_type, ticker, quantity, price, strike, expiration, option_type, side
            )
            VALUES (?, 'stock', ?, ?, ?, NULL, NULL, NULL, 'long')
        """, (trade_id, ticker, qty, price))

        conn.commit()
        conn.close()

    # -----------------------------
    # Sell helpers
    # -----------------------------
    def get_total_shares(self, user_id, ticker):
        conn = self._get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(quantity) FROM trade_legs
            JOIN trades ON trades.trade_id = trade_legs.trade_id
            WHERE trades.user_id = ?
              AND trade_legs.ticker = ?
              AND trade_legs.asset_type = 'stock';
        """, (user_id, ticker))

        result = cur.fetchone()[0]
        conn.close()
        return result if result else 0

    def get_buy_lots(self, user_id, ticker):
        conn = self._get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT trade_legs.leg_id, trade_legs.quantity, trade_legs.price, trades.date
            FROM trade_legs
            JOIN trades ON trades.trade_id = trade_legs.trade_id
            WHERE trades.user_id = ?
              AND trade_legs.ticker = ?
              AND trade_legs.asset_type = 'stock'
              AND trade_legs.quantity > 0
            ORDER BY trades.date ASC;
        """, (user_id, ticker))

        rows = cur.fetchall()
        conn.close()
        return rows

    def sell_stock_fifo(self, user_id, ticker, qty, price):
        total_shares = self.get_total_shares(user_id, ticker)

        if qty > total_shares:
            return f"Error: You are trying to sell {qty} shares but only hold {total_shares}."

        remaining = qty
        buy_lots = self.get_buy_lots(user_id, ticker)

        conn = self._get_db()
        cur = conn.cursor()

        # Create parent trade
        cur.execute("""
            INSERT INTO trades (user_id, trade_type, action, date, ticker_symbol)
            VALUES (?, 'stock', 'sell', DATE('now'), ?)
        """, (user_id, ticker))
        trade_id = cur.lastrowid

        for lot in buy_lots:
            if remaining <= 0:
                break

            lot_qty = lot["quantity"]
            qty_to_sell = min(lot_qty, remaining)

            # Insert SELL leg
            cur.execute("""
                INSERT INTO trade_legs (
                    trade_id, asset_type, ticker, quantity, price, strike, expiration, option_type, side
                )
                VALUES (?, 'stock', ?, ?, ?, NULL, NULL, NULL, 'long')
            """, (trade_id, ticker, -qty_to_sell, price))

            remaining -= qty_to_sell

        conn.commit()
        conn.close()
        return None
