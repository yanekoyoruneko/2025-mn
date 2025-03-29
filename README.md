# Analiza wskażnika MACD
# Jan Wiśniewski

## Wstęp

### **EMA**
Wartość EMA dla $i$-tego przedziału czasu można obliczyć rekurencyjnie za pomocą zależności:

$$
EMA_N = \frac{p_0 + (1 - \alpha) p_1 + (1 - \alpha)^2 p_2 + \dots + (1 - \alpha)^N p_N}
{1 + (1 - \alpha) + (1 - \alpha)^2 + \dots + (1 - \alpha)^N}
$$

gdzie:

- $p_i$ jest próbką z i-tego dnia, $p_0$ jest próbką z aktualnego dnia, $p_N$ - to próbka sprzed
$N$ dni.
- liczba okresów: $N$,
- współczynnik wygładzający: $\alpha = \frac{2}{N + 1}$.

### **MACD**
Wskaźnik **MACD** (Moving Average Convergence Divergence) to popularne narzędzie analizy technicznej stosowane w tradingu, które służy do identyfikacji zmian momentum na rynku. Składa się z trzech głównych elementów:

1. **Linia MACD** – różnica między krótkoterminową (zwykle 12-okresową) i długoterminową (zwykle 26-okresową) średnią kroczącą.
2. **Linia sygnałowa** – wygładzona średnia krocząca (zwykle 9-okresowa) linii MACD.
3. **Histogram MACD** – różnica między linią MACD a linią sygnałową, która wizualizuje siłę i kierunek trendu.

### Wejście

Wejście składa się z dwóch zestawów danych: **acp_d** które zawierają historyczne notowania odpowiednich instrumentów finansowych.

### **Struktura wejścia:**

Każdy zbiór danych to tabela, w której każda kolumna reprezentuje określoną cechę notowań giełdowych.

- **Data** – data notowania.
- **Cena zamknięcia** – wartość akcji na koniec dnia.

## Analiza MACD w pomocy przy kupnie sprzedaży

---

![acp_d.csv-macd.png](acp_d.csv1000-macd.png)

