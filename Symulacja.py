import random
import math
import matplotlib.pyplot as plt

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
    print(f"Symulacja: {czasOtwarcia}s, krzesełko co {interwalKrzeselek}s, pojemność {pojemnoscKrzeselka}, wyciągów: {liczbaWyciagow}")

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
    czasy_kolejki = []
    dlugosci_kolejki = []

    def losuj_liczbe_pasazerow(pojemnosc):
        # im mniej osób na krzesełku, tym mniejsze prawdopodobieństwo dla tej kombinacji
        base = 0.1  # minimalna waga
        full_weight = 1.0
        middle_weights = [base + (full_weight - base) * (i / pojemnosc) for i in range(pojemnosc)]
        weights = middle_weights + [full_weight]
        return random.choices(range(pojemnosc + 1), weights=weights)[0]

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
                    czasy_oczekiwania.append(t - czas_przyjscia)

            czasy_kolejki.append(t)
            dlugosci_kolejki.append(len(kolejka))

    obsluzeni = len(czasy_oczekiwania)
    srednie_czekanie = sum(czasy_oczekiwania) / obsluzeni if obsluzeni else 0
    nieobsluzeni = len(kolejka)

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
        'odjazdy': liczba_odjazdow
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