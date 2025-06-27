import random
import math
import matplotlib.pyplot as plt
import params


def SymulacjaWyciaguNarciarskiego(
    czasOtwarcia,
    interwalKrzeselek,
    pojemnoscKrzeselka,
    liczbaWyciagow,
    liczbaNarciarzy,
    czasSzczytu,
    szerokoscSzczytu,
    prawdopodobienstwo_awarii=0.002,
    prawdopodobienstwo_postoju=0.05
):
    print(f"\n\nSymulacja: {czasOtwarcia}s, krzesełko co {interwalKrzeselek}s, pojemność {pojemnoscKrzeselka}, wyciągów: {liczbaWyciagow}")

    czasy = generuj_czasy_przyjsc_narciarzy(czasOtwarcia, liczbaNarciarzy, czasSzczytu, szerokoscSzczytu)

    zdarzenia = []
    for t in czasy:
        zdarzenia.append(("A", t))  # przyjście narciarza

    liczba_awarii = 0
    liczba_postojow = 0
    niepelne_krzeselka = 0
    liczba_odjazdow = 0

    for wyciag in range(liczbaWyciagow):
        t = 0
        while t < czasOtwarcia:
            delay = 0

            # Postój
            if random.random() < prawdopodobienstwo_postoju:
                postoj = random.randint(10, 30)
                delay += postoj
                liczba_postojow += 1

            # Awaria
            if random.random() < prawdopodobienstwo_awarii:
                awaria = random.randint(300, 900)  # 5–15 minut
                delay += awaria
                liczba_awarii += 1

            zdarzenia.append(("B", t))  # odjazd krzesełka
            t += interwalKrzeselek + delay

    zdarzenia.sort(key=lambda x: x[1])

    kolejka = []
    czasy_oczekiwania = []

    # Średni czas oczekiwania na minutę
    minuty_dnia = czasOtwarcia // 60
    suma_na_minute = [0 for _ in range(minuty_dnia)]
    liczba_na_minute = [0 for _ in range(minuty_dnia)]

    czasy_kolejki = []
    dlugosci_kolejki = []

    def losuj_liczbe_pasazerow(pojemnosc, p_pelne=0.75):
        pozostale_prawdopodobienstwo = 1.0 - p_pelne
        liczba_opcji_niepelnych = pojemnosc

        # Im mniej osób, tym mniejsza waga
        odwrotne_wagi = list(range(1, liczba_opcji_niepelnych + 1))  # [1, 2, ..., pojemnosc]
        suma_wag = sum(odwrotne_wagi)
        prawdopodobienstwa_niepelne = [
            pozostale_prawdopodobienstwo * (waga / suma_wag) for waga in reversed(odwrotne_wagi)
        ]

        # Przykład (dla pojemność = 4):
        # pełne: 75%
        # 3 osoby: 15%
        # 2 osoby: 6%
        # 1 osoba: 3%
        # 0 osób: 1%

        prawdopodobienstwa = prawdopodobienstwa_niepelne + [p_pelne]
        liczby_pasazerow = list(range(pojemnosc)) + [pojemnosc]

        return random.choices(liczby_pasazerow, weights=prawdopodobienstwa)[0]

    for typ, t in zdarzenia:
        if typ == "A":
            kolejka.append(t)
            czasy_kolejki.append(t)
            dlugosci_kolejki.append(len(kolejka))

        elif typ == "B":
            liczba_pasazerow = losuj_liczbe_pasazerow(pojemnoscKrzeselka)
            liczba_odjazdow += 1

            if liczba_pasazerow < pojemnoscKrzeselka:
                niepelne_krzeselka += 1

            for _ in range(liczba_pasazerow):
                if kolejka:
                    czas_przyjscia = kolejka.pop(0)
                    oczekiwanie = t - czas_przyjscia
                    czasy_oczekiwania.append(t - czas_przyjscia)

                    minuta = int(t // 60)
                    if minuta < minuty_dnia:
                        suma_na_minute[minuta] += oczekiwanie
                        liczba_na_minute[minuta] += 1

            czasy_kolejki.append(t)
            dlugosci_kolejki.append(len(kolejka))

    obsluzeni = len(czasy_oczekiwania)
    srednie_czekanie = sum(czasy_oczekiwania) / obsluzeni if obsluzeni else 0
    nieobsluzeni = len(kolejka)

    srednia_na_minute = [
        suma_na_minute[i] / liczba_na_minute[i] if liczba_na_minute[i] > 0 else 0
        for i in range(minuty_dnia)
    ]

    # 🔚 Wypisanie wyników
    print(f"\n📊 WYNIKI SYMULACJI:")
    print(f"🧍‍♂️ Obsłużono narciarzy: {obsluzeni}")
    print(f"⌛ Średni czas oczekiwania: {srednie_czekanie:.2f} sek")
    print(f"❌ Nieobsłużeni narciarze: {nieobsluzeni}")
    print(f"⚠️ Liczba awarii: {liczba_awarii}")
    print(f"⏸ Liczba postojów: {liczba_postojow}")
    print(f"🪑 Liczba niepełnych krzesełek: {niepelne_krzeselka}")

    return {
        'czasy_oczekiwania': czasy_oczekiwania,
        'czasy_kolejki': czasy_kolejki,
        'dlugosci_kolejki': dlugosci_kolejki,
        'sredni_czas_oczekiwania': srednie_czekanie,
        'obsluzeni': obsluzeni,
        'nieobsluzeni': nieobsluzeni,
        'awarie': liczba_awarii,
        'postoje': liczba_postojow,
        'niepelne_krzeselka': niepelne_krzeselka,
        'odjazdy': liczba_odjazdow,
        'czasy_oczekiwania_na_minute': srednia_na_minute
    }


def generuj_czasy_przyjsc_narciarzy(
    czasOtwarciaSekundy: int,
    liczbaNarciarzy: int,
    szczytCzas: int,
    sigma: int
):
    czasy = []

    def pdf(t):
        return math.exp(-((t - szczytCzas) ** 2) / (2 * sigma ** 2))

    max_pdf = pdf(szczytCzas)

    while len(czasy) < liczbaNarciarzy:
        t = random.uniform(0, czasOtwarciaSekundy)
        p = random.uniform(0, max_pdf)
        if p < pdf(t):
            czasy.append(t)

    czasy.sort()
    return czasy

def rysuj_wykresy(czasy_kolejki, dlugosci_kolejki, czasy_oczekiwania):
    plt.figure(figsize=(12, 5))

    # Wykres długości kolejki
    plt.subplot(1, 2, 1)
    plt.step(czasy_kolejki, dlugosci_kolejki, where='post')
    plt.xlabel("Czas [s]")
    plt.ylabel("Długość kolejki")
    plt.title("Długość kolejki w czasie")

    # Histogram czasu oczekiwania
    plt.subplot(1, 2, 2)
    plt.hist(czasy_oczekiwania, bins=30, color='orange', edgecolor='black')
    plt.xlabel("Czas oczekiwania [s]")
    plt.ylabel("Liczba narciarzy")
    plt.title("Histogram czasu oczekiwania")

    plt.tight_layout()
    plt.show()

def UruchomSymulacje(
    liczba_powtorzen,
    **parametry_symulacji
):
    wyniki_zbiorcze = {
        'sredni_czas_oczekiwania': [],
        'obsluzeni': [],
        'nieobsluzeni': [],
        'awarie': [],
        'postoje': [],
        'niepelne_krzeselka': [],
        'odjazdy': [],
        'czasy_oczekiwania_na_minute': []
    }

    for _ in range(liczba_powtorzen):
        wynik = SymulacjaWyciaguNarciarskiego(**parametry_symulacji)
        for klucz in wyniki_zbiorcze:
            wyniki_zbiorcze[klucz].append(wynik[klucz])

    def srednia(lista):
        return sum(lista) / len(lista)

    def srednia_lista_list(lista_list):
        liczba_powtorzen = len(lista_list)
        dlugosc_listy = len(lista_list[0])
        return [
            sum(lista_list[i][j] for i in range(liczba_powtorzen)) / liczba_powtorzen
            for j in range(dlugosc_listy)
        ]

    # Podsumowanie
    print(f"\n📈 ŚREDNIE WYNIKI Z {liczba_powtorzen} SYMULACJI:")
    for klucz, lista in wyniki_zbiorcze.items():
        if klucz == 'czasy_oczekiwania_na_minute':
            print(f"{klucz}: [lista {len(lista[0])} wartości]")
        else:
            print(f"{klucz}: {srednia(lista):.2f}")

    return {
        klucz: srednia_lista_list(lista) if klucz == 'czasy_oczekiwania_na_minute' else srednia(lista)
        for klucz, lista in wyniki_zbiorcze.items()
    }

def oszacuj_liczbe_symulacji(odchylenie_std, epsilon=5, poziom_ufnosci=0.95):
    z = 1.96 if poziom_ufnosci == 0.95 else 2.58  # można rozszerzyć na inne poziomy
    n = (z * odchylenie_std / epsilon) ** 2
    return math.ceil(n)


import statistics

params = {
    'czasOtwarcia': 28800,
    'interwalKrzeselek': 20,
    'pojemnoscKrzeselka': 8,
    'liczbaWyciagow': 14,
    'liczbaNarciarzy': 50000,
    'czasSzczytu': 14400,
    'szerokoscSzczytu': 3600
}

#proby = [SymulacjaWyciaguNarciarskiego(**params)['sredni_czas_oczekiwania'] for _ in range(40)]
#std = statistics.stdev(proby)

#potrzebne_n = oszacuj_liczbe_symulacji(std, epsilon=120)  # cel: +/- 120 sekund
#print(f"\n\n📉 Odchylenie standardowe średniego czasu oczekiwania (z 40 prób): {std:.2f} s")
#print(f"🔍 Oszacowana liczba symulacji dla ±2min: {potrzebne_n}")