from ktl.acquisition.osmnx.tram_stops import TramStopsData


def test_greater():
    TramStopsData.from_api()
    num = 100
    assert num >= 100


def test_greater_equal():
    num = 100
    assert num >= 100


def test_less():
    num = 100
    assert num < 200
