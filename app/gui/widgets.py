from functools import wraps

layers = {}
def widget(*, layer=0):
    def outer_wrapper(cls):
        @wraps(cls)
        def inner_wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            if not layer in layers.keys():
                layers[layer] = []
            layers[layer].append(instance)
            return instance
        
        return inner_wrapper
    return outer_wrapper

def update(layer, *args, **kwargs):
    for widget in layers[layer]:
        widget.update(*args, **kwargs)