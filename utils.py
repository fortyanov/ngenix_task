import os
import csv
import zipfile
from uuid import uuid4
from string import ascii_letters, digits
from random import randint, choice
import xml.etree.cElementTree as ET
from multiprocessing import Pool

from consts import ZIP_COUNT, ZIP_NAME, XML_COUNT


def random_string(size=10, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(size))


def create_xml():
    xml_id = str(uuid4())

    root = ET.Element('root')
    ET.SubElement(root, 'var', name='id', value=xml_id)
    ET.SubElement(root, 'var', name='level', value=str(randint(1, 100)))
    objects = ET.SubElement(root, 'objects')
    for i in range(randint(1, 10)):
        ET.SubElement(objects, 'object', name=random_string())

    xmlstr = ET.tostring(root, encoding='utf8', method='xml').decode('utf-8')
    return {'name': xml_id, 'content': xmlstr}


def create_zip_files(directory):
    for zip_index in range(ZIP_COUNT):
        zf = zipfile.ZipFile(
            os.path.join(directory, '%s_%s.zip' % (ZIP_NAME, zip_index)),
            mode='w',
            compression=zipfile.ZIP_DEFLATED,
        )
        try:
            for xml_index in range(XML_COUNT):
                xml = create_xml()
                zf.writestr('%s.xml' % xml['name'], xml['content'])
        finally:
            zf.close()


def get_zip_names(directory):
    result = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith('.zip')
    ]
    return result


def parse_zip(name):
    zip_file = zipfile.ZipFile(name, 'r')
    xml_name_list = zip_file.namelist()

    for name in xml_name_list:
        data = zip_file.read(name)
        xml = ET.fromstring(data.decode('utf-8'))
        yield xml


def create_csv_files(xml):
    with open('levels.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)


def add_xml_to_levels(file):
    pass


def add_xml_to_objects():
    pass


def parse_zip_name(name):
    levels = open('levels.csv', 'wb')
    objects = open('objects.csv', 'wb')

    for xml in parse_zip(name):
        add_xml_to_levels(levels, xml)
        add_xml_to_objects(objects, xml)

    levels.close()
    objects.close()


def parse_zip_files(directory):
    zip_names_list = get_zip_names(directory)
    pool = Pool()
    pool.map(parse_zip_name, zip_names_list)
    pool.close()
    pool.join()
