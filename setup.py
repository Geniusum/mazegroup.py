from setuptools import setup, find_packages

setup(
    name="mazegroup",
    version="0.1.4.1",
    description="MazeGroup.py is an general prupose library for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Genius_um",
    python_requires=">=3.9",
    url="https://github.com/Geniusum/mazegroup.py",
    packages=find_packages(),#["mazegroup", "mazegroup/cli", "mazegroup/echo", "mazegroup/saves"], # find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'mg = mazegroup.cli:main',
            'mazegroup = mazegroup.cli:main'
        ]
    },
    install_requires=[
        "cryptography",
        "colorama",
        "keyboard"
    ]
)
