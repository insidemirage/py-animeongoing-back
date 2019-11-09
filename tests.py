import unittest
from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
w = [
    ['Вавилон ~ (18:00)', 'Понедельник', '5', '12', 'emmdxeklxk'],
    ['Фантастическая звезда онлайн 2: Эпизод Оракул ~ (20:30)', 'Понедельник', 5, 12, 'uyiqktrfth']
    , ['Сцена для моих героев ~ (21:00)', 'Понедельник', 4, 12, 'crbtkkdhlz']]
links = {'https://a30.agorov.org/tip/tv/2350-phantasy-star-online-2-episode-oracle.html',
         'https://a30.agorov.org/tip/tv/2326-babylon.html',
         'https://a30.agorov.org/tip/tv/2334-stand-my-heroes-piece-of-truth.html',
         'https://a30.agorov.org/tip/tv/2322-watashi-nouryoku-wa-heikinchi-de-tte-itta-yo-ne.html',
         'https://a30.agorov.org/tip/tv/1894-black-clover.html',
         'https://a30.agorov.org/tip/tv/2241-diamond-no-ace-act-ii.html',
         'https://a30.agorov.org/tip/tv/2320-z-x-code-reunion.html',
         'https://a30.agorov.org/tip/tv/2340-kandagawa-jet-girls.html',
         'https://a30.agorov.org/tip/tv/2321-chihayafuru-3.html'}

class TestAnimevost(unittest.TestCase):
    def setUp(self):
        self.animevost = Animevost('https://a30.agorov.org/','https://a30.agorov.org/','animevost.csv')

    def test_get_ongoing(self):
        for link in links:
            self.assertIsNot(self.animevost.get_ongoing(link), False)
        self.assertFalse(self.animevost.get_ongoing(123124))
        self.assertFalse(self.animevost.get_ongoing('12412fasf'))
        self.assertFalse(self.animevost.get_ongoing(['kek']))
        self.assertFalse(self.animevost.get_ongoing({'kek'}))

    def test_randid(self):
        ids = []
        for i in range(0,255):
            id = self.animevost.randid(ids,0)
            ids.append([id])

        file = open('log.txt','w')
        line = ''
        for i in ids:
            line = line+i[0]+','

        file.write(line)
        file.close()
        
    def test_getlinks(self):
        self.assertIsInstance(self.animevost.get_links(), list)


class TestShiza(unittest.TestCase):
    def setUp(self):
        self.shiza = Shizaprj('http://shiza-project.com/', 'http://shiza-project.com/releases/view/1410','shiza.csv')

    def test_randid(self):
        ids = []
        for i in range(0, 255):
            id = self.shiza.randid(ids, 0)
            ids.append([id])

    def test_getlinks(self):
        self.assertIsInstance(self.shiza.get_links(), list)

    def test_fullupd(self):
        self.assertTrue(self.shiza.full_update())


class TestAnilibria(unittest.TestCase):
    def setUp(self):
        self.anilibria = Anilibria('https://www.anilibria.tv', 'https://www.anilibria.tv/pages/schedule.php', 'anilib.csv')

    def test_randid(self):
        ids = []
        for i in range(0, 255):
            id = self.anilibria.randid(ids, 0)
            ids.append([id])

    def test_getlinks(self):
        self.assertIsInstance(self.anilibria.get_links(), list)

    def test_fullupd(self):
        self.assertTrue(self.anilibria.full_update())


if __name__ == '__main__':

    unittest.main()