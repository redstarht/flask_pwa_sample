from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entry_exit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# モデル定義
class EntryExit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return f'<EntryExit {self.name} {self.action} {self.timestamp}>'
# DB初期化
with app.app_context():
    db.create_all()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        action = request.form.get('action')
        if name and action in ['入室', '退室']:
            log = EntryExit(name=name, action=action)
            db.session.add(log)
            db.session.commit()
        return redirect(url_for('index'))
    logs = EntryExit.query.order_by(EntryExit.timestamp.desc()).all()
    return render_template('index.html', logs=logs)
if __name__ == '__main__':
    app.run(debug=True)