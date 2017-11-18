import functools
from uuid import uuid4
from string import ascii_letters, digits
from random import randint, choice
import xml.etree.cElementTree as ET
from multiprocessing import Pool
import zipfile


def random_string(size=10, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(size))


def create_xml():
    xml_id = str(uuid4())
    # xml_path = '/tmp/%s.xml' % xml_id

    root = ET.Element('root')
    ET.SubElement(root, 'var', name='id', value=xml_id)
    ET.SubElement(root, 'var', name='level', value=str(randint(1, 100)))
    objects = ET.SubElement(root, 'objects')
    for i in range(randint(1, 10)):
        ET.SubElement(objects, 'object', name=random_string())

    tree = ET.ElementTree(root)
    # tree.write(xml_path)
    #
    # return xml_path
    xmlstr = ET.tostring(tree, encoding='utf8', method='xml')
    return {'name': xml_id, 'content': xmlstr}


# class MultiprocRun:
#     def __init__(self, count):
#         self.count = count
#
#     def __call__(self, fn):
#         @functools.wraps(fn)
#         def decorated(*args, **kwargs):
#             pool = Pool()
#             pool.map(fn, my_foo_obj_list)
#             pool.close()
#             pool.join()
#             fn(*args, **kwargs)
#
#         return decorated



