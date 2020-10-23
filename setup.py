import setuptools
import re

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open("teleNex/__init__.py", 'r', encoding="utf-8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name                          = 'TeleNex',
    version                       = version,
    author                        = 'iNex',
    author_email                  = 'inex552@gmail.com',
    description                   = 'TeleNex is a Python library for easy making telegram bots',
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = 'https://github.com/inex550/TeleNex',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires='>=3.6'
)