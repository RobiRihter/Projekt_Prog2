'''
Avtorja: Robi Rihter in Luka Oblak
Datum: April 2022
'''

import requests
import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from bs4 import BeautifulSoup
import json

podatki = pd.read_csv (r'/Users/robirihter/Desktop/Programiranje2/csvData.csv')

class Drzava:
    def __init__(self, podatki):
        self.name = podatki['name']
        self.pop2022 = podatki['pop2022']
        self.pop2050 = podatki['pop2050']
        self.pop2015 = podatki['pop2015']
        self.pop2010 = podatki['pop2010']
        self.pop2000 = podatki['pop2000']
        self.pop1990 = podatki['pop1990']
        self.pop1980 = podatki['pop1980']
        self.pop1970 = podatki['pop1970']
        self.area = podatki['area']
        self.gostota = podatki['Density']
        self.rast = podatki['GrowthRate']
        self.svet_odstotek = podatki['WorldPercentage']
        self.rank = podatki['rank']
    
    def pricakovano_pove(self, drzava):
        '''Pričakovana procentualna povečanost populacije za državo.'''
        drzave = self.name
        pop2022 = self.pop2022   
        pop2050 = self.pop2050
        tab = [((pop2050[i] - pop2022[i])/abs(pop2022[i]))*100 for i in range(len(podatki))]
        pop = {}
        for i in range(len(drzave)):
            pop[drzave[i]] = tab[i]
        return "\n  Pričakovana rast populacije za državo {} do leta 2050: {}%\n".format(drzava, round(pop[drzava],2))
    
    def povecanje_pop(self, drzava):
        '''Procentualna povečanost populacije za državo od leta 1980.'''
        drzave = self.name
        pop2022 = self.pop2022
        pop1980 = self.pop1980
        tab = [((pop2022[i] - pop1980[i])/abs(pop1980[i]))*100 for i in range(len(podatki))]
        popu = {}
        for i in range(len(drzave)):
            popu[drzave[i]] = tab[i]
        return "\n  Rast populacije za državo {} od leta 1980: {}%".format(drzava, round(popu[drzava],2))
    
    def izpis(self, drzava):
        '''Izpis podatkov za vhodno državo.'''
        indeks = podatki[podatki['name'] == drzava].index.values.astype(int)[0] #Indeks vhodne države.
        for drz in self.name:
            if drz == drzava:
                niz = ''
                niz += "{:>30s} | {:s}\n".format('Država', drz)
                niz += "{:>30s} | {}\n".format('Populacija(2022)', self.pop2022[indeks])
                niz += "{:>30s} | {}\n".format('Pričakovana populacija(2050)', self.pop2050[indeks])
                niz += "{:>30s} | {}\n".format('Svetovni odstotek', self.svet_odstotek[indeks])
                niz += "{:>30s} | {}\n".format('Stopnja rasti', self.rast[indeks])
                niz += "{:>30s} | {}\n".format('Svetovni rank', self.rank[indeks])
                return niz

    def izris(self, drzava1, drzava2):
        '''Grafično primerjanje populacij dveh vhodnih držav.'''
        indeks = podatki[podatki['name'] == drzava1].index.values.astype(int)[0] #Indeks prve države.
        indeks2 = podatki[podatki['name'] == drzava2].index.values.astype(int)[0]# Indeks druge države.
        x1 = [1970, 1980, 1990, 2000, 2010, 2015, 2022]
        x2 = x1 # x osi sta enaki za oba grafa.
        for drz in self.name:
            if drz == drzava1:
                y1 = [self.pop1970[indeks], self.pop1980[indeks], self.pop1990[indeks],self.pop2000[indeks],self.pop2010[indeks], self.pop2015[indeks], self.pop2022[indeks]]
            if drz == drzava2:
                y2 = [self.pop1970[indeks2], self.pop1980[indeks2], self.pop1990[indeks2],self.pop2000[indeks2],self.pop2010[indeks2], self.pop2015[indeks2], self.pop2022[indeks2]]
        #Graf.
        plt.yscale('log',base = 10)
        plt.grid(linestyle = '-', linewidth = 1)
        plt.plot(x2, y2, label = drzava2)        
        plt.plot(x1, y1, label = drzava1) 
        plt.xlabel('Leta')
        plt.ylabel('Populacija')
        plt.title('Primerjava populacij dveh držav.')
        plt.legend()
        plt.show()
        
