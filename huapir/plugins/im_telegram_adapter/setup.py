from setuptools import find_packages, setup

setup(
    name="huapir-telegram-adapter",
    version="1.0.0",
    description="Telegram adapter plugin for huapir",
    author="Internal",
    packages=find_packages(),
    install_requires=["python-telegram-bot", "telegramify-markdown"],
    entry_points={
        "chatgpt_mirai.plugins": [
            "telegram = im_telegram_adapter.plugin:TelegramAdapterPlugin"
        ]
    },
)
