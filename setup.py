from setuptools import setup, find_packages

setup(
    name="mazegroup",
    version="0.0.1",
    description="MazeGroup.py is an general prupose library for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Genius_um & Rayanis55",
    python_requires=">=3.9",
    url="https://github.com/Geniusum/mazegroup.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
