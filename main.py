from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
from multiprocessing import Process
from datetime import datetime
from time import sleep
import schedule

def fulupd():
    animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv','AnimeVost')
    anilibria = Anilibria('https://www.anilibria.tv', 'https://www.anilibria.tv/pages/schedule.php', 'anilib.csv','Anilibria')
    shiza = Shizaprj('http://shiza-project.com/', 'http://shiza-project.com/status/ongoing', 'shiza.csv','Shiza project')
    animevostprc = Process(target=animevost.full_update)
    shizaprc = Process(target=shiza.full_update)
    anilibriaprc = Process(target=anilibria.full_update)
    animevostprc.start()
    shizaprc.start()
    anilibriaprc.start()
    animevostprc.join()
    shizaprc.join()
    anilibriaprc.join()


def halfupd():
    # Отправляем на отслеживание обновлений только те сериалы, которые выходят в течении суток обновляем каждые mins
    mins = 15
    today = datetime.today().weekday()
    animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv', 'AnimeVost')
    animevostprc = Process(target=animevost.update, args=(today, mins,))
    anilibria = Anilibria('https://www.anilibria.tv', 'https://www.anilibria.tv/pages/schedule.php', 'anilib.csv','Anilibria')
    anilibriaprc = Process(target=anilibria.update, args=(today,mins,))

    anilibriaprc.start()
    animevostprc.start()
    animevostprc.join()
    anilibriaprc.join()
    print('----------------------------------------------------------------')

def main():
    fulupd()
    schedule.every(30).minutes.do(halfupd)
    schedule.every().day.at("04:00").do(fulupd)

    while 1:
        schedule.run_pending()
        sleep(1)
    # TODO загнать dev function в tests
    # animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv', 'AnimeVost')
    # animevost.devonly()
    

if __name__ == "__main__":
    main()