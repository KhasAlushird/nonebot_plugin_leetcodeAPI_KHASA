# Nonebot Plugin for LeetCode API

本插件功能为:获取 LeetCode（非中文站）中有关试题、用户和讨论相关的信息，并通过 QQ 进行发送。使用了 [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api) 进行开发，实现了原 API 的绝大部分功能。

## 基本功能

- `/lc_dpb`: 获取每日一题
- `/lc_spb`: 获取指定题目
- `/lc_mpb`: 随机获取指定数量的题目列表
- `/lc_tpb`: 随机获取指定数量指定标签的题目

- `/lc_1dc`: 获取最热门的若干个讨论
- `/lc_2dc`: 根据 ID 获取讨论
- `/lc_3dc`: 根据 ID 获取讨论的评论

- `/lc_pf`: 获取指定用户的简介
- `/lc_depf`: 获取指定用户的详细数据
- `/lc_bdu`: 获取指定用户的徽章
- `/lc_svu`: 获取指定用户的解决问题列表
- `/lc_cthis`: 获取指定用户的竞赛历史
- `/lc_sub`: 获取指定用户的提交历史
- `/lc_acsub`: 获取指定用户的 AC 提交历史

可以通过命令 `/lc_h` 获取指令信息。

## 配置文件

- `ONLY_SHOW_FREQUENTLY_USED_COMMANDS`: 在输入 `/lc_h` 的时候，是否仅输出常用的命令。
- `API_BASE_URL`: API 基础 URL，默认为 `https://alfa-leetcode-api.onrender.com`。
- 以下是某些获取指定数量的信息的命令的数量默认值和数量限制：
  - `DEFAULT_DISCUSSION_NUM`: 3
  - `MAX_DISCUSSION_NUM`: 10
  - `DEFAULT_PROBLEM_NUM`: 2
  - `MAX_PROBLEM_NUM`: 5
  - `SUBMISSION_LIMIT`: 5
  - `CALENDAR_LIMIT`: 7

## 常见问题

1. **为何题目是英文？**
   - 因为原 API 获取的就不是 LeetCode 中文站的信息。（可以借此锻炼一下英文水平喵）

2. **如果信息反复获取失败，可以在浏览器里面手动访问一下 [https://alfa-leetcode-api.onrender.com](https://alfa-leetcode-api.onrender.com)，若显示 `too many requests in 1 hour. try again later`，可能是使用了校园网的原因。解决方案是将此项目 [https://github.com/alfaarghya/alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api) 本地部署，然后在 config 里面修改 `API_BASE_URL` 即可。

## 其它

这是我在 GitHub 上面的第一个正式项目，如有任何问题，欢迎各位大佬批评指正！
