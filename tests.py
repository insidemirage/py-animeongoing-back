import unittest
from animevost import Animevost
from anilibria import Anilibria

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


if __name__ == '__main__':
    unittest.main()