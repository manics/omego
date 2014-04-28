#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from xml.etree.ElementTree import XML, Element, SubElement, Comment, ElementTree, tostring
import xml.dom.minidom

import fileutils


def read_xml1(filename):
    with open(filename) as f:
        x = f.read()
        return XML(x)


def read_xml2(filename):
    return xml.dom.minidom.parse(filename)


def xml_tostring1(elem):
    return tostring(elem)


def element_to_xml(self, elem):
    string = tostring(elem, 'utf-8')
    return xml.dom.minidom.parseString(string).toprettyxml("  ", "\n", None)


def update_template_java_heapsize(filename):
    with open(filename) as f:
        x = XML(f.read())
    set_java_heapsize(x)
    fileutils.rename_backup(filename)
    tmp = filename + '.tmp'
    with open(tmp, 'w') as f:
        f.write(tostring(x))


def set_java_heapsize(x):
    replacements = [
        ('./server-template[@id="BlitzTemplate"]/server/option',
         '-Xmx\d+M$', '-Xmx1024M'),
        ('./server-template[@id="IndexerTemplate"]/server/option',
         '-Xmx\d+M$', '-Xmx1024M'),
        ('./server-template[@id="PixelDataTemplate"]/server/option',
         '-Xmx\d+M$', '-Xmx1024M'),
        ]
    for (p, match, replace) in replacements:
        print 'Searching for %s' % p
        es = x.findall(p)
        for e in es:
            if re.match(match, e.text):
                print 'Changing %s %s to %s' % (p, e.text, replace)
                e.text = replace
