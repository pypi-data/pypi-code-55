def join_horizontally(text_images, spacing=2):
    text_images = tuple(text_images)
    return tuple((' ' * spacing).join(image[i] for image in text_images) for i in range(len(text_images[0])))
