import requests
from bs4 import BeautifulSoup

IMG_FOLDER = 'fruit_images/'


def run():
    for (idx, page) in enumerate(range(380)):
        resp = requests.get(
            'https://usdawatercolors.nal.usda.gov/pom/search.xhtml?start={}&searchText=&searchField=&sortField='.format(
                idx * 20))
        soup = BeautifulSoup(resp.text, 'html.parser')
        for (div_idx, div) in enumerate(soup.select('div.document')):
            doc = div.select_one('dl.defList')
            artist = doc.select_one(':nth-child(2)>a').get_text()
            year = doc.select_one(':nth-child(4)>a').get_text()
            # cannot parse scientific name or common name for some pictures, just use 'none' instead to avoid terminating
            scientific_name = 'none' if doc.select_one(':nth-child(6)>a') is None else doc.select_one(
                ':nth-child(6)>a').get_text()
            common_name = 'none' if doc.select_one(':nth-child(8)>a') is None else doc.select_one(
                ':nth-child(8)>a').get_text()
            thumb_pic_src = div.select_one('div.thumb-frame>a>img')['src']
            id = (idx + 1) * 20 + div_idx + 1
            info = FruitInfo(id, artist, year, scientific_name, common_name, thumb_pic_src)
            print(info)
            info.download_and_save()


class FruitInfo:
    def __init__(self, id, artist, year, scientific_name, common_name, thumb_pic_url):
        self.id = id
        self.artist = artist
        self.year = year
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.thumb_pic_url = thumb_pic_url

    def download_and_save(self):
        filename = '{}-{}-{}-{}.png'.format(self.id, self.common_name, self.year, self.artist).replace(' ', '_')
        print('filename = ', filename)
        ori_img_url = self.__parse_ori_img_url()
        print('original img url = ', ori_img_url)
        resp = requests.get(ori_img_url)
        with open(IMG_FOLDER + filename, 'wb') as f:
            f.write(resp.content)
            print('saved...', filename)

    def __parse_ori_img_url(self) -> str:
        img_id = self.thumb_pic_url.split('/')[2]
        print('img id = ', img_id)
        return 'https://usdawatercolors.nal.usda.gov/pom/download.xhtml?id={}'.format(img_id)

    def __str__(self):
        return 'FruitInfo(artist={},year={},scientific_name={},common_name={},thumb_pic_url={})'.format(self.artist,
                                                                                                        self.year,
                                                                                                        self.scientific_name,
                                                                                                        self.common_name,
                                                                                                        self.thumb_pic_url)


if __name__ == '__main__':
    run()
