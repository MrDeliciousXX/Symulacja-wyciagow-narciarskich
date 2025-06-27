import matplotlib.pyplot as plt
import numpy as np
import os
import Symulacja

def analiza_liczby_wyciagow(liczbaNarciarzy, zakres):
    wyniki = []

    for n in zakres:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
            czasOtwarcia=28800,
            interwalKrzeselek=15,
            pojemnoscKrzeselka=2,
            liczbaWyciagow=n,
            liczbaNarciarzy=liczbaNarciarzy,
            czasSzczytu=14400,
            szerokoscSzczytu=7200
        )
        wyniki.append((n, wynik['sredni_czas_oczekiwania']))

    # Wykres
    x = [w[0] for w in wyniki]
    y = [w[1] / 60 for w in wyniki]

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.xlabel("Liczba wyciągów")
    plt.ylabel("Średni czas oczekiwania [min]")
    plt.title("Wpływ liczby wyciągów na czas oczekiwania")
    plt.grid(True)
    plt.show()

def analiza_pojemnosci_krzeselek(liczbaNarciarzy, zakres):
    wyniki = []

    for pojemnosc in zakres:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
            czasOtwarcia=28800,
            interwalKrzeselek=15,
            pojemnoscKrzeselka=pojemnosc,
            liczbaWyciagow=2,
            liczbaNarciarzy=liczbaNarciarzy,
            czasSzczytu=14400,
            szerokoscSzczytu=7200
        )
        wyniki.append((pojemnosc, wynik['sredni_czas_oczekiwania']))

    x = [w[0] for w in wyniki]
    y = [w[1] / 60 for w in wyniki]

    plt.figure()
    plt.plot(x, y, marker='o', color='green')
    plt.xlabel("Pojemność krzesełka")
    plt.ylabel("Średni czas oczekiwania [min]")
    plt.title(f"Wpływ pojemności krzesełka (narciarzy: {liczbaNarciarzy})")
    plt.grid(True)
    plt.show()

def analiza_pojemnosci_i_wyciagow(liczbaNarciarzy, zakres_pojemnosci, zakres_wyciagow):
    heatmap = []

    for pojemnosc in zakres_pojemnosci:
        wiersz = []
        for wyciagi in zakres_wyciagow:
            wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
                czasOtwarcia=28800,
                interwalKrzeselek=15,
                pojemnoscKrzeselka=pojemnosc,
                liczbaWyciagow=wyciagi,
                liczbaNarciarzy=liczbaNarciarzy,
                czasSzczytu=14400,
                szerokoscSzczytu=7200
            )
            wiersz.append(wynik['sredni_czas_oczekiwania'] / 60)
        heatmap.append(wiersz)

    heatmap = np.array(heatmap)

    plt.figure(figsize=(8, 6))
    im = plt.imshow(heatmap, cmap='YlOrRd', origin='lower')

    plt.colorbar(im, label='Średni czas oczekiwania [min]')
    plt.xticks(ticks=range(len(zakres_wyciagow)), labels=zakres_wyciagow)
    plt.yticks(ticks=range(len(zakres_pojemnosci)), labels=zakres_pojemnosci)
    plt.xlabel("Liczba wyciągów")
    plt.ylabel("Pojemność krzesełka")
    plt.title(f"Średni czas oczekiwania (narciarzy: {liczbaNarciarzy})")
    plt.tight_layout()
    plt.show()

