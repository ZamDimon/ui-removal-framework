from setuptools import find_packages, setup

setup(
    name="geo deep fill",
    packages=[
        "deep_fill/model",
        "deep_fill/utils",
        "deep_fill/cleaner",
    ],
    package_dir={
        "deep_fill/cleaner": "./cleaner",
        "deep_fill/utils": "./utils",
        "deep_fill/model": "./model",
    },
    version="0.2.2",
    description="This lib is used to  detect XXX,  analyze XXX and  do XXX",
    author="DL",
    install_requires=[],
    setup_requires=["pytest-runner"],
)
