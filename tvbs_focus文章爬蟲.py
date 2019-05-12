import requests
from bs4 import BeautifulSoup
import json

final_dic = {};
count = 320000
id_check = [];

# 起始點 「count = 0 ; range(697168, 1116259, 1)」
for i in range(1017168, 1047168, 1):
    count += 1;
    url = "https://news.tvbs.com.tw/focus/" + str(i);
    r = requests.get(url);
    content = r.text;
    soup = BeautifulSoup(content, 'html.parser');

    check = soup.find('div', class_='error_right');
    if check:
        if check.find('h1').text == '哎呀！抱歉，你訪問的頁面出現錯誤或不存在了！':
            id_check.append(i);
    else:
        content_area = soup.find('div', class_='newsdetail_content');
        if content_area:
# 標題 title
            titles = content_area.find('h1', class_='margin_b20');
            title_text = titles.text;
            title = title_text.replace('　', '_').replace('快訊／','');

 # 時間 time
            times = content_area.find('div', class_='icon_time time leftBox2');
            time_text = times.text.rstrip();
            time = time_text.replace(' ', '_');

 # 作者 author
            authors = content_area.find('h4', class_='font_color5 leftBox1');
            if authors.find('a'):
                author_text = authors.find('a').text;
                author = author_text.replace('\n', '');
            else:
                author = '';

# 內文 text
            text_area = content_area.find('div', class_='h7 margin_b20', id='news_detail_div');
            text_text = text_area.text.replace('最HOT話題在這！想跟上時事，快點我加入TVBS新聞LINE好友！', '');
            text = text_text.replace('\n', '').replace('\t', '').replace(' ', '').replace('\xa0', '');

# 關鍵字列表 keyword_list
            keyword_list = [];
            keyword_area = soup.find(attrs={"name": "news_keywords"})['content'];
            keywords = keyword_area.split(',')
            for keyword in keywords:
                keyword_list.append(keyword)

# 類別 type_list
            type = [];
# 比對 C:/news_tvbs/tvbs_type_dic.json中 dictionary的key值，得到類別(value)
            with open("C:/news_tvbs/tvbs_type_dic.json", "r") as reader:
                jf = json.loads(reader.read());
                if str(i) in jf:
                    types = jf[str(i)];
                    type.append(types);
                else:
                    id_check.append(str(i));
                

        dic = {};
        dic['title'] = title;
        dic['time'] = time;
        dic['author'] = author;
        dic['text'] = text;
        dic['url'] = url;
        dic['tags'] = keyword_list;
        dic['type_list'] = type;
        dic['source'] = 'TVBS';
        dic['views'] = '';
        dic['share'] = '';
        dic['like'] = '';
        # print(dic);

        final_key = time + '_' + author;
        final_dic[final_key] = dic;
        # print('.',end = '');
        print(count);
        
#每 10000筆輸出一次
    if count % 10000 == 0:
        with open("C:/news_tvbs/tvbs" + str(count) + ".json", "w") as fjson:
            json.dump(final_dic, fjson);
            final_dic = {};

#全部結束後輸出沒有配對到type的文章ID    
with open("C:/news_tvbs/tvbs_id_check.json", "w") as fjson2:
            json.dump(id_check, fjson2);
            id_check = [];