import ast
import os
import os.path

from setuptools import setup


def get_version():
    module_path = os.path.join(os.path.dirname(__file__), 'logging_spinner.py')
    module_file = open(module_path)
    try:
        module_code = module_file.read()
    finally:
        module_file.close()
    tree = ast.parse(module_code, module_path)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, = node.targets
        if isinstance(target, ast.Name) and target.id == '__version__':
            value = node.value
            if isinstance(value, ast.Str):
                return value.s
            raise ValueError('__version__ is not defined as a string literal')
    raise ValueError('could not find __version__')


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except IOError:
        pass


setup(
    name='logging-spinner',
    version=get_version(),
    description='Non-intrusive spinner through standard logging library',
    long_description=readme(),
    url='https://github.com/dahlia/logging-spinner',
    author='Hong Minhee',
    author_email='hong.minhee' '@' 'gmail.com',
    license='GPLv3 or later',
    py_modules=['logging_spinner'],
    python_requires='>=2.7.0',
    install_requires=['pyspin'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX'
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Logging',
        'Topic :: Terminals',
    ]
)
