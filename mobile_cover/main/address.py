import requests
import pyproj
from main.models import Cover


class Address:
    """
    Class used to manipulate query datas sended from url GET request
    """

    def __init__(self, address):
        self.address = address
        self.coord = []

    def get_geoloc(self):
        """
        Method used to request gouv API to get GPS coordonates of
        asked position in the GET request
        """
        search_list = self.address.split(" ")
        result = requests.get(  # requesting API REST
            f"https://api-adresse.data.gouv.fr/search/?q={self.address}"
        )
        json_result = result.json()  # format into json
        infos = json_result["features"]
        api_result = infos[0]

        try:
            city = api_result["properties"]["city"].lower()
        except:
            return {"result": "city matching found"}
        try:
            postcode = api_result["properties"]["postcode"]
        except:
            return {"result": "code matching found"}

        city_name = False
        city_code = False

        for word in search_list:
            if word == city:
                city_name = True
            if word[0:2] == postcode[0:2]:
                city_code = True

        self.coord = api_result.get("geometry")
        self.coord = self.coord.get("coordinates")

        if city_name or city_code:
            print(self.coord)
            return self.coord  # returns x and y coordonates
        else:
            return {"result": "no matching found"}

    def get_result(self):
        """
        Method used to find matches from x,y in the database
        and return a dict response
        """
        result = {}
        x = str(self.coord[0])  # formating long
        x = x[0:6]

        y = str(self.coord[1])  # formating lat
        y = y[0:4]

        test_result = Cover.objects.filter(x__startswith=x).filter(
            y__startswith=y
        )

        for i in test_result:  # response construction
            result[i.operator] = {"2G": i.G2, "3G": i.G3, "4G": i.G4}

        return result
