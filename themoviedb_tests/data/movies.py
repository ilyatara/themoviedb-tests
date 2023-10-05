import datetime
from dataclasses import dataclass


@dataclass
class Movie:
    id: int
    title: str
    original_language: str
    overview: str
    release_date: datetime.date

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, value):
        self._release_date = value.strftime('%Y-%m-%d')


fight_club = Movie(
    id=550,
    title='Fight Club',
    original_language='en',
    overview='A ticking-time-bomb insomniac and a slippery soap salesman channel '
             'primal male aggression into a shocking new form of therapy. Their '
             'concept catches on, with underground \"fight clubs\" forming in every '
             'town, until an eccentric gets in the way and ignites an out-of-control '
             'spiral toward oblivion.',
    release_date=datetime.date(1999, 10, 15)
)
