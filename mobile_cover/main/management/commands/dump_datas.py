from django.core.management.base import BaseCommand, CommandError
from django.db import models
from tqdm import tqdm
from main.models import Cover
import csv
import os
import pyproj


class Command(BaseCommand):
    '''
    Command created to store dats from CSV into database after being
    converted from lambert93 to GPS.
    '''
    help = "Dump coverage datas values from csv file"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Dumping datas from CSV"))

        workpath = os.path.dirname(  # used to find the csv file
            os.path.abspath(__file__)
        )
        with open(os.path.join(workpath, "mobiles.csv"), "r") as csv_file:

            csv_reader = csv.reader(csv_file)
            temp = []
            for line in csv_reader:
                temp.append(line[0].split(";"))

            for el in tqdm(temp):
                if el[0] == "20801":
                    el[0] = "Orange"
                elif el[0] == "20810":
                    el[0] = "SFR"
                elif el[0] == "20815":
                    el[0] = "FREE"
                elif el[0] == "20820":
                    el[0] = "Bouygue"
                try:
                    (
                        x_coord,
                        y_coord,
                    ) = self.convert_coord(  # convert l93 to GPS
                        int(el[1]), int(el[2])
                    )
                except:
                    x_coord, y_coord = self.convert_coord(
                        1000, 1000
                    )  # fake datas

                if el[3] == "1":
                    el[3] = True
                else:
                    el[3] = False

                if el[4] == "1":
                    el[4] = True
                else:
                    el[4] = False

                if el[5] == "1":
                    el[5] = True
                else:
                    el[5] = False

                x_coord = str(x_coord)
                y_coord = str(y_coord)

                c = Cover(  # Inserting datas in database
                    operator=el[0],
                    x=x_coord[0:10],
                    y=y_coord[0:10],
                    G2=el[3],
                    G3=el[4],
                    G4=el[5],
                )
                c.save()

        self.stdout.write(self.style.SUCCESS("Opération terminée: [OK]"))

    def convert_coord(self, x, y):
        """Method used to convert lambert93 to GPS coord"""

        self.x = x
        self.y = y
        lambert = pyproj.Proj("+proj=lcc +lat_1=49 +lat_2=44 "
                              "+lat_0=46.5 +lon_0=3 +x_0=700000 "
                              "+y_0=6600000 +ellps=GRS80 "
                              "+towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        )
        wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
        long, lat = pyproj.transform(lambert, wgs84, x, y)

        return long, lat  # returns converted L93 coords to GPS
