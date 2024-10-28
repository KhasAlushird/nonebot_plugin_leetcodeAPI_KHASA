from nonebot.adapters.onebot.v11 import  MessageSegment
from nonebot import CommandGroup, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State

from nonebot.plugin import PluginMetadata, require

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_localstore")
__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-leetcodeapi-khasa",
    description="A Nonebot plugin for interacting with LeetCode (Using API made by alfaarghya)",
    usage=(
        "/lc_dpb: 获取每日一题\n"
        "/lc_spb: 获取指定题目\n"
        "/lc_mpb: 随机获取指定数量的题目列表\n"
        "/lc_tpb: 随机获取指定数量指定标签的题目\n"
        "/lc_1dc: 获取最热门的若干个讨论\n"
        "/lc_2dc: 根据 ID 获取讨论\n"
        "/lc_3dc: 根据 ID 获取讨论的评论\n"
        "/lc_pf: 获取指定用户的简介\n"
        "/lc_depf: 获取指定用户的详细数据\n"
        "/lc_bdu: 获取指定用户的徽章\n"
        "/lc_svu: 获取指定用户的解决问题列表\n"
        "/lc_cthis: 获取指定用户的竞赛历史\n"
        "/lc_sub: 获取指定用户的提交历史\n"
        "/lc_acsub: 获取指定用户的 AC 提交历史\n"
        "/lc_h: 获取指令信息"
    ),
    type="application",
    homepage="https://github.com/KhasAlushird/nonebot_plugin_leetcodeAPI_KHASA",
    supported_adapters={"~onebot.v11"},
)

from .get_problem_data import *
from .get_discussion_data import *
from .get_user_data import *
import os
import base64
from .config import conf


from nonebot_plugin_htmlrender import html_to_pic


ONLY_SHOW_FREQUENTLY_USED_COMMANDS = conf.ONLY_SHOW_FREQUENTLY_USED_COMMANDS


#<-----------------------------------------help------------------------------------------------------------> 
cmd_lc_h = CommandGroup(
    "lc_h",
    rule=to_me(),
    priority=1,
    block=True,
)

matcher_lc_h = cmd_lc_h.command(tuple())

@matcher_lc_h.handle()
async def handle_lc_h():
    if(ONLY_SHOW_FREQUENTLY_USED_COMMANDS):
        frequently_used_command = ''
        frequently_used_command += "/lc_dpb:获取每日一题\n"
        frequently_used_command += "/lc_spb:获取指定题目\n"
        frequently_used_command += "/lc_1dc:获取最热门的若干个讨论\n"
        frequently_used_command += "/lc_pf:获取指定用户的简介\n"
        frequently_used_command += "/lc_depf:获取指定用户的详细数据\n"
        await matcher_lc_h.send(frequently_used_command)
    else:
        all_command=''
        all_command+="/lc_h.pb：输出题目相关的命令列表\n"
        all_command+="/lc_h.dc:输出话题讨论相关的命令列表\n"
        all_command+="/lc_h.user:输出用户相关的命令列表\n"
        await matcher_lc_h.send(all_command)


matcher_lc_h_pb = cmd_lc_h.command("pb")
@matcher_lc_h_pb.handle()
async def handle_lc_h_pb(event: Event):
    problem_command_data = ""
    problem_command_data += "/lc_dpb:获取每日一题\n"
    problem_command_data += "/lc_spb:获取指定题目\n"
    problem_command_data += "/lc_mpb:随机获取指定数量的题目列表\n"
    problem_command_data += "/lc_tpb:随机获取指定数量指定标签的题目列表\n"
    await matcher_lc_h_pb.send(problem_command_data)

matcher_lc_h_dc = cmd_lc_h.command("dc")
@matcher_lc_h_dc.handle()
async def handle_lc_h_dc(event:Event):
    discussion_command_data = ""
    discussion_command_data += "/lc_1dc:获取最热门的若干个讨论\n"
    discussion_command_data += "/lc_2dc:根据ID获取讨论\n"
    discussion_command_data += "/lc_3dc:根据ID获取讨论的评论\n"
    await matcher_lc_h_pb.send(discussion_command_data)

matcher_lc_h_user = cmd_lc_h.command("user")
@matcher_lc_h_user.handle()
async def handle_lc_h_user(event:Event):
    user_data = ''
    user_data += "/lc_pf:获取指定用户的简介\n"
    user_data += "/lc_depf:获取指定用户的详细数据\n"
    user_data += "/lc_bdu:获取指定用户的徽章\n"
    user_data += "/lc_svu:获取指定用户的解决问题列表\n"
    user_data += "/lc_cthis:获取指定用户的竞赛历史\n"
    user_data += "/lc_sub:获取指定用户的提交历史\n"
    user_data += "/lc_acsub:获取指定用户的AC提交历史\n"
    await matcher_lc_h_user.send(user_data)
    

