import requests
import re
from grab import Grab

#request_page = requests.post('https://yandex.ru/search/', data={'text':'Автомобиль', 'lr':'50', 'rnd':'86478'});
#request_page = requests.post('https://yandex.ru/search/', data={'text':'auto'})

# ---------------- Метод для получения ссылок со страницы ----------------
def get_links_list(html_page):
    links_list = []
    result = re.findall(r'<a\s[a-zA-Z0-9].[^<>]*>.[^<>]*</a>', req_text) # Ищем все теги <a></a>
    next_page_url = ''

    print('----> info: ')

    for key in result:
        url = re.search(r'href="[a-zA-Z0-9?&;%@=//:._-]+"*', key)
        text = re.search(r'>.[^<>]*<', key)

        formated_url = re.sub('href=["]+', '', url.group(0))  # Ссылка на сайт
        formated_url = re.sub('["]+', '', formated_url);
        formated_text = re.sub('[><]+', '', text.group(0))

        next_page = re.search('дальше', formated_text)
        word = re.search('[a-zA-Z]+', formated_text)

        if (next_page and not word):
            next_page_url = formated_url

        #search_domain = re.search(r'/[a-zA-Z\.-]+[^(php|html|js|css)]+/', formated_url)
        search_domain = re.search(r'/[a-zA-Z\.-]+/', formated_url)
        search_yandex = re.search(r'(yandex)+', formated_url)

        if (not search_yandex):
            print('\nURL :>', formated_url)
            domain_name = re.search('/.[^/]+/', formated_url)
            domain_name = re.sub('[/]+', '', domain_name.group(0));
            links_list.append(domain_name) # Добавляем найденное доменное имя в список ссылок
    links_list.append(next_page_url)

    return links_list
# --------------------------------------------------------------------------


g = Grab(log_file='out.html')
g.go('http://ya.ru')
g.doc.set_input('text', 'авто')
g.doc.submit()

#print (g.doc.unicode_body())

#print(r.text)

#result = re.findall(r'<(a|A)\s[a-zA-Z]*\s*>\s*[a-zA-Z0-9]\s*</(a|A)>)', request_page.text)

cur_page_num = 1
last_search_page = 5

req_text = g.doc.unicode_body()
links_list = get_links_list(req_text)

#for key in links_list:
#    print('\nurl: ', key)

while(cur_page_num < last_search_page):
    req_text = g.doc.unicode_body()
    links_list = get_links_list(req_text)

    next_page_url = links_list.pop()

    print('------------- page: ', cur_page_num, ' ---------------')
    for key in links_list:
        print('\nurl: ', key)

    g.go('http://yandex.ru' + next_page_url)
    cur_page_num = cur_page_num + 1