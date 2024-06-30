import pygame
import sys
import random




# 初始化 Pygame
pygame.init()

# 定义屏幕尺寸
screen_width = 1300
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# 加载图片
background = pygame.image.load('image/background.jpg')
nail = pygame.image.load('image/nail.png')
xcp = pygame.image.load('image/xcp.png')

# 获取图片的矩形区域
nail_rect = nail.get_rect()
xcp_rect = xcp.get_rect()
background_rect = background.get_rect()

# 设置 xcp 初始位置
xcp_rect.center = (screen_width // 2, screen_height - xcp_rect.height // 2)

# 定义初始血量
health = 114514
# 设置字体，加载支持中文的字体文件
font_path = 'simsun.ttf'  # 请确保这个路径是正确的
font = pygame.font.Font(font_path, 74)
large_font = pygame.font.Font(font_path, 100)  # 调整大字体大小


# 定义铁钉的速度
nail_speed = 5
# 定义 xcp 的移动速度
xcp_speed = 10

# 创建铁钉列表
nails = []

# 定义生成整行铁钉的函数
def create_row_of_nails():
    nail_width = nail_rect.width
    for x in range(0, screen_width, nail_width):
        new_nail = nail_rect.copy()
        new_nail.x = x
        new_nail.y = -nail_rect.height
        nails.append(new_nail)

# 游戏主循环
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and xcp_rect.top > 0:
        xcp_rect.y -= xcp_speed
    if keys[pygame.K_s] and xcp_rect.bottom < screen_height:
        xcp_rect.y += xcp_speed
    if keys[pygame.K_a] and xcp_rect.left > 0:
        xcp_rect.x -= xcp_speed
    if keys[pygame.K_d] and xcp_rect.right < screen_width:
        xcp_rect.x += xcp_speed

    if not game_over:
        # 每帧生成一整行新的铁钉
        create_row_of_nails()

        # 移动铁钉
        for nail_rect in nails:
            nail_rect.y += nail_speed

        # 检查铁钉是否与 xcp 碰撞
        for nail_rect in nails:
            if nail_rect.colliderect(xcp_rect):
                health -= 2
                nails.remove(nail_rect)
                if health <= 0:
                    game_over = True
                    break

        # 移除已移出屏幕的铁钉
        nails = [nail for nail in nails if nail.y <= screen_height]

    # 绘制背景
    screen.blit(background, background_rect)

    # 绘制铁钉
    for nail_rect in nails:
        screen.blit(nail, nail_rect)

    # 绘制 xcp
    screen.blit(xcp, xcp_rect)

    # 绘制血量
    health_text = font.render(f'Health: {health}', True, (255, 0, 0))
    screen.blit(health_text, (10, 10))

    # 如果游戏结束，显示 "你失败了"
    if game_over:
        game_over_text = large_font.render("你失败了", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(game_over_text, text_rect)

    # 更新屏幕
    pygame.display.flip()

    # 设置帧率
    pygame.time.Clock().tick(60)

# 退出 Pygame
pygame.quit()
sys.exit()
