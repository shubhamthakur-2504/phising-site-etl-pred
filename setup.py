from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements() -> List[str]:
    requirements = []
    try:
        with open("requirements.txt", "r") as file :
            line = file.readlines()
            for requirement in line:
                requirement = requirement.strip()
                if requirement == HYPEN_E_DOT:
                    continue
                requirements.append(requirement)
    except Exception as e:
        raise e
    return requirements

setup(
    name='NetworkSecurity',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
   
    author='shubhamthakur-2504',
    author_email='shubhamthakur60278@gmail.com',
    python_requires='>=3.6',
)
