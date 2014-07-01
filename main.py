#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Standardize record names by removing diacritic and special characters.
"""


import functools
import glob
import os
import re
import sys
import unicodedata


__author__ = "Alain Clément-Pavon"
__contact__ = "unisis@unil.ch"
__copyright__ = "Copyright 2014, University of Lausanne, Switzerland"
__credits__ = ["Gérard Bagnoud", "Nathalie Farenc", "Nathalie Montet", "Raphaël Mottier"]
__license__ = "GPL"
__date__ = "2014-06-23"
__version__ = "1.0.4"
__maintainer__ = "Alain Clément-Pavon"
__email__ = "alain.clement-pavon@unil.ch"
__status__ = "Production"


PRINTABLE = {'Lu', 'Ll', 'Nd', 'Zs', 'Pc'}
VOID_WORDS = ["l'", 'le', 'la', 'les',
              "d'", 'de', 'des',
              'un', 'une',
              "s'", 'si',
              'à',
              "n'",
              'en', 'sur']


def compose(*functions):
    """
    Compose functions.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)


def remove_diacritics(string):
    """
    Remove diacritic characters.
    """
    return unicodedata.normalize('NFKD', string.decode('utf-8'))\
        .encode('ASCII', 'ignore').decode('ASCII').encode('utf-8')


def remove_void_words(string):
    """
    Remove void words.
    """
    return ' '.join(
        [word for word in string.replace("'", "' ").split()
         if word.lower() not in VOID_WORDS]
    )


def remove_non_printable(string):
    """
    Remove non printable characters.
    http://www.sql-und-xml.de/unicode-database/#kategorien
    """

    result = []
    for c in string.decode('utf-8'):
        c = unicodedata.category(c) in PRINTABLE and c or u'#'
        result.append(c)
    return (u''.join(result).replace(u'#', u'')).encode('utf-8')


def remove_multiple_spaces(string):
    """
    Remove multiple spaces.
    """
    return ' '.join(string.split())


def substitute_underscore_to_space(string):
    """
    Substitute underscores to spaces.
    """
    string = re.sub(r'(_+) +(_*)', '\\1\\2', string)
    string = re.sub(r' +(_+)', '\\1', string)
    string = re.sub(r' +', '_', string)
    return string


def substitute_underscore_to_minus(string):
    """
    Substitute underscores to minuses.
    """
    string = re.sub(r'(_+)-+(_*)', '\\1\\2', string)
    string = re.sub(r'-+(_+)', '\\1', string)
    string = re.sub(r'-+', '_', string)
    return string


def substitute_underscore_to_periods(string):
    """
    Substitute underscores to periods.
    """
    string = re.sub(r'(_+)\.+(_*)', '\\1\\2', string)
    string = re.sub(r'\.+(_+)', '\\1', string)
    string = re.sub(r'\.+', '_', string)
    return string


def strip_underscores(string):
    """
    Strip underscores.
    """
    return string.strip('_')


standardize = compose(
    strip_underscores,
    substitute_underscore_to_space,
    remove_multiple_spaces,
    remove_non_printable,
    substitute_underscore_to_periods,
    substitute_underscore_to_minus,
    remove_diacritics,
    remove_void_words
)


def safe_rename(source, target):
    new_element = target
    while os.path.exists(new_element):
        path, basename = os.path.split(new_element)
        name, extension = os.path.splitext(basename)
        if os.path.isdir(new_element) and extension != ".app":
            name += extension
            extension = ""
        raw_name, inc = (re.findall(r'(.*)_DISAMB_(\d+)$', name) or [(name, '0')])[0]
        new_element = os.path.join(path, raw_name + '_DISAMB_' + str(int(inc)+1) + extension)
    os.rename(source, new_element)
    return new_element


def standardize_element(source):
    path, basename = os.path.split(source)
    name, extension = os.path.splitext(basename)
    if os.path.isdir(source) and extension != ".app":
        name += extension
        extension = ""
    new_name = standardize(name)
    if new_name != name:
        target = os.path.join(path, new_name + extension)
        print safe_rename(source, target)


def standardize_tree(source):
    if os.path.isfile(source):
        standardize_element(source)
    elif os.path.isdir(source):
        for element in glob.glob((source.decode('utf-8') + u'/*').encode('utf-8')):
            standardize_tree(element)
        standardize_element(source)


def main():
    for line in sys.stdin:
        source = os.path.abspath(line).strip()
        standardize_tree(source)


if __name__ == "__main__":
    main()
