
import requests


class ConcurrencyStub(object):

    OCCUPIED_ROUTE = "/occupied"

    def __init__(self, host, port):
        self.address = "http://{}:{}".format(host, port)

    def get_occupied(self):
        url = self.address + self.OCCUPIED_ROUTE
        r = requests.get(url)
        return set(r.json())

    def update_occupied(self, past_id, next_id):
        url = self.address + self.OCCUPIED_ROUTE
        data = {"past_id": past_id, "next_id": next_id}
        r = requests.post(url, payload=data)
        return r.json()


class DistributionStub(object):

    GET_DIST_ROUTE = "/get_info"
    POST_DIST_ROUTE = "/update_info"
    BOX_ROUTE = "/box"

    def __init__(self, host, port):
        self.address = "http://{}:{}".format(host, port)

    def get_distribution(self, time, node_id):
        url = (self.address + self.GET_DIST_ROUTE + "/{}/{}")\
            .format(int(time), node_id)
        r = requests.get(url)
        if not r.status_code == 200:
            raise RuntimeError("HTTP SHIT")
        else:
            return r.json()["Value"]

    def update_distribution(self, time, node_id, value):
        url = self.address + self.POST_DIST_ROUTE
        data = {"time": time, "node_id": node_id, "value": value}
        r = requests.post(url, payload=data)
        if not r.status_code == 200:
            raise RuntimeError("HTTP SHIT")

        return self

    def get_bounding_box(self):
        url = self.address + self.BOX_ROUTE
        r = requests.get(url)
        if not r.status_code == 200:
            raise RuntimeError("HTTP SHIT")
        j = r.json()

        return j["Left"], j["Bottom"], j["Right"], j["Top"]


def make_ds(host, port):
    return DistributionStub(host, port)


def make_cs(host, port):
    return ConcurrencyStub(host, port)
