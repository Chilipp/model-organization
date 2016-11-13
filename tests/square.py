#!/usr/bin/env python
import os
import os.path as osp
import numpy as np
from model_organization import ModelOrganizer


class SquareModelOrganizer(ModelOrganizer):

    name = 'square'

    commands = ModelOrganizer.commands[:]

    # insert the new run command to the other commands, right before the
    # archiving
    commands.insert(commands.index('archive'), 'preproc')
    commands.insert(commands.index('archive'), 'run')
    commands.insert(commands.index('archive'), 'postproc')

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
        self.logger.info('Saving input data to %s', osp.relpath(infile))
        np.savetxt(infile, data)

    def _modify_preproc(self, parser):
        """Modify the parser for the preprocessing command"""
        parser.update_arg('which', short='w', choices=['sin', 'cos', 'tan'])

    def run(self, **kwargs):
        """
        Run the model

        Parameters
        ----------
        ``**kwargs``
            Any other parameter for the
            :meth:`model_organization.ModelOrganizer.app_main` method
        """
        from calculate import compute
        self.app_main(**kwargs)

        # get the default output name
        output = osp.join(self.exp_config['expdir'], 'output.dat')

        # save the paths in the configuration
        self.exp_config['output'] = output

        # run the model
        data = np.loadtxt(self.exp_config['infile'])
        out = compute(data)
        # save the output
        self.logger.info('Saving output data to %s', osp.relpath(output))
        np.savetxt(output, out)

        # store some additional information in the configuration of the
        # experiment
        self.exp_config['mean'] = mean = float(out.mean())
        self.exp_config['std'] = std = float(out.std())
        self.logger.debug('Mean: %s, Standard deviation: %s', mean, std)

    def postproc(self, close=True, **kwargs):
        """
        Postprocess and visualize the data

        Parameters
        ----------
        close: bool
            Close the figure at the end
        ``**kwargs``
            Any other parameter for the
            :meth:`model_organization.ModelOrganizer.app_main` method
        """
        import matplotlib.pyplot as plt
        import seaborn as sns  # for nice plot styles
        self.app_main(**kwargs)

        # ---- load the data
        indata = np.loadtxt(self.exp_config['infile'])
        outdata = np.loadtxt(self.exp_config['output'])
        x_data = np.linspace(-np.pi, np.pi)

        # ---- make the plot
        fig = plt.figure()
        # plot input data
        plt.plot(x_data, indata, label='input')
        # plot output data
        plt.plot(x_data, outdata, label='squared')
        # draw a legend
        plt.legend()
        # use the description of the experiment as title
        plt.title(self.exp_config.get('description'))

        # ---- save the plot
        self.exp_config['plot'] = ofile = osp.join(self.exp_config['expdir'],
                                                   'plot.png')
        self.logger.info('Saving plot to %s', osp.relpath(ofile))
        fig.savefig(ofile)

        if close:
            plt.close(fig)

    def _modify_postproc(self, parser):
        # The figures if parsed from the command line, should always be closed
        parser.pop_arg('close')


if __name__ == '__main__':
    SquareModelOrganizer.main()
