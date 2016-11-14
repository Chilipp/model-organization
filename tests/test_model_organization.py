"""Test module for the :mod:`gwgen.main` module"""
import os
import os.path as osp
import unittest
import tempfile
import shutil
import six
import copy
from collections import OrderedDict
from model_organization import ModelOrganizer


class OrganizerTest(unittest.TestCase):
    """Test the :class:`model_organization.ModelOrganizer` class"""

    test_dir = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix='tmp_model_organizer_test')
        os.environ['MODEL_ORGANIZERCONFIGDIR'] = self.config_dir = osp.join(
            self.test_dir, 'config')
        if not osp.exists(self.test_dir):
            os.makedirs(self.test_dir)
        if not osp.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.organizer = ModelOrganizer()

    def tearDown(self):
        if osp.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if osp.exists(self.config_dir):
            shutil.rmtree(self.config_dir)
        del self.organizer
        del self.test_dir
        del self.config_dir

    def _test_setup(self):
        """Test the setup of a project. We make this method private such that
        it is not called everytime"""
        self.organizer.setup(self.test_dir, 'test_project0', link=False)
        mpath = osp.join(self.test_dir, 'test_project0')
        self.assertTrue(osp.isdir(mpath))
        self.assertIn('test_project0', self.organizer.config.projects)

        # createa new project and let it automatically assign the name
        self.organizer.setup(self.test_dir)
        mpath = osp.join(self.test_dir, 'test_project1')
        self.assertTrue(osp.isdir(mpath))
        self.assertIn('test_project1', self.organizer.config.projects)

    def _test_init(self):
        """Test the intialization of a new experiment. We make this method
        private such that it is not called everytime"""
        self.organizer.setup(self.test_dir)
        projectname = self.organizer.projectname
        self.organizer.init(experiment='testexp0')
        expdir = osp.join(self.test_dir, projectname, 'experiments',
                          'testexp0')
        self.assertTrue(osp.exists(expdir),
                        msg='Experiment directory %s does not exist!' % expdir)
        self.assertIn('testexp0', self.organizer.config.experiments)

        # test without argument
        self.organizer.setup(self.test_dir)
        projectname = self.organizer.projectname
        self.organizer.init(experiment=None)
        expdir = osp.join(self.test_dir, projectname, 'experiments',
                          'testexp1')
        self.assertTrue(osp.exists(expdir),
                        msg='Experiment directory %s does not exist!' % expdir)
        self.assertIn('testexp1', self.organizer.config.experiments)

    def test_setup(self):
        """Reimplemented to do the test here"""
        self._test_setup()

    def test_init(self):
        """Reimplemented to do the test here"""
        self._test_init()

    def test_set_value(self):
        """Test set_value command"""
        self._test_init()
        self.organizer.parse_args(['set-value', 'test=1', 'test2=test'])
        exp_config = self.organizer.exp_config
        self.assertEqual(exp_config['test'], '1')
        self.assertEqual(exp_config['test2'], 'test')
        self.organizer.parse_args(['set-value', 'testd.okay=12', '-dt', 'int'])
        self.assertEqual(exp_config['testd']['okay'], 12)

    def test_get_value(self):
        """Test get_value command"""
        self.test_set_value()
        self.organizer.print_ = str
        val = self.organizer.parse_args(['get-value', 'testd.okay']).get_value
        self.assertEqual(int(val), self.organizer.exp_config['testd']['okay'])

    def test_del_value(self):
        """Test del_value command"""
        self.test_set_value()
        self.organizer.parse_args(['del-value', 'test'])
        self.assertNotIn('test', self.organizer.exp_config)

    def test_info(self):
        from model_organization.config import ordered_yaml_load
        self._test_init()
        organizer = self.organizer
        organizer.print_ = str
        # test exp_config
        d = ordered_yaml_load(organizer.parse_args(['info', '-nf']).info)
        self.assertEqual(d.pop('id'), organizer.experiment)
        self.assertEqual(d, self.organizer.rel_paths(organizer.exp_config))

        # test project_config
        d = ordered_yaml_load(organizer.parse_args(['info', '-P', '-nf']).info)
        self.assertEqual(d, organizer.project_config)

        # test global config
        d = ordered_yaml_load(organizer.parse_args(['info', '-g', '-nf']).info)
        self.assertEqual(d, organizer.global_config)

        # test all
        organizer.init(new=True)
        d = ordered_yaml_load(organizer.parse_args(['info', '-a']).info)
        self.assertEqual(d, organizer.config.experiments)

        # test if the projectname argument works
        projectname = organizer.projectname
        organizer.setup(self.test_dir)  # make a new project the current one
        self.assertNotEqual(projectname, organizer.projectname,
                            msg='Projectnames should differ after setup!')
        # test project_config
        d = ordered_yaml_load(organizer.parse_args(
            ['info', '-P', '-p', projectname, '-nf']).info)
        self.assertEqual(d, organizer.config.projects[projectname])

        # test file names
        self.organizer.config.save()
        projectname = self.organizer.exp_config['project']
        self.assertEqual(self.organizer.info(exp_path=True),
                         osp.join(self.test_dir, projectname,
                                  '.project',
                                  self.organizer.experiment + '.yml'))
        self.assertEqual(self.organizer.info(project_path=True),
                         osp.join(self.test_dir, self.organizer.projectname,
                                  '.project', '.project.yml'))
        self.assertEqual(self.organizer.info(global_path=True),
                         osp.join(self.config_dir, 'globals.yml'))

    def test_archive(self):
        """Test the archiving command"""
        self._test_init()
        organizer = self.organizer
        organizer.project_config['archived'] = {}
        exps = copy.deepcopy(self.organizer.config.experiments)
        projects = copy.deepcopy(self.organizer.config.projects)

        projectname = organizer.projectname
        project_root = self.organizer.project_config['root']
        experiment = organizer.experiment
        for fmt in ['tar', 'zip']:
            # make archive
            organizer.archive(self.test_dir, fmt=fmt, rm_project=True)
            archive_name = osp.join(self.test_dir, projectname + '.' + fmt)
            self.assertTrue(osp.exists(archive_name), msg=(
                "Archive file %s is missing!"))
            self.assertNotEqual(organizer.config.experiments, exps)
            self.assertTrue(organizer.is_archived(experiment))
            self.assertFalse(osp.exists(project_root),
                             msg='%s exists but should not!' % project_root)

            # unarchive
            organizer.unarchive(experiment=experiment, match=True,
                                complete=True)
            for cmd in ['archive', 'unarchive']:
                organizer.config.experiments[experiment]['timestamps'].pop(
                    cmd, None)
            self.assertEqual(organizer.config.experiments, exps)
            self.assertEqual(organizer.config.projects, projects)
            self.assertFalse(organizer.is_archived(experiment))
            self.assertTrue(osp.exists(project_root),
                            msg='%s does not exist!' % project_root)

    def test_remove(self):
        """Test the removement of an experiment"""
        self._test_init()
        organizer = self.organizer
        experiment = organizer.experiment
        project = self.organizer.projectname
        root = self.organizer.project_config['root']
        exp_dir = organizer.fix_paths(organizer.exp_config)['expdir']
        self.organizer.parse_args(['-id', experiment, 'remove', '-y'])
        self.assertNotIn(experiment, organizer.config.experiments)
        self.assertFalse(osp.exists(exp_dir),
                         msg='%s exists but should not!' % exp_dir)
        self.assertTrue(osp.exists(root),
                        msg='%s does not exist!' % root)

        self.organizer.parse_args(['remove', '-a', '-p', project, '-y'])
        self.assertNotIn(project, organizer.config.projects)
        self.assertFalse(osp.exists(root),
                         msg='%s exists but should not!' % root)

    def test_save(self):
        """Test the saving and loading of the configuration"""
        self._test_init()
        self.organizer.setup(self.test_dir)
        self.organizer.init()
        d = copy.deepcopy(OrderedDict(self.organizer.config.experiments))
        self.organizer.config.save()
        organizer = ModelOrganizer()
        for key, val in d.items():
            self.assertEqual(organizer.config.experiments[key], val)

    def test_square(self):
        """Test the square model from the documentation"""
        import subprocess as spr
        import sys
        os.environ['SQUARECONFIGDIR'] = self.config_dir
        script = osp.join(osp.dirname(__file__), 'square.py')
        spr.call(
            [sys.executable, script] +
            ('-v -id sine setup %s -p trigo init preproc run postproc '
             'archive -p trigo -rm remove -ay' % self.test_dir).split())
        self.assertTrue(osp.exists('trigo.tar'), msg='Archive not found!')
        project_dir = osp.join(self.test_dir, 'trigo')
        self.assertFalse(osp.exists(project_dir),
                         msg='Project directory %s unexpectedly found!' % (
                            project_dir))
        spr.call(
            [sys.executable] +
            (script + ' -v -id sine unarchive -f trigo.tar').split())
        self.assertTrue(osp.exists(project_dir),
                        msg=project_dir + ' not found!')
        os.remove('trigo.tar')

    def test_app_main(self):
        """Test the :meth:`ModelOrganizer.app_main` method"""
        self._test_init()
        organizer = self.organizer
        organizer.init(experiment='test_main4')
        organizer.init(experiment='dummy')
        organizer.init(experiment='dummy2')

        # test regex
        organizer.app_main(experiment='main', match=True)
        self.assertEqual(organizer.experiment, 'test_main4')

        # test error
        if six.PY3:
            with self.assertRaisesRegex(ValueError, 'dummy2'):
                organizer.app_main(experiment='dummy', match=True)

        self.organizer.app_main('main', match=True, new=True)
        self.assertEqual(organizer.experiment, 'test_main5')

    def test_config(self):
        """Test whether the ExperimentConfig works correctly"""
        self._test_init()
        exp = self.organizer.experiment
        self.organizer.config.save()
        organizer2 = self.organizer.__class__()
        # the experiment config should not have been loaded
        self.assertIsInstance(dict(organizer2.config.experiments)[exp],
                              six.string_types)


if __name__ == '__main__':
    unittest.main()