def analiza_zbiorcza(liczbaNarciarzy, zakres_pojemnosci, zakres_wyciagow):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Wpływ liczby wyciągów
    wyniki_wyciagi = []
    for wyc in zakres_wyciagow:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(28800, 15, 2, wyc, liczbaNarciarzy, 14400, 7200)
        wyniki_wyciagi.append(wynik['sredni_czas_oczekiwania'] / 60)

    axs[0].plot(zakres_wyciagow, wyniki_wyciagi, marker='o')
    axs[0].set_title("Liczba wyciągów")
    axs[0].set_xlabel("Wyciągi")
    axs[0].set_ylabel("Średni czas oczekiwania [min]")
    axs[0].grid(True)

    # 2. Wpływ pojemności krzesełka
    wyniki_poj = []
    for poj in zakres_pojemnosci:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(28800, 15, poj, 2, liczbaNarciarzy, 14400, 7200)
        wyniki_poj.append(wynik['sredni_czas_oczekiwania'] / 60)

    axs[1].plot(zakres_pojemnosci, wyniki_poj, marker='s', color='green')
    axs[1].set_title("Pojemność krzesełka")
    axs[1].set_xlabel("Pojemność")
    axs[1].set_ylabel("Średni czas oczekiwania [min]")
    axs[1].grid(True)

    # 3. Heatmapa: pojemność vs wyciągi
    import numpy as np
    heatmap = []
    for poj in zakres_pojemnosci:
        wiersz = []
        for wyc in zakres_wyciagow:
            wynik = Symulacja.SymulacjaWyciaguNarciarskiego(28800, 15, poj, wyc, liczbaNarciarzy, 14400, 7200)
            wiersz.append(wynik['sredni_czas_oczekiwania'] / 60)
        heatmap.append(wiersz)

    heatmap = np.array(heatmap)
    im = axs[2].imshow(heatmap, origin='lower', cmap='YlOrRd')
    axs[2].set_xticks(range(len(zakres_wyciagow)))
    axs[2].set_xticklabels(zakres_wyciagow)
    axs[2].set_yticks(range(len(zakres_pojemnosci)))
    axs[2].set_yticklabels(zakres_pojemnosci)
    axs[2].set_xlabel("Wyciągi")
    axs[2].set_ylabel("Pojemność")
    axs[2].set_title("Czas oczekiwania [min]")
    fig.colorbar(im, ax=axs[2], fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()

def analiza_wplywu_narciarzy(liczbaWyciagow, pojemnoscKrzeselka, zakres_narciarzy):
    wyniki = []

    for liczba in zakres_narciarzy:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
            czasOtwarcia=28800,
            interwalKrzeselek=15,
            pojemnoscKrzeselka=pojemnoscKrzeselka,
            liczbaWyciagow=liczbaWyciagow,
            liczbaNarciarzy=liczba,
            czasSzczytu=14400,
            szerokoscSzczytu=7200
        )
        wyniki.append(wynik['sredni_czas_oczekiwania'] / 60)  # minuty

    # Wykres
    plt.figure(figsize=(8, 5))
    plt.plot(zakres_narciarzy, wyniki, marker='^', color='purple')
    plt.title(f"Średni czas oczekiwania vs liczba narciarzy\n(wyciągów: {liczbaWyciagow}, pojemność: {pojemnoscKrzeselka})")
    plt.xlabel("Liczba narciarzy")
    plt.ylabel("Średni czas oczekiwania [min]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analiza_narciarzy_dla_wyciagow_i_pojemnosci(
    max_wyciagow,
    max_pojemnosc,
    zakres_narciarzy,
    katalog='wyniki_symulacji',
    pokaz_wykresy=False
):
    os.makedirs(katalog, exist_ok=True)

    max_oczekiwanie = Symulacja.SymulacjaWyciaguNarciarskiego(
        czasOtwarcia=28800,
        interwalKrzeselek=15,
        pojemnoscKrzeselka=1,
        liczbaWyciagow=1,
        liczbaNarciarzy=max(zakres_narciarzy),
        czasSzczytu=14400,
        szerokoscSzczytu=7200
    )['sredni_czas_oczekiwania'] / 60
    max_y = max_oczekiwanie * 1.1

    for liczba_wyciagow in range(1, max_wyciagow + 1):
        for pojemnosc in range(1, max_pojemnosc + 1):
            wyniki = []

            for liczba_narciarzy in zakres_narciarzy:
                wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
                    czasOtwarcia=28800,
                    interwalKrzeselek=15,
                    pojemnoscKrzeselka=pojemnosc,
                    liczbaWyciagow=liczba_wyciagow,
                    liczbaNarciarzy=liczba_narciarzy,
                    czasSzczytu=14400,
                    szerokoscSzczytu=7200
                )
                wyniki.append(wynik['sredni_czas_oczekiwania'] / 60)  # w minutach

            # Wykres
            plt.figure(figsize=(8, 5))
            plt.plot(zakres_narciarzy, wyniki, marker='o', color='navy')
            plt.ylim(0, max_y)
            plt.title(f"Wyciągi: {liczba_wyciagow}, Pojemność: {pojemnosc}")
            plt.xlabel("Liczba narciarzy")
            plt.ylabel("Średni czas oczekiwania [min]")
            plt.grid(True)
            plt.tight_layout()

            # Zapis
            filename = f"{katalog}/czas_w{liczba_wyciagow}_p{pojemnosc}.png"
            plt.savefig(filename)

            if pokaz_wykresy:
                plt.show()
            else:
                plt.close()

    print(f"Zapisano wszystkie wykresy w katalogu '{katalog}'.")

def analiza_zapelnienia(liczbaNarciarzy, zakres_pojemnosci, liczbaWyciagow):
    zapelnienia = []

    for pojemnosc in zakres_pojemnosci:
        wynik = Symulacja.SymulacjaWyciaguNarciarskiego(
            czasOtwarcia=28800,
            interwalKrzeselek=15,
            pojemnoscKrzeselka=pojemnosc,
            liczbaWyciagow=liczbaWyciagow,
            liczbaNarciarzy=liczbaNarciarzy,
            czasSzczytu=14400,
            szerokoscSzczytu=7200
        )

        liczba_odjazdow = wynik['odjazdy']
        suma_osob = wynik['obsluzeni']
        srednie_zapelnienie = suma_osob / (liczba_odjazdow * pojemnosc) if liczba_odjazdow > 0 else 0
        zapelnienia.append(srednie_zapelnienie)

    indeksy = list(range(len(zakres_pojemnosci)))

    plt.figure(figsize=(10, 5))
    plt.bar(indeksy, zapelnienia, color='steelblue')
    plt.axhline(1.0, color='green', linestyle='--', label='100% zapełnienia')
    plt.ylim(0, 1.1)
    plt.xticks(indeksy, zakres_pojemnosci)
    plt.xlabel("Pojemność krzesełka")
    plt.ylabel("Średni stopień zapełnienia")
    plt.title("Średnie zapełnienie krzesełek")
    plt.grid(True, axis='y')
    plt.legend()
    plt.tight_layout()
    plt.show()