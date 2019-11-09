from animevost import Animevost
from anilibria import Anilibria
from shizaprj import Shizaprj
from database import DBWriter


def main():
    pass



if __name__ == "__main__":
    # Testing
    # animevost = Animevost()
    # animevost.full_update()
    f = Shizaprj().full_update()
    if f is False:
        print('bad return')


        #   self.link = 'http://shiza-project.com/'
        #         self.ongoinglink = 'http://shiza-project.com/releases/view/1410'