from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nonebot_plugin_leetcodeAPI_KHASA",
    version="0.2.8",
    description="A Nonebot plugin for interacting with LeetCode (Using API made by alfaarghya)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KhasAlushird",
    author_email="KhasAlushird@sjtu.edu.cn",
    url="https://github.com/KhasAlushird/nonebot_plugin_leetcodeAPI_KHASA",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "nonebot2",
        "nonebot-adapter-onebot",
        "nonebot-plugin-htmlrender",
        "httpx",
        "jinja2",
        "nonebot-plugin-localstore",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)