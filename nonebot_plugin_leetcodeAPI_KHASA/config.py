from nonebot import get_plugin_config
from nonebot_plugin_localstore import get_data_dir
from pydantic import BaseModel

class Config(BaseModel):
    only_show_frequently_used_commands: bool = False
    api_base_url: str = "https://alfa-leetcode-api.onrender.com"
    default_discussion_num: int = 3
    max_discussion_num: int = 10
    default_problem_num: int = 2
    max_problem_num: int = 5
    submission_limit: int = 5
    calendar_limit: int = 7

# 从 Nonebot 的配置中获取插件的配置项
conf = get_plugin_config(Config)

# 设置数据目录
DATA_PATH = get_data_dir("nonebot_plugin_leetcodeAPI_KHASA")