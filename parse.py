import argparse
import sys
import urllib2
from bs4 import BeautifulSoup
import bs4

class Contestent(object):
    def __init__(self, name, party, votes):
        self.name = name
        self.party = party
        self.votes = int(votes)

    def __str__(self):
        return '''{name: '%s', party: '%s', votes: %s}''' % (self.name, self.party, self.votes)

    def __repr__(self):
        return self.__str__()

class Constituency(object):
    def __init__(self, url, name, done, contestents):
        self.url = url
        self.name = name
        self.done = done
        self.contestents = contestents

    def __str__(self):
        return '''{url: '%s', name: '%s', result_status: %s, contestents: %s}''' % (self.url, self.name, str(self.done).lower(), self.contestents)

    def __repr__(self):
        return self.__str__()

def parse_constituency(url):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    result_table = soup.find('div', attrs = {'id':'div1'}).contents[1].contents
    constituency = result_table.pop(0).find('td').text
    done = 'Counting In Progress' not in str(result_table.pop(0).text)
    try:
        result_table.pop(0) # table title: Candidate | Party | Votes
        contestents = []
        for row in result_table:
            if type(row) is bs4.element.NavigableString:
                continue
            details = row.find_all('td')
            contestents.append(Contestent(details[0].text, details[1].text, details[2].text))
        return Constituency(url, constituency, done, contestents)
    except:
        return Constituency(url, constituency, done, [])

def get_all_constituency():
    for i in xrange(1, 224):
        yield parse_constituency("http://eciresults.nic.in/ConstituencywiseS10{0}.htm?ac={0}".format(i))

def print_all():
    for c in get_all_constituency():
        if len(c.contestents) > 2:
            print ('%s %s %s %d %d' % (c.name, c.contestents[0].name, c.contestents[0].party, c.contestents[0].votes, c.contestents[0].votes - c.contestents[1].votes))

def print_inprogress():
    for c in get_all_constituency():
        if not c.done and len(c.contestents) > 2:
            print ('%s %s %s %d %d' % (c.name, c.contestents[0].name, c.contestents[0].party, c.contestents[0].votes, c.contestents[0].votes - c.contestents[1].votes))

def print_winners():
    for c in get_all_constituency():
        if c.done and len(c.contestents) > 2:
            print ('%s %s %s %d %d' % (c.name, c.contestents[0].name, c.contestents[0].party, c.contestents[0].votes, c.contestents[0].votes - c.contestents[1].votes))

def main():
    parser = argparse.ArgumentParser(prog='parser', description='Scrap results from ECI official website, use grep to filter further', )
    parser.add_argument('--winner', '-w', action='store_true', help='shows result declared constituencies with candidate info')
    parser.add_argument('--inprogress', '-p', action='store_true', help='shows counting inprogress constituencies')
    parser.add_argument('--all', '-a', action='store_true', help='show all')
    args = parser.parse_args()
    if args.winner:
        print_winners()
    elif args.inprogress:
        print_inprogress()
    else:
        print_all()

    # print "["
    # for c in get_all_constituency():
    #     print (str(c) + ",")
    # print "]"


if __name__ == '__main__':
    sys.exit(main())

