import setuptools
import subprocess

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()

version = subprocess.check_output("git describe --abbrev=0 --tag", shell=True).decode()
if version[-2:] == "\n":
    version = version[:-2]

setuptools.setup(
    name="flexpoolapi",
    version=version,
    author="nekusu",
    author_email="nosoynahuel11@gmail.com",
    description="🐍 Pythonic wrapper for Flexpool API v2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nekusu/py-flexpoolapi-v2",
    packages=["flexpoolapi"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
