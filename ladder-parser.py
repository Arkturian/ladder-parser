def get_html_pages(urls):
    import requests
    html_pages =  [ requests.get(url) for url in urls ]
    return html_pages

def get_html_pages_async(urls):
    import grequests
    responses  = [ grequests.get(url) for url in urls ]
    html_pages = grequests.map(responses)
    return html_pages

def parse_html_tables(html_pages):
    from lxml import html
    trees  = ( html.fromstring(page.text) for page in html_pages )
    tables = [ tree.xpath('.//table[@class="StyledTable"]')[0] for tree in trees ]
    # from itertools import chain
    return tables

def parse_ladder(html_tables):

    ranks, levels, races, names, xp, wins, losses = (  [] for _ in xrange(7)  )

    p_ranks  = './/tr/td[position() = 1]/text()'
    p_levels = './/tr/td[position() = 2]/div/div[@class="level_number"]/text()'
    p_races  = './/tr/td[position() = 4]/div[@class="PlayerWithIcon"]/@style'
    p_names  = './/tr/td[position() = 4]/div/a/text()'
    p_xp     = './/tr/td[position() = 5]/text()'
    p_wins   = './/tr/td[position() = 6]/text()'
    p_losses = './/tr/td[position() = 7]/text()'

    for tree in html_tables:
        ranks .extend( ( int(i) for i in tree.xpath(p_ranks ) ) )
        levels.extend( ( int(i) for i in tree.xpath(p_levels) ) )
        races .extend( ( s[-9]  for s in tree.xpath(p_races ) ) )
        names .extend(                   tree.xpath(p_names )   )
        xp    .extend( ( int(i) for i in tree.xpath(p_xp    ) ) )
        wins  .extend( ( int(i) for i in tree.xpath(p_wins  ) ) )
        losses.extend( ( int(i) for i in tree.xpath(p_losses) ) )

    # from itertools import izip
    ladder = zip(ranks, levels, races, names, xp, wins, losses)
   
    return ladder

def get_current_time_string():
    from datetime import datetime
    return datetime.utcnow().strftime("%Y-%m-%d--%H-%M")

def save_to_json(data, file):
    import json
    json.dump(data, file)

def main():

    url  = 'http://tft.w3arena.net/ladder?lc=100&lp=%s'
    urls = ( url % i for i in xrange(1,11) )

    html_pages  = get_html_pages_async(urls)
    html_tables = parse_html_tables(html_pages)
    ladder      = parse_ladder(html_tables)

    titles = ('rank', 'level', 'race', 'player', 'xp', 'wins', 'losses')    
    time   = get_current_time_string()    

    final_result = {'time': time, 'titles': titles, 'data': ladder}
    
    filename = 'ladder--' + time + '.json'
    filename = './db/' + filename

    with open(filename, 'w') as f:
        save_to_json(final_result, f)

if __name__ == '__main__':
    main()

# tree.findall('.//table')[1]
# tree.xpath('//table[@class="StyledTable"]')

# len(table.xpath('.//tr'))
