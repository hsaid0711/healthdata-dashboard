from flask import render_template

# Based on the apology function from Week 9, finance

def apology(message, code=400):
    return render_template(
        "apology.html",
        top=code,
        bottom=message
    ), code
