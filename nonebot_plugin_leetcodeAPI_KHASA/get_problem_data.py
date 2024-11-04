import os
import random
import httpx
from nonebot.log import logger
import json
from jinja2 import Environment, FileSystemLoader
from .config import conf
import jinja2
from pathlib import Path

templates_path = Path(__file__).resolve().parent / "templates"
if not templates_path.exists():
    raise FileNotFoundError(f"模板文件夹 {templates_path} 不存在，请确保模板文件夹存在。")
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
)
API_BASE_URL = conf.api_base_url
DEFAULT_PROBLEM_NUM = conf.default_problem_num
MAX_PROBLEM_NUM = conf.max_problem_num


def render_problem_html(problem_data, command_type):
    '''渲染题目数据为HTML'''
    template = env.get_template("problem_template.html")
    link_data = ''
    if command_type == "daily":
        link_data = problem_data.get('questionLink', 'N/A')
    elif command_type == "selected":
        link_data = problem_data.get('link', 'N/A')
    html_content = template.render(
        questionTitle=problem_data.get('questionTitle', 'N/A'),
        difficulty=problem_data.get('difficulty', 'N/A'),
        description=problem_data.get('question', 'N/A'),
        exampleTestcases=problem_data.get('exampleTestcases', 'N/A'),
        hints=problem_data.get('hints', []),
        topicTags=problem_data.get('topicTags', []),
        questionLink=link_data
    )
    return [html_content, link_data]


def render_problems_html(problems_data):
    '''渲染问题数据为HTML(顺便获取链接)'''
    template = env.get_template("many_problems_template.html")
    the_problems = problems_data.get('problemsetQuestionList', [])
    html_content = template.render(
        problems=the_problems
    )
    linklist = []
    namelist = []
    for problem in the_problems:
        problem_name = problem.get('titleSlug', 'N/A')
        namelist.append(problem_name)
        linklist.append(get_url_by_name(problem_name))
    return [html_content, linklist, namelist]


async def get_daily_problem():
    '''获取每日一题'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/daily")
            res.raise_for_status()
            daily_data = res.json()
            logger.info("每日一题获取成功")
            return daily_data
    except Exception as e:
        logger.error("每日一题获取失败喵~", e)
        raise e


def _convert_string(input_str: str):
    stripped_str = input_str.strip()
    lower_str = stripped_str.lower()
    result_str = lower_str.replace(" ", "-")
    return result_str


async def get_selected_problem(title_slug):
    '''获取选定问题'''
    the_title_slug = _convert_string(title_slug)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/select?titleSlug={the_title_slug}")
            res.raise_for_status()
            selected_data = res.json()
            logger.info("指定题目获取成功")
            return selected_data
    except Exception as e:
        logger.error("指定题目获取失败喵~", e)
        raise e


async def get_problems(limit):
    '''获取指定数量的随机问题'''
    if limit <= 0:
        limit = DEFAULT_PROBLEM_NUM
    if limit > MAX_PROBLEM_NUM:
        limit = MAX_PROBLEM_NUM
    try:
        async with httpx.AsyncClient() as client:
            # 获取总问题数量
            res = await client.get(f"{API_BASE_URL}/problems?limit=1")
            res.raise_for_status()
            total_q_num = int(res.json().get('totalQuestions', 0))
            if total_q_num == 0:
                raise Exception("总问题数量为0")

            # 计算随机跳过的数量
            random_skip_max = total_q_num + 1 - limit
            random_skip_num = random.randint(0, random_skip_max)

            # 获取指定数量的问题
            res = await client.get(f"{API_BASE_URL}/problems?limit={limit}&skip={random_skip_num}")
            res.raise_for_status()
            problems_data = res.json()
            logger.info("问题获取成功")
            return problems_data
    except httpx.RequestError as e:
        logger.error(f"请求错误: {e}")
        raise e
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP状态错误: {e.response.status_code}")
        raise e
    except Exception as e:
        logger.error(f"问题获取失败喵~: {e}")
        raise e


async def get_url_by_name(problem_name):
    '''根据题目名获取链接'''
    the_problem_name = _convert_string(problem_name)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/select?titleSlug={the_problem_name}")
            res.raise_for_status()
            selected_data = res.json()
            return selected_data.get('link', 'N/A')
    except Exception as e:
        logger.error("获取链接失败喵~", e)
        raise e


async def get_problems_with_tags(tags, limit):
    '''获取带有指定标签的问题'''
    if limit <= 0:
        limit = DEFAULT_PROBLEM_NUM
    if limit > MAX_PROBLEM_NUM:
        limit = MAX_PROBLEM_NUM
    try:
        tags_str = '+'.join(tags)
        async with httpx.AsyncClient() as client:
            # 获取总问题数量
            res = await client.get(f"{API_BASE_URL}/problems?tags={tags_str}&limit=1")
            res.raise_for_status()
            total_q_num = int(res.json().get('totalQuestions', 0))
            if total_q_num == 0:
                raise Exception("总问题数量为0")

            # 计算随机跳过的数量
            random_skip_max = total_q_num + 1 - limit
            random_skip_num = random.randint(0, random_skip_max)

            # 获取指定数量的问题
            res = await client.get(f"{API_BASE_URL}/problems?tags={tags_str}&limit={limit}&skip={random_skip_num}")
            res.raise_for_status()
            problems_data = res.json()
            logger.info("问题获取成功")
            return problems_data
    except httpx.RequestError as e:
        logger.error(f"请求错误: {e}")
        raise e
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP状态错误: {e.response.status_code}")
        raise e
    except Exception as e:
        logger.error(f"问题获取失败喵~: {e}")
        raise e
