import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

def apply_custom_style():
    # 创建自定义样式
    style = ttk.Style()
    
    # 设置主题颜色
    primary_color = "#2196F3"  # 主色调：现代蓝
    secondary_color = "#E3F2FD"  # 次要色调：浅蓝
    accent_color = "#1976D2"  # 强调色：深蓝
    text_color = "#212121"  # 文字颜色：深灰
    bg_color = "#FFFFFF"  # 背景色：白色
    
    # 配置全局字体
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=10, family="Helvetica Neue")
    
    # 设置窗口背景
    style.configure(".", background=bg_color, foreground=text_color)
    
    # 主框架样式
    style.configure("Custom.TFrame", background=bg_color)
    
    # 标签样式
    style.configure("Custom.TLabel",
                    background=bg_color,
                    foreground=text_color,
                    font=("Helvetica Neue", 10))
    
    # 按钮样式
    style.configure("Custom.TButton",
                    background=primary_color,
                    foreground=text_color,  # 修改按钮文字颜色为深色
                    padding=(20, 10),      # 增大按钮内边距
                    font=("Helvetica Neue", 10, "bold"))
    style.map("Custom.TButton",
              background=[("active", accent_color), ("disabled", "#BDBDBD")],
              foreground=[("disabled", "#757575")])
    
    # 输入框样式
    style.configure("Custom.TEntry",
                    fieldbackground=bg_color,
                    background=bg_color,
                    foreground=text_color,
                    padding=5)
    
    # 下拉框样式
    style.configure("Custom.TCombobox",
                    background=bg_color,
                    fieldbackground=bg_color,
                    foreground=text_color,
                    arrowcolor=primary_color,
                    padding=5)
    
    # 滑块样式
    style.configure("Custom.Horizontal.TScale",
                    background=bg_color,
                    troughcolor=secondary_color,
                    slidercolor=primary_color)
    
    # 树形视图样式
    style.configure("Custom.Treeview",
                    background=bg_color,
                    foreground=text_color,
                    fieldbackground=bg_color,
                    rowheight=30)
    style.configure("Custom.Treeview.Heading",
                    background=secondary_color,
                    foreground=text_color,
                    font=("Helvetica Neue", 10, "bold"),
                    justify="left")  # 设置列标题左对齐
    style.map("Custom.Treeview",
              background=[("selected", primary_color)],
              foreground=[("selected", "white")])
    
    # 标签框样式
    style.configure("Custom.TLabelframe",
                    background=bg_color,
                    foreground=text_color)
    style.configure("Custom.TLabelframe.Label",
                    background=bg_color,
                    foreground=text_color,
                    font=("Helvetica Neue", 10, "bold"))
    
    # 滚动条样式
    style.configure("Custom.Vertical.TScrollbar",
                    background=bg_color,
                    troughcolor=secondary_color,
                    arrowcolor=primary_color)
    
    return style