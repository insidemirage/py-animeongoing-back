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