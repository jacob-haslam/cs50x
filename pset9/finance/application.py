import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # check how much cash user has
    userid = session["user_id"]
    usercash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

    transactions = db.execute("SELECT symbol, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY symbol", userid)

    total = 0.00

    for transaction in transactions:

        transaction["name"] = lookup(transaction["symbol"])["name"]
        transaction["price"] = float(lookup(transaction["symbol"])["price"])
        transaction["shares"] = int(transaction['SUM(amount)'])
        transaction["total"] = transaction["shares"] * transaction["price"]
        total += transaction["total"]
        transaction["total"] = usd(transaction["total"])
        transaction["price"] = usd(lookup(transaction["symbol"])["price"])

    grandtotal = total + usercash
    grandtotal = usd(grandtotal)
    usercash = usd(usercash)

    return render_template("index.html", **locals())


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # query share
        symbol = request.form.get("symbol")
        reqshares = request.form.get("shares")

        if not symbol or not reqshares:
            return apology("Please complete all fields", 400)

        shareinfo = lookup(symbol)

        if not shareinfo:
            return apology("Please choose correct symbol", 400)

        if not reqshares.isdigit() or int(reqshares) < 1:
            return apology("Amount must be whole number")

        # check how much cash user has
        userid = session["user_id"]
        usercash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

        # lookup share
        price = shareinfo["price"]
        totalprice = price * int(reqshares)

        if usercash < totalprice:
            return apology("not enough money in account")

        db.execute("INSERT INTO transactions (user_id, symbol, price, amount) VALUES(?, ?, ?, ?)", userid, symbol, price, reqshares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", usercash - totalprice, userid)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # check how much cash user has
    userid = session["user_id"]
    usercash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", userid)

    return render_template("history.html", **locals())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        shareinfo = lookup(request.form.get("symbol"))
        if not shareinfo:
            return apology("Please complete all fields", 400)

        shareinfo["price"] = usd(shareinfo["price"])
        return render_template("quoted.html", **locals())

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # get details
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("You must type username", 400)
        if not password:
            return apology("You must type password", 400)

        if not any(char.isdigit() for char in password):
            return apology("Pass must contain numbers", 400)

        # check password
        if password == confirmation:
            hash = generate_password_hash(password)
        else:
            return apology("Passwords do not match")

        idquery = db.execute("SELECT * FROM users WHERE username = ?", username)
        print(idquery)
        if len(idquery) > 0:
            return apology("User already exists", 400)

        # insert user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    userid = session["user_id"]

    if request.method == "POST":

        symbol = request.form.get("symbol")
        reqshares = int(request.form.get("shares"))

        if not symbol:
            return apology("Please complete all fields", 400)

        shareamount = db.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND symbol = ?",
                                 userid, symbol)[0]['SUM(amount)']

        if reqshares > shareamount:
            return apology("you do not have the required amount of shares.")

        usercash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]
        price = lookup(symbol)["price"]
        totalprice = price * int(reqshares)
        # make negative
        reqshares = reqshares - (reqshares*2)

        db.execute("INSERT INTO transactions (user_id, symbol, price, amount) VALUES(?, ?, ?, ?)", userid, symbol, price, reqshares)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", usercash + totalprice, userid)

        return redirect("/")

    else:

        # get transactions and shares
        transactions = db.execute("SELECT symbol, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY symbol", userid)
        reqshares = request.form.get("shares")

        for transaction in transactions:
            transaction["shares"] = transaction['SUM(amount)']

        return render_template("sell.html", **locals())


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
