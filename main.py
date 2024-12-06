# İçe aktar
from flask import Flask, render_template,request, redirect
# Veri tabanı kitaplığını bağlama
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Veri tabanı oluşturma
db = SQLAlchemy(app)
# Tablo oluşturma

class Card(db.Model):
    # Sütun oluşturma
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Başlık
    title = db.Column(db.String(100), nullable=False)
    # Tanım
    subtitle = db.Column(db.String(300), nullable=False)
    # Metin
    text = db.Column(db.Text, nullable=False)

    # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'



class User (db.Model):
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(30),nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)



# İçerik sayfasını çalıştırma
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']

            #Ödev #4. yetkilendirmeyi uygulamak
            db_users=User.query.all()
            for user in db_users:
                if form_login==user.email and form_password== user.password:
                    return redirect('/index')
            else:
                error = 'Bir işi de düzgün yap!!'
                return render_template('login.html', error=error)



        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    hata=''
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        if len(password)>=8 and len(password)<20:
            user=User(email=login,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        else:
            hata='Şifre uzunluğun 8 ila 20 arası olmalı'
            return render_template('/registration.html',hata=hata)

    else:
        return render_template('registration.html',hata=hata)


# İçerik sayfasını çalıştırma
@app.route('/index')
def index():
    # Veri tabanı girişlerini görüntüleme
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Kayıt sayfasını çalıştırma
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Giriş oluşturma sayfasını çalıştırma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Giriş formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Veri tabanına gönderilecek bir nesne oluşturma
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')



class FeedBack (db.Model):
    note=db.Column(db.String(50),nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(50),nullable=False)
    report=db.Column(db.String(150),nullable=False)


@app.route('/report',methods=['POST','GET'])
def report():
    if request.method=='POST':
        email=request.form["email"]
        note=request.form["note"]
        report=request.form["report"]
        card=FeedBack(email=email,note=note,report=report)
        db.session.add(card)
        db.session.commit()
        return render_template('feedback.html',
                               email=email
                               )
    else:
        return render_template("report.html")







@app.route('/delete/<int:id>')
def delete(id):
    card=Card.query.get(id)
    if card:
        db.session.delete(card)
        db.session.commit()
    return redirect ('/')







if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
