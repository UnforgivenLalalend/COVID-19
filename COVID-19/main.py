import pip
import argparse
import sys

try:
    import requests
    import lxml
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(["install", "requests"])
    pip.main(["install", "bs4"])
    pip.main(["install", "lxml"])
    import requests
    import lxml
    from bs4 import BeautifulSoup


class CovidParser:
    def __init__(self, user_choice, country):
        self.url = "https://www.worldometers.info/coronavirus/"
        self.result = user_choice
        self.country = country

    def req_result(self):
        responce = requests.get(self.url)
        responce.encoding = "utf-8"

        return responce.text

    def parse_html(self):
        soup = BeautifulSoup(self.req_result(), "lxml")
        array = soup.find_all("td")

        for i in range(len(array)):
            array[i] = array[i].text
            if array[i] == "" or array[i] == " ":
                array[i] = "N/A"

        array = array[133:]
        array[0] = "0"

        return array

    def print_result(self):
        array = self.parse_html()

        if self.result == 2:
            answer = -1
            for x in range(len(array)):
                if array[x] == self.country:
                    answer = x - 1
                    break

            if answer == -1:
                print("This country does not exist")
                sys.exit(1)

            array = array[answer : answer + 19]

        print(
            """
|=====|========================|=============|===========|=============|===========|=================|==============|============|
|  №  |        Location        | Total Cases | New Cases | Total Death | New Death | Total Recovered | Active Cases | Population |
|=====|========================|=============|===========|=============|===========|=================|==============|============|
""",
            end="",
        )

        for i in range(0, len(array) - 9130, 19):
            if len(array[i]) == 1:
                array[i] = "00" + array[i]
            elif len(array[i]) == 2:
                array[i] = "0" + array[i]

            spaces_i1 = (23 - len(array[i + 1])) * " "
            spaces_i2 = (12 - len(array[i + 2])) * " "
            spaces_i3 = (10 - len(array[i + 3])) * " "
            spaces_i4 = (12 - len(array[i + 4])) * " "
            spaces_i5 = (10 - len(array[i + 5])) * " "
            spaces_i6 = (16 - len(array[i + 6])) * " "
            spaces_i8 = (13 - len(array[i + 8])) * " "
            spaces_i13 = (11 - len(array[i + 13])) * " "

            print(
                f"| {array[i]} | {array[i + 1]}{spaces_i1}| {array[i + 2]}{spaces_i2}| {array[i + 3]}{spaces_i3}| {array[i + 4]}{spaces_i4}| {array[i + 5]}{spaces_i5}| {array[i + 6]}{spaces_i6}| {array[i + 8]}{spaces_i8}| {array[i + 13]}{spaces_i13}|"
            )


def main():
    parser = argparse.ArgumentParser(description="Hydra on python")
    required = parser.add_argument_group("Required arguments")

    required.add_argument(
        "-a", "--all", dest="all", action="store_true", help="All countries"
    )
    required.add_argument(
        "-c",
        "--country",
        dest="country",
        help="Adding to charset lower_case letters",
    )

    args = parser.parse_args()

    all_flag = args.all
    country = args.country

    if country == None:
        user_choice = 1
    else:
        user_choice = 2

    start = CovidParser(user_choice, country)
    start.print_result()


if __name__ == "__main__":
    main()