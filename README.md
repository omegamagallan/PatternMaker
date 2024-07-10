# Сайт генерации паттернов
REST API для создание взаимосовмещающихся паттернов из изображений по заданному, кастомному пресету
Ниже приводится полный список обязательных параметров:

<table>
  <tr>
    <th>Param</th>
    <th>Data type</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>image</td>
    <td>Base64</td>
    <td>Изображение</td>
  </tr>
  <tr>
    <td>width</td>
    <td>int</td>
    <td>Ширина изображения в пикселях</td>
  </tr>
  <tr>
    <td>scale</td>
    <td>int</td>
    <td>Размер изображения, в процентах от исходного изображения</td>
  </tr>
  <tr>
    <td>pattern_name</td>
    <td>str</td>
    <td>Название используемого паттерна</td>
  </tr>
</table>

## Пример использования

```
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
```
