from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlalchemy as sa
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
# "mysql://sql12625244:w3lsiUP7lU@sql12.freesqldatabase.com/sql12625244"

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))


class Reward(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    reward_name = sa.Column(sa.String(250))
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("rewards", lazy="dynamic"))


class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward
        load_instance = True
        include_fk = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    rewards = ma.Nested(RewardSchema, many=True)


@app.route("/")
def index():
    return "<h1> Hello from flask </h1>"


@app.route("/rewards")
def rewards():
    rewards = Reward.query.all()
    reward_schema = RewardSchema(many=True)
    output = reward_schema.dump(rewards)
    return jsonify({"data": output})


@app.route("/users")
def users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    return jsonify({"data": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
