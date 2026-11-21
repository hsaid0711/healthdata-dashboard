# COVID-19 Global Data Dashboard

**Author:** Hannah Said

**Date:** 15th February 2026


#### Video Demo: [https://youtu.be/re3HtYMnaMA](https://youtu.be/re3HtYMnaMA)

## Description:
A healthcare data project consisting of a web-based Flask application which enables users to view COVID-19 data by country using a publicly available [World Health Organisation (WHO)](https://data.who.int/dashboards/covid19/data) global dataset. Users can view a grid of four charts, displaying daily and cumulative cases and deaths for the selected country.

## Instructions:
From the homepage (or by selecting the 'Country Selection' link in the navigation bar) select the country of interest from the dropdown list.
On the resulting page, a grid of four charts specific to that country will be displayed:
- Daily new cases
- Cumulative cases
- Daily deaths
- Cumulative deaths

The daily charts are by default displayed as scatter graphs plotting the data points. Toggle the trend switch on and off to switch between data points and a trend line.
The total cases and total deaths displayed to the top right of the charts are accurate to January 2026, as highlighted by the tooltip.
Hover over the data points to display tool tips showing the exact data.
Explore the navigation bar links:
- About: More about the project.
- Extensions: Planned extensions for the future.
- Country Selection: to display data for another country. Alternatively, if the country code is known, the last two characters of the URL can be updated directly. If an incorrect country code is entered, an error message is displayed and the user is provided with a link to the home (country selection) page.

## Technology & Architecture

This project demonstrates several of the languages and frameworks introduced in CS50. I built on my knowledge of these technologies in order to deliver this project. I also learnt about Chart.js, exploring the various options and settings so that I could display the data as I wanted.

* **Backend:** Flask and Python query an SQLite database (`covid_global.db`) containing cleaned WHO COVID-19 data.

* **Frontend:** HTML, Bootstrap, CSS and JavaScript (including Chart.js) are used to deliver a responsive layout with four charts per country.

* **Data Processing:** I wrote a Python script (`healthcare.py`) to read the WHO csv, clean it, validate country codes (using `pycountry`), exclude problematic entries and create a table in the SQLite database `covid_global.db`.

* **Data Flow:**

    * Backend queries the database and returns:

        * `stats` — aggregated totals (`total_cases` and `total_deaths`)
        * `daily_cases` / `daily_deaths` — for daily charts
        * `cum_cases` / `cum_deaths` — for cumulative charts
    * Frontend uses Chart.js to render charts in a responsive Bootstrap grid.



## Design Decisions

* **X-axis limit:** I limited the x-axis to February 2023 to focus on the main pandemic period. The totals to the top right of the charts reflect data all the way through to January 2026, and I clarified this difference with a tooltip.

* **Refactoring to use macros:** Initially, I wrote all the chart code in `country.html`. It became repetitive and long, so I moved the chart logic into two macros for the two types of chart (`/templates/macros/charts.html`), allowing the daily and cumulative charts to use reusable macros.

* **Responsive layout:** Ensuring four charts fit neatly on desktop while remaining readable on mobile required careful use of Bootstrap classes and Chart.js sizing options. I used the 'hamburger' menu layout for mobile and stacked the 4 charts vertically on mobile (as opposed to the 2 by 2 grid on desktop).  I made adjustments to the CSS until I was happy with the formatting on both desktop and mobile.

* **Daily charts:** include a toggle to switch between scatter points and a trend line.

* **Cumulative charts:** display totals formatted for readability:

    `{{ "{:,}".format(value) }}`

## Challenges

#### 1. Understanding structures:

I wasn't sure the exact format of the structure that would be returned by my SQL query to gather the stats (total cases and total deaths) for a particular country.

    stats = db.execute("""
        SELECT
            country,
            SUM(new_cases) AS total_cases,
            SUM(new_deaths) AS total_deaths
        FROM covid_global
        WHERE country_code = ?
    """, code)

I added some debugging code to `app.py` to help me better understand the exact structure of the information.

    print(stats)
    print(stats[0])
    print(type(stats))
    print(type(stats[0]))


This returned the following:
```
[{'country': 'United Kingdom of Great Britain and Northern Ireland', 'total_cases': 25103762, 'total_deaths': 232112}]
{'country': 'United Kingdom of Great Britain and Northern Ireland', 'total_cases': 25103762, 'total_deaths': 232112}
<class 'list'>
<class 'dict'>
```
This confirmed that `stats` is a list of dictionaries, which should just have one entry as the country codes are unique. `stats[0]` therefore is a dictionary of format `{'country': value, 'total_cases': value, 'total_deaths': value}`


#### 2. Encoding issues

Some country names (Réunion and Curaçao) had special characters that despite trying many different encodings continued to give me display issues.  As this is a demo project, I took the decision to filter these two countries out.   This would not be a valid approach if delivering a full solution.

## Use of AI

Once I had functionally correct code, I used AI (Chat GPT) to suggest how I could incorporate Bootstrap to improve the style and formatting.  I have noted in my code comments where I used AI to assist me, retaining my original code for reference.  I have mixed thoughts regarding the use of AI - whilst powerful and in some instances helpful, AI can enable coders to implement functionality without fully understanding it and it also reduces the satisfaction of developing the end-to-end code from scratch.

## Future Improvements

I broke my project down into achievable objectives to allow phased delivery, with a functioning solution at each stage.
Future plans include:

* Interactive map for country selection.
* Rolling 7 day averages to account for weekend reporting differences.
* Customisable date ranges
* Country comparisons - display countries side by side.
* Vaccination uptake data - overlay option to assess impact.
* Normalisation based on country populations - cases per 100,000 people.

## Files included

healthcare.py - a Python script for populating the database table
app.py - defines the flask web application
helpers.py - provides error handling, apology format
requirements.txt - lists the prereqs
covid_global.db - COVID-19 global dataset, generated by healthcare.py
testing folder - can be ignored
/templates/macros/charts.html - macros for producing the two chart formats (daily and cumulative)
/templates/about.html - the about page
/tempates/apology.html - error handling if the country code is invalid
/templates/country.html - uses Charts.js to display charts displaying the data
/templates/future.html - details future extensions
/templates/index.html - country selection page (homepage)
/templates/layout.html - provides a common layout and structure across the pages, including the nav bar
/static/style.css - provides styling and mobile responsive layout
/data/WHO-COVID-19-global-daily-data.csv - publically available COVID-19 global data set
