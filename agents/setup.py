import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="tvt_agents",
    version="0.1.0",
    author="Zoltan Fabian",
    author_email="zoltan.dzooli.fabian@gmail.com",
    packages=["tvt_agents"],
    description="Agents for the TvTrader suite",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/dzooli/tvtrader",
    license="MIT",
    python_requires=">=3.8",
    install_requires=["aio_pika", "ws4py", "wsaccel"],
)
