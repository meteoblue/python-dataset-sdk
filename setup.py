import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meteoblue-dataset-sdk", # Replace with your own username
    version="0.0.2",
    author="Jonas Wolff",
    author_email="jonas.wolff@meteoblue.com",
    description="Provides easy access to meteoblue dataset sdk.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meteoblue/python-dataset-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
