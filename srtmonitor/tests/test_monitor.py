import os
import shutil
import subprocess as sp
import multiprocessing
import time
from ..monitor import main


class TestMonitor(object):
    @classmethod
    def setup_class(klass):
        import os

        klass.curdir = os.path.dirname(__file__)
        klass.datadir = os.path.join(klass.curdir, 'data')

        klass.config_file = \
            os.path.abspath(os.path.join(klass.datadir, "config.yaml"))

        klass.file_empty_init = \
            os.path.abspath(os.path.join(klass.datadir,
                                         "srt_data_initial.fits"))
        klass.file_empty = \
            os.path.abspath(os.path.join(klass.datadir,
                                         "srt_data.fits"))
        klass.file_empty_hdf5 = \
            os.path.abspath(os.path.join(klass.datadir,
                                         "srt_data.hdf5"))
        klass.file_empty_pdf0 = \
            os.path.abspath(os.path.join(klass.datadir,
                                         "srt_data_0.pdf"))
        klass.file_empty_pdf1 = \
            os.path.abspath(os.path.join(klass.datadir,
                                         "srt_data_1.pdf"))
        if os.path.exists(klass.file_empty_pdf0):
            os.unlink(klass.file_empty_pdf0)
        if os.path.exists(klass.file_empty_pdf1):
            os.unlink(klass.file_empty_pdf1)

    def test_monitor_installed(self):
        sp.check_call('SDTpreprocess -h'.split())

    def test_all(self):
        def process():
            main([self.datadir, '--test'])

        w = multiprocessing.Process(name='worker', target=process)
        w.start()
        time.sleep(1)

        sp.check_call('cp {} {}'.format(self.file_empty_init,
                                        self.file_empty).split())

        time.sleep(5)

        assert os.path.exists(self.file_empty_pdf0)
        assert os.path.exists(self.file_empty_pdf1)
        w.terminate()

    @classmethod
    def teardown_class(klass):
        if os.path.exists(klass.file_empty):
            os.unlink(klass.file_empty)
        if os.path.exists(klass.file_empty_hdf5):
            os.unlink(klass.file_empty_hdf5)
        if os.path.exists(klass.file_empty_pdf0):
            os.unlink(klass.file_empty_pdf0)
        if os.path.exists(klass.file_empty_pdf1):
            os.unlink(klass.file_empty_pdf1)
