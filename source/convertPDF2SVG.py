import os
import shutil
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import re
import sys
import json

class PDFToSVGConverter:
    def __init__(self, root):
        self.root = root
        
        # 定义现代化的颜色方案
        self.bg_color = "#FFFFFF"  # 纯白色背景
        self.accent_color = "#2196F3"  # Material Design 蓝色
        self.text_color = "#212121"  # 深灰色文本
        self.secondary_color = "#757575"  # 次要文本颜色
        
        self.root.configure(bg=self.bg_color)
        
        self.config_file = "config.json"
        self.load_config()
        
        self.file_name_mapping = {}
        
        self.create_widgets()
        self.apply_style()
        self.update_ui_language()

    def load_config(self):
        default_config = {
            'output_dir': '',
            'language': 'zh_CN'  # 默认中文
        }
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = default_config
            self.save_config()
        
        self.output_dir = self.config.get('output_dir', '')
        self.current_language = self.config.get('language', 'zh_CN')

    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # 创建顶部栏框架
        top_bar = ttk.Frame(self.root, style="TopBar.TFrame")
        top_bar.pack(fill=tk.X, padx=10, pady=5)

        # 语言切换按钮放在右上角
        self.lang_button = ttk.Button(
            top_bar,
            text="Switch to English" if self.current_language == "zh_CN" else "切换为中文",
            command=self.toggle_language,
            style="Language.TButton"
        )
        self.lang_button.pack(side=tk.RIGHT)

        # 主内容区域
        main_frame = ttk.Frame(self.root, padding="20", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 输出路径选择区域（使用LabelFrame美化）
        self.path_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10", style="Custom.TLabelframe")
        self.path_frame.pack(fill=tk.X, pady=(0, 20))

        self.output_path_entry = ttk.Entry(self.path_frame, width=50, style="Custom.TEntry")
        self.output_path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.output_path_entry.insert(0, self.output_dir)

        self.output_button = ttk.Button(
            self.path_frame,
            text="选择输出路径",
            command=self.select_output_path,
            style="Custom.TButton"
        )
        self.output_button.pack(side=tk.RIGHT)

        # 文件选择区域
        self.select_frame = ttk.LabelFrame(main_frame, text="PDF文件选择", padding="10", style="Custom.TLabelframe")
        self.select_frame.pack(fill=tk.X, pady=(0, 20))

        # 添加提示文本
        self.hint_label = ttk.Label(
            self.select_frame,
            text="提示：您可以按住Ctrl键同时选择多个PDF文件",
            style="Hint.TLabel"
        )
        self.hint_label.pack(pady=(0, 10))

        self.select_button = ttk.Button(
            self.select_frame,
            text="选择并转换 PDF 文件",
            command=self.select_pdfs,
            style="Custom.TButton"
        )
        self.select_button.pack()

        # 日志区域
        self.log_frame = ttk.LabelFrame(main_frame, text="转换日志", padding="10", style="Custom.TLabelframe")
        self.log_frame.pack(expand=True, fill=tk.BOTH)

        # 调试信息文本框和滚动条
        self.debug_text = tk.Text(
            self.log_frame,
            height=12,
            wrap=tk.WORD,
            bg="white",
            fg=self.text_color,
            font=("Segoe UI", 9)
        )
        self.debug_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.debug_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.debug_text.config(yscrollcommand=scrollbar.set)

    def apply_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # 主框架样式
        style.configure("Main.TFrame", background=self.bg_color)
        style.configure("TopBar.TFrame", background=self.bg_color)
        
        # 标签框架样式
        style.configure("Custom.TLabelframe", background=self.bg_color)
        style.configure("Custom.TLabelframe.Label", 
                       foreground=self.text_color,
                       background=self.bg_color,
                       font=("Segoe UI", 9, "bold"))
        
        # 按钮样式
        style.configure("Custom.TButton",
                       padding=(15, 8),
                       font=("Segoe UI", 9),
                       background=self.accent_color)
        
        # 语言切换按钮特殊样式
        style.configure("Language.TButton",
                       padding=(10, 5),
                       font=("Segoe UI", 9),
                       background="#E0E0E0")
        
        # 提示文本样式
        style.configure("Hint.TLabel",
                       foreground=self.secondary_color,
                       background=self.bg_color,
                       font=("Segoe UI", 9, "italic"))
        
        # 输入框样式
        style.configure("Custom.TEntry",
                       fieldbackground="white",
                       padding=5)

    def toggle_language(self):
        """切换界面语言"""
        self.current_language = "en_US" if self.current_language == "zh_CN" else "zh_CN"
        self.config['language'] = self.current_language
        self.save_config()
        self.update_ui_language()

    def update_ui_language(self):
        translations = {
            'zh_CN': {
                'title': "PDF 转 SVG 转换器",
                'select_output': "选择输出路径",
                'select_convert': "选择并转换 PDF 文件",
                'switch_lang': "Switch to English",
                'output_set': "输出目录设置为: ",
                'select_dir_first': "请先选择输出目录。",
                'output_settings': "输出设置",
                'pdf_selection': "PDF文件选择",
                'conversion_log': "转换日志",
                'multi_select_hint': "提示：您可以按住Ctrl键同时选择多个PDF文件",
                'error_title': "错误",
                'pdf2svg_missing': "错误：找不到pdf2svg.exe文件 ({exe_path})，转换无法进行",
                'pdf2svg_missing_dialog': "无法找到pdf2svg.exe文件\n\n请确保pdf2svg.exe文件位于以下位置:\n{exe_path}\n\n转换功能需要此文件才能正常工作"
            },
            'en_US': {
                'title': "PDF to SVG Converter",
                'select_output': "Select Output Path",
                'select_convert': "Select and Convert PDF",
                'switch_lang': "切换为中文",
                'output_set': "Output directory set to: ",
                'select_dir_first': "Please select an output directory first.",
                'output_settings': "Output Settings",
                'pdf_selection': "PDF File Selection",
                'conversion_log': "Conversion Log",
                'multi_select_hint': "Tip: Hold Ctrl key to select multiple PDF files",
                'error_title': "Error",
                'pdf2svg_missing': "Error: Cannot find pdf2svg.exe file ({exe_path}), conversion cannot proceed",
                'pdf2svg_missing_dialog': "Cannot find pdf2svg.exe file\n\nPlease make sure pdf2svg.exe is located at:\n{exe_path}\n\nThis file is required for conversion functionality"
            }
        }
        
        lang = translations[self.current_language]
        
        self.root.title(lang['title'])
        self.output_button.configure(text=lang['select_output'])
        self.select_button.configure(text=lang['select_convert'])
        self.lang_button.configure(text=lang['switch_lang'])
        self.path_frame.configure(text=lang['output_settings'])
        self.select_frame.configure(text=lang['pdf_selection'])
        self.log_frame.configure(text=lang['conversion_log'])
        self.hint_label.configure(text=lang['multi_select_hint'])
        self.translations = lang

    def select_output_path(self):
        new_output_dir = filedialog.askdirectory(title="Select Output Directory")
        if new_output_dir:
            self.output_dir = new_output_dir
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, self.output_dir)
            self.log_message(f"{self.translations['output_set']}{self.output_dir}")
            self.config['output_dir'] = self.output_dir
            self.save_config()

    def select_pdfs(self):
        pdf_files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf")]
        )
        if pdf_files:
            if not self.output_dir:
                messagebox.showerror("Error", self.translations['select_dir_first'])
                return
            self.log_message(f"Selected PDF files: {pdf_files}")
            self.convert_pdfs_to_svg(pdf_files)

    def get_pdf2svg_path(self):
        if getattr(sys, 'frozen', False):  # 检查是否是打包后的环境
            # 将pdf2svg.exe放在与主程序相同的目录下
            exe_path = os.path.join(os.path.dirname(sys.executable), "pdf2svg.exe")
        else:
            exe_path = os.path.join(os.path.dirname(__file__), "pdf2svg.exe")  # 使用开发环境路径
        
        if not os.path.exists(exe_path):
            error_msg = self.translations['pdf2svg_missing'].format(exe_path=exe_path)
            self.log_message(error_msg)
            messagebox.showerror(
                self.translations['error_title'],
                self.translations['pdf2svg_missing_dialog'].format(exe_path=exe_path)
            )
            return None
        return exe_path

    def convert_pdfs_to_svg(self, pdf_files):
        pdf2svg_path = self.get_pdf2svg_path()
        if pdf2svg_path is None:  # 检查是否成功获取路径
            return
            
        self.log_message(f"Using pdf2svg executable at: {pdf2svg_path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            self.log_message(f"Temporary directory created at: {temp_dir}")

            for pdf_file in pdf_files:
                base_name = os.path.basename(pdf_file)
                self.log_message(f"Original PDF file: {pdf_file}")

                # 记录原始文件名和英文化文件名的映射
                sanitized_name = self.sanitize_filename(base_name)
                self.file_name_mapping[sanitized_name] = base_name

                temp_pdf_path = os.path.join(temp_dir, sanitized_name)
                svg_file_name = os.path.splitext(sanitized_name)[0] + ".svg"
                temp_svg_path = os.path.join(temp_dir, svg_file_name)

                # 复制文件到临时目录
                shutil.copy(pdf_file, temp_pdf_path)
                self.log_message(f"Copied PDF to temporary directory: {temp_pdf_path}")

                # 转换文件
                try:
                    subprocess.run([pdf2svg_path, temp_pdf_path, temp_svg_path], check=True)
                    self.log_message(f"Successfully converted {temp_pdf_path} to {temp_svg_path}")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"Error converting {pdf_file}: {e}")
                    self.log_message(f"Error converting {temp_pdf_path}: {e}")

                # 将 SVG 文件恢复为原始文件名，并移动到输出目录
                original_svg_name = self.file_name_mapping[sanitized_name]
                output_svg_path = os.path.join(self.output_dir, os.path.splitext(original_svg_name)[0] + ".svg")
                shutil.move(temp_svg_path, output_svg_path)
                self.log_message(f"Moved SVG file to output directory: {output_svg_path}")

    def sanitize_filename(self, filename):
        # 替换中文字符和其他非法字符
        # 将所有非 ASCII 字符替换为下划线
        sanitized = re.sub(r'[^\x00-\x7F]', '_', filename)  # 替换非 ASCII 字符
        sanitized = re.sub(r'[^\w\s.-]', '_', sanitized)    # 替换其他非法字符
        return sanitized.strip()

    def load_output_path(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return config.get('output_dir', '')
        except FileNotFoundError:
            return ''

    def save_output_path(self):
        config = {'output_dir': self.output_dir}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def log_message(self, message):
        self.debug_text.insert(tk.END, message + '\n')
        self.debug_text.see(tk.END)
        self.root.update_idletasks()  # 强制更新 UI

# 创建主窗口
root = tk.Tk()
app = PDFToSVGConverter(root)
root.mainloop()
