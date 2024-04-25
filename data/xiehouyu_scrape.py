import json
from os.path import exists

import requests
from bs4 import BeautifulSoup
import os
import logging

BASE_URL = f'http://xhy.5156edu.com/html2/xhy'
# 新建结果目录 results
RESULT_DIR = 'xiehouyu_results'
exists(RESULT_DIR) or os.makedirs(RESULT_DIR)
# 存储最终答案数列
details = []

# 爬取相应页面的html代码
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        # 启用 SSL 证书验证
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)
        return []

def parse_detail(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tr_elements = soup.find_all(lambda tag: tag.name == 'tr' and tag.get('bgcolor') == '#ffffff')
        for tr_tag in tr_elements:
            td_tags = tr_tag.find_all(lambda tag: tag.name == 'td')
            if len(td_tags) > 1:
                first_td_tag = td_tags[0]
                second_td_tag = td_tags[1]
                single_xiehouyu = {  # 在每次迭代时创建新的字典
                    'system': '你是一个歇后语小助手',
                    'input': first_td_tag.text,
                    'output': second_td_tag.text
                }
                temp = {
                    "conversation": [
                        single_xiehouyu
                    ]
                }
                details.append(temp)
        return details
    except Exception as e:
        print("获取歇后语数据失败:", e)

def save_data(data):
    data_path = f'{RESULT_DIR}/xiehouyu_xtuner.jsonl'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def main(page):
    if page != 1:
        url = BASE_URL + '_' + str(page) + '.html'
    else:
        url = BASE_URL + '.html'
    print('Scraping：' + url)
    detail_html = scrape_page(url)
    data = parse_detail(detail_html)
    logging.info('get detail data %s', data)
    logging.info('saving data to json data')
    save_data(data)
    logging.info('data saved successfully')

if __name__ == "__main__":
    # 获取歇后语数据
    pages = range(1, 282)
    for page in pages:
        main(page)
    print('抓取完毕')