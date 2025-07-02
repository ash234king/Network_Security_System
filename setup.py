from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r',encoding='utf-8') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and not requirement.startswith("#") and requirement!='-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_list               

print(get_requirements)

setup(
    name="Network Security",
    version="0.0.1",
    author="Yashvardhan Singh",
    author_email="yashvardhansingh9532@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)