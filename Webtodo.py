from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
app = Flask(__name__)


def dodaj(var):
    lista.append(var)
    zapis()

def usun(xxx):
    lista.pop(int(xxx))
    zapis()

def zapis():
    with open('ToDo2.txt','w') as plik :
        for p in range(len(lista)):
            #linijka = temp_list[p]
            plik.write(lista[p]+'\n')
    #print(lista)


def odczyt():
    """Wczytuje zawartosc pliku ToDo2.txt do listy i zwraca ta liste"""

    file_cont = []
    #str_pom = ''
    with open('ToDo2.txt') as plik :
        file_cont = plik.readlines()
    for d in range(len(file_cont)):
        file_cont[d]=file_cont[d][:-1]
    return file_cont

# def wydruk():
#     wynik = ''
#     j = 0
#     for i in lista:
#         wynik += (str(j)+ ' - ' + i + ' ')
#         j += 1
#     return wynik


lista = []
lista = odczyt()

class TODO:
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

#todo=TODO()

#--------------------------------

@app.route("/")
def index():
    return render_template('form.html',ll=TODO.get_all_files())






# @app.route('/formularz', methods=['POST', 'GET'])
# def formularz():
    
#     Task = None
#     ID = None
#     #lista = odczyt()
#     todo = TODO('ToDo2.txt')
#     todo.odczyt()
#     if request.method == 'POST':
#         Task = request.form.get('Zadanie')
#         ID = request.form.get('ID')
#         #print('Task:{} ID:{}'.format(Task,ID))
#         if Task not in ['',None]:
#             todo.dodaj(Task)
#         if ID not in ['',None]:
#             todo.usun(int(ID))
#         todo.zapis()
    
#         return render_template('form.html',zm=enumerate(todo.show()))
#     return render_template('form.html',zm=enumerate(todo.show()))

@app.route('/<nazwa_listy>',methods=['POST', 'GET'])
def nazwa_listy(nazwa_listy):
    
    Task = None
    ID = None
    #lista = odczyt()
    todo = TODO(nazwa_listy+'.txt')
    todo.odczyt()
    if request.method == 'POST':
        Task = request.form.get('Zadanie')
        ID = request.form.get('ID')
        #print('Task:{} ID:{}'.format(Task,ID))
        #if Task not in ['',None]:
        if Task :
            todo.dodaj(Task)
        if ID not in ['',None]:
            todo.usun(int(ID))
        todo.zapis()
    
    return render_template('form.html',zm=enumerate(todo.show()),ll=todo.get_all_files())   