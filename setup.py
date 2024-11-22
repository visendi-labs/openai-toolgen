from setuptools import setup, find_packages

setup(
    name="openai-toolgen",
    version="0.3.1",
    author="Rasmus Nordström",
    author_email="nordstrom.rasmus@gmail.com",
    description="A library for generating tools for OpenAI projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/visendi-labs/openai-toolgen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
