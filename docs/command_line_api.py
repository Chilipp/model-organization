#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate the command line api"""
import os
import os.path as osp
from model_organization import ModelOrganizer
from docrep import dedents


def document_parsers(parser, base_key='model'):
    f = open(osp.join(api_dir, base_key + '.rst'), 'w')
    if len(base_key.split('.')) == 1:
        f.write('.. _command-line-api:\n\n')
        title = 'Command Line API Reference'
    else:
        title = base_key.replace('.', ' ')
        f.write('.. _command-' + base_key.replace('.', '-') + ':\n\n')
    f.write(title + '\n')
    f.write('=' * len(title) + '\n\n')

    if parser._subparsers:
        f.write(dedents("""
        .. toctree::
            :maxdepth: 1""") + '\n\n')
        for key, p in parser._subparsers_action.choices.items():
            sp_key = base_key + '.' + key
            f.write('    ' + sp_key + '\n')
            document_parsers(p, sp_key)
        f.write('\n')
    path = base_key.split('.')
    if len(path) == 1:
        path = ''
    else:
        path = ':path: ' + ' '.join(path[1:])
    f.write(dedents("""
    .. argparse::
       :module: model_organization
       :func: _get_parser
       :prog: model
       """ + path) + '\n')
    f.close()


parser = ModelOrganizer.get_parser()

api_dir = 'command_line'

if not osp.exists(api_dir):
    os.makedirs(api_dir)

document_parsers(parser)
