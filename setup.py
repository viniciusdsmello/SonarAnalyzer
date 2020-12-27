from setuptools import setup, find_packages

REQUIREMENTS = [
    "numpy==1.19.4",
    "streamlit==0.72.0",
    "scipy==1.5.4",
    "soundfile==0.10.2",
    "matplotlib==3.3.3"
]

s = setup(  # pylint: disable=invalid-name
    name="sonar-analyzer",
    version="20201226.0",
    description="""Sonar Analyzer is an app created with streamlit in order to analyze Passive Sonar Signals""",
    url="https://github.com/viniciusdsmello/sonar-analyzer",
    author="Vinícius Mello",
    author_email="viniciusdsmello@poli.ufrj.br",
    install_requires=REQUIREMENTS,
    python_requires=">= 3.7",
    zip_safe=False,
)