#<-------------------------------------get_problem_data--------------------------------------------------------->
req_daily_problem_data = on_command("lc_dpb", priority=10, block=True)
req_selected_problem_data = on_command("lc_spb", priority=10, block=True)
req_problems = on_command("lc_mpb", priority=10, block=True)
req_problems_with_tags = on_command("lc_tpb", priority=10, block=True)

@req_daily_problem_data.handle()
async def send_daily_problem(bot: Bot, event: Event):
    try:
        daily_problem_data = get_daily_problem()
        render_result = render_problem_html(daily_problem_data,"daily")
        daily_problem_html = render_result[0]
        pic = await html_to_pic(daily_problem_html, viewport={"width": 840, "height": 400})
        await req_daily_problem_data.send(MessageSegment.image(pic))
        await req_daily_problem_data.send(f"Link:{render_result[1]}")
    except Exception as e:
        await req_daily_problem_data.send("每日一题获取失败喵~")

@req_selected_problem_data.handle()
async def handle_spb(bot: Bot, event: Event, state: T_State):
    the_pb_title = str(event.get_message()).split()
    try:
        state["title_slug"] = the_pb_title[1]
    except Exception:
        pass

@req_selected_problem_data.got("title_slug", prompt="请输入英文标题喵~")
async def send_selected_problem(bot: Bot, event: Event, state: T_State):
    title_slug = state["title_slug"]
    logger.info(title_slug)
    #特别注意：这里的title_slug是nonebot的某种message类型，需要转换成str类型
    title_slug_str = str(title_slug)
    try:
        selected_problem_data = get_selected_problem(title_slug_str)
        render_result = render_problem_html(selected_problem_data,"selected")
        selected_problem_html = render_result[0]
        pic = await html_to_pic(selected_problem_html, viewport={"width": 840, "height": 400})
        await req_selected_problem_data.send(MessageSegment.image(pic))
        await req_selected_problem_data.send(f"Link:{render_result[1]}")
    except Exception as e:
        await req_selected_problem_data.send("指定题目获取失败喵~")



@req_problems.handle()
async def handle_send_problems(bot: Bot, event: Event, state: T_State):
    the_limit = str(event.get_message()).split()
    try:
        state["limit"] = the_limit[1]
    except Exception:
        pass

@req_problems.got("limit", prompt="请输入获取的问题数量喵~")
async def send_problems(bot: Bot, event: Event, state: T_State):
    limit = state["limit"]
    #特别注意：这里的limit是nonebot的某种message类型，需要转换类型
    str_limit = str(limit)
    try:
        int_limit = int(str_limit)
    except ValueError:
        await req_problems.send("请输入有效的数字喵~")
    try:
        problems_data = get_problems(int_limit)
        render_result = render_problems_html(problems_data)
        problems_html = render_result[0]
        links = render_result[1]
        names = render_result[2]
        pic = await html_to_pic(problems_html, viewport={"width": 840, "height": 400})
        await req_problems.send(MessageSegment.image(pic))
        link_to_send = ""
        name_order = 0
        for link in links:
            link_to_add = names[name_order]+" : "+link
            name_order+=1
            link_to_send += link_to_add + "\n"
        await req_problems.send(link_to_send)
    except Exception as e:
        await req_problems.send("获取问题失败喵~")



