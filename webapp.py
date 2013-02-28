import json
from calendar import timegm
from collections import defaultdict
try:
    from urllib.parse import quote
    from urllib.request import urlopen
except:
    from urllib import quote, urlopen

import flask


app = flask.Flask(__name__)


@app.route('/')
def start():
    q = flask.request.args.get('q', '')
    keywords = q.split(',')
    series = []
    for keyword in keywords:
        url = 'http://newslibrary.naver.com/api/search/countByPeriod/json?keyword={}'.format(quote(keyword))
        data = json.loads(urlopen(url).read().decode('utf-8'))
        stats_by_year = defaultdict(int)
        units = data['result']['countUnits']
        if not units:
            continue
        for unit in units.get('countUnit', []):
            stats_by_year[int(unit['year'])] += int(unit['articleCount'])
        entry = {
            'name': keyword,
            'data': [],
        }
        for year in range(1920, 2000):
            entry['data'].append({
                'x': timegm((year, 1, 1, 0, 0, 0)),
                'y': stats_by_year[year],
            })
        series.append(entry)
    links = []
    for keyword in keywords:
        links.append((keyword, quote(json.dumps({
            'mode': 1,
            'sort': 0,
            'trans': 1,
            'pageSize': 10,
            'keyword': keyword,
            'status': 'success',
            'startIndex': 1,
            'page': 1,
            'startDate': '1920-04-01',
            'endDate': '1999-12-31',
        }))))
    return flask.render_template(
        'main.html',
        links=links,
        series=series)


@app.template_filter('urlquote')
def urlquote(string):
    return quote(string)
app.jinja_env.globals['urlquote'] = urlquote


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
