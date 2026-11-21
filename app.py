from cs50 import SQL
from flask import Flask, redirect, render_template, request
from helpers import apology

# Configure application
app = Flask(__name__)

# Reference the global COVID db
db = SQL("sqlite:///covid_global.db")

@app.route("/")
def index():
    """Show Countries that we have Covid-19 data for"""
    try:
        countries = db.execute("""
            SELECT DISTINCT country, country_code
            FROM covid_global
            WHERE country_code IS NOT NULL
            ORDER BY UPPER(country)
        """)
    except ValueError:
        return apology("Something went wrong", 403)

    return render_template("index.html", countries=countries)

@app.route("/country")
def country():
    """ Return the data for the specified country code """
    code = request.args.get("code")

    if not code:
        return redirect("/")

        # Convert country code to uppercase to allow selection directly from the url
    code = code.upper()
    stats = db.execute("""
        SELECT
            country,
            SUM(new_cases) AS total_cases,
            SUM(new_deaths) AS total_deaths
        FROM covid_global
        WHERE country_code = ?
    """, code)

    # get daily new cases for chart plotting
    daily_cases = db.execute("""
        SELECT
            date,
            new_cases
        FROM covid_global
        WHERE country_code = ?
        ORDER BY date
    """, code)

    # get daily deaths for chart plotting
    daily_deaths = db.execute("""
        SELECT
            date,
            new_deaths
        FROM covid_global
        WHERE country_code = ?
        ORDER BY date
    """, code)

    # get cumulative deaths for chart plotting
    cum_deaths = db.execute("""
        SELECT
            date,
            cum_deaths
        FROM covid_global
        WHERE country_code = ?
        ORDER BY date
    """, code)

    # get cumulative cases for chart plotting
    cum_cases = db.execute("""
        SELECT
            date,
            cum_cases
        FROM covid_global
        WHERE country_code = ?
        ORDER BY date
    """, code)

    if not stats or stats[0]["total_cases"] is None:
        # no data available for this country, show apology page
        return apology("No COVID data available for this country code", 400)

    return render_template(
        "country.html",
        stats=stats[0],             # aggregated totals
        daily_cases=daily_cases,    # daily cases
        daily_deaths=daily_deaths,  # daily deaths
        cum_cases=cum_cases,        # cumulative cases
        cum_deaths=cum_deaths       # cumulative deaths
    )

@app.route("/about")
def about():
    """ Background information on the project """
    return render_template("about.html")

@app.route("/future")
def future():
    """ Future extension plans """
    return render_template("future.html")
