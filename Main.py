import Symulacja
import Analizy

'''
czasOtwarcia=28800,
interwalKrzeselek=10,
pojemnoscKrzeselka=4,
liczbaWyciagow=2,
liczbaNarciarzy=400,
czasSzczytu=1800,
szerokoscSzczytu=600,
prawdopodobienstwo_awarii=0.002,     # ~1 awaria na 500 wyjazdów
prawdopodobienstwo_postoju=0.05      # 5% szansy na postój


wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
    czasOtwarcia,    # 8 godzin
    interwalKrzeselek,       # co 15 sekund
    pojemnoscKrzeselka,        # pojemność krzesełka
    liczbaWyciagow,        # liczba wyciągów
    liczbaNarciarzy,     # liczba narciarzy
    czasSzczytu,    # szczyt o 4h
    szerokoscSzczytu      # szerokość szczytu
)

Symulacja.rysuj_wykresy(
    wynik['czasy_kolejki'],
    wynik['dlugosci_kolejki'],
    wynik['czasy_oczekiwania']
)
'''
#Analizy.analiza_liczby_wyciagow(liczbaNarciarzy=10000, zakres=[1, 2, 3, 4, 5])
#Analizy.analiza_pojemnosci_krzeselek(liczbaNarciarzy=10000, zakres=[1, 2, 3, 4])
#Analizy.analiza_pojemnosci_i_wyciagow(liczbaNarciarzy=50000, zakres_pojemnosci=[1, 2, 4, 6, 8], zakres_wyciagow=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

#Analizy.analiza_zbiorcza(liczbaNarciarzy=20000, zakres_wyciagow=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], zakres_pojemnosci=[1, 2, 3, 4, 5, 6])
#Analizy.analiza_wplywu_narciarzy(liczbaWyciagow=8, pojemnoscKrzeselka=8, zakres_narciarzy=range(40000, 100001, 1000))

#Analizy.analiza_zapelnienia(liczbaNarciarzy=50000, zakres_pojemnosci=[8], liczbaWyciagow=8)

#Analizy.analiza_w_czasie(50000, 7, 8)
#Analizy.analiza_w_czasie(50000, 8, 8)
#Analizy.analiza_w_czasie(50000, 9, 6)
#Analizy.analiza_w_czasie(50000, 10, 6)
#Analizy.analiza_w_czasie(50000, 13, 4)
#Analizy.analiza_w_czasie(50000, 14, 4)

#wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
#    czasOtwarcia=28800,
#    interwalKrzeselek=15,
#    pojemnoscKrzeselka=8,
#    liczbaWyciagow=8,
#    liczbaNarciarzy=50000,
#    czasSzczytu=14400,
#    szerokoscSzczytu=7200
#)
#Analizy.analiza_statystyczna_wyniku(wynik)
