from animevost import Animevost
from database import DBWriter
if __name__ == "__main__":
    # Testing
    users = Animevost().get_links()
    DBWriter().pushtodb(users)