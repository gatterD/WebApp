import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ships.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Модель для базы данных
class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    year_built = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    wikipedia_link = db.Column(db.String(200), nullable=False)
    country_of_origin = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Ship {self.name}>'


@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    query = request.form.get('query')
    category = request.form.get('category')
    per_page = 3

    if query and category:
        ships = Ship.query.filter(Ship.name.like(f'%{query}%'), Ship.type.like(f'%{category}%')).paginate(page=page,
                                                                                                          per_page=per_page,
                                                                                                          error_out=False)
    elif query:
        ships = Ship.query.filter(Ship.name.like(f'%{query}%')).paginate(page=page, per_page=per_page, error_out=False)
    elif category:
        ships = Ship.query.filter(Ship.type.like(f'%{category}%')).paginate(page=page, per_page=per_page,
                                                                            error_out=False)
    else:
        ships = Ship.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html', ships=ships)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        year_built = request.form['year_built']
        description = request.form['description']
        image_url = request.form['image_url']
        short_description = request.form['short_description']
        is_active = request.form.get('is_active') == 'on'
        wikipedia_link = request.form['wikipedia_link']
        country_of_origin = request.form['country_of_origin']

        # Проверка на существование корабля
        existing_ship = Ship.query.filter_by(name=name).first()
        if existing_ship:
            flash('A ship with this name already exists in the database.', 'error')
            return redirect(url_for('upload'))

        new_ship = Ship(
            name=name,
            type=type_,
            year_built=year_built,
            description=description,
            image_url=image_url,
            short_description=short_description,
            is_active=is_active,
            wikipedia_link=wikipedia_link,
            country_of_origin=country_of_origin
        )
        db.session.add(new_ship)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/edit/<int:ship_id>', methods=['GET', 'POST'])
def edit_ship(ship_id):
    ship = Ship.query.get_or_404(ship_id)
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        year_built = request.form['year_built']
        description = request.form['description']
        image_url = request.form['image_url']
        short_description = request.form['short_description']
        is_active = request.form.get('is_active') == 'on'
        wikipedia_link = request.form['wikipedia_link']
        country_of_origin = request.form['country_of_origin']

        if Ship.query.filter(Ship.name == name, Ship.id != ship_id).first():
            flash('Корабль с таким названием уже существует!', 'danger')
        else:
            ship.name = name
            ship.type_ = type_
            ship.year_built = year_built
            ship.description = description
            ship.image_url = image_url
            ship.short_description = short_description
            ship.is_active = is_active
            ship.is_active = is_active
            ship.wikipedia_link = wikipedia_link
            ship.country_of_origin = country_of_origin

            db.session.commit()
            flash('Информация о корабле успешно обновлена!', 'success')
            return redirect(url_for('index'))
    return render_template('edit.html', ship=ship)


@app.route('/delete/<int:ship_id>', methods=['GET'])
def delete_ship(ship_id):
    ship = Ship.query.get_or_404(ship_id)
    return render_template('delete.html', ship=ship)

@app.route('/confirm_delete_ship/<int:ship_id>', methods=['POST'])
def confirm_delete_ship(ship_id):
    ship = Ship.query.get_or_404(ship_id)
    db.session.delete(ship)
    db.session.commit()
    flash('Корабль успешно удалён!', 'success')
    return redirect(url_for('index'))



@app.errorhandler(404)
def error_reaction(error):
    return render_template('error404.html', title='Страница не найдена')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
