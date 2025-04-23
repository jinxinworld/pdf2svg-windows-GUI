# pdf2svg-windows-GUI

## 项目简介
pdf2svg-windows-GUI 是一个基于 Python 的图形界面工具，旨在让用户在 Windows 系统下轻松将 PDF 文件批量转换为 SVG 矢量图。相比原始的 pdf2svg.exe 命令行工具，本项目支持多语言文件名（包括中文等），并提供中英文双语界面，极大提升了易用性和兼容性。

## 主要特性
- **图形界面操作**：无需命令行基础，所有操作均可通过直观的窗口界面完成。
- **批量转换**：支持一次选择多个 PDF 文件，批量转换为 SVG。
- **多语言文件名支持**：自动处理中文等非 ASCII 文件名，避免原版工具无法识别的问题。
- **中英文界面切换**：界面可一键切换中文或英文，适合不同用户群体。
- **输出路径自定义**：可自定义 SVG 文件的输出目录。
- **转换日志实时显示**：界面内置日志区域，实时显示转换进度和错误信息。

## 对比原始 pdf2svg.exe 的改进
- 原版 pdf2svg.exe 仅支持命令行操作且不支持非 ASCII 文件名，使用不便。
- 本项目封装了 pdf2svg.exe，自动处理文件名编码问题，支持多语言。
- 提供现代化美观的 GUI，适合所有用户。

## 项目结构
```markdown
convertPDF2SVG/
├── README.md                  # 项目英文说明文档
├── README.zh.md               # 项目中文说明文档
├── .gitignore                 # Git忽略规则文件
├── config.json                # 用户配置文件
├── release/                   # 发布目录（含打包好的可执行文件）
│   ├── PDFToSVGConverter.exe  # 主程序可执行文件
│   └── pdf2svg.exe            # 核心转换工具
└── source/                    # 源代码和依赖文件目录
    ├── build/                 # PyInstaller打包中间文件
    ├── dist/                  # PyInstaller打包输出目录
    ├── convertPDF2SVG.py      # 主程序源码
    ├── create_icon.py         # 图标生成脚本
    ├── pdf2svg.exe            # 核心转换工具
    ├── iconv.dll              # 字符编码转换库
    ├── libbz2-1.dll           # 数据压缩库
    ├── libcairo-2.dll         # 矢量图形库
    ├── libfreetype-6.dll      # 字体渲染库
    ├── libjpeg-62.dll         # JPEG图像处理库
    ├── libpng16-16.dll        # PNG图像处理库
    └── ...                    # 其他运行依赖库
```

## 安装与运行
1. **环境准备**：
   - Windows 10/11
   - 已集成 pdf2svg.exe 及所需依赖（无需单独安装）
   - 推荐使用已打包的 convertPDF2SVG.exe
2. **运行方法**：
   - 确保 `pdf2svg.exe` 和 `convertPDF2SVG.exe` 位于同一目录下
   - 双击 `convertPDF2SVG.exe` 

## 界面使用说明
1. **选择输出路径**：
   - 点击“选择输出路径”按钮，指定 SVG 文件保存的文件夹。
2. **选择 PDF 文件**：
   - 点击“选择并转换 PDF 文件”按钮，在弹出的文件选择框中按住 Ctrl 可多选 PDF 文件。
3. **开始转换**：
   - 选择文件后自动开始转换，进度和日志会在下方“转换日志”区域实时显示。
4. **切换界面语言**：
   - 右上角按钮可在中文和英文界面间切换。

## 注意事项
- 输出目录需有写入权限。
- 若遇到转换失败，请查看日志区域的详细错误信息。

## 截图预览
![界面截图](screenshots/main_ui_cn.png)

## 开源协议
本项目遵循 GPL 协议，欢迎二次开发与反馈建议。