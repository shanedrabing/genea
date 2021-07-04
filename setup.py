import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="genea",
    version="0.0.0",
    author="Shane Drabing",
    author_email="shane.drabing@gmail.com",
    packages=setuptools.find_packages(),
    url="https://github.com/shanedrabing/genea",
    description="Scrape parent-child relationships from Wikipedia infoboxes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    data_files=[
        ("", ["LICENSE"])
    ],
    install_requires=[
        "opencv-python", "numpy"
    ]
)
