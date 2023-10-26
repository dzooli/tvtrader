import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

setuptools.setup(
    name="tvt_agents",
    version="0.1.0",
    author="Zoltan Fabian",
    author_email="zoltan.dzooli.fabian@gmail.com",
    packages=["tvt_agents"],
    entry_points={
        "console_scripts": ["tvtrader_distributor = tvt_agents.__main__:main"]
    },
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
    ],
    description="Distributed agents framework for the TvTrader suite",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/dzooli/tvtrader",
    license="MIT",
    python_requires=">=3.11",
    install_requires=["aio_pika", "ws4py", "wsaccel", "click", "click-default-group"],
)
