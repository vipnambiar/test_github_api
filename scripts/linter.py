"""
linter.py
---------
Script to do automated linting
"""


import abc
from datetime import datetime as dt
import os
from subprocess import Popen, PIPE, CalledProcessError
import logging
import scripts.api_wrapper as wrapper


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Linter(metaclass=abc.ABCMeta):
    """
    Abstract class for linters
    """
    @abc.abstractmethod
    def lint(self, filename, *args, **kwargs):
        """
        Performs the lint on the filename
        """
        return

    @abc.abstractmethod
    def report(self):
        """
        Generate the lint report
        """
        return


class Pyflake(object):
    """
    Implements Pyflake linter
    """
    def __init__(self, executable):
        self.executable = executable
        self.result = ''
        self._lintfile = ''

    def lint(self, filename):
        """
        Run Pyflakes on the given filename
        :param filename:
        :return:
        """
        self._lintfile = filename
        cmd = [self.executable, self._lintfile]
        try:
            process = Popen(cmd, stderr=PIPE, stdout=PIPE)
            output, error = process.communicate()
        except CalledProcessError as err:
            logger.error(err)
        else:
            if output:
                logger.info(output.decode(encoding='utf-8'))
                self.result = output.decode(encoding='utf-8')
            elif error:
                logger.error(error)
        return self.result or 0

    def report(self, filename=None):
        """
        Generate report for the last pyflakes execution
        :param filename:
        :return:
        """
        if not self._lintfile:
            print("lint not yet run, so nothing to report!")
            return
        if not filename:
            filename = '%s.txt' % os.path.basename(self._lintfile).strip('.py')

        file_path = os.path.join(os.path.dirname(__file__),
                                 os.path.pardir,
                                 'reports',
                                 'pyflakes',
                                 filename)
        file_path = os.path.normpath(file_path)
        with open(file_path, "w") as file_handler:
            begin = dt.now().strftime('%b %d, %Y %H:%M')
            file_handler.write("Pyflakes report generated on %s\n" % begin)
            file_handler.write("="*47)
            file_handler.write("\n\nFilename: %s\n\n" % os.path.basename(self._lintfile))
            file_handler.write(self.result)
            file_handler.write("\n----- End -----\n")
        return


Linter.register(Pyflake)

if __name__ == '__main__':
    flake = Pyflake("pyflakes")
    flake.lint("/home/vipin/Projects/jiva_buildout/src/jiva.sre.web/Products/ZeSentinel/ZeSentinelModel.py")
    flake.report()