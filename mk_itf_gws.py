#!/usr/bin/env python
# coding: utf-8
from xml.etree.ElementTree import *
import csv
import os

def parser_xml(xml, wr):
    tree = parse(xml)
    elem = tree.getroot()
    idx = 1
    bodys = []
    for eitem in elem.getiterator("item"):
        name = eitem.get('name')
        #print(name, eitem.tag)
        if name != 'comma':
            for subitem in eitem:
                if subitem.tag == 'holder_type':
                    htype = subitem.text
                if subitem.tag == 'required':
                    mandatory = 'R' if subitem.text == 'Yes' else 'O'
                if subitem.tag == 'type':
                    ttype = 'TEXT' if subitem.text == 'X' else 'DIGIT'
                if subitem.tag == 'to':
                    sto = int(subitem.text)
                if subitem.tag == 'from':
                    sfrom = int(subitem.text)
                if subitem.tag == 'min_size':
                    attr = 'Fixed' if subitem.text != '0' else 'Variable'
                if subitem.tag == 'trim':
                    trim = subitem.text
                if subitem.tag == 'align':
                    align = subitem.text
            size = str(sto - sfrom + 1)
            body = [idx, name, '', mandatory, ttype, size, attr, trim, align, htype, '', '']
            idx += 1
            bodys.append(body)
    wr.writerows(bodys)

def main():
    # mk_xxxを実行
    path = "D:/work/workspace/GWS/format"
    header = ['No.', 'Item Name', 'Meaning', 'Mandatory', 'Type', 'Size',
                'Attribute', 'Trim', 'Align', 'HType', 'Format', 'GWS comment']
    file_list = ['GIDM194FixedFormat.xml', 'GIDM195FixedFormat.xml', 'GIDM196FixedFormat.xml',
                'GIDM197FixedFormat.xml', 'GIDM198FixedFormat.xml', 'GIDM199FixedFormat.xml',
                'GIDM200FixedFormat.xml', 'GIDM201FixedFormat.xml', 'GIDM202FixedFormat.xml']
    with open(os.path.join(path, 'interface.csv'), 'w', newline='') as cf:
        for f in file_list:
            writer = csv.writer(cf)
            writer.writerow(header)
            parser_xml(os.path.join(path, f), writer)

if __name__ == '__main__':
    main()