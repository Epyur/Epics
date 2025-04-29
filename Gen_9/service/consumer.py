import pandas as pd

from Gen_9.service.rout_map import cus_book, ns


class ConsumerInfo:

    def __init__(self, data, email):
        self.email = email
        self.data = data

    def ask_lusie(self, word):
        self.lusya = self.data.loc[self.data[ns[10]] == self.email, word].iloc[0]
        return self.lusya

    @property
    def cons_name(self):
        try:
            self.name = self.ask_lusie(ns[11])
            return self.name
        except:
            return 'no data'

    @property
    def cons_tel(self):
        try:
            self.name = self.ask_lusie(ns[95])
            return self.name
        except:
            return 'no data'

    @property
    def cons_place_of_work(self):
        try:
            self.name = self.ask_lusie(ns[93])
            return self.name
        except:
            return 'no data'

    @property
    def cons_co_requesits(self):
        try:
            self.name = self.ask_lusie(ns[94])
            return self.name
        except:
            return 'no data'

    @property
    def cons_sbe(self):
        try:
            self.name = self.ask_lusie(ns[96])
            return self.name
        except:
            return 'no data'

    @property
    def cons_ind(self):
        try:
            self.name = self.ask_lusie(ns[97])
            return self.name
        except:
            return 'no data'

