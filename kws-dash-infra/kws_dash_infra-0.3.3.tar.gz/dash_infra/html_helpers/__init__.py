def CustomElement(elem):
    def wrapper(*args, classes=None, **kwargs):
        if classes:
            class_name = kwargs.pop("className", "") + " " + " ".join(classes)
            return elem(*args, **kwargs, className=class_name)

        else:
            return elem(*args, **kwargs)

    return wrapper
