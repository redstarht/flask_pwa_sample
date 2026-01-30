from flask import request,Blueprint,render_template, request, redirect, url_for
from .models import EntryExit

from .db import SessionLocal

main = Blueprint('main', __name__)



@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        action = request.form.get('action')
        if name and action in ['入室', '退室']:
            session = SessionLocal()
            
            try:
                log = EntryExit(name=name, action=action)
                
                session.add(log)
                session.commit()
            except Exception as e:
                session.rollback()
                print("Error",e)
                
            finally:                    
                return redirect(url_for('main.index'))
    
    session = SessionLocal()
    try:
        logs = session.query(EntryExit).order_by(EntryExit.timestamp.desc()).all()
    finally:
        session.close()
    return render_template('index.html', logs=logs)
