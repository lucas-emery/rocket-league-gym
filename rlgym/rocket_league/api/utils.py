
def create_default_init(slots):
    # Utility function to create a default __init__ function for a class with __slots__
    func = 'def __init__(self):'
    for attr in slots:
        func += ' self.{}=None;'.format(attr)
    return func
