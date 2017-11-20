import os
import csv
import zipfile
from uuid import uuid4
from string import ascii_letters, digits
from random import randint, choice
import xml.etree.cElementTree as ET
from multiprocessing import Pool, cpu_count

from xmltodict import parse

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
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith('.zip')
    ]


def parse_zip(name):
    zip_file = zipfile.ZipFile(name, 'r')
    xml_name_list = zip_file.namelist()

    for name in xml_name_list:
        # yield ET.fromstring(data.decode('utf-8'))
        yield zip_file.read(name)


def parse_zip_name(name):
    xmls = []
    for xml in parse_zip(name):
        xml_dict = parse(xml)
        xmls.append(xml_dict['root'])

    return xmls


def parse_zip_files(directory):
    zip_names_list = get_zip_names(directory)

    with open('levels.csv', 'w') as levels, open('objects.csv', 'w') as objects:
        levels_writer = csv.writer(levels, lineterminator='\n', delimiter=';')
        objects_writer = csv.writer(objects, lineterminator='\n', delimiter=';')

        with Pool(cpu_count()) as pool:
            for result in pool.imap(parse_zip_name, zip_names_list):
                for xml in result:
                    # xml_id = [var['@value'] for var in xml['var'] if var['@name'] == 'id'][0]
                    [xml_id] = map(
                        lambda var: var['@value'],
                        filter(lambda var: var['@name'] == 'id', xml['var'])
                    )

                    levels_writer.writerow([var['@value'] for var in xml['var']])

                    objects_rows = [
                        (xml_id, obj['@name']) for obj in xml['objects']['object']
                    ] \
                        if isinstance(xml['objects']['object'], list) \
                        else [(xml_id, xml['objects']['object']['@name'])]

                    objects_writer.writerows(objects_rows)
