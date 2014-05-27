#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Standardize record names by removing diacritic and special characters.
"""


import functools
import os
import re
import sys
import unicodedata


__author__ = "Alain Clément-Pavon"
__contact__ = "unisis@unil.ch"
__copyright__ = "Copyright 2014, University of Lausanne, Switzerland"
__credits__ = ["Gérard Bagnoud", "Nathalie Montet", "Raphaël Mottier"]
__license__ = "GPL"
__date__ = "2014-05-25"
__version__ = "1.0.1"
__maintainer__ = "Alain Clément-Pavon"
__email__ = "alain.clement-pavon@unil.ch"
__status__ = "Production"


PRINTABLE = {'Lu', 'Ll', 'Nd', 'Zs', 'Pc'}
VOID_WORDS = ['l\'', 'le', 'la', 'les', 'd\'', 'de', 'des', 'un', 'une', 's\'', 'si']


def compose(*functions):
    """
    Compose functions.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)


def remove_diacritics(string):
    """
    Remove diacritic characters.
    """
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')


def remove_void_words(string):
    """
    Remove void words.
    """
    regex = re.compile(
        r'\b(' + '|'.join(VOID_WORDS) + r')\b',
        flags=re.IGNORECASE + re.UNICODE)
    return regex.sub('', string)


def remove_non_printable(string):
    """
    Remove non printable characters.
    http://www.sql-und-xml.de/unicode-database/#kategorien
    """

    result = []
    for c in string.decode('utf-8'):
        c = unicodedata.category(c) in PRINTABLE and c or u'#'
        result.append(c)
    return u''.join(result).replace(u'#', u' ')


def remove_multiple_spaces(string):
    """
    Remove multiple spaces.
    """
    return ' '.join(string.split())


def substitute_underscore_to_space(string):
    """
    Substitute underscores to spaces.
    """
    return re.sub(r'([^_]) +([^_])', '\\1_\\2', string).replace(' ', '')


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
    remove_diacritics,
    remove_void_words,
)


def main():
    for line in sys.stdin:
        source = os.path.abspath(line.decode('utf-8')).strip()
        path, basename = os.path.split(source)
        name, extension = os.path.splitext(basename)
        new_name = standardize(name)
        target = os.path.join(path, new_name + extension)
        os.rename(source, target)
        print target


if __name__ == "__main__":
    main()
