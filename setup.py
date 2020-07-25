import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tplot",
    version="0.0.2",
    author="Jeroen Delcour",
    author_email="jeroendelcour@gmail.com",
    description="Create text-based graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeroendelcour/tplot",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["colorama", "numpy"],
    python_requires=">=3.8",
)
