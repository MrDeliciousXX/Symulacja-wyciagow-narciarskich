import Symulacja
import Analizy

czasOtwarcia = 28800
interwalKrzeselek = 15
pojemnoscKrzeselka = 2
liczbaWyciagow = 1
liczbaNarciarzy = 3000
czasSzczytu = 14400
szerokoscSzczytu = 7200
'''
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
#Analizy.analiza_pojemnosci_i_wyciagow(liczbaNarciarzy=10000, zakres_pojemnosci=[1, 2, 3, 4], zakres_wyciagow=[1, 2, 3, 4])

Analizy.analiza_zbiorcza(liczbaNarciarzy=100000, zakres_wyciagow=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], zakres_pojemnosci=[1, 2, 3, 4, 5, 6])

