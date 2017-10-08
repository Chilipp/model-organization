.. currentmodule:: model_organization

.. _getting_started:


Getting started
===============

Motivation
----------
Developing computational models can be quite a mess in terms of the file and
configuration management. Therefore most of the (climate) models are
accompanied with some kind of framework to guide the user
through their piece of software. Those however can be very complex and every
model follows it's own strategy. Therefore this package tries to organize the
procedure focusing at the end-user by providing an outer framework that allows
the user to interfere with the model from the command line.

How does the package work
-------------------------
When doing research, we usually have a specific (funding) *project* that
requests multiple runs (*experiments*) of our model. The framework of the
model-organization package mirrors this basic structure: It works with
projects, each project contains several experiments. The package keeps track of
your projects and experiments and saves the configuration in separate
configuration (.yml) files.


Configuration files
*******************
All the paths to the projects are stored in the configuration directory
determined by the :attr:`~ModelOrganizer.name` attribute of your model (see the
:func:`config.get_configdir` function). By default, it's (on linux and mac)
``"~/.config/<name>"``, but you can determine it via the global
``<NAME>CONFIGDIR`` variable, where ``<name>`` must be replaced by the
:attr:`ModelOrganizer.name` of your model. Our
:ref:`example below <square_example>` would store the
configuration files in ``"$HOME/.config/square"`` and the corresponding
environment variable is ``SQUARECONFIGDIR``.

The above directory contains 3 files:

globals.yml
    The global configuration that should be applicable to all projects
projects.yml
    A mapping from project name to project directory
experiments.yml
    The list of experiments

Additional, each project directory contains a ``'.project'`` directory where
each experiment is represented by one yaml file (e.g. ``'sine.yml'`` in
our :ref:`example <square_example>`) and the
project configuration is stored in ``'.project/.project.yml'``. To get the
specific name of the configuration file, you can also use the `exp_path`
parameter of the :meth:`~ModelOrganizer.info` method or the command
:ref:`command-model-info` respectively.


Creating your own :class:`ModelOrganizer`
*****************************************
The :class:`ModelOrganizer` class is designed for subclassing in order to fit
to your specific model. See the incode documentation of the
:class:`ModelOrganizer` for more information.


Using the command line argument
*******************************
Each method that is listed in the :attr:`~ModelOrganizer.commands` attribute
is implemented as a subparser for the for the main command line utility (see
our :ref:`square_example`). If you subclassed the model organizer, you can use
the :meth:`~ModelOrganizer.main` method to run your model. You can do
(for example) as we did in the :ref:`example <square_example>` via::

    if __name__ == '__main__':
        SquareModelOrganizer.main()

You can see, the results of this methodology in the :ref:`command_line_api`.


Parallel usage
--------------
The usage of configuration files includes some limitations because the
configuration cannot be accessed in parallel. Hence, you should not
:meth:`setup projects <ModelOrganizer.setup>` and
:meth:`initialize experiments <ModelOrganizer.init>` in parallel. The same
for the archiving method. However, the ``run``, ``postproc`` and
``preproc`` method as we implemented in in our :ref:`example <square_example>`,
could be used in parallel.
