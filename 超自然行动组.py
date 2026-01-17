import turtle
import easygui
import random
import time

# 全局变量（用于解决作用域问题）
current_score = 0
current_special = None
current_special_type = None

# 游戏初始化
def init_game():
    # 主窗口设置
    screen = turtle.Screen()
    screen.title("超自然行动组")
    screen.setup(width=500, height=400)
    screen.tracer(0)  # 关闭自动刷新，提高流畅度
    screen.colormode(1.0)  # 设置颜色模式为0-1范围

    # 玩家乌龟
    player = turtle.Turtle()
    player.shape("turtle")
    player.color("red")
    player.penup()
    player.goto(0, 0)

    # 分数变量
    global current_score
    current_score = 0
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.penup()
    score_display.goto(-220, 180)
    score_display.write(f"分数: {current_score}", font=("Arial", 12, "normal"))

    return screen, player, score_display

# 创建游戏元素（方块、绿色圆圈、蓝色圆圈）
def create_game_elements():
    # 方块障碍（7个）
    blocks = []
    for _ in range(7):
        block = turtle.Turtle()
        block.shape("square")
        block.penup()
        # 随机位置（-230~230 x, -180~180 y）
        x = random.randint(-23, 23) * 10
        y = random.randint(-18, 18) * 10
        block.goto(x, y)
        blocks.append(block)

    # 绿色奖励圈（7个，+1000分）
    green_coins = []
    for _ in range(7):
        coin = turtle.Turtle()
        coin.shape("circle")
        coin.color(0, 1, 0)
        coin.penup()
        x = random.randint(-23, 23) * 10
        y = random.randint(-18, 18) * 10
        coin.goto(x, y)
        green_coins.append(coin)

    # 蓝色奖励圈（5个，+5000分）
    blue_coins = []
    for _ in range(5):
        coin = turtle.Turtle()
        coin.shape("circle")
        coin.color(0, 0, 1)
        coin.penup()
        x = random.randint(-23, 23) * 10
        y = random.randint(-18, 18) * 10
        coin.goto(x, y)
        blue_coins.append(coin)

    # 特殊奖励（紫色+15000，金色+30000）
    special_items = {
        "purple": turtle.Turtle(),
        "gold": turtle.Turtle()
    }
    for key, item in special_items.items():
        item.shape("circle")
        item.penup()
        item.hideturtle()
        if key == "purple":
            item.color(1, 0, 1)
        else:
            item.color(1, 0.8, 0)

    return blocks, green_coins, blue_coins, special_items

# 玩家移动函数
def move_up(player):
    y = player.ycor()
    if y < 180:  # 边界限制
        player.sety(y + 10)

def move_down(player):
    y = player.ycor()
    if y > -180:
        player.sety(y - 10)

def move_left(player):
    x = player.xcor()
    if x > -230:
        player.setx(x - 10)

def move_right(player):
    x = player.xcor()
    if x < 230:
        player.setx(x + 10)

# 分数更新函数
def update_score(score_display, add_score):
    global current_score
    current_score += add_score
    score_display.clear()
    score_display.write(f"分数: {current_score}", font=("Arial", 12, "normal"))

# 特殊奖励触发函数
def trigger_special(special_items, score_display):
    global current_special, current_special_type, current_score
    if current_special and current_special.isvisible():
        # 根据特殊奖励类型加分
        if current_special_type == "gold":
            update_score(score_display, 30000)
        else:
            update_score(score_display, 15000)
        # 隐藏特殊奖励并重置状态
        current_special.hideturtle()
        current_special = None
        current_special_type = None
        # 取消空格键绑定
        turtle.onkey(None, "space")

# 碰撞检测
def check_collisions(player, blocks, green_coins, blue_coins, special_items, score_display):
    global current_special, current_special_type
    px, py = player.xcor(), player.ycor()
    
    # 检测方块碰撞（触发特殊奖励）
    for block in blocks:
        if block.isvisible() and abs(px - block.xcor()) < 15 and abs(py - block.ycor()) < 15:
            block.hideturtle()  # 隐藏方块
            
            # 只有当前没有激活的特殊奖励时才生成新的
            if not current_special or not current_special.isvisible():
                # 随机出现特殊奖励
                special_type = random.choice(["purple", "gold"])
                current_special = special_items[special_type]
                current_special_type = special_type
                # 特殊奖励位置偏移，避免和方块重叠
                offset_x = 10 if special_type == "gold" else -10
                current_special.goto(block.xcor() + offset_x, block.ycor())
                current_special.showturtle()  # 显示特殊奖励
                
                # 绑定空格键触发特殊奖励
                turtle.onkey(lambda: trigger_special(special_items, score_display), "space")
            break
    
    # 检测绿色硬币碰撞
    for coin in green_coins:
        if coin.isvisible() and abs(px - coin.xcor()) < 15 and abs(py - coin.ycor()) < 15:
            coin.hideturtle()
            update_score(score_display, 1000)
    
    # 检测蓝色硬币碰撞
    for coin in blue_coins:
        if coin.isvisible() and abs(px - coin.xcor()) < 15 and abs(py - coin.ycor()) < 15:
            coin.hideturtle()
            update_score(score_display, 5000)

# 主游戏循环（使用ontimer实现非阻塞循环）
def game_loop(screen, player, blocks, green_coins, blue_coins, special_items, score_display):
    # 刷新屏幕
    screen.update()
    
    # 碰撞检测
    check_collisions(player, blocks, green_coins, blue_coins, special_items, score_display)
    
    # 检测胜利条件
    if current_score >= 140000:
        easygui.msgbox("恭喜你！完成超自然任务！", title="游戏胜利")
        turtle.bye()
        return
    
    # 递归调用循环（每隔10ms执行一次，替代while循环）
    screen.ontimer(lambda: game_loop(screen, player, blocks, green_coins, blue_coins, special_items, score_display), 10)

# 主程序
if __name__ == "__main__":
    # 欢迎界面
    choice = easygui.ynbox(
        "欢迎您来到超自然行动组!\n\n操作说明：\nW/S/A/D - 上下左右移动\nSpace - 拾取特殊奖励\nESC - 退出游戏",
        title="超自然行动组",
        choices=("开始游戏", "关于我们")
    )
    
    if choice:
        # 初始化游戏
        screen, player, score_display = init_game()
        
        # 创建游戏元素
        blocks, green_coins, blue_coins, special_items = create_game_elements()
        
        # 绑定按键
        turtle.listen()
        turtle.onkey(lambda: move_up(player), "w")
        turtle.onkey(lambda: move_down(player), "s")
        turtle.onkey(lambda: move_left(player), "a")
        turtle.onkey(lambda: move_right(player), "d")
        turtle.onkey(turtle.bye, "Escape")  # ESC退出
        
        # 开始游戏循环（非阻塞方式）
        game_loop(screen, player, blocks, green_coins, blue_coins, special_items, score_display)
        
        # 保持窗口运行
        turtle.done()
    else:
        easygui.msgbox("超自然行动组 v1.0\n创作日期:2025/12/21\n开发者:蒋蒋工作室\n\n操作说明：\nW/S/A/D - 上下左右\nSpace - 拾取特殊奖励\nESC - 退出", title="关于我们")
