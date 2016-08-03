"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db, get_user_by_email


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register or sign up user"""

# and if not, creating a new user in the database.
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        result = get_user_by_email(user_email) #querying DB for username

        if result:
            ##SHOW ALERT, "username exists"
            flash("That %s already exists. Please login or use a different email" % user_email)
            return redirect("/register")
        else:
            print "Ok to add new username"
            return redirect("/")
            # username doesn't exist, list will be empty.
    else:
        return render_template("register.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
