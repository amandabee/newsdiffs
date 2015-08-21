from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup

class SFPPParser(BaseParser):
    domains = ['www.sfpublicpress.org']

    feeder_pat   = '^http://www.sfpublicpress.org/*'
    feeder_pages = ['http://sfpublicpress.org/news/searise/2015-07/major-sf-bayfront-developments-advance-despite-sea-rise-warnings'        ]


    def _parse(self, html):

            soup = bs4.BeautifulSoup(html)
            self.meta = soup.findAll('meta')
            self.title = soup.find('h1', attrs={'class':'title'}).string
            self.byline = soup.find(attrs={'class':'field-field-authors'}).text
            self.byline = re.sub('[\s]+', ' ', self.byline).strip()
            self.date = soup.find('div', attrs={'class':'date-created'}).string
            self.date = re.sub('[\s]+', ' ', self.date).strip()
            p_tags = soup.findAll('p')[2:]
            real_p_tags = [p for p in p_tags if
                         not p.findAll(attrs={'class':"twitter-follow-button"})]
            self.body = '\n'+'\n\n'.join([p.getText() for p in real_p_tags])
