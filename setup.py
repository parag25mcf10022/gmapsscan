from setuptools import setup, find_packages

setup(
    name="gmapsscan",
    version="1.1.0",
    author="Parag",
    packages=find_packages(),
    install_requires=["requests>=2.31.0"],
    entry_points={
        "console_scripts": [
            "gmapsscan=gmapsscan_pkg.main:run_cli", # Points to the new folder name
        ],
    },
)
