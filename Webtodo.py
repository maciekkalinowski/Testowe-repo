from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Wiersz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    wpis = db.Column(db.String(100), nullable=False)





def odczyt():
    """Wczytuje zawartosc pliku ToDo2.txt do listy i zwraca ta liste"""

    file_cont = []
    #str_pom = ''
    with open('ToDo2.txt') as plik :
        file_cont = plik.readlines()
    for d in range(len(file_cont)):
        file_cont[d]=file_cont[d][:-1]
    return file_cont




lista = []
lista = odczyt()

class TODO:
    list_path= Path('./lists')

    def __init__(self, nazwa_pliku, db):
        self.list = []
        self.list_db = []
        self.nazwa_pliku = self.list_path / nazwa_pliku
        self.db = db

    @classmethod
    def get_all_files(cls):
        #wynik = list(self.list_path.glob('*.txt'))
        wynik = [x.stem for x in cls.list_path.glob('*.txt') ]
        return wynik

    def dodaj(self, element):
        self.list.append(element)

    def dodaj_db(self, element):
        wiersz= Wiersz(wpis=element)
        self.db.session.add(wiersz)
        self.db.session.commit()
        
    def usun(self, index):
        self.list.pop(index)

    def usun_db(self, index):
        wiersz= Wiersz.query.get(index)
        self.db.session.delete(wiersz)
        self.db.session.commit()

    def zapis(self):
        with open(self.nazwa_pliku,'w') as plik :
            for p in range(len(self.list)):
                #linijka = temp_list[p]
                plik.write(self.list[p]+'\n')

    def zapis_db(self):
        db.session.commit()
    
    def odczyt(self):
        """Wczytuje zawartosc pliku ToDo2.txt do listy i zwraca ta liste"""

        file_cont = []
        #str_pom = ''
        with open(self.nazwa_pliku) as plik :
            file_cont = plik.readlines()
        for d in range(len(file_cont)):
            file_cont[d]=file_cont[d][:-1]
        self.list = file_cont

    def odczyt_db(self):     
        self.list_db = {i.id: i.wpis for i in Wiersz.query.all()}


    def show(self):
        return self.list

    def show_db(self):
        return self.list_db

#todo=TODO()

#--------------------------------

@app.route("/")
def index():
    return render_template('form.html',ll=TODO.get_all_files())







@app.route('/<nazwa_listy>',methods=['POST', 'GET'])
def nazwa_listy(nazwa_listy):
    
    Task = None
    ID = None
    #lista = odczyt()
    todo = TODO(nazwa_listy+'.txt', db)
    #todo.odczyt()
    todo.odczyt_db()
    if request.method == 'POST':
        Task = request.form.get('Zadanie')
        ID = request.form.get('ID')  
        #print('Task:{} ID:{}'.format(Task,ID))
        #if Task not in ['',None]:
        if Task :
            #todo.dodaj(Task)
            todo.dodaj_db(Task)
        if ID not in ['',None]:
            #todo.usun(int(ID))
            todo.usun_db(int(ID))
        #todo.zapis()
        todo.zapis_db()
    todo.odczyt_db()
    #return render_template('form.html',zm=enumerate(todo.show()),zm_db=todo.show_db().items(),ll=todo.get_all_files())
    return render_template('form.html',zm_db=todo.show_db().items(),ll=todo.get_all_files())