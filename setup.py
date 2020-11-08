import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="makeup_service_client",
    version="1.0.0",
    author="Artem Baraniuk",
    author_email="artem.baranyuk@gmail.com",
    description="Client for makeup service application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Art95/makeup_service_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'flask-socketio',
        'numpy',
        'eventlet'
    ]
)
