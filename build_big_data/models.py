from utils import get_random_number, get_random_string


class CITY:
    def __init__(self):
        self.data = dict({"name": str(),
                          "code": int(),
                          "country": str(),
                          "citizens": int()})

    def get_random_data(self):
        self.data.clear()
        self.data['code'] = get_random_number(0, 10000)
        self.data['citizens'] = get_random_number(500, 500000)
        self.data['name'] = get_random_string(size=8)
        self.data['country'] = get_random_string(size=7)
        return self.data