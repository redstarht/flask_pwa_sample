from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, EntryExit # EntryExit をインポート
import datetime # datetime をインポート

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    # ログデータを取得してテンプレートに渡す
    logs = g.db.query(EntryExit).order_by(EntryExit.timestamp.desc()).all()
    return render_template('index.html',logs=logs)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = g.db.query(User).filter_by(username=username).first()

        if user:
            flash('ユーザー名が既に存在します。別のユーザー名をお試しください。', 'danger')
            return redirect(url_for('main.register'))

        # パスワードをハッシュ化
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        
        g.db.add(new_user)
        g.db.commit()
        flash('ユーザー登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False # ログイン状態を保持するかどうか

        user = g.db.query(User).filter_by(username=username).first()

        # ユーザーが存在しない、またはパスワードが一致しない場合
        if not user or not check_password_hash(user.password, password):
            flash('ユーザー名またはパスワードが間違っています。', 'danger')
            return redirect(url_for('main.login'))

        # ログイン成功
        login_user(user, remember=remember)
        flash('ログインしました。', 'success')
        
        # ログイン前にアクセスしようとしたページがあればそこへリダイレクト
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))

    return render_template('login.html')

@main.route('/logout')
@login_required # ログインしているユーザーのみアクセス可能
def logout():
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('main.index'))

# ログインユーザーのみがアクセスできる保護されたルートの例
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# app.js からデータを受け取る API エンドポイント
@main.route('/api/input', methods=['POST'])
def api_input():
    data = request.get_json()
    name = data.get('name')
    action = data.get('action')

    if not name or not action:
        return jsonify({'status': 'error', 'message': 'Name and action are required'}), 400

    try:
        new_entry = EntryExit(name=name, action=action, timestamp=datetime.datetime.now())
        g.db.add(new_entry)
        g.db.commit()
        logs = g.db.query(EntryExit).order_by(EntryExit.timestamp.desc()).all()
        
    except Exception as e:
        g.db.rollback()
        print("Error",e)
        return jsonify({'status': 'error', 'message': 'Failed to save data'}), 500
    finally:
        return render_template('index.html', logs=logs)


    # return jsonify({'status': 'success', 'message': 'Data saved successfully'}), 200
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     action = request.form.get('action')
    #     if name and action in ['入室', '退室']:
    #         session = SessionLocal()
            
    #         try:
    #             log = EntryExit(name=name, action=action)
                
    #             session.add(log)
    #             session.commit()
    #         except Exception as e:
    #             session.rollback()
    #             print("Error",e)
                
    #         finally:                    
    #             return redirect(url_for('main.index'))
    
    # session = SessionLocal()
    # try:
    #     logs = session.query(EntryExit).order_by(EntryExit.timestamp.desc()).all()
    # finally:
    #     session.close()
    # return render_template('index.html', logs=logs)
