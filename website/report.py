import zipfile
import xml.etree.ElementTree as ET

def doc_reader(docxfile):
    """Parse docx files."""
    try:
        zfile = zipfile.ZipFile(docxfile)
    except:
        print('Sorry, can\'t open {}.'.format(docxfile))
        return
    body = ET.fromstring(zfile.read('word/document.xml'))
    text = '\n'.join([et.text.strip() for et in body.iter() if et.text])
    return text
