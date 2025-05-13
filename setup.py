import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="talosbot",
    version="0.1.0",
    author="Sergio Perez Rodriguez",
    author_email="sergiopr89@gmail.com",
    description="Talos chatops framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergiopr89/talosbot",
    packages=setuptools.find_packages(),
    install_requires=[
        "jsonschema",
        "python-telegram-bot",
        "sentence-transformers",
        "spacy",
        "spacy-transformers",
        "spacy-lookups-data",
    ],
    entry_points={
        "console_scripts": [
            "talos=talosbot.cli.entrypoint:TalosCLI.run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
