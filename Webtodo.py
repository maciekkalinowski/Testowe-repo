from flask import Flask, render_template, request
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

def wydruk():
    wynik = ''
    j = 0
    for i in lista:
        wynik += (str(j)+ ' - ' + i + ' ')
        j += 1
    return wynik


lista = []
lista = odczyt()
wydruk = wydruk()



#--------------------------------

@app.route("/")
def index():
    return render_template('home.html')





@app.route('/formularz', methods=['POST', 'GET'])
def formularz():
    
    Task = None
    ID = None
    if request.method == 'POST':
        Task = request.form.get('Zadanie')
        ID = request.form.get('ID')
        #print('Task:{} ID:{}'.format(Task,ID))
        if Task not in ['',None]:
            dodaj(Task)
        if ID not in ['',None]:
            usun(ID)
    
    return render_template('form.html',zm=wydruk)

