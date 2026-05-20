想分别打开 V1、V2、V3
cd D:\pythonproject2025\codex_try
git worktree add --detach D:\pythonproject2025\codex_try_V1 V1_version
git worktree add --detach D:\pythonproject2025\codex_try_V2 V2_version
git worktree add --detach D:\pythonproject2025\codex_try_V3 V3_version
建议先复制新生成图片到主项目目录，再删除 worktree：
cd D:\pythonproject2025
Copy-Item D:\pythonproject2025\codex_try_V3\outputs\* D:\pythonproject2025\codex_try\outputs\ -Force
删除 worktree：
cd D:\pythonproject2025\codex_try
git worktree remove --force D:\pythonproject2025\codex_try_V3
git worktree prune
git worktree list
