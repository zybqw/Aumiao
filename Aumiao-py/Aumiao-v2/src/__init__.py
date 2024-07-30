from .app import acquire, data, file, tool
from .client import community, other, post, shop, union, user, work

# 定义版本、作者和团队信息
version = "2.0.0"
author = "Aurzex"
team = "Aumiao Team"
team_members = "Aurzex, MoonLeaaaf, Nomen, MiTao"


# 实例化app模块中的类
app_acquire = acquire.CodeMaoClient()
app_data = data.CodeMaoData()
app_file = file.CodeMaoFile()
app_tool_process = tool.CodeMaoProcess()
app_tool_routine = tool.CodeMaoRoutine()

# 实例化client模块中的类
client_community_obtain = community.Obtain()
client_community_login = community.Login()
client_post_obtain = post.Obtain()
client_shop_obtain = shop.Obtain()
client_shop_motion = shop.Motion()
client_union_community = union.CommunityUnion()
client_union_work = union.WorkUnion()
client_union_user = union.UserUnion()
client_user_obtain = user.Obtain()
client_user_motion = user.Motion()
client_work_motion = work.Motion()
client_work_obtain = work.Obtain()
client_other = other.PickDuck()
