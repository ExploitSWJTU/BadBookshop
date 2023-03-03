import io
import requests
from PIL import Image


base_url = 'http://www.wzkj.shop'

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    def fetch(self):
        chap = 1
        page = 1
        img_list = []

        while True:
            page = 1
            while True:
                r = requests.get(base_url+'/book/{}/{}/{}.jpg'.format(self.id, chap, page))
                if r.status_code == 404:
                    break
                img_list.append(Image.open(io.BytesIO(r.content)))
                print('{}-{}'.format(chap, page))
                page += 1
            if page == 1:
                break
            chap += 1

        img_list[0].save('output/{}.pdf'.format(self.name), save_all=True, append_images=img_list[1:])

def query(q):
    data = {
        'name': q,
        'schoolId': 12,
        'page': 1,
        'rowNum': 2147483647
    }
    r = requests.post(base_url+'/wzxy/wz/onlinebook.html', data=data)
    return r.json()

def main():
    q = input('Please input the book name:\n')
    result = query(q)
    print('-----------------')
    for i in result:
        print(result.index(i), i['name'])
    print('-----------------')
    id = input('Please input the index number:\n')
    print('-----------------')
    print('Fetching...')
    Book(result[int(id)]).fetch()
    print('-----------------')
    print('Done!')

if __name__ == '__main__':
    main()
