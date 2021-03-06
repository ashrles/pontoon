"""
Parsing resource files.

See base.py for the ParsedResource base class.
"""
import os.path

from pontoon.sync.formats import (
    compare_locales,
    ftl,
    json_extensions,
    json_qlik,
    lang,
    po,
    silme,
    xliff,
)

# To add support for a new resource format, add an entry to this dict
# where the key is the extension you're parsing and the value is a
# callable returning an instance of a ParsedResource subclass.
SUPPORTED_FORMAT_PARSERS = {
    '.dtd': silme.parse_dtd,
    '.ftl': ftl.parse,
    '.inc': silme.parse_inc,
    '.ini': silme.parse_ini,
    '.json': json_extensions.parse,
    '.lang': lang.parse,
    '.po': po.parse,
    '.pot': po.parse,
    '.properties': silme.parse_properties,
    '.qlang': json_qlik.parse,
    '.xlf': xliff.parse,
    '.xliff': xliff.parse,
    '.xml': compare_locales.parse,
}


def parse(path, source_path=None, locale=None):
    """
    Parse the resource file at the given path and return a
    ParsedResource with its translations.

    :param path:
        Path to the resource file to parse.
    :param source_path:
        Path to the corresponding resource file in the source directory
        for the resource we're parsing. Asymmetric formats need this
        for saving. Defaults to None.
    :param locale:
        Object which describes information about currently processed locale.
        Some of the formats require information about things like e.g. plural form.
    """
    root, extension = os.path.splitext(path)
    if extension in SUPPORTED_FORMAT_PARSERS:
        return SUPPORTED_FORMAT_PARSERS[extension](path, source_path=source_path, locale=locale)
    else:
        raise ValueError('Translation format {0} is not supported.'
                         .format(extension))
