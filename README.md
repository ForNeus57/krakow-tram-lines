# krakow-tram-lines
Simulation of Kraków's Tram Lines

## Opis

krakow-tram-lines to projekt symulujący krakowską sieć tramwajową, dane zebrane zostały za pomocą następujących stron:
-   http://www.ttss.krakow.pl/
-   http://rozklady.mpk.krakow.pl/
-   https://api.ttss.pl/vehicles/trams/

Symulacja została stworzona w środowisku Godot 4, za pomocą zebranych wcześniej danych. W symulacji możemy obserwować połączenia między tramwajami, jak i tramwaje przemieszczające się po nich. Symulacja posiada kilka dodatkowych funkcjonalności:

- Możliwość nawigowania po mapie, przybliżania i oddalania.
- Możliwość podejrzenia danych tramwaju o konkretnym ID.
- Możliwość zatrzymania symulacji, przejścia do następnego kroku.
- Możliwość podglądnięcia lub schowania nazw przystanków.
- Możliwość wyświetlenia specyficznej linii tramwajowej.

## Instrukcja instalacji

### Instrukcja generacji danych

Podstawą naszego backendu jest python (**3.12**), w związku z czym stworzyliśmy paczkę `ktl`. Komenty muszą być użyte w głównym working directory projektu.

1.   Instalacja dependency pythona.
```bash
pip install -r .\requirements.txt         # Wymagane paczki wymagane do zbudowania i sprawdzenia projektu

pip install -r .\requirements_dev.txt     # Wymagane paczki do testowania paczki
```
2.   Instalacja paczki projektu
```bash
pip install -e .
```
3.   (Opcjonalne) Sprawdzenie Flake8:
```bash
flake8 .
```
4. (Opcjonalne) Sparwdzenie pylint:
```bash
pylint src
```
5.   (Opcjonalne) Sprawdzenie PyTest:
```bash
pytest .
```
6.   (Opcjonalne) Sprawdzenie całości przy pomocy tox:
```bash
tox .
```
7.   (Opcjonalne) Budowa dokumentacji:
```bash
sphinx-apidoc -o docs/source src/ktl
sphinx-build -M html docs/source/ docs/build/
```

#### Zbieranie danych

Aby zbudować wszyskie dane wejściowe modelu należy:

1.   Odpalić następujący program po zainstalowaniu paczki:
```bash
python .\src\ktl\acquisition\__main__.py -c ./res/config.json -s ./data/generated -f True 
```
gdzie:
-   [-c] to config do API i webscrapperów.
-   [-s] to folder gdzie zapisać dane.
-   [-f] to aby nadpisać ten folder jeżeli trzeba.
-   [-o] to w jakim formacie zapisać - wymagany jest mimium pickle, a excel jest do wglądu w schemat danych.

Wszyskie dane są już umieszczone w repozytorium, także w przypadku niepowodzenia w instalacji jes możliwość odtworzenia jak działał program.

Program następnie zbierze i stworzy odpowiednie dane w poodanym folderze.

#### Przetwarzanie danych

Stworzy dane dotyczące konkretnych pojezdów oraz ich rozkładów.
```bash
python ./src/ktl/aggregation/merge/tram_data_mergere.py
```

Stworzy informacje dotyczące obróbki pozycji przystanków.
```bash
python ./src/ktl/aggregation/create_json_lines.py
```

Aby wygenerować własny plik zawierający informacje o pasażerach symulacji linii tramwajowych należy

1. Uruchomić następujący program
```bash
python .\src\ktl\model\simulate_people.py 
```
Wygenerowany zostanie plik people.json na podstawie ustalonych parametrów w folderze ./data/generated/json

2. Można zwizualizować funkcję generacji programem
```bash
python .\src\ktl\model\probability.py 
```

### Instrukcja symulacji
   Projekt symulacji znajduje się w folderze src/ktl/visualisation/ktl-godot. Odpalony w środowisku Godot 4 można podejrzeć projekt od podszewki. W samym projekcie, w folderze Data znajdują się pliki json, będące kopią tych z poprzedniego kroku. Można je podmienić, jeśli ktoś chce wykorzystać inne dane. Sama aplikacja znajduje się w GITHUB REALISES. Należy pobrać całą zawartość tego folderu i odpalić element krakow-tram-line.exe.

## Autorzy
- Robert Barcik, robertbarcik32@gmail.com
- Dominik Breksa, dominikbreksa@gmail.com
- Miłosz Góralczyk, Goralczyk.Milosz2k@gmail.com
