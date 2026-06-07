from setuptools import setup, find_packages

setup(
    name="factorialhr-j",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "pytest>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "factorialhr-j=factorialhr_j.cli:cli",
        ],
    },
    author="jpromocion",
    description="Herramienta CLI para interactuar con la API REST de Factorial HR para control horario.",
    python_requires=">=3.12",
)