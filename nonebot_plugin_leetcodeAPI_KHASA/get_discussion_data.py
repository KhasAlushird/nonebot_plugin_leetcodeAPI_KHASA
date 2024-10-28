import os
import httpx
from nonebot.log import logger
import json
from jinja2 import Environment, FileSystemLoader
from .config import conf
import jinja2
from pathlib import Path


templates_path = Path(__file__).resolve().parent / "templates"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
)
API_BASE_URL = conf.API_BASE_URL
DEFAULT_DISCUSSION_NUM = conf.DEFAULT_DISCUSSION_NUM
MAX_DISCUSSION_NUM = conf.MAX_DISCUSSION_NUM

def render_discussion_html(discussion_data):
    '''渲染讨论数据为HTML'''
    template = env.get_template("templates/discussion_template.html")
    html_content = template.render(
         discussions=discussion_data.get('cachedTrendingCategoryTopics', [])
    )
    return html_content


def render_discussion_by_id_html(discussion_data):
    '''渲染特定ID的讨论数据为HTML'''
    template = env.get_template("templates/discussion_by_id_template.html")
    html_content = template.render(
        discussion=discussion_data.get('data', {}).get('topic', {})
    )
    return html_content

def render_discussion_comments_html(comments_data):
    '''渲染讨论评论数据为HTML'''
    template = env.get_template("templates/discussion_comments_template.html")
    html_content = template.render(
        comments=comments_data.get('data', {}).get('topicComments', {}).get('data', [])[:3]  # 只获取前三个评论
    )
    return html_content

def get_trending_discussion(discussion_num=DEFAULT_DISCUSSION_NUM):
    '''获取热门讨论'''
    if discussion_num>MAX_DISCUSSION_NUM:
        discussion_num = MAX_DISCUSSION_NUM
    try:
        res = httpx.get(f"{API_BASE_URL}/trendingDiscuss?first={discussion_num}")
        res.raise_for_status()
        trending_data = res.json()
        logger.info("热门讨论获取成功")
        return trending_data
    except Exception as e:
        logger.error("热门讨论获取失败喵~", e)
        raise e
    


def get_discussion_by_id(discussion_id):
    '''根据ID获取讨论'''
    try:
        res = httpx.get(f"{API_BASE_URL}/discussTopic/{discussion_id}")
        res.raise_for_status()
        discussion_data = res.json()
        logger.info("讨论获取成功")
        return discussion_data
    except Exception as e:
        logger.error("讨论获取失败喵~", e)
        raise e
    



def get_discussion_comments(discussion_id):
    '''根据ID获取讨论评论'''
    try:
        res = httpx.get(f"{API_BASE_URL}/discussComments/{discussion_id}")
        res.raise_for_status()
        comments_data = res.json()
        logger.info("讨论评论获取成功")
        return comments_data
    except Exception as e:
        logger.error("讨论评论获取失败喵~", e)
        raise e