import gc
import io
import requests
from PIL import Image


base_url = 'http://www.wzkj.shop'

class Book:
    def __init__(self, data, degree):
        self.id = data['id']
        self.name = data['name']
        self.degree = degree

    def fetch(self):
        chap = 1
        page = 1
        img_list = []

        while True:
            while True:
                r = requests.get(base_url+'/book/{}/{}/{}.jpg'.format(self.id, chap, page))
                if r.status_code == 404:
                    break
                img_list.append(Image.open(io.BytesIO(r.content)))
                print('- {}-{}'.format(chap, page))
                page += 1
            if page == 1:
                break
            chap += 1
            page = 1

        if len(img_list) > 1:
            img_list[0].save('output/{}/{}-{}.pdf'.format(self.degree, self.id, self.name), save_all=True, append_images=img_list[1:])

def main(degree):
    data = {
        'page': 1,
        'rowNum': 2147483647
    }
    if degree == 'undergraduate':
        r = requests.post(base_url+'/wzxy/wz/onlinebook.html', data=data)
    elif degree == 'master':
        r = requests.post(base_url+'/wzxy/wz/masterOnlinebook.html', data=data)
    books = [{'id': int(i['id']), 'name': i['name'].strip().replace('/', '_')} for i in r.json()]
    books.sort(key=lambda x: x['id'])
    for i in books:
        print('-----------------')
        print('Fetching {}-{}...'.format(i['id'], i['name']))
        Book(i, degree).fetch()
        gc.collect()

if __name__ == '__main__':
    main('undergraduate')
    main('master')
