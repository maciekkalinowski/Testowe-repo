from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.create_all()

class Zadanie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    wpis = db.Column(db.String(100), nullable=False)


#class listaZadan(db.Model):




class ToDoDB:

    def __init__(self, db):

        self.list_db = []
        self.db = db


   
    def dodaj(self, element):
        zadanie= Zadanie(wpis=element)
        self.db.session.add(zadanie)
        self.db.session.commit()
        
   
    def usun(self, index):
        zadanie= Zadanie.query.get(index)
        self.db.session.delete(zadanie)
        self.db.session.commit()


    def zapis(self):
        db.session.commit()
    

    def odczyt(self):     
        self.list_db = {i.id: i.wpis for i in Zadanie.query.all()}


    def show(self):
        return self.list_db

#--------------------------------------   

class ToDoFile:
    list_path= Path('./lists')

    def __init__(self, nazwa_pliku):
        self.list = []

        self.nazwa_pliku = self.list_path / nazwa_pliku


    @classmethod
    def get_all_files(cls):
        #wynik = list(self.list_path.glob('*.txt'))
        wynik = [x.stem for x in cls.list_path.glob('*.txt') ]
        return wynik

    def dodaj(self, element):
        self.list.append(element)


        
    def usun(self, index):
        self.list.pop(index)



    def zapis(self):
        with open(self.nazwa_pliku,'w') as plik :
            for p in range(len(self.list)):
                #linijka = temp_list[p]
                plik.write(self.list[p]+'\n')


    
    def odczyt(self):
        """Wczytuje zawartosc pliku ToDo2.txt do listy i zwraca ta liste"""

        file_cont = []
        #str_pom = ''
        with open(self.nazwa_pliku) as plik :
            file_cont = plik.readlines()
        for d in range(len(file_cont)):
            file_cont[d]=file_cont[d][:-1]
        self.list = file_cont

    def show(self):
        return self.list

#--------------------------------------





@app.route("/")
def index():
    return render_template('form.html')







@app.route('/<nazwa_listy>',methods=['POST', 'GET'])
def nazwa_listy(nazwa_listy):
    
    Task = None
    ID = None
    todo = ToDoDB(db)
    todo.odczyt()
    
    if request.method == 'POST':
        Task = request.form.get('Zadanie')
        ID = request.form.get('ID')  
        if Task :
            todo.dodaj(Task)
        if ID not in ['',None]:
            todo.usun(int(ID))

        todo.zapis()

    todo.odczyt()
    #return render_template('form.html',zm=enumerate(todo.show()),zm_db=todo.show_db().items(),ll=todo.get_all_files())
    return render_template('form.html',zm_db=todo.show().items())