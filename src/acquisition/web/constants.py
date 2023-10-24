from pathlib import Path

URL_TRAM_MODELS = r'https://api.ttss.pl/vehicles/trams/'
DEFAULT_TRAM_MODELS_SAVE_PATH = Path('./data/generated/data/')

URL_TRAM_TIME_TABLE = r'./cache/Rozkłady jazdy Miejskie Przedsiębiorstwo Komunikacyjne S.A. w Krakowie.html'  # r'https://rozklady.mpk.krakow.pl/?lang=PL&rozklad=20231021&linia='

TRAM_NAME_LENGTH = 5

PARSER_REGEX = r'''
<table style=" vertical-align: top; ">
    <tbody>
        <tr>
            <td style=" white-space: nowrap; ">
                Przystanki
            </td>
        </tr>
    </tbody>
</table>
'''