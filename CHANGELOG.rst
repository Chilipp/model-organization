v0.1.6
======

Changed
-------
* You can modify the behaviour of the logging via the environment variable
  ``'LOG_' + ModelOrganizer.name.upper()`` (previously, it was
  ``ModelOrganizer.name.capitalize()``)
* The ExperimentsConfig class only loads the configuration when it is directly
  accessed via the ``__getitem__`` method, i.e. via
  ``organizer.config.experiments[exp]``. Conversion to a dictionary, or the
  ``items``, ``values``, ``iteritems``, and ``itervalues`` methods will not
  load the experiment

v0.1.5
======

Added
-----
* Added as_ordereddict method for ExperimentsConfig that avoids a loading of
  all experiments when converting to an OrderedDict


v0.1.4
======

Changed
-------
* Fixed bug that loads all experiments in Python2.7 when initializing a
  ExperimentsConfig

v0.1.3
======

Added
-----
* Added fix_paths and rel_paths method for ProjectConfig to store only the
  relative paths

Changed
-------
* Dump a deepcopy of the configuration when saving the experiment and project
* load all experiments in the info method if the *complete* parameter
  (``'-a'`` flag) is True

v0.1.2
======

Added
-----
* Added changelog

Changed
-------
* The model_organization.config.setup_logging function is now called every
  new initialzation of a model_organizer if no config is provided
