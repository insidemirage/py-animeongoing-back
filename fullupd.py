from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
from multiprocessing import Process
from datetime import datetime

def fulupd():
    animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv','AnimeVost')
    # anilibria = Anilibria('https://www.anilibria.tv', 'https://www.anilibria.tv/pages/schedule.php', 'anilib.csv','Anilibria')
    # shiza = Shizaprj('http://shiza-project.com/', 'http://shiza-project.com/status/ongoing', 'shiza.csv','Shiza project')
    animevostprc = Process(target=animevost.full_update)
    # shizaprc = Process(target=shiza.full_update)
    # anilibriaprc = Process(target=anilibria.full_update)
    animevostprc.start()
    # shizaprc.start()
    # anilibriaprc.start()
    animevostprc.join()
    # shizaprc.join()
    # anilibriaprc.join()

def main():
    fulupd()


if __name__ == "__main__":
    main()