from setuptools import find_packages, setup

setup(
    name="huapir-qqbot-adapter",
    version="1.0.0",
    description="QQBot adapter plugin for huapir",
    author="Internal",
    packages=find_packages(),
    install_requires=["ymbotpy"],
    entry_points={
        "chatgpt_mirai.plugins": [
            "qqbot = im_qqbot_adapter.plugin:QQBotAdapterPlugin"
        ]
    },
)
