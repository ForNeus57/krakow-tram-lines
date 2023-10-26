from pathlib import Path

URL_TRAM_MODELS = r'https://api.ttss.pl/vehicles/trams/'
DEFAULT_EXCEL_INPUT_PATH = Path('data/Tramwaje_dane_modeli.xlsx')

URL_TRAM_TIME_TABLE = "https://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20231021&linia=1__1__1"

TRAM_NAME_LENGTH = 5

PARSER_REGEX_TRAM_STOPS = r'''<table style=" vertical-align: top; ">\s*
    <tbody>\s*
        <tr>\s*
            <td style=" white-space: nowrap; ">\s*
                Przystanki
            </td>\s*
        </tr>\s*
        <tr>.*
        </tr>
    </tbody>
</table>
'''

