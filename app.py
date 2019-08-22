import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success", methods=('GET', 'POST'))
def success():
    results = []
 
    qry = db_session.query(Items)
    results = qry.all()
    total = len(results)
    return render_template('result.html', results=results, total=total)
  

@app.route("/remove/<int:id>", methods=['POST'])
def remove(id):
    items = db_session.query(Items).filter_by(id).first()
    db_session.delete(items)
    db_session.commit()
    return redirect(url_for('success'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
