import unittest
from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
w = [
    ['Вавилон ~ (18:00)', 'Понедельник', '5', '12', 'emmdxeklxk'],
    ['Фантастическая звезда онлайн 2: Эпизод Оракул ~ (20:30)', 'Понедельник', 5, 12, 'uyiqktrfth']
    , ['Сцена для моих героев ~ (21:00)', 'Понедельник', 4, 12, 'crbtkkdhlz']]


class TestAnimeVost(unittest.TestCase):
    def test_randid(self):

        Animevost().randid(w)

    def test_checkid(self):
        Animevost().check_id(w, '1231245215')


class TestAnilibria(unittest.TestCase):
    def test_getlinks(self):
        Anilibria().get_links()

    def test_fullupdate(self):
        Anilibria().full_update()

class TestShiza(unittest.TestCase):
    def test_getongoing(self):
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1438'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1435'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1444'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1417'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1425'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1238'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1398'))
        self.assertIsNotNone(Shizaprj().get_ongoing('http://shiza-project.com/releases/view/1410'))
        self.assertIsNotNone(Shizaprj().get_ongoing('https://shasfhasf.rua/asf'))
    def test_getlinks(self):
        self.assertIsNotNone(Shizaprj().get_links())
if __name__ == '__main__':
    unittest.main()