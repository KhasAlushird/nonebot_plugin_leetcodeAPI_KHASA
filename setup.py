from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nonebot_plugin_leetcodeAPI_KHASA",
    version="0.3.7",
    description="A Nonebot plugin for interacting with LeetCode (Using API made by alfaarghya)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KhasAlushird",
    author_email="KhasAlushird@sjtu.edu.cn",
    url="https://github.com/KhasAlushird/nonebot_plugin_leetcodeAPI_KHASA",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "nonebot2>=2.2.0",
        "nonebot-adapter-onebot>=2.2.0",
        "nonebot-plugin-htmlrender>=0.1.0",
        "httpx>=0.21.0",
        "jinja2>=3.0.0",
        "nonebot-plugin-localstore>=0.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)