import csv


class DBWriter:
    def __init__(self, filename):
        self.filename = filename

    def push(self, anim):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(anim)
