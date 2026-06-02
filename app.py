from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import subprocess
from pathlib import Path

app = Flask(__name__)

DATA_FILE = "data.csv"

if not Path(DATA_FILE).exists():
    pd.DataFrame(columns=["name","age"]).to_csv(DATA_FILE, index=False)

@app.route('/')
def home():
    df = pd.read_csv(DATA_FILE)
    people = df.to_dict(orient='records')
    edit_id = request.args.get('edit')
    person_to_edit = None

    if edit_id is not None:
        edit_id = int(edit_id)
        if 0 <= edit_id < len(people):
            person_to_edit = people[edit_id]

    return render_template('index.html', people=people,
                           person_to_edit=person_to_edit,
                           edit_id=edit_id)

@app.route('/save', methods=['POST'])
def save():
    df = pd.read_csv(DATA_FILE)

    name = request.form['name']
    age = int(request.form['age'])
    edit_id = request.form.get('edit_id')

    if edit_id:
        df.loc[int(edit_id)] = [name, age]
    else:
        df.loc[len(df)] = [name, age]

    df.to_csv(DATA_FILE, index=False)

    subprocess.run(["python", "train.py"])

    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    df = pd.read_csv(DATA_FILE)

    if 0 <= id < len(df):
        df = df.drop(id).reset_index(drop=True)

    df.to_csv(DATA_FILE, index=False)

    subprocess.run(["python", "train.py"])

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
