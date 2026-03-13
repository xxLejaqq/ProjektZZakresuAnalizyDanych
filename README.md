# Happiness Prediction Project

Projekt z zakresu analizy danych dotyczący predykcji poziomu szczęścia w poszczególnych krajach.

[Link do raportu](https://htmlpreview.github.io/?https://raw.githubusercontent.com/xxLejaqq/ProjektZZakresuAnalizyDanych/refs/heads/main/Happiness_Prediction_Report.html)

## Spis treści

1. [Cel projektu](#1-cel-projektu)
2. [Charakterystyka zbioru danych](#2-charakterystyka-zbioru-danych)
3. [Czyszczenie danych](#3-czyszczenie-danych)
4. [Pytania badawcze i hipotezy](#4-pytania-badawcze-i-hipotezy)
5. [Eksploracyjna analiza danych (EDA)](#5-eksploracyjna-analiza-danych-eda)
6. [Tworzenie modeli uczenia maszynowego](#6-tworzenie-modeli-uczenia-maszynowego)
7. [Porównanie i omówienie wyników modeli](#7-porównanie-i-omówienie-wyników-modeli)
8. [Analiza SHAP dla najlepszego modelu](#8-analiza-shap-dla-najlepszego-modelu)
9. [Aplikacja](#9-aplikacja)
10. [Podsumowanie](#10-podsumowanie)

---

## 1. Cel projektu

Głównym celem badania jest opracowanie modelu uczenia maszynowego służącego do predykcji poziomu szczęścia w poszczególnych krajach na podstawie wskaźników ekonomicznych, społecznych oraz regionalnych. Dodatkowy cel stanowi weryfikacja postawionych w toku pracy pytań oraz hipotez badawczych.

---

## 2. Charakterystyka zbioru danych

### Źródło danych

Dane zostały zaczerpnięte z platformy Kaggle. Wykorzystany zbiór zawiera zestawienie wyników z lat 2015–2024, dla większości państw świata. Wyjątek stanowią kraje, dla których dane nie były dostępne.

Oryginalnie dane pochodzą ze Światowego Raportu Szczęścia (World Happiness Report) - oficjalnego, globalnego, rankingu szczęścia, publikowanego corocznie przy wsparciu ONZ.

### Opis danych

| Zmienna | Znaczenie |
|---------|-----------|
| Ranking | Zmienna porządkowa wskazująca pozycję kraju w globalnym zestawieniu szczęścia |
| Happiness score | Wartość szczęścia [wyznaczana na podstawie ankiet] |
| GDP per capita | Produkt krajowy brutto na mieszkańca skorygowany o parytet siły nabywczej |
| Social support | Poziom wsparcia społecznego [średnia z odpowiedzi binarnych w ankietach] |
| Healthy life expectancy | Średnia oczekiwana długość życia w zdrowiu |
| Freedom to make life choices | Postrzegana swoboda podejmowania ważnych decyzji życiowych |
| Generosity | Poziom hojności na podstawie ankiet, skorygowany o PKB |
| Perceptions of corruption | Postrzegana korupcja w sektorze rządowym i biznesowym |
| Year | Rok obserwacji |
| Country | Nazwa kraju |
| Regional indicator | Region geograficzny |

---

## 3. Czyszczenie danych

### Nadanie odpowiednich typów

Zmienne ilościowe zostały wczytane jako typ `object` z powodu występowania przecinków w danych. Wykonano konwersję na typ `float`.

### Oczyszczenie danych z błędów grubych

Podczas eksploracyjnej analizy danych zidentyfikowano błędy grube występowające w latach 2015-2018 w kolumnie GDP per Capita. Podjęto decyzję o ograniczeniu analizowanego zbioru do lat 2019-2024.

### Ujednolicenia klasyfikacji regionalnej

Naprawiono niespójności w kolumnie Region indicator, wykorzystując bibliotekę `country_converter` do wygenerowania poprawnych regionów.

### Odrzucenie zbędnych kolumn

Odrzucono kolumnę 'Ranking', która powiela informacje z kolumny 'Happiness score'.

---

## 4. Pytania badawcze i hipotezy

### Pytania:

1. Czy możliwe jest na podstawie zaledwie kilku zmiennych określić poziom szczęścia w danym państwie?
2. Czy pandemia COVID-19 negatywnie wpłynęła na poziom szczęścia?

### Hipotezy:

1. **Zamożność społeczeństwa**, wyrażona przez PKB na mieszkańca, stanowi jeden z najsilniejszych predyktorów poziomu szczęścia
2. **Hojność** jest najsłabszym predyktorem szczęścia

---

## 5. Eksploracyjna analiza danych (EDA)

### Analiza korelacji

Na podstawie macierzy korelacji Pearsona wyciągnięto następujące wnioski:

- **Główne filary szczęścia**: GDP per capita oraz Social support mają najsilniejszy, pozytywny związek z Happiness score
- **Istotny wpływ**: Healthy life expectancy oraz Freedom to make life choices
- **Brak liniowej zależności**: Generosity oraz Perceptions of corruption nie wykazują wyraźnej liniowej zależności

### Analiza trendu

Analiza trendu globalnego poziomu szczęścia w latach 2019–2024 wskazuje na stabilność tego wskaźnika. Okres pandemii COVID-19 nie spowodował załamania trendu.

### Weryfikacja hipotezy o wpływie pandemii

Test ANOVA potwierdził brak istotnych różnic w Happiness score między latami (p-wartość = 0.858).

### Analiza regionalna

Wyróżniono 3 grupy regionów:
- **Liderzy**: Europa Północna, Europa Zachodnia, Ameryka Północna, Australia i Nowa Zelandia
- **Grupa umiarkowana**: Pozostałe regiony Europy, Ameryki i większość Azji
- **Najniższe wskaźniki**: Wszystkie regiony Afryki oraz Azja Południowa

---

## 6. Tworzenie modeli uczenia maszynowego

Zaimplementowano następujące algorytmy:

| Model | Opis |
|-------|------|
| Linear Regression | Regresja liniowa - wyznaczanie liniowej relacji między cechami a zmienną celu |
| SVR | Regresja Wektorów Nośnych - wyznaczenie hiperpłaszczyzny w marginesie tolerancji |
| Decision Tree | Drzewo decyzyjne - podział przestrzeni danych na spójne obszary |
| Random Forest | Las losowy - agregacja wyników wielu drzew |
| XGBoost | Wzmacnianie gradientowe - sekencyjna optymalizacja błędów |
| MLP | Sieć neuronowa typu Multi-Layer Perceptron |

### Transformacje danych

W ramach pipeline zastosowano następujące transformacje:
- Podniesienie do kwadratu: Social support, Freedom to make life choices
- Pierwiastkowanie: Generosity
- Zamiana na zmienną binarną: Perceptions of corruption

---

## 7. Porównanie i omówienie wyników modeli

| Model | Train R² | Test R² | Test RMSE | Test MAE |
|-------|----------|---------|-----------|----------|
| **XGBoost** | 0.9998 | **0.9177** | 0.3631 | 0.2684 |
| Random Forest | 0.9854 | 0.9172 | 0.3642 | 0.2747 |
| SVM | 0.9346 | 0.9012 | 0.3978 | 0.2852 |
| Linear Regression | 0.8490 | 0.8619 | 0.4703 | 0.3504 |
| MLP | 0.8833 | 0.8493 | 0.4914 | 0.3689 |
| DecisionTree | 0.9063 | 0.8384 | 0.5088 | 0.3825 |

### Wnioski

- **Najlepszy model**: XGBoost wyjaśnia ponad 91% wariancji na zbiorze testowym
- **Stabilność regresji liniowej**: Osiągnęła 85% wariancji, co dowodzi liniowej struktury zależności
- Wyniki pozwalają twierdząco odpowiedzieć na postawione pytanie badawcze

---

## 8. Analiza SHAP dla najlepszego modelu

Weryfikacja hipotez za pomocą analizy SHAP:

### Hipoteza 1: PKB jako najsilniejszy predyktor
✅ **Potwierdzona** - GDP per capita ma największy wpływ na predykcję

### Hipoteza 2: Hojność jako najsłabszy predyktor
❌ **Obalona** - zmienna Generosity uplasowała się w środkowej części rankingu, wykazując silniejszy wpływ niż oczekiwana długość życia czy postrzeganie korupcji

### Dodatkowe obserwacje:
- Region ma istotny wpływ na predykcję
- Perceptions of corruption jest najsłabszym predyktorem
- Healthy life expectancy wykazuje zaskakująco niewielki wpływ

---

## 9. Aplikacja

Zapisan model: `XGBoost_happines`

Stworzono interaktywną aplikację do weryfikacji hipotez oraz testowania modelu dla dowolnych danych wejściowych.

---

## 10. Podsumowanie

### Główne osiągnięcia:

1. **Osiągnięto główny cel projektu**: Model XGBoost wyjaśnia ponad 91% wariancji na zbiorze testowym

2. **Weryfikacja hipotez**:
   - ✅ PKB jest najsilniejszym predyktorem szczęścia
   - ❌ Hojność NIE jest najsłabszym predyktorem (jest nim Perceptions of corruption)
   - ✅ Pandemia COVID-19 nie miała istotnego negatywnego wpływu na globalny poziom szczęścia
   - ✅ Można z wysoką dokładnością przewidzieć poziom szczęścia na podstawie kilku zmiennych

---

## Autorzy

Maja Djan Darczuk, Jan Walkiewicz

---

## Technologie

- Python
- pandas, numpy
- scikit-learn
- XGBoost
- TensorFlow / Keras
- KerasTuner
- SHAP
- Plotly
- Matplotlib / Seaborn
- Country Converter

## Wymagania

```
pandas
numpy
scipy
matplotlib
seaborn
plotly
tensorflow
keras-tuner
country-converter
scikit-learn
xgboost
shap
joblib
```
