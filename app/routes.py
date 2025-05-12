import sqlalchemy as sa
from sqlalchemy import func
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app, url_for, redirect, flash, render_template
from flask_login import current_user, login_user, login_required, logout_user

from app.db_models import db, User, Planet, HostStar
from app.utils import allowed_file
import csv, os

api_bp = Blueprint('api', __name__)


@api_bp.route('/', methods=['GET', 'POST'])
def index():
    # 分页参数
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except Exception:
        page = 1
    per_page = 20
    # 查询带分页的行星及主星信息
    query = db.session.query(Planet, HostStar).join(HostStar, Planet.host_star_id == HostStar.id)
    total = query.count()
    planets = query.offset((page - 1) * per_page).limit(per_page).all()
    planet_data = [
        {
            'pl_name': p.pl_name,
            'discoverymethod': p.discoverymethod,
            'disc_year': p.disc_year,
            'disc_facility': p.disc_facility,
            'host_star': h.hostname,
            'sy_dist': h.sy_dist
        }
        for p, h in planets
    ]
    # 分页信息
    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page
    }
    return render_template('index.html', planet_data=planet_data, pagination=pagination)


@api_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Success registration
        login_user(user)        # Auto login
        flash(f'Hi {form.username.data}, welcome to Price Trend !', 'success')
        return redirect(request.referrer)
    else:
        errors = []
        for field in form:
            for err in field.errors:
                errors.append(err)
        if errors:
            if len(errors) == 1:
                msg = f"{errors[0]} is required."
            else:
                msg = f"{', '.join(errors[:-1])} and {errors[-1]} are required."
            flash(f"Registration failed: {msg.capitalize()}", 'danger')
    return redirect(request.referrer)


@api_bp.route('/login', methods=['GET', 'POST'])            # Updated in routes.handle_login_post()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        # failed login
        if user is None or not user.check_password(form.password.data):
            flash('Login failed: Invalid username or password', 'danger')
            return redirect(request.referrer)
        # successful login
        login_user(user)
        flash(f'Welcome back, {form.username.data} !', 'success')
        return redirect(request.referrer)
    else:
        errors = []
        for field in form:
            for err in field.errors:
                errors.append(field.label.text)
        if errors:
            if len(errors) == 1:
                msg = f"{errors[0]} is required."
            else:
                msg = f"{', '.join(errors[:-1])} and {errors[-1]} are required."
            flash(f"Login failed: {msg.capitalize()}", 'danger')
    return redirect(request.referrer)


@login_required
@api_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'warning')
    return redirect(request.referrer)


@api_bp.route('/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in merchants])

@api_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # parse the CSV file and insert data into the database 
        try:
            with open(file_path, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile) 
                for row in csvreader:
                    product_id = row['product_id']
                    price = float(row['price'])
                    date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    new_price = PriceData(product_id=product_id, price=price, date=date)
                    db.session.add(new_price)
                
                db.session.commit()  

            return jsonify({"message": "File uploaded and data inserted successfully."}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type, only CSV files are allowed."}), 400

@api_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
