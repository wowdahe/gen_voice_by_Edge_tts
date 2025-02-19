# Edge TTS 转换器

这是一个基于Edge TTS引擎的文字转语音工具，提供了简单直观的图形界面，让用户可以轻松地将文字转换为语音文件。

## 功能特点

- 支持多种中英文语音选择
- 可调节语速和语调
- 实时显示文本字数统计
- 自动保存生成的音频文件
- 支持音频文件的播放、定位和删除操作
- 简洁美观的图形界面

## 安装说明

1. 确保您的系统已安装Python 3.7或更高版本
2. 克隆或下载本项目到本地
3. 安装所需依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 软件界面

![软件界面截图](images/interface.png)

软件界面采用简洁直观的设计，主要包括以下区域：
- 左侧：文本输入区域，用于输入需要转换的文字
- 右上：语音设置区域，可选择语音类型并调节语速和语调
- 右下：文件列表区域，显示已生成的语音文件，支持播放、定位和删除操作

## 使用方法

1. 运行程序：
   ```bash
   python tts_app.py
   ```

2. 在文本输入区域输入要转换的文字

3. 选择语音类型：
   - zh-CN-XiaoxiaoNeural：小筱（女声）
   - zh-CN-YunxiNeural：云希（男声）
   - zh-CN-YunjianNeural：云健（男声）
   - zh-CN-XiaoyiNeural：小艺（女声）
   - en-US-JennyNeural：Jenny（英语女声）
   - en-US-GuyNeural：Guy（英语男声）

4. 调节语速和语调：
   - 语速：-50% 到 +50%
   - 语调：-50Hz 到 +50Hz

5. 点击"开始转换"按钮

6. 转换完成后，可以在文件列表中：
   - 播放：试听生成的语音文件
   - 定位：在文件管理器中查看文件位置
   - 删除：删除不需要的语音文件

## 注意事项

- 生成的语音文件将以"output_时间戳.mp3"格式保存在程序运行目录下
- 转换过程中请保持网络连接
- 建议每次转换的文本长度适中，过长的文本可能需要更多处理时间

## 技术依赖

- Python 3.7+
- edge-tts
- tkinter
- pygame
- asyncio

## 许可证

本项目采用MIT许可证。欢迎使用和改进。

## 联系作者

如果您在使用过程中有任何建议或需要交流，欢迎添加作者微信：dahebro（请备注：github）