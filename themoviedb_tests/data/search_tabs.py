import enum


class SearchTabs(enum.Enum):
    movies = {'css_id': '#movie', 'tab_name': 'Movies'}
    tv_shows = {'css_id': '#tv', 'tab_name': 'TV Shows'}
    people = {'css_id': '#person', 'tab_name': 'People'}
    collections = {'css_id': '#collection', 'tab_name': 'Collections'}
    companies = {'css_id': '#company', 'tab_name': 'Companies'}
    keywords = {'css_id': '#keyword', 'tab_name': 'Keywords'}
    networks = {'css_id': '#network', 'tab_name': 'Networks'}

    def __init__(self, vals):
        self.css_id = vals['css_id']
        self.tab_name = vals['tab_name']

    def get_no_results_text(self):
        if self.tab_name == 'TV Shows':
            text = 'TV shows'
        else:
            text = self.tab_name.lower()
        return f'There are no {text} that matched your query.'
