.. currentmodule:: model_organization

.. _square_example:

Starting example: square
------------------------
This small example will you demonstrate the basic methodology how our package
works. We use a very simple model represented by only one function that squares
the input data and we create a project to investigate trigonmetric functions
(sine, cosine, etc.).

.. only:: builder_html

    You can also :download:`download the complete script square.py <square.py>`.

So let's define our model function

.. literalinclude:: calculate.py

and save it in a file called ``'calculate.py'`` file. This function runs
only in python and does not know anything about where the input is from and
where it is saved.

We start from the pure :class:`ModelOrganizer` to manage our model named
*square*

.. literalinclude:: square_sparse.py

and save it in the file called ``'square.py'``. If we run our model from the
command line, (for technical reasons we run it here from inside IPython), we
see already several preconfigured commands

.. ipython::

    @suppress
    In [1]: import shutil, os, os.path as  osp, tempfile, stat
       ...: shutil.copyfile('square_sparse.py', 'square.py')
       ...: st = os.stat('square.py')
       ...: os.chmod('square.py', st.st_mode | stat.S_IEXEC)
       ...: os.environ['SQUARECONFIGDIR'] = tempfile.mkdtemp(prefix='square_')
       ...: if osp.exists('trigo'):
       ...:     shutil.rmtree('trigo')

    In [1]: !./square.py -h

So to setup our new project, we use the :meth:`~ModelOrganizer.setup` method

.. ipython::

    In [2]: !./square.py setup . -p trigo

And we initialize one experiment for the sine, one for the cosine, and one for
the tangent functions

.. ipython::

    In [3]: !./square.py -id sine init -d "Squared Sine"

    In [4]: !./square.py -id cosine init -d "Squared Cosine"

    In [5]: !./square.py -id tangent init -d "Squared Tangent"

Now of course, we, need the input data, so we enhance our
:class:`ModelOrganizer` subclass with a preprocess method

.. literalinclude:: square_preproc.py

The code should be more or less self explanatory. We start with the
:meth:`ModelOrganizer.app_main` method which chooses the right experiment from
the given `id` parameter. The we use the :any:`numpy.sin`, :any:`numpy.cos` and
:any:`numpy.tan` functions from the numpy module and calculate the data from
:math:`-\pi` to :math:`\pi`.

Finally we store it to an input file inside the experiment directory.

.. hint::

    If you want to see the configuration values in the experiment config, use
    the :meth:`~ModelOrganizer.info` and the
    :meth:`get-value <ModelOrganizer.get_value>` commands

    .. ipython::

        In [6]: !./square.py info

        In [7]: !./square.py get-value expdir

In the ``_modify_preproc`` section, we update argument of the ``--which``
argument to include a shorter ``-w`` command and some choices (see the
:class:`funcargparse.FuncArgParser` class for more information). Note the style
of the documentation of the ``preproc`` method. We follow the
`numpy documentation guidelines`_ such that the
:class:`funcargparse.FuncArgParser` can extract the docstring. Our new command
now has been translated to a command line argument:

.. ipython::

    @suppress
    In [8]: shutil.copyfile('square_preproc.py', 'square.py')

    In [8]: !./square.py preproc -h

and we can use it to create our input data

.. ipython::

    In [9]: !./square.py -id sine preproc

    In [10]: !./square.py -id cosine preproc -w cos

    # by default, the last created experiment (tangent) is used so the -id
    # argument is not necessary
    In [11]: !./square.py preproc -w tan

Finally, we include a ``run`` command that uses our input data of the given
experiment and for our model

.. literalinclude:: square_full.py
   :pyobject: SquareModelOrganizer.run

and we run it

.. ipython::

    @suppress
    In [12]: shutil.copyfile('square_full.py', 'square.py')

    In [12]: !./square.py -v -id sine run

    In [13]: !./square.py -v -id cosine run

    In [14]: !./square.py -v run

Now, finally, let's create a postproc command that visualizes our data

.. literalinclude:: square_full.py
   :pyobject: SquareModelOrganizer.postproc

.. ipython::

    In [15]: !./square.py -v -id sine postproc

    In [16]: !./square.py -v -id cosine postproc

    In [17]: !./square.py -v postproc

    @suppress
    In [18]: if not osp.exists('_static'):
       ....:     os.makedirs('_static')
       ....: os.rename('trigo/experiments/tangent/plot.png',
       ....:           '_static/tangent.png')

.. image:: ./_static/tangent.png
    :alt: Result image for tangent experiment

Finally, we can archive our project to save disc space

.. ipython::

    In [18]: !./square.py archive -p trigo -rm

.. hint::

    You can also do everything from above in one line by
    :ref:`chaining the subparser commands <funcargparse:chain_subparsers>`.

    .. ipython::

        @suppress
        In [19]: !./square.py remove -ay -ap

        In [19]: !./square.py -v -id sine setup . -p trigo init -d "Squared Sine" preproc run postproc archive -p trigo -rm

        @suppress
        In [19]: !./square.py remove -ay -ap

.. _numpy documentation guidelines: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
