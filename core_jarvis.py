import json

class CoreJarvis:
    """ Core of the Jarvis helper  """

    def __init__(self):
        self.__duties = {
            'Living room': 'Tima',
            'Balcony': 'Nazarbek',
            'Toilets': 'Sanzhar',
            'Kitchen top': 'Alisher',
            'Kitchen bottom': 'Daniyar'}

    def get_duties(self):
        duties = json.dumps(self.__duties, indent=1)
        ind1 = duties.find('\n')
        ind2 = duties.rfind('\n')
        return duties[ind1:ind2]

    def update_duties(self):
        tasks = self.__duties.keys()
        ppl = [list(self.__duties.values())[-1]] + list(self.__duties.values())[:-1]
        self.__duties = dict(zip(tasks, ppl))

