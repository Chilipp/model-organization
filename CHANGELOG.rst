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
