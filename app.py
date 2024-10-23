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
        return f"<Person {self.name} (Team: {self.team.name})>"


def create_team(team_name, people_names):
    t = Team(name=team_name)
    db.session.add(t)
    db.session.commit()
    persons = [Person(name=p, team_id=t.id) for p in people_names]
    db.session.add_all(persons)
    db.session.commit()


@app.route("/people", methods=["GET"])
def people():
    team_id = request.args.get('select-team')
    people = Person.query.filter(Team.id == team_id)
    return render_template('fragments/list.html', people=people)


def get_names(team_id):
    return Person.query.filter(Team.id == team_id)


def get_teams():
    return Team.query.all()


@app.route("/partecipants", methods=["GET", "POST"])
def partecipants():
    if request.method == "POST":
        create_team("myteam", ["p1", "p2", "p3"])
        print(get_names("myteam"))
    elif request.method == "GET":
        print(request.json())
        return render_template("fragments/list.html", people=[Person(name="name")])


@app.route("/")
def index():
    return render_template("index.html", teams=get_teams())
