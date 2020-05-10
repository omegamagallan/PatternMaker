import requests
import base64
from io import BytesIO
from PIL import Image


api_server = "http://127.0.0.1:8080/api/create_pattern"

img = Image.new("RGBA", (50, 50), "#FFFF00FF")
img_io = BytesIO()
img.save(img_io, 'PNG', quality=100)
img_io.seek(0)
img = base64.b64encode(img_io.getvalue())

width = 100
scale = 100
pattern = "wave_shift"

params = {
    "image": img,
    "width": width,
    "scale": scale,
    "pattern_name": pattern
}

response = requests.post(api_server, data=params).content

img = Image.open(BytesIO(base64.b64decode(response)))
img.show()
