import os
import numpy as np
import fiona
from zipfile import ZipFile
from datetime import datetime
import cv2
from ultralytics import YOLO
import numpy as np
from PIL import Image
from ultralytics.utils.plotting import Annotator
from shapely.geometry import Polygon, mapping, shape
import cv2
import rasterio
import pyproj
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from shapely.geometry import Point, shape
from random import randint


def convert_tif_to_jpg(path_to_image, output_folder="result"):
    """
    Конвертирует изображение в формате TIFF в формат JPEG.

    Parameters:
    - path_to_image (str): Путь к файлу изображения формата TIFF.
    - output_folder (str): Папка для сохранения конвертированного изображения в формате JPEG.

    Returns:
    - str: Путь к сохраненному изображению в формате JPEG.
    """
    print(datetime.now())
    print('PATH: /system/server.py -> convert_tif_to_jpg')

    # Создание папки для сохранения, если её не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with Image.open(path_to_image) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Создание пути к выходному файлу, заменяя расширение на .jpg
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(path_to_image))[0] + '.jpg')
        # Сохранение изображения в формате JPEG
        img.save(output_path, 'JPEG')
        print(f"Converted {path_to_image} to {output_path}")
        return output_path


def image_processing(path_to_tif):
    """
    Обрабатывает изображение в формате TIFF, используя модель YOLO для детекции объектов.

    Parameters:
    - path_to_tif (str): Путь к файлу изображения формата TIFF.

    Returns:
    - результат выполнения функции find_parcel_for_building.
    """
    model = YOLO("yolo_100epochs_first.pt", task="detect")
    names = model.names
    print(datetime.now())
    print('PATH: /system/server.py -> image_processing')

    # Генерация уникального имени для файла
    name = os.path.splitext(os.path.basename(path_to_tif))[0] + str(randint(5, 10000))

    # Конвертация из TIFF в JPEG
    path_to_jpg = convert_tif_to_jpg(path_to_tif)
    img = Image.open(path_to_jpg)
    img = np.ascontiguousarray(img)

    # Получение предсказаний модели YOLO
    results = model.predict(img)

    # Путь к выходному файлу Shapefile
    output_shapefile_path = 'result/' + name +  ".shp"

    with rasterio.open(path_to_tif) as src:
        transform = src.transform
        schema = {'geometry': 'Polygon', 'properties': [('id', 'int'), ('Name', 'str')]}
        annotator = Annotator(img)

        with fiona.open(output_shapefile_path, mode='w', driver='ESRI Shapefile', schema=schema, crs=src.crs) as shp:
            object_id = 1

            # Обработка результатов детекции
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    label = names[int(box.cls)]
                    box_geo = [
                                transform * (b[0], b[1]),
                                transform * (b[0], b[3]),
                                transform * (b[2], b[3]),
                                transform * (b[2], b[1]),
                                transform * (b[0], b[1])
                               ]

                    polygon = Polygon(box_geo)

                    row_dict = {
                        'geometry': mapping(polygon),
                        'properties': {'id': object_id, 'Name': names[int(box.cls)]}
                    }
                    shp.write(row_dict)
                    object_id += 1
                    annotator.box_label(b, label, color=(79, 226, 104))

    # Сохранение изображения с обозначенными рамками в файл
    cv2.imwrite('result/' + name + '_boxed.jpg', annotator.result())

    # Вызов функции find_parcel_for_building для дополнительной обработки
    return find_parcel_for_building(name)


