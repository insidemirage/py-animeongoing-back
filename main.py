from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
from multiprocessing import Process
import os


def fulupd():
    animevost = Animevost('https://a30.agorov.org/', 'https://a30.agorov.org/', 'animevost.csv')
    anilibria = Anilibria('https://www.anilibria.tv', 'https://www.anilibria.tv/pages/schedule.php', 'anilib.csv')
    shiza = Shizaprj('http://shiza-project.com/', 'http://shiza-project.com/status/ongoing', 'shiza.csv')
    animevostprc = Process(target=animevost.full_update)
    shizaprc = Process(target=shiza.full_update)
    anilibriaprc = Process(target=anilibria.full_update)
    animevostprc.start()
    shizaprc.start()
    anilibriaprc.start()
    animevostprc.join()
    shizaprc.join()
    anilibriaprc.join()


def main():
    fulupd()

if __name__ == "__main__":
    # Testing
    # animevost = Animevost()
    # animevost.full_update()
    # f = Shizaprj('http://shiza-project.com/', 'http://shiza-project.com/', 'shiza.csv').full_update()
    # if f is False:
    #     print('bad return')
    main()