@req_problems_with_tags.handle()
async def handle_send_problems_with_tags(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["tags_and_limit"] = user_input[1]
    except Exception:
        pass

@req_problems_with_tags.got("tags_and_limit", prompt="请输入标签和数量，格式为 TAG1-TAG2-TAG3-NUMBER 喵~")
async def send_problems_with_tags(bot: Bot, event: Event, state: T_State):
    tags_and_limit = state["tags_and_limit"]
    #特别注意：这里的tags_and_limit是nonebot的某种message类型，需要转换类型
    str_tags_and_limit = str(tags_and_limit)
    try:
        parts = str_tags_and_limit.split('-')
        if len(parts) < 2:
            raise ValueError("输入格式错误")
        tags = parts[:-1]
        if len(tags) > 3:
            tags = tags[:3]
        limit = int(parts[-1])
    except ValueError:
        await req_problems_with_tags.send("请输入有效的标签和数量，格式为 TAG1-TAG2-TAG3-NUMBER 喵~")
        return
    try:
        problems_data = get_problems_with_tags(tags, limit)
        render_result = render_problems_html(problems_data)
        problems_html = render_result[0]
        links = render_result[1]
        names = render_result[2]
        pic = await html_to_pic(problems_html, viewport={"width": 840, "height": 400})
        await req_problems_with_tags.send(MessageSegment.image(pic))
        link_to_send = ""
        name_order = 0
        for link in links:
            link_to_add = names[name_order]+" : "+link
            name_order+=1
            link_to_send += link_to_add + "\n"
        await req_problems_with_tags.send(link_to_send)
    except Exception as e:
        await req_problems_with_tags.send("获取问题失败喵~")

#<---------------------------------get_discussion_data-------------------------------------------------------------------->
req_top_discussion_data = on_command("lc_1dc", priority=10, block=True)
req_discussion_by_id = on_command("lc_2dc", priority=10, block=True)
req_discussion_comments_by_id = on_command("lc_3dc", priority=10, block=True)

@req_top_discussion_data.handle()
async def handle_send_top_discussion(bot: Bot, event: Event, state: T_State):
    the_dc_num = str(event.get_message()).split()
    try:
        state["dc_num"] = the_dc_num[1]
    except Exception:
        pass

@req_top_discussion_data.got("dc_num", prompt="请输入获取的话题数量喵~")
async def send_selected_problem(bot: Bot, event: Event, state: T_State):
    dc_num = state["dc_num"]
    #特别注意：这里的dc_num是nonebot的某种message类型，需要转换类型
    str_dc_num = str(dc_num)
    try:
        int_dc_num = int(str_dc_num)   
    except ValueError:
        await req_top_discussion_data.send("请输入有效的数字喵~")
    try:
        if int_dc_num<=0:
            trending_discussions_data = get_trending_discussion()
        else:
            trending_discussions_data = get_trending_discussion(int_dc_num)
        trending_discussions_html = render_discussion_html(trending_discussions_data)
        pic = await html_to_pic(trending_discussions_html, viewport={"width": 840, "height": 400})
        await req_top_discussion_data.send(MessageSegment.image(pic))
    except Exception as e:
        await req_top_discussion_data.send("获取最热话题失败喵~")



@req_discussion_by_id.handle()
async def handle_send_discussion_by_id(bot: Bot, event: Event, state: T_State):
    the_discussion_id = str(event.get_message()).split()
    try:
        state["discussion_id"] = the_discussion_id[1]
    except Exception:
        pass

@req_discussion_by_id.got("discussion_id", prompt="请输入讨论ID喵~")
async def send_discussion_by_id(bot: Bot, event: Event, state: T_State):
    discussion_id = state["discussion_id"]
    #特别注意：这里的discussion_id是nonebot的某种message类型，需要转换类型
    str_discussion_id = str(discussion_id)
    try:
        discussion_data = get_discussion_by_id(str_discussion_id)
        discussion_html = render_discussion_by_id_html(discussion_data)
        pic = await html_to_pic(discussion_html, viewport={"width": 840, "height": 400})
        await req_discussion_by_id.send(MessageSegment.image(pic))
    except Exception as e:
        await req_discussion_by_id.send("获取讨论失败喵~")



@req_discussion_comments_by_id.handle()
async def handle_send_discussion_comments_by_id(bot: Bot, event: Event, state: T_State):
    the_discussion_id = str(event.get_message()).split()
    try:
        state["discussion_id"] = the_discussion_id[1]
    except Exception:
        pass

@req_discussion_comments_by_id.got("discussion_id", prompt="请输入讨论ID喵~")
async def send_discussion_comments_by_id(bot: Bot, event: Event, state: T_State):
    discussion_id = state["discussion_id"]
    #特别注意：这里的discussion_id是nonebot的某种message类型，需要转换类型
    str_discussion_id = str(discussion_id)
    try:
        comments_data = get_discussion_comments(str_discussion_id)
        comments_html = render_discussion_comments_html(comments_data)
        pic = await html_to_pic(comments_html, viewport={"width": 840, "height": 400})
        await req_discussion_comments_by_id.send(MessageSegment.image(pic))
    except Exception as e:
        await req_discussion_comments_by_id.send("获取讨论评论失败喵~")


#<-------------------------------get_user_data---------------------------------------------------------------------->
req_user_profile = on_command("lc_pf", priority=10, block=True)
req_detailed_user_profile = on_command("lc_depf", priority=10, block=True)
req_user_badges = on_command("lc_bdu", priority=10, block=True)
req_user_solved_problems = on_command("lc_svu", priority=10, block=True)
req_user_contest_history = on_command("lc_cthis", priority=10, block=True)
req_user_submissions = on_command("lc_sub", priority=10, block=True)
req_user_ACsubmissions = on_command("lc_acsub", priority=10, block=True)

@req_user_profile.handle()
async def handle_send_user_profile(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_profile.got("username", prompt="请输入用户名喵~")
async def send_user_profile(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        profile_data = get_user_profile(str_username)
        profile_html = render_user_profile_html(profile_data)
        pic = await html_to_pic(profile_html, viewport={"width": 840, "height": 400})
        await req_user_profile.send(MessageSegment.image(pic))
        await req_user_profile.send(f"Link:https://leetcode.com/u/{str_username}")
    except Exception as e:
        await req_user_profile.send("获取用户个人资料失败喵~")

        


@req_user_badges.handle()
async def handle_send_user_badges(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_badges.got("username", prompt="请输入用户名喵~")
async def send_user_badges(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        badges_data = get_user_badges(str_username)
        badges_html = render_user_badges_html(badges_data)
        pic = await html_to_pic(badges_html, viewport={"width": 840, "height": 400})
        await req_user_badges.send(MessageSegment.image(pic))
    except Exception as e:
        await req_user_badges.send("获取用户徽章失败喵~")


@req_user_solved_problems.handle()
async def handle_send_user_solved_problems(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_solved_problems.got("username", prompt="请输入用户名喵~")
async def send_user_solved_problems(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        solved_data = get_user_solved_problems(str_username)
        solved_html = render_user_solved_problems_html(solved_data)
        pic = await html_to_pic(solved_html, viewport={"width": 840, "height": 400})
        await req_user_solved_problems.send(MessageSegment.image(pic))
    except Exception as e:
        await req_user_solved_problems.send("获取用户解决的问题列表失败喵~")





@req_user_contest_history.handle()
async def handle_send_user_contest_history(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_contest_history.got("username", prompt="请输入用户名喵~")
async def send_user_contest_history(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        contest_history_data = get_user_contest_history(str_username)
        contest_history_html = render_user_contest_history_html(contest_history_data)
        pic = await html_to_pic(contest_history_html, viewport={"width": 840, "height": 400})
        await req_user_contest_history.send(MessageSegment.image(pic))
    except Exception as e:
        await req_user_contest_history.send("获取用户竞赛历史失败喵~")

@req_user_submissions.handle()
async def handle_send_user_submissions(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_submissions.got("username", prompt="请输入用户名喵~")
async def send_user_submissions(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        limit = config["SUBMISSION_LIMIT"]  # 从config.json中读取limit
        submissions_data = get_user_submissions(str_username, limit)
        submissions_html = render_user_submissions_html(submissions_data)
        pic = await html_to_pic(submissions_html, viewport={"width": 840, "height": 400})
        await req_user_submissions.send(MessageSegment.image(pic))
    except Exception as e:
        await req_user_submissions.send("获取用户提交记录失败喵~")



@req_user_ACsubmissions.handle()
async def handle_send_user_ACsubmissions(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_user_ACsubmissions.got("username", prompt="请输入用户名喵~")
async def send_user_ACsubmissions(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        limit = config["SUBMISSION_LIMIT"]  # 从config.json中读取limit
        submissions_data = get_user_ACsubmissions(str_username, limit)
        submissions_html = render_user_submissions_html(submissions_data)
        pic = await html_to_pic(submissions_html, viewport={"width": 840, "height": 400})
        await req_user_submissions.send(MessageSegment.image(pic))
    except Exception as e:
        await req_user_submissions.send("获取用户AC提交记录失败喵~")


@req_detailed_user_profile.handle()
async def handle_send_detailed_user_profile(bot: Bot, event: Event, state: T_State):
    user_input = str(event.get_message()).split()
    try:
        state["username"] = user_input[1]
    except Exception:
        pass

@req_detailed_user_profile.got("username", prompt="请输入用户名喵~")
async def send_detailed_user_profile(bot: Bot, event: Event, state: T_State):
    username = state["username"]
    #特别注意：这里的username是nonebot的某种message类型，需要转换类型
    str_username = str(username)
    try:
        profile_data = get_detailed_user_profile(str_username)
        profile_html = render_detailed_user_profile_html(profile_data)
        pic = await html_to_pic(profile_html, viewport={"width": 840, "height": 400})
        await req_detailed_user_profile.send(MessageSegment.image(pic))
        await req_detailed_user_profile.send(f"Link:https://leetcode.com/u/{str_username}")
    except Exception as e:
        await req_detailed_user_profile.send("获取用户详细个人资料数据失败喵~")



    