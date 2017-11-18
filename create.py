import os
import zipfile
from multiprocessing import Pool

from consts import ZIP_COUNT, XML_COUNT
from utils import create_xml


# class CreateZips:
#     def __init__(self, count, directory):
#         self.count = count,
#         self.directory = directory
#         self.create_zips()
#
#     def create_zips(self):
#         for i in range(self.count):

def create_zips(directory):
    for zip_index in range(ZIP_COUNT):
        zf = zipfile.ZipFile(
            'zipfile_writestr.zip',
            mode='w',
            compression=zipfile.ZIP_DEFLATED,
        )
        try:
            for xml_index in range(XML_COUNT):
                xml = create_xml()
                zf.writestr(os.path.join(directory, '%s.xml' % xml['name']), xml['content'])
        finally:
            zf.close()
