from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
from multiprocessing import Process
from datetime import datetime



def halfupd():
    # Отправляем на отслеживание обновлений только те сериалы, которые выходят в течении суток обновляем каждые mins
    mins = 15
    today = datetime.today().weekday()
    animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv', 'AnimeVost')
    animevostprc = Process(target=animevost.update, args=(today, mins,))
    animevostprc.start()
    animevostprc.join()


def main():
    halfupd()
    # TODO загнать dev function в tests
    # animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv', 'AnimeVost')
    # animevost.devonly()


if __name__ == "__main__":
    main()