def podatki_zivljenska_doba():
    '''Pridobivanje podatkov iz spletne strani, nato shrenjeni v list.'''
    rq = requests.get("https://www.worlddata.info/life-expectancy.php")
    soup = BeautifulSoup(rq.text, 'html.parser')
    tab = soup.find('div', class_ = 'tablescroller')
    drzava = []
    for ele in tab.find_all('tr'):
        podatki = []
        for el in ele.find_all('td'):
            podatki.append(el.text)
        drzava.append(podatki)
    drzava = drzava[1:]
    # Numerične podatke pretvorimo iz niza v float.
    for i in range(len(drzava)):
        for j in range(1, 5):
            drzava[i][j] = float(drzava[i][j].split(" ")[0])
    return drzava

tab_doba = podatki_zivljenska_doba()
class Zivljenska_doba:
    def __init__(self, tab_doba):
        self.drzava = tab_doba
        
    def slovar(self, drz):
        '''list drzava spremenjen v slovar.'''
        drzava = self.drzava
        drzave = [vrstica[0] for vrstica in drzava]
        podatki = {}
        for i in range(len(drzave)):
            podatki[drzave[i]] = drzava[i][1:]
        # Izpis podatkov za vhodno državo.
        niz = ''
        niz += 'Pričakovana življenska doba moškega: {} let\n\n'.format(podatki[drz][0])
        niz += 'Pričakovana življenska doba ženske: {} let\n\n'.format(podatki[drz][1])
        niz += 'Rodnost: {}%\n\n'.format(podatki[drz][2])
        niz += 'Smrtnost: {}%'.format(podatki[drz][3])
        return niz
        
    def razlike_v_letih(self):
        '''Izris histograma'''
        drzava = self.drzava
        razlike = []
        for pricakovana in drzava:
            i, j = 1,2
            razlike.append(abs(pricakovana[j] - pricakovana[i]))
        maks = round(max(razlike), 1)
        plt.title('Razlike življenskih dob med moškimi in ženskami')
        plt.grid(axis = 'y', alpha=0.75)
        plt.xlabel('Razlike v letih')
        plt.ylabel('Frekvenca (število držav)')
        plt.grid(axis='y')
        plt.hist(razlike, bins = 'auto', alpha=0.7, rwidth=0.85)
        plt.show() 

    def naj_razlika_v_letih(self):
        '''Država z največjo razliko med pričakovano življensko dobo moških in žensk.'''
        drzava = self.drzava
        drzave = [vrstica[0] for vrstica in drzava]
        razlike = [abs(pricakovana[2] - pricakovana[1]) for pricakovana in drzava]
        maks = round(max(razlike), 1)
        sl_raz = {}
        for i in range(len(drzave)):
            sl_raz[drzave[i]] = round(razlike[i], 1)
        val_list = list(sl_raz.values())
        key_list = list(sl_raz.keys())

        position = val_list.index(maks)
        return key_list[position]


    def naj_rod_smrt(self, niz):
        '''Država z najvišjo rodnostjo ali najvišjo smrtnostjo.'''
        drzava = self.drzava
        drzave = [vrstica[0] for vrstica in drzava]
        if niz == 'rod':
            rodnosti = [vrstica[3] for vrstica in drzava]
            return [(el[0]) for el in drzava if el[3] == max(rodnosti)][0]
        else:
            smrtnosti = [vrstica[4] for vrstica in drzava]
            return [(el[0]) for el in drzava if el[4] == max(smrtnosti)][0]
    def min_rod_smrt(self, niz):
        '''Država z najmanjšo rodnostjo ali najmanjšo smrtnostjo.'''
        drzava = self.drzava
        drzave = [vrstica[0] for vrstica in drzava]
        if niz == 'rod':
            rodnosti = [vrstica[3] for vrstica in drzava]
            return [(el[0]) for el in drzava if el[3] == min(rodnosti)][0]
        else:
            smrtnosti = [vrstica[4] for vrstica in drzava]
            return [(el[0]) for el in drzava if el[4] == min(smrtnosti)][0]
      
    def povprecje(self, spol):
        '''Povprečje pričakovanih življenskih dob v odvisnosti od spola.'''
        drzava = self.drzava
        if spol == 'Moški':
            return round(sum([vrstica[1] for vrstica in drzava]) / len(drzava), 1)
        elif spol == 'Ženske':
            return round(sum([vrstica[2] for vrstica in drzava]) / len(drzava), 1) 
    def st_odklon(self, spol):
        '''Standardni odklon v odvisnosti od spola.'''
        drzava = self.drzava
        if spol == 'Moški':
            tab = [vrstica[1] for vrstica in drzava]
        elif spol == 'Ženske':
            tab = [vrstica[2] for vrstica in drzava]
        return np.std(tab)

    def plot(self, spol):
        '''Izris grafa odstopanj let pričakovane življenske dobe od povprečja za dani spol.'''
        drzava = self.drzava
        data = [vrstica[1] for vrstica in drzava]
        drz = [vrstica[0] for vrstica in drzava]
        povp = Zivljenska_doba.povprecje(self, spol)
        odklon = Zivljenska_doba.st_odklon(self, spol)
        naj = max(data)
        mal = min(data)
        
        plt.title("Odstopanja življenskih dob od povprečja " + '(' + str(spol) + ')')
        plt.ylim(mal - 10, naj + 15)
        plt.ylabel('Leta')
        plt.scatter(x = range(len(data)), y = data)
        plt.hlines(y = povp, xmin = 0, xmax = len(data))
        
        plt.hlines(y = povp - odklon, xmin = 0, xmax = len(data), colors='r')
        plt.hlines(y = povp + odklon, xmin = 0, xmax = len(data), colors='r')
        plt.hlines(y = povp - 2 * odklon, xmin = 0, xmax = len(data), colors='g')
        plt.hlines(y = povp + 2 * odklon, xmin = 0, xmax = len(data), colors='g')
        
        plt.show()
    
