
def create_default_init(slots):
    func = 'def __init__(self):'
    for attr in slots:
        func += ' self.{}=None;'.format(attr)
    return func