Pierwszy wykres przedstawia notowania akcji firmy Asseco Poland w całym badanym
okresie. Spadek jest zauważalny w 2021 spowodowany pandemią oraz 2023.
Duży wzrost można zauważyć zaczynając od początku stycznia 2024 były to skutki
[solidnych wyników](https://pl.asseco.com/aktualnosci/asseco-z-dobrymi-wynikami-po-trzech-kwartalach-2024-roku-i-solidnym-portfelem-zamowien-na-caly-biezacy-rok-5417?utm_source=chatgpt.com)
finansowych spółki oraz rosnący portfel zamówień.

Dolny wykres przedstawia wskaźnik MACD (Moving Average Convergence Divergence) dla akcji Asseco Poland w analizowanym okresie.

Kluczowe momenty:

- 2021-07-2022-01: Wystąpił bearish cross, gdy
  linia MACD przecięła linię sygnałową od góry, co zwiastowało spadek cen.

- 2022-07-2023-01: Odnotowano bullish cross, czyli
  przecięcie linii MACD od dołu, sygnalizujące potencjalny wzrost wartości
  akcji.

- 2024-01-2025-01: Wskaźnik MACD pozostaje w trendzie wzrostowym, co
  potwierdza silną pozycję spółki, wspieraną przez dobre wyniki finansowe i
  rosnący portfel zamówień.

Wykres MACD uzupełnia analizę cen akcji, pokazując momenty zmiany trendu oraz siłę ruchów cenowych.

![acp_d.csv100-macd.png](acp_d.csv100-macd.png "Okres spadku")

### **Opis okresu spadku (2021-09 – 2022-03)**

1. **Wartość kapitału (wykres górny)**
   - W okresie od **września 2021 do marca 2022** widoczny jest **spadek wartości portfela** z około **77 500 zł do 67 500 zł**, co oznacza stratę na poziomie **~13%**.
   - Największe spadki występują w **listopadzie 2021** oraz **styczniu–lutym 2022**, co może być związane z ogólną niepewnością rynkową (np. inflacja, zmiany stóp procentowych).

2. **Analiza wskaźnika MACD (wykres dolny)**
   - **2021-10 – 2021-11:** Wystąpiło **bearish cross** (skrzyżowanie niedźwiedzie), gdy linia MACD przecięła linię sygnałową **od góry**, co było wczesnym sygnałem do sprzedaży.
   - **2022-01 – 2022-02:** Kolejne przecięcie w dół (**bearish cross**) potwierdziło kontynuację trendu spadkowego.
   - W tym okresie **brak wyraźnych sygnałów kupna** (bullish cross), co wskazuje na **słabość rynku**.

---

### **Ocena przydatności MACD w podejmowaniu decyzji**

#### **Transakcja 1: Sprzedaż po bearish cross (2021-10)**
- **Sygnał:** Bearish cross (MACD przecina SIGNAL od góry).
- **Akcja:** Sprzedaż akcji na początku listopada 2021.
- **Wynik:** Uniknięcie dalszych spadków – gdyby inwestor trzymał akcje do marca 2022, strata wyniosłaby **~13%**.

#### **Transakcja 2: Brak sygnału kupna (2022-01 – 2022-03)**
- **Sygnał:** Brak bullish cross (MACD pozostaje poniżej SIGNAL).
- **Interpretacja:** Wskaźnik prawidłowo **nie generował fałszywych sygnałów kupna**, co potwierdzało trend spadkowy.

#### **Podsumowanie skuteczności MACD**
- **Zalety:**
  - Wykrył **początek trendu spadkowego** (bearish cross w 2021-10).
  - Uniknął **fałszywych sygnałów kupna** w trakcie spadków.
- **Wady:**
  - Nie wskazał **optymalnego momentu wyjścia** (np. odbicia w marcu 2022), ponieważ MACD reaguje z opóźnieniem.
- **Wniosek:** MACD jest **przydatny jako filtr trendu**, ale powinien być używany z innymi wskaźnikami (np. RSI, wolumen) dla lepszej precyzji.


## Symulacja

Program został opracowany w celu automatycznego podejmowania decyzji o kupnie lub sprzedaży instrumentu finansowego na podstawie sygnałów generowanych przez wskaźnik **MACD**

- Przecięcie od dołu – sygnał kupna aktywa,
- Przecięcie od góry – sygnał sprzedaży aktywa

Symulacja została przeprowadzona z kapitałem początkowym wynoszącym 1000 jednostek instrumentu finansowego. Analizowany okres wynosi 150 ostatnich dni z zawartych danych. Analiza obejmuje zmiany wartości portfela inwestycyjnego oraz skuteczność transakcji.

### Wyniki Symulacji dla acp_d
- **Analizowany okres**: od 2024-07-23 do 2025-02-28
- **Kapitał początkowy:** 1000 jednostek
- **Kapitał końcowy:** 135526.42 jednostek
- **Liczba transakcji:** 4 (2 kupna, 2 sprzedaże)

#### Analiza Transakcji dla symulacji acp_d
1. **SELL 2024-10-29**: Sprzedano instrumenty za 89750.0 PLN jednostek po cenie 89.75.
2. **BUY 2024-11-26**: Zakupiono 1044.21 jednostek za 85.95 jednostek każda.
	- Wzrot 4%
3. **SELL 2024-12-16**: Sprzedano instrumenty za 96955.06 PLN jednostek po cenie 92.85.
	- Wzrot 12%
4. **BUY 2025-01-20**: Zakupiono 1003.16 jednostek za 96.65 jednostek każda.
	- Wzrot 1%
5. **SELL 2025-02-20**: Sprzedano instrumenty za 135526.42 PLN jednostek po cenie 135.1.
	- Wzrot 23%

Końcowo: 53%

---

### Wyniki Symulacji dla wig20_d
- **Analizowany okres**: od 2024-08-07 do 2025-03-17
- **Kapitał początkowy:** 1000 jednostek
- **Kapitał końcowy:** 2386334.55 jednostek
- **Liczba transakcji:** 7 (4 kupna, 3 sprzedaże)

#### Analiza Transakcji dla symulacji wig20_d
1. **SELL 2024-11-15**: Sprzedano instrumenty za 2188750.0 jednostek po cenie 2188.75.
2. **BUY 2024-11-25**: Zakupiono 993.64 jednostek za 2202.76 jednostek każda.
	- Wzrot 1%
3. **SELL 2024-12-17**: Sprzedano instrumenty za 2197821.93 jednostek po cenie 2211.89.
	- Wzrot 2%
4. **BUY 2025-01-09**: Zakupiono 977.70 jednostek za 2247.94 jednostek każda.
p	- Wzrot 1%
5. **SELL 2025-02-05**: Sprzedano instrumenty za 2341329.46 jednostek po cenie 2394.72.
	- Wzrot 13%
6. **BUY 2025-02-10**: Zakupiono 933.72 jednostek za 2507.54 jednostek każda.
	- Wzrot 3%
7. **SELL 2025-02-24**: Sprzedano instrumenty za 2386334.55 jednostek po cenie 2555.74.
	- Wzrot 5%
8. **BUY 2025-03-13**: Zakupiono 889.41 jednostek za 2683.05 jednostek każda.
	- Wzrot 2%

Końcowo: 17%

---

### Wykresy
- **Wartość Portfela:** Wykres ilustruje wzrost wartości portfela inwestycyjnego po każdej transakcji, osiągając końcową wartość 135526.42 jednostek dla **acp_d** i 2386334.55 jednostek dla **wig20_d**.
- **MACD:** Wykres pokazuje sygnały kupna i sprzedaży na podstawie przecięcia linii MACD i Signal Line.

![acp_d.csv-capital.png](acp_d.csv-capital.png)
![wig20_d.csv-capital.png](wig20_d.csv-capital.png)

---

### Skuteczność Transakcji
- **Transakcje z zyskiem:** Wszystkie transakcje zakończyły się zyskiem, co wskazuje na wysoką skuteczność zastosowania wskaźnika **MACD** w tym przypadku.
- **Skuteczność MACD:** Wskaźnik **MACD** okazał się skuteczny w generowaniu sygnałów kupna i sprzedaży, prowadząc do znaczącego wzrostu kapitału.

---

### Wnioski
Program oparty na wskaźniku MACD wykazał wysoką skuteczność w automatycznym handlu, prowadząc do znacznego wzrostu kapitału inwestycyjnego. Wszystkie transakcje zakończyły się zyskiem, co potwierdza przydatność MACD w podejmowaniu decyzji inwestycyjnych. Jednak należy pamiętać, że MACD najlepiej sprawdza się w trendowych warunkach rynkowych. W sytuacjach dynamicznych zmian cen lub na rynkach o dużej zmienności może generować mylne sygnały, prowadząc do nietrafionych decyzji inwestycyjnych. Warto również zauważyć, że dane użyte w analizie były zgodne z dominującym trendem, co mogło dodatkowo wpłynąć na wysoką skuteczność strategii. Trend jest potwierdzony biorąc pod uwage szerszą perspektywe dla wykresu z 2000 dni. Lącznie MACD przyniósł zysk w przeważającej liczbie tranzakcji.

---

### Zalecenia
- **Dalsze testy:** Warto przeprowadzić dodatkowe testy na różnych zestawach danych, aby zweryfikować skuteczność strategii w różnych warunkach rynkowych.
- **Optymalizacja:** Można rozważyć optymalizację parametrów **MACD**, aby dostosować strategię do specyfiki danego instrumentu finansowego.

---

### Pliki
Wykres wartości portfela oraz wskaźnika **MACD** dla **acp_d** okresu 150 oraz 2000 dni.

- **acp_d.csv-capital.png**
- **acp_d.csv-macd.png**
- **acp_d2000.csv-capital.png**
- **acp_d2000.csv-macd.png**

Wykres wartości portfela oraz wskaźnika **MACD** dla **wig20_d** okresu 150 oraz 2000 dni.

- **wig20_d.csv-capital.png**
- **wig20_d.csv-macd.png**
- **wig20_d2000.csv-capital.png**
- **wig20_d2000.csv-macd.png**

---
