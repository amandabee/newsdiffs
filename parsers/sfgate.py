from baseparser import BaseParser
import bs4
import re


class SFGateParser(BaseParser):
    '''
    Look for links matching the "feeder_pat" regular expression
    on any feeder_pages
    '''
    domains = ['www.sfgate.com']

    feeder_pat = '^http://www.sfgate.com/bayarea'
    feeder_pages = ['http://www.sfgate.com/bayarea/']

    def _parse(self, html):
        soup = bs4.BeautifulSoup(html)
        self.meta = soup.findAll('meta')
        elt = soup.find('h1', attrs={'class': 'headline'})
        if elt is None:
            self.real_article = False
            return
        self.title = elt.getText()
        try:
            self.byline = soup.find(attrs={'class': 'byline'}).text
            self.byline = re.sub('[\s]+', ' ', self.byline).strip()
        except:
            self.byline = ""
        self.date = soup.find('h5', attrs={'class': 'timestamp'}).string
        self.date = re.sub('[\s]+', ' ', self.date).strip()
        p_tags = soup.findAll('p')[2:]
        real_p_tags = [p for p in p_tags if
                       not p.findAll(attrs={'class': "twitter-follow-button"})]
        self.body = '\n'+'\n\n'.join([p.getText() for p in real_p_tags])
