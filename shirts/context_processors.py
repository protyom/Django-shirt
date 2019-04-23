import cloudinary


def consts(request):
    return {
        'THUMBNAIL': {
            "class": "thumbnail inline", "format": "jpg", "crop": "fill", "height": 150, "width": 150,
        },
    }
