import random
from forms import LoginForm
import secrets

from flask import Flask, render_template, request, flash
from models import db, Student, Mark, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('base.html')


@app.route('/task3')
def index():
    students = Student.query.all()
    marks = Mark.query.all()
    return render_template('index_3.html', students=students, marks=marks)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("fill-table3")
def fill_task3_table():
    for i in range(1, 20):
        new_mark = Mark(subject=f'Subject{i}',
                        mark=random.randint(1, 6),
                        student_id=random.randint(1, 11))
        db.session.add(new_mark)
    db.session.commit()

    for i in range(1, 11):
        new_student = Student(
            first_name=f'First_name{i}',
            last_name=f'Last_name{i}',
            group=random.randint(100, 200),
            email=f'last_name{i}@email.com',
        )
        db.session.add(new_student)
    db.session.commit()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        new_user = User(username=username, email=email)
        users = User.query.filter(User.username == username).all()
        if len(users) > 0:
            flash('Имя пользователя не уникально!','error')
            for user in users:
                if user.email == email:
                    flash('Email не уникальный!', 'error')
            return render_template('register.html', form=form)
        else:
            db.session.add(new_user)
            db.session.commit()
            return render_template('success.html')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(Debug=True)