def find_parcel_for_building(name):
    """
    Идентифицирует земельные участки, на которых расположены здания, и создает новый Shapefile с результатами.

    Parameters:
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - Результат выполнения функции write_results_to_pdf.
    """
    print(datetime.now())
    print('PATH: /system/server.py -> find_parcel_for_building')

    # Открытие файлов Shapefile для зданий и земельных участков
    parcels = fiona.open('ЗУ/ZU.shp', 'r')
    buildings_shp_path = 'result/' + name +  ".shp"
    buildings = fiona.open(buildings_shp_path, 'r')
    results = []

    # Получение CRS для земельных участков
    buildings_crs = pyproj.CRS.from_string(buildings.crs_wkt)
    parcels_crs = pyproj.CRS.from_string(parcels.crs_wkt)

    # Проверка наличия несоответствия CRS и создание трансформатора
    if buildings_crs != parcels_crs:
        transformer = pyproj.Transformer.from_crs(buildings_crs, parcels_crs, always_xy=True)
    else:
        transformer = None
    
    # Определение схемы для нового Shapefile
    schema = {
        'geometry': 'Polygon',
        'properties': [('id', 'int'), ('Name', 'str'), ("cadastral_", 'str')]
    }
    
    # Путь к новому Shapefile
    path = 'result/' + name + "_with_parcel.shp"
    
    # Создание нового Shapefile и запись результатов
    with fiona.open(path, 'w', driver='ESRI Shapefile', schema=schema, crs=buildings.crs) as output:
        for building in buildings:
            building_polygon = shape(building['geometry'])
            building_center = building_polygon.centroid
            
            # Преобразование координат, если CRS различаются
            if buildings_crs != parcels_crs:
                lon, lat = transformer.transform(building_center.x, building_center.y)
                building_center = Point(lon, lat)
            found = False
            
            # Поиск соответствующего земельного участка
            for i, parcel in enumerate(parcels.values()):
                parcel_polygon = shape(parcel['geometry'])
                if building_center.within(parcel_polygon):
                    found = True
                    cadastral = parcel['properties']['cadastral_']
                    results.append({
                        'building_id': building['properties']['id'],
                        'building_type': building['properties']['Name'],
                        'building_position': (lon, lat),
                        'parcel_id': i,
                        'cadastral_': parcel['properties']['cadastral_']
                    })
            
            # Обработка случая, если земельный участок не найден
            if not found:
                cadastral = "Not found"
                results.append({
                    'building_id': building['properties']['id'],
                    'building_type': building['properties']['Name'],
                    'building_position': (lon, lat),
                    'parcel_id': "Not found",
                    'cadastral_': "Not found"
                })
            
            # Обновление информации о здании в новом Shapefile
            updated_building = {
                'geometry': building['geometry'],
                'properties': {
                    'id': building['properties']['id'],
                    'Name': building['properties']['Name'],
                    'cadastral_': cadastral
                }
            }
            output.write(updated_building)
    
    # Закрытие файлов Shapefile
    buildings.close()
    parcels.close()
    
    # Вызов функции write_results_to_pdf для создания PDF-документа с результатами
    return write_results_to_pdf(results, name)


def write_results_to_pdf(results, name):
    """
    Создает PDF-документ с результатами обработки и включает в него информацию о зданиях и изображение с обозначенными рамками.

    Parameters:
    - results (list): Список словарей с информацией о зданиях и соответствующих им земельных участках.
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - Результат выполнения функции archive_and_delete_files.
    """
    print(datetime.now())
    print('PATH: /system/server.py -> write_results_to_pdf')

    # Путь к PDF-документу
    pdf_path = 'result/' + name +  ".pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    y_coordinate = 700

    # Добавление информации о зданиях в PDF
    for result in results:
        building_info = f"Building ID: {result['building_id']}, Building Type: {result['building_type']}, Building Position: {result['building_position']}, Parcel ID: {result['parcel_id']}, cadastral_: {result['cadastral_']}"
        
        info_lines = building_info.split(', ')
        
        for line in info_lines:
            c.drawString(100, y_coordinate, line)
            y_coordinate -= 14
        c.showPage()
        y_coordinate = 700

    # Добавление изображения с обозначенными рамками в PDF
    c.showPage()
    image_reader = ImageReader('result/' + name + '_boxed.jpg')
    c.drawImage(image_reader, 100, 100, width=500, height=500)

    # Сохранение PDF-документа
    c.save()

    # Вызов функции archive_and_delete_files для архивации и удаления временных файлов
    return archive_and_delete_files(name)
    
    
def archive_and_delete_files(name):
    """
    Архивирует временные файлы, создает ZIP-архив и удаляет исходные файлы.

    Parameters:
    - name (str): Уникальное имя для файлов и результатов обработки.

    Returns:
    - str or None: Путь к созданному ZIP-архиву или None, если файлы отсутствуют.
    """
    print(datetime.now())
    print('PATH: /system/server.py -> archive_and_delete_files')

    # Получение списка файлов для архивации
    folder_path = "result/"
    files_to_archive = [f for f in os.listdir(folder_path) if f.startswith(name)]

    # Проверка наличия файлов для архивации
    if not files_to_archive:
        print('Файлы куда-то испарились...')
        return None

    # Создание ZIP-архива
    zip_file_path = os.path.join("static/from_ml", f'{name}_archive.zip')
    with ZipFile(zip_file_path, 'w') as zipf:
        for file_name in files_to_archive:
            file_path = os.path.join(folder_path, file_name)
            # Добавление файла в архив
            zipf.write(file_path, os.path.basename(file_path))

    # Удаление заархивированных файлов
    for file_name in files_to_archive:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

    print(datetime.now())
    print(f'Files from {name} archived and deleted. Archive created at: {zip_file_path}')
    print("Done!")

    # Возвращение пути к созданному ZIP-архиву
    return zip_file_path
