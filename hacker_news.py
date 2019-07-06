import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

from operator import itemgetter

#执行API调用
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status code:', r.status_code)

#处理API调用返回的信息
story_ids = r.json()
story_dicts = []

#提前排名前38的文章，调用API返回每篇文章的信息并处理
for story_id in story_ids[0:38]:
    story_url = 'https://hacker-news.firebaseio.com/v0/item/' \
                + str(story_id) + '.json'
    story_r = requests.get(story_url)
    print(story_r.status_code)
    response_dict = story_r.json()

    story_dict = {
        'title': response_dict['title'],
        'link': response_dict['url'],
        'conments': response_dict.get('descendants', 0),
        'score': response_dict['score'],
    }
    story_dicts.append(story_dict)

story_dicts = sorted(story_dicts, key = itemgetter('conments'), reverse = True)

#可视化
my_style = LS('#662211', base_style = LCS)

my_config = pygal.Config()
my_config.show_y_guides = False
my_config.show_legend = False

chart = pygal.Bar(my_config, style = my_style)
chart.title = 'Most_Conment Stories on Hacker News'

chart.add('', story_dicts)
chart.render_to_file('hacker_news.svg')