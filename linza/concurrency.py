
class ConcurrencyModel(object):

    def __init__(self):
        self.occupied = set()

    def get_occupied(self):
        return self.occupied

    def update_occupied(self, past_id, next_id):
        if past_id in self.occupied:
            self.occupied.remove(past_id)
        self.occupied.add(next_id)
        return self


def make():
    return ConcurrencyModel()
