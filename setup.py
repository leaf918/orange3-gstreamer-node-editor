#!/usr/bin/env python

from os import path, walk

import sys
from setuptools import setup, find_packages

NAME = "Orange3 Gstreamer Node Editor"

VERSION = "0.1.0"

AUTHOR = 'Leef Lee'
AUTHOR_EMAIL = 'leef918@gmail.com'

URL = 'https://github.com/leaf918/orange3-gstreamer-node-editor'
DESCRIPTION = "Add-on containing gstreamereditor widgets"
LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.pypi'),
                        'r', encoding='utf-8').read()

LICENSE = "BSD"

KEYWORDS = [
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'orange3 add-on','gstreamer editor nodes'
]

PACKAGES = find_packages()

PACKAGE_DATA = {
    'keyecontrib.gstreamereditor': ['tutorials/*.ows'],
    'keyecontrib.gstreamereditor': ['datas/*'],
    'keyecontrib.gstreamereditor.widgets': ['icons/*'],
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]

INSTALL_REQUIRES = [
    # 'Orange3', # at least version of orange3
]

ENTRY_POINTS = {
    # Entry points that marks this package as an orange add-on. If set, addon will
    # be shown in the add-ons manager even if not published on PyPi.
    'orange3.addon': (
        'gstreamereditor = keyecontrib.gstreamereditor',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'gstreamertutorials = keyecontrib.gstreamereditor.tutorials',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    keyecontrib/gstreamereditor/widgets/__init__.py
        'Gstreamer Nodes = keyecontrib.gstreamereditor.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index = keyecontrib.gstreamereditor.widgets:WIDGET_HELP_PATH',)
}

NAMESPACE_PACKAGES = ["keyecontrib"]

TEST_SUITE = "keyecontrib.gstreamereditor.tests.suite"


def include_documentation(local_dir, install_dir):
    global DATA_FILES
    if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
        print("Directory '{}' does not exist. "
              "Please build documentation before running bdist_wheel."
              .format(path.abspath(local_dir)))
        sys.exit(0)

    doc_files = []
    for dirpath, dirs, files in walk(local_dir):
        doc_files.append((dirpath.replace(local_dir, install_dir),
                          [path.join(dirpath, f) for f in files]))
    DATA_FILES.extend(doc_files)


if __name__ == '__main__':
    include_documentation('doc/_build/html', 'help/orange3-gstreamereditor')
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        license=LICENSE,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        keywords=KEYWORDS,
        namespace_packages=NAMESPACE_PACKAGES,
        zip_safe=False,
    )
