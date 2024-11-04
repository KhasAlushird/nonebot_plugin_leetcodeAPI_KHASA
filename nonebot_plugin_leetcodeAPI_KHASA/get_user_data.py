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

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
)
API_BASE_URL = conf.api_base_url


def render_user_profile_html(profile_data):
    '''渲染用户个人资料数据为HTML'''
    template = env.get_template("user_profile_template.html")
    html_content = template.render(
        username=profile_data.get('username', 'N/A'),
        name=profile_data.get('name', 'N/A'),
        birthday=profile_data.get('birthday', 'N/A'),
        avatar=profile_data.get('avatar', 'N/A'),
        ranking=profile_data.get('ranking', 'N/A'),
        reputation=profile_data.get('reputation', 'N/A'),
        gitHub=profile_data.get('gitHub', 'N/A'),
        twitter=profile_data.get('twitter', 'N/A'),
        linkedIN=profile_data.get('linkedIN', 'N/A'),
        website=profile_data.get('website', []),
        country=profile_data.get('country', 'N/A'),
        company=profile_data.get('company', 'N/A'),
        school=profile_data.get('school', 'N/A'),
        skillTags=profile_data.get('skillTags', []),
        about=profile_data.get('about', 'N/A')
    )
    return html_content

def render_user_badges_html(badges_data):
    '''渲染用户徽章数据为HTML'''
    template = env.get_template("user_badges_template.html")
    html_content = template.render(
        badges=badges_data.get('badges', []),
        upcomingBadges=badges_data.get('upcomingBadges', []),
        activeBadge=badges_data.get('activeBadge', {})
    )
    return html_content


def render_user_solved_problems_html(solved_data):
    '''渲染用户解决的问题列表数据为HTML'''
    template = env.get_template("user_solved_problems_template.html")
    html_content = template.render(
        solvedProblem=solved_data.get('solvedProblem', 0),
        easySolved=solved_data.get('easySolved', 0),
        mediumSolved=solved_data.get('mediumSolved', 0),
        hardSolved=solved_data.get('hardSolved', 0),
        totalSubmissionNum=solved_data.get('totalSubmissionNum', []),
        acSubmissionNum=solved_data.get('acSubmissionNum', [])
    )
    return html_content


def render_user_contest_history_html(contest_history_data):
    '''渲染用户竞赛历史数据为HTML'''
    template = env.get_template("user_contest_history_template.html")
    html_content = template.render(
        contestHistory=contest_history_data.get('contestHistory', [])[:5]  # 只获取前5个竞赛历史
    )
    return html_content


def render_user_submissions_html(submissions_data):
    '''渲染用户提交记录数据为HTML'''
    template = env.get_template("user_submissions_template.html")
    html_content = template.render(
        submissions=submissions_data.get('submission', [])
    )
    return html_content

def render_detailed_user_profile_html(profile_data):
    '''渲染用户详细个人资料数据为HTML'''
    template = env.get_template("detailed_user_profile_template.html")
    html_content = template.render(
        totalSolved=profile_data.get('totalSolved', 0),
        totalSubmissions=profile_data.get('totalSubmissions', []),
        totalQuestions=profile_data.get('totalQuestions', 0),
        easySolved=profile_data.get('easySolved', 0),
        totalEasy=profile_data.get('totalEasy', 0),
        mediumSolved=profile_data.get('mediumSolved', 0),
        totalMedium=profile_data.get('totalMedium', 0),
        hardSolved=profile_data.get('hardSolved', 0),
        totalHard=profile_data.get('totalHard', 0),
        ranking=profile_data.get('ranking', 0),
        contributionPoint=profile_data.get('contributionPoint', 0),
        reputation=profile_data.get('reputation', 0),
        submissionCalendar=dict(list(profile_data.get('submissionCalendar', {}).items())[:config["CALENDAR_LIMIT"]]),
        recentSubmissions=profile_data.get('recentSubmissions', [])[:config["SUBMISSION_LIMIT"]],
        matchedUserStats=profile_data.get('matchedUserStats', {})
    )
    return html_content


async def get_user_profile(username):
    '''根据用户名获取用户个人资料'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}")
            res.raise_for_status()
            profile_data = res.json()
            logger.info("用户个人资料获取成功")
            return profile_data
    except Exception as e:
        logger.error("用户个人资料获取失败喵~", e)
        raise e

async def get_user_badges(username):
    '''根据用户名获取用户徽章'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}/badges")
            res.raise_for_status()
            badges_data = res.json()
            logger.info("用户徽章获取成功")
            return badges_data
    except Exception as e:
        logger.error("用户徽章获取失败喵~", e)
        raise e


async def get_user_solved_problems(username):
    '''根据用户名获取用户解决的问题列表'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}/solved")
            res.raise_for_status()
            solved_data = res.json()
            logger.info("用户解决的问题列表获取成功")
            return solved_data
    except Exception as e:
        logger.error("用户解决的问题列表获取失败喵~", e)
        raise e


async def get_user_contest_history(username):
    '''根据用户名获取用户竞赛历史'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}/contest/history")
            res.raise_for_status()
            contest_history_data = res.json()
            logger.info("用户竞赛历史获取成功")
            return contest_history_data
    except Exception as e:
        logger.error("用户竞赛历史获取失败喵~", e)
        raise e


async def get_user_submissions(username, limit):
    '''根据用户名获取用户提交记录'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}/submission?limit={limit}")
            res.raise_for_status()
            submissions_data = res.json()
            logger.info("用户提交记录获取成功")
            return submissions_data
    except Exception as e:
        logger.error("用户提交记录获取失败喵~", e)
        raise e

async def get_user_ACsubmissions(username, limit):
    '''根据用户名获取用户AC提交记录'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/{username}/acSubmission?limit={limit}")
            res.raise_for_status()
            submissions_data = res.json()
            logger.info("用户AC提交记录获取成功")
            return submissions_data
    except Exception as e:
        logger.error("用户AC提交记录获取失败喵~", e)
        raise e


async def get_detailed_user_profile(username):
    '''根据用户名获取用户详细个人资料数据'''
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{API_BASE_URL}/userProfile/{username}")
            res.raise_for_status()
            profile_data = res.json()
            logger.info("用户详细个人资料获取成功")
            return profile_data
    except Exception as e:
        logger.error("用户详细个人资料获取失败喵~", e)
        raise e
