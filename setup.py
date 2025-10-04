from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "ANIME-RECOMMENDER-SYSTEM",
    version = "0.1",
    author ="Meenatchi Sundari",
    author_email = "meenatchisundarimuthirulappan@gmail.com",
    description = "An Anime Recommender System using Grafna Cloud , Chroma DB, Groq and HuggingFace",
    packages = find_packages(),
    install_requires = requirements,
)