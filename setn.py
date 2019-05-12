import requests
import re
from bs4 import BeautifulSoup
import json

final_dic = {};
count = 150000
# 起始點 「count = 0 ; range(212289, 527350, 1)」
for i in range(362289, 527289, 1):
    count += 1;
    url = "https://www.setn.com/News.aspx?NewsID=" + str(i);
    r = requests.get(url);
    content = r.text;
    soup = BeautifulSoup(content, 'html.parser');

    check1 = soup.find('div',style='text-align : center;');
    check2 = soup.find('head', runat='server');
    check3 = soup.find(attrs={"name":"section"});
    if check1:
        if check1.find('img').get('src')=='/images/404.png':
            print('x');
    elif check2:
        print('x');
    elif check3 == None:
        print('x');
    else:

# 類別 style
        type = [];
        types = soup.find(attrs={"name":"section"})['content'];
        if (len(types) == 4):
            types = types[0:2];
        type.append(types);

        pattern_slide = re.compile(r'／');
# 標題 title
        title_area = soup.find('div',class_='col-lg-9 col-md-8 col-sm-12 contLeft');
        if title_area:
            titles = title_area.find('h1').text;
            title = titles.replace('　','_');
            if pattern_slide.search(title):
                title = title.split('／')[1];

# 時間 time
            times = title_area.find('time');
            for j in times:
                time = j[0:16].replace(' ','_');

# 內文 text
        pattern_report = re.compile(r'報導');
        pattern_author = re.compile(r'記者');
        pattern_first = re.compile(r'文／');
        pattern_intern = re.compile(r'（整理：實習編輯')
        pattern_star = re.compile(r'★');
        pattern_starcircle = re.compile(r'✪');
        pattern_conn = re.compile(r'https://goo.gl');

        news = '';
        slide = [];
        author = '';
        content_area = soup.find('div',id='Content1');
        if content_area:
            texts = content_area.find_all('p',style='');
            if texts:
                for text in texts:
                    text_string = text.text;
                    # 有'報導'，有'／'，則判斷有無作者
                    if pattern_report.search(text_string):
                        if pattern_slide.search(text_string):
                            slide = re.split(pattern_slide, text_string);
                            check_author = re.match(pattern_author, slide[0]);
                            if check_author:
                                authors = re.split(pattern_author, slide[0]);
                                author = authors[1];
                            continue;
                    if pattern_first.search(text.text[0:10]):
                        continue;
                    if text_string[0:5].__contains__('【'):
                        if text_string.__contains__('】'):
                            text_string = text_string.split('】');
                            text_string = text_string[1];
                        else:
                            continue;
                    if text_string[0:5].__contains__('（'):
                        if text_string.__contains__('）'):
                            text_string = text_string.split('）',1);
                            text_string = text_string[1];
                        else:
                            continue;
                    if pattern_intern.search(text_string):
                        text_string = re.split(pattern_intern, text_string);
                        text_string = text_string[0];
                    if pattern_star.search(text_string):
                        text_string = re.split(pattern_star, text_string);
                        text_string = text_string[0];
                    if pattern_starcircle.search(text_string):
                        text_string = re.split(pattern_starcircle, text_string)[0];
                    if text_string.__contains__('▲'):
                        text_string = text_string.split('▲');
                        text_string = text_string[0];
                    if text_string.__contains__('▼'):
                        text_string = text_string.split('▼');
                        text_string = text_string[0];
                    if pattern_conn.search(text_string):
                        if text_string.__contains__('影片連結'):
                            text_string = text_string.split('影片連結');
                            text_string = text_string[0];
                        if text_string.__contains__('《'):
                            text_string = text_string.split('《');
                            text_string = text_string[0];
                        if text_string.__contains__('☞'):
                            text_string = text_string.split('☞');
                            text_string = text_string[0];
                    news = news + text_string;

# 關鍵字 keyword
        tags=[];
        keyword_area = soup.find('div',class_='keyword page-keyword-area');
        keywords = keyword_area.findAll('a',class_='gt');
        for keyword in keywords:
            if keyword:
                kw = keyword.find('strong');
                tags.append(kw.text);

# 塞進字典
        dic={};
        dic['title'] = title;
        dic['time'] = time;
        dic['author'] = author;
        dic['text'] = news;
        dic['url'] = url;
        dic['tags'] = tags;
        dic['type_list'] = type;
        dic['source'] = '三立';
        dic['views'] = '';
        dic['share'] = '';
        dic['like'] = '';

        final_key = time + '_' + author;
        final_dic[final_key] = dic;
        # print('.',end = '');
        print(count);

    if count % 10000 == 0:
        with open("D:/news/setn" + str(count) + ".json", "w") as fjson:
            json.dump(final_dic, fjson);
            final_dic = {};

# 影印區
# print('title:' + title);
# print('time:' + time.text[0:10]+'_'+time.text[11:16]);
# print('author:' + author);
# print('text:' + news);
# print('url:' + url);
# print('tags:' + tags);
# print('source:' + '三立')
# print('type:' + type);
# print('views:');
# print('share:');
# print('like:');



