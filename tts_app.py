import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
import asyncio
import edge_tts
import os
from datetime import datetime
import pygame

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edge TTS 转换器")
        self.root.geometry("800x600")
        
        # 配置根窗口的网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # 文本输入区域
        input_frame = ttk.Frame(self.main_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.text_label = ttk.Label(input_frame, text="输入要转换的文本:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.text_area = scrolledtext.ScrolledText(input_frame, height=10)
        self.text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.text_area.bind('<<Modified>>', self.update_char_count)
        
        # 字数统计标签
        self.char_count_var = tk.StringVar(value="字数: 0")
        self.char_count_label = ttk.Label(input_frame, textvariable=self.char_count_var)
        self.char_count_label.grid(row=2, column=0, sticky=tk.E, pady=2)
        
        # 语音设置区域
        settings_frame = ttk.LabelFrame(self.main_frame, text="语音设置", padding="5")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # 语音选择
        self.voice_label = ttk.Label(settings_frame, text="语音:")
        self.voice_label.grid(row=0, column=0, sticky=tk.W)
        
        self.voice_var = tk.StringVar(value="zh-CN-XiaoxiaoNeural")
        self.voice_combo = ttk.Combobox(settings_frame, textvariable=self.voice_var)
        self.voice_combo['values'] = [
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-YunxiNeural",
            "zh-CN-YunjianNeural",
            "zh-CN-XiaoyiNeural",
            "en-US-JennyNeural",
            "en-US-GuyNeural"
        ]
        self.voice_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # 语速调节
        self.rate_label = ttk.Label(settings_frame, text="语速:")
        self.rate_label.grid(row=1, column=0, sticky=tk.W)
        
        self.rate_var = tk.StringVar(value="+0%")
        self.rate_scale = ttk.Scale(settings_frame, from_=-50, to=50, orient=tk.HORIZONTAL,
                                  command=lambda v: self.rate_var.set(f"{int(float(v)):+d}%"))
        self.rate_scale.set(0)
        self.rate_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.rate_value_label = ttk.Label(settings_frame, textvariable=self.rate_var)
        self.rate_value_label.grid(row=1, column=2, sticky=tk.W)
        
        # 语调调节
        self.pitch_label = ttk.Label(settings_frame, text="语调:")
        self.pitch_label.grid(row=2, column=0, sticky=tk.W)
        
        self.pitch_var = tk.StringVar(value="+0Hz")
        self.pitch_scale = ttk.Scale(settings_frame, from_=-50, to=50, orient=tk.HORIZONTAL,
                                   command=lambda v: self.pitch_var.set(f"{int(float(v)):+d}Hz"))
        self.pitch_scale.set(0)
        self.pitch_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        self.pitch_value_label = ttk.Label(settings_frame, textvariable=self.pitch_var)
        self.pitch_value_label.grid(row=2, column=2, sticky=tk.W)
        
        # 转换按钮
        self.convert_button = ttk.Button(self.main_frame, text="开始转换", command=self.start_conversion)
        self.convert_button.grid(row=2, column=0, pady=10)
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=0)
        
        # 文件列表区域
        files_frame = ttk.LabelFrame(self.main_frame, text="生成的文件", padding="5")
        files_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        files_frame.grid_columnconfigure(0, weight=1)
        
        # 创建文件列表
        self.files_tree = ttk.Treeview(files_frame, columns=("文件名",), show="headings", height=5)
        self.files_tree.heading("文件名", text="文件名")
        self.files_tree.column("文件名", width=600)
        self.files_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建操作按钮框架
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 添加操作按钮
        self.play_button = ttk.Button(buttons_frame, text="播放", state="disabled", command=self.play_selected)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.locate_button = ttk.Button(buttons_frame, text="定位", state="disabled", command=self.locate_selected)
        self.locate_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(buttons_frame, text="删除", state="disabled", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # 文件列表滚动条
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_tree.configure(yscrollcommand=scrollbar.set)
        
        # 绑定选择事件
        self.files_tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # 初始化pygame用于音频播放
        pygame.mixer.init()
        
        # 更新文件列表
        self.update_file_list()

    def update_char_count(self, event=None):
        if self.text_area.edit_modified():
            text = self.text_area.get("1.0", tk.END).strip()
            self.char_count_var.set(f"字数: {len(text)}")
            self.text_area.edit_modified(False)
    
    def on_select(self, event):
        selected = self.files_tree.selection()
        if selected:
            self.play_button.state(['!disabled'])
            self.locate_button.state(['!disabled'])
            self.delete_button.state(['!disabled'])
        else:
            self.play_button.state(['disabled'])
            self.locate_button.state(['disabled'])
            self.delete_button.state(['disabled'])
    
    def update_file_list(self):
        # 清空现有列表
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        # 获取所有mp3文件
        mp3_files = [f for f in os.listdir() if f.endswith('.mp3')]
        for file in sorted(mp3_files, reverse=True):
            self.files_tree.insert("", tk.END, values=(file,))
    
    def play_selected(self):
        selected = self.files_tree.selection()
        if selected:
            file = self.files_tree.item(selected[0])['values'][0]
            try:
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("错误", f"播放失败: {str(e)}")
    
    def locate_selected(self):
        selected = self.files_tree.selection()
        if selected:
            file = self.files_tree.item(selected[0])['values'][0]
            os.system(f'open -R "{file}"')
    
    def delete_selected(self):
        selected = self.files_tree.selection()
        if selected:
            file = self.files_tree.item(selected[0])['values'][0]
            if messagebox.askyesno("确认", f"确定要删除文件 {file} 吗？"):
                try:
                    os.remove(file)
                    self.update_file_list()
                except Exception as e:
                    messagebox.showerror("错误", f"删除失败: {str(e)}")

    async def convert_text_to_speech(self, text, voice, rate, pitch):
        rate_value = rate
        pitch_value = pitch  # 已经是Hz格式
        
        communicate = edge_tts.Communicate(text, voice, rate=rate_value, pitch=pitch_value)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output_{timestamp}.mp3"
        
        try:
            await communicate.save(output_file)
            return output_file
        except Exception as e:
            raise Exception(f"转换失败: {str(e)}")

    def start_conversion(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("错误", "请输入要转换的文本")
            return
        
        voice = self.voice_var.get()
        rate = self.rate_var.get()
        pitch = self.pitch_var.get()
        
        self.convert_button.state(['disabled'])
        self.convert_button.configure(text="处理中...")
        self.status_var.set("正在转换...")
        
        async def process():            
            try:
                output_file = await self.convert_text_to_speech(text, voice, rate, pitch)
                self.root.after(0, lambda: self.conversion_complete(output_file))
            except Exception as error:
                error_msg = str(error)
                self.root.after(0, lambda: self.conversion_failed(error_msg))
        
        asyncio.run(process())
    
    def conversion_complete(self, output_file):
        self.convert_button.state(['!disabled'])
        self.convert_button.configure(text="开始转换")
        self.status_var.set(f"转换完成! 已保存为: {output_file}")
        self.update_file_list()
        messagebox.showinfo("完成", f"转换完成!\n文件已保存为: {output_file}")
    
    def conversion_failed(self, error_message):
        self.convert_button.state(['!disabled'])
        self.convert_button.configure(text="开始转换")
        self.status_var.set("转换失败")
        messagebox.showerror("错误", f"转换失败: {error_message}")

def main():
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()