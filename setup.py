from setuptools import setup, find_packages

setup(
    name="wificracker",
    version="2.0.0",
    packages=find_packages(),
    install_requires=["scapy>=2.5.0"],
    entry_points={
        "console_scripts": [
            "wificracker=wificracker.menu:main",
            "wificracker-cli=wificracker.cli:main",
        ]
    },
    python_requires=">=3.9",
)
