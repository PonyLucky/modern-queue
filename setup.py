import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modernqueue",
    version="1.0.0",
    author="Margot Louis",
    description="A modern queue in a multithreaded environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["modernqueue"],
    package_dir={'':'modernqueue/src'},
    install_requires=[],
    home_page="https://github.com/PonyLucky/modern-queue",
    keywords=["thread", "queue", "modern"]
)