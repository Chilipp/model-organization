#!/usr/bin/env python
import os.path as osp
import numpy as np
from model_organization import ModelOrganizer


class SquareModelOrganizer(ModelOrganizer):

    name = 'square'

    commands = ModelOrganizer.commands[:]

    # insert the new run command to the other commands, right before the
    # archiving
    commands.insert(commands.index('archive'), 'preproc')

    def preproc(self, which='sin', **kwargs):
        """
        Create preprocessing data

        Parameters
        ----------
        which: str
            The name of the numpy function to apply
        ``**kwargs``
            Any other parameter for the
            :meth:`model_organization.ModelOrganizer.app_main` method
        """
        self.app_main(**kwargs)
        config = self.exp_config
        config['infile'] = infile = osp.join(config['expdir'], 'input.dat')

        func = getattr(np, which)  # np.sin, np.cos or np.tan
        data = func(np.linspace(-np.pi, np.pi))
        self.logger.info('Saving input data to %s', infile)
        np.savetxt(infile, data)

    def _modify_preproc(self, parser):
        """Modify the parser for the preprocessing command"""
        parser.update_arg('which', short='w', choices=['sin', 'cos', 'tan'])

if __name__ == '__main__':
    SquareModelOrganizer.main()
