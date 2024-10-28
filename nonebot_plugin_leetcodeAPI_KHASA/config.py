from nonebot import get_plugin_config
from nonebot_plugin_localstore import get_data_dir
from pydantic import BaseModel

class Config(BaseModel):
    ONLY_SHOW_FREQUENTLY_USED_COMMANDS: bool = False
    API_BASE_URL: str = "https://alfa-leetcode-api.onrender.com"
    DEFAULT_DISCUSSION_NUM: int = 3
    MAX_DISCUSSION_NUM: int = 10
    DEFAULT_PROBLEM_NUM: int = 2
    MAX_PROBLEM_NUM: int = 5
    SUBMISSION_LIMIT: int = 5
    CALENDAR_LIMIT: int = 7

# 从 Nonebot 的配置中获取插件的配置项
conf = get_plugin_config(Config)

# 设置数据目录
DATA_PATH = get_data_dir("nonebot_plugin_leetcodeAPI_KHASA")