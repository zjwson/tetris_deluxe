from pathlib import Path

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
FPS = 60

# 游戏板设置
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# 颜色定义
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (128, 128, 128),
    'CYAN': (0, 255, 255),
    'BLUE': (0, 0, 255),
    'ORANGE': (255, 165, 0),
    'YELLOW': (255, 255, 0),
    'GREEN': (0, 255, 0),
    'PURPLE': (255, 0, 255),
    'RED': (255, 0, 0),
    'BACKGROUND': (20, 20, 35)
}

# 方块形状定义
SHAPES = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'J': [(0, 0), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 2), (1, 0), (1, 1), (1, 2)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'S': [(0, 1), (0, 2), (1, 0), (1, 1)],
    'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]
}

# 游戏速度设置
INITIAL_FALL_SPEED = 1.0  # 每秒下落一格
SPEED_INCREASE = 0.05  # 每级增加的速度
SOFT_DROP_SPEED = 20  # 软降速度倍数

# 分数设置
SCORES = {
    1: 100,    # 消除1行
    2: 300,    # 消除2行
    3: 500,    # 消除3行
    4: 800     # 消除4行
}

# 特效设置
PARTICLE_COUNT = 20  # 消行时的粒子数量
PARTICLE_LIFETIME = 30  # 粒子生命周期（帧数）
FLASH_DURATION = 20  # 闪烁持续时间（帧数）

# 音效设置
SOUND_EFFECTS = {
    'ROTATE': 'rotate.wav',
    'MOVE': 'move.wav',
    'DROP': 'drop.wav',
    'CLEAR': 'clear.wav',
    'GAME_OVER': 'game_over.wav'
}

# 音量设置
SOUND_VOLUME = 0.3  # 30% 音量

# 资源路径
ASSETS_DIR = Path(__file__).parent.parent / 'assets'
FONTS_DIR = ASSETS_DIR / 'fonts'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
THEMES_DIR = ASSETS_DIR / 'themes'
