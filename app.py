import random

from flask import Flask, render_template, request
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
htmx = HTMX(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return f"<Team {self.name}>"


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)

    __table_args__ = (UniqueConstraint("name", "team_id", name="unique_name"),)

    def __repr__(self):
        return f"<Person {self.name} (Team: {self.team_id})>"


def create_team(team_name, partecipants_names):
    t = Team(name=team_name)
    db.session.add(t)
    db.session.commit()
    persons = [Person(name=p, team_id=t.id) for p in partecipants_names]
    db.session.add_all(persons)
    db.session.commit()


def get_by_team(team_id):
    return Person.query.filter(Person.team_id == team_id)


def get_teams():
    return Team.query.all()


def secret_santa(members):
    """Given a list of partecipants, return a random permutation for secret sant"""
    random.shuffle(members)
    return list(zip(members, members[1:] + [members[0]]))


@app.route("/partecipants", methods=["GET", "POST"])
def partecipants():
    if request.method == 'GET':
        team_id = request.args.get('select-team')
        partecipants = get_by_team(team_id)
        names = [p.name for p in partecipants]
        return render_template('fragments/list.html',
                               partecipants=partecipants,
                               draw=secret_santa(names))

    elif request.method == 'POST':
        team_name = request.form['team-name']
        members = request.form['team-members'].split(",")
        create_team(team_name, members)
        return render_template('fragments/created_team.html')


@app.route("/")
def index():
    return render_template("index.html", teams=get_teams())
