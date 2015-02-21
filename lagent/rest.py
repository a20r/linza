
import urllib
import urllib2
import json


class DistributionServer(object):

    DISTRIBUTION_ROUTE = "/dist"

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.address = "http://{}:{}".format(hostname, port)

    def get_distribution(self, time, node_id):
        url = self.address + self.DISTRIBUTION_ROUTE
        data = {"time": time, "node_id": node_id}
        encdata = urllib.urlencode(data)
        req = urllib2.Request(url=url, data=encdata)
        res_str = urllib2.urlopen(req).read()
        res_dict = json.loads(res_str)
        if res_dict["error"] > 0:
            raise RuntimeError("balls")
        else:
            return res_dict["dist"]

    def update_distribution(self, time, node_id, value):
        pass
