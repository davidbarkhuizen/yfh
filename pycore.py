import sys
import logging

# -------------------------------------------------------------
# PYTHON VERSION

# initialization
# logging
# config
# platform (runtime, os) checking

def check_min_python_version(min_major_reqd, min_minor_reqd, verbose=True):

	(major, minor, micro, release_level, serial) = sys.version_info

	if verbose:
		print('python version {}.{} installed'.format(major, minor))
		print('python version {}.{} required'.format(min_major_reqd, min_minor_reqd))

	return (major, minor) > (min_major_reqd, min_minor_reqd)

# -------------------------------------------------------------
# LOGGING

DEFAULT_LOG_FORMAT = "%(message)s"
DEFAULT_LOG_LEVEL = logging.INFO 

def configure_logging(log_file_path, log_level=None):

	log_level = log_level if log_level is None else logging.INFO

	logging.basicConfig(filename=log_file_path, level=DEFAULT_LOG_LEVEL, format=DEFAULT_LOG_FORMAT)

def log(s):
	print(s)
	logging.info(s)

# -------------------------------------------------------------

if __name__ == '__main__':

	if not check_min_python_version(3, 5):
		print('bad version')