def narisi():
    '''Grafični prikaz gostot držav.'''
    drzave = json.load(open('custom.geo.json', "r"))
    drzava_id = {}
    st = 1
    for lasnost in drzave['features']:
        lasnost['id'] = st
        drzava_id[lasnost['properties']['name']] = lasnost['id']
        st += 1
        
    df = pd.read_csv("csvData.csv")
    indeks = 0
    indeksi = []
    for drzava in df['name']:
        if drzava not in drzava_id.keys():
            indeksi.append(indeks)
        indeks += 1
    df.drop(indeksi ,axis = 0, inplace = True)

    df['id'] = df['name'].apply(lambda x: drzava_id[x])
    df['Lestvica gostote'] = np.log10(df['Density'])

    fig = px.choropleth(df,
                        locations = 'id',
                        geojson = drzave,
                        color = 'Lestvica gostote',
                        title = 'Gostote držav',
                        hover_name = 'name',
                        hover_data = ['Density'])
    fig.show() 
        
#Obrazec
def obrazec():
    def click():
        Vnesi_drzavo = textentry.get()
        output.delete(0.0, END)
        ven = Drzava(podatki)
        try:
            output.insert(END, ven.izpis(Vnesi_drzavo))
            output.insert(END, ven.povecanje_pop(Vnesi_drzavo))
            output.insert(END, ven.pricakovano_pove(Vnesi_drzavo))
        except:
            output.insert(END, 'Ta država ne obstaja.')

        
    def click2():
        drzava1 = drugivnos.get()
        drzava2 = tretjivnos.get()
        ven = Drzava(podatki)
        try:
            izpis = ven.izris(drzava1, drzava2)
        except:
            izpis = "Ta država ne obstaja.\n"
            
    def click3():
        narisi()
        
    def click4():
        A = Zivljenska_doba(tab_doba)
        A.razlike_v_letih()
        
    def click5():
        ven.delete(0.0, END)
        A = Zivljenska_doba(tab_doba)
        niz = ''
        niz += 'Država z največjo razliko življenskih dob med spoloma: {}\n'.format(A.naj_razlika_v_letih())
        niz += 'Povprečna starostna doba moškega: {} let \n'.format(A.povprecje('Moški'))
        niz += 'Povprečna starostna doba ženske: {} let \n'.format(A.povprecje('Ženske'))
        niz += 'Država z najvišjo rodnostjo: {} \n'.format(A.naj_rod_smrt('rod'))
        niz += 'Država z najvišjo smrtnostjo: {} \n'.format(A.naj_rod_smrt('smrt'))
        niz += 'Država z najmanjšo rodnostjo: {} \n'.format(A.min_rod_smrt('rod'))
        niz += 'Država z najmanjšo smrtnostjo: {}'.format(A.min_rod_smrt('smrt'))
        ven.insert(END, niz)
        
    def click6():
        A = Zivljenska_doba(tab_doba)
        drz = vnos.get()
        ven.delete(0.0, END)
        try:
            ven.insert(END, A.slovar(drz))
        except:
            ven.insert(END, 'Za to državo ni podatka.')
    
    def click7():
        A = Zivljenska_doba(tab_doba)
        spol = vnos2.get()
        try:
            A.plot(spol)
        except:
            pass
        
    window = Tk()
    window.title('Populacije držav')
    window.configure(background = "light green")
    Label (window, text = "Vnesi državo: ",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 1, column = 0, sticky = W)
    #Vnos
    textentry = Entry(window, width = 20)
    textentry.grid(row = 2, column = 0, sticky = W)
    #Gumb
    Button(window, text = "Prikaz:",font = ("Courier", 16),bg = 'green', width = 7, command = click).grid(row = 3, column = 0, sticky = W)
    Label(window, text = "\nIzpis (Osnovni podatki, rast populacije v zadnjih letih in pričakovana rast):  ",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 4, column = 0)
    output = Text(window, width = 80, height = 9, font = ("Courier", 16), bg = "light grey")
    output.grid(row = 5, column = 0)
    ######
    Label (window, text = "Grafično primerjanje rasti populacij dveh držav.",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 6, column = 0, sticky = W)
    Label (window, text = "Prva država: ",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 7, column = 0, sticky = W)
    Label (window, text = "Druga država: ",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 7, columnspan = 1)
    #Vnos
    drugivnos = Entry(window, width = 20)
    tretjivnos = Entry(window, width = 20)
    drugivnos.grid(row = 8, column = 0, sticky = W)
    tretjivnos.grid(row = 8, columnspan = 1)
    #Gumb
    Gumb = Button(window, text = "Primerjaj",font = ("Courier", 17),bg = 'green', width = 8, command = click2).grid(row = 10, column = 0, sticky = W)
    ######
    Label (window, text = "Prikaz gostot držav:",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 11, column = 0, sticky = W)
    Button(window, text = "Prikaži",font = ("Courier", 17),bg = 'green', width = 7, command = click3).grid(row = 11, columnspan = 1)
    Label (window, text = "Histogram:",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 12, column = 0, sticky = W)
    Button(window, text = "Prikaži",font = ("Courier", 17),bg = 'green', width = 7, command = click4).grid(row = 12, columnspan = 1)   
    Label (window, text = "Življenska doba (Osnovni podatki):",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 13, column = 0, sticky = W)
    Button(window, text = "Prikaži",font = ("Courier", 17),bg = 'green', width = 7, command = click5).grid(row = 13, columnspan = 1)   
    ven = Text(window, width = 80, height = 7, font = ("Courier", 16), bg = "light grey")
    ven.grid(row = 18, column = 0)
    
    vnos = Entry(window, width = 20)
    Label (window, text = "Življenska doba za državo:",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 14, column = 0, sticky = W)
    vnos.grid(row = 14, columnspan = 1)
    Button(window, text = "Prikaz:",font = ("Courier", 17),bg = 'green', width = 8, command = click6).grid(row = 15, column = 0, sticky = W)
    
    Label (window, text = "Odstopanje pričakovanih življenskih dob od povprečja",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 19, column = 0, sticky = W)
    Label (window, text = "Vnesi spol (Moški, Ženske):",fg = 'black', bg = 'light green', font = ("Courier", 16)).grid(row = 20, column = 0, sticky = W)
    vnos2 = Entry(window, width = 15)
    vnos2.grid(row = 20, columnspan = 1)
    Button(window, text = "Prikaz",font = ("Courier", 17),bg = 'green', width = 7, command = click7).grid(row = 21, columnspan = 1)   
    ######
    
#Glavni program  
def main():
    obrazec()
    
if __name__ == "__main__":
    main()