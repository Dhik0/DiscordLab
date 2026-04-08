import os
import json
import customtkinter as ctk
import colorsys

CONFIG_PATH = "config.json"

# --- 1. 核心 CSS 生成引擎 ---
def generate_css(font_name, line_height, font_size, text_color, bg_color, version_num):
    padding_top = f"{int(font_size * (line_height - 1.0) / 2) + 2}px"
    return f"""/**
 * @name Dhik0_Stable_Style
 * @author Dhik0
 * @version {version_num}
 * @description 极致排版优化 (v2.2 亮度修复版)。
 */
[class^="contents_"] {{ overflow: visible !important; }}
[class^="markup_"] {{
    font-family: "{font_name}", "Source Han Serif CN", serif !important;
    font-size: {font_size}px !important;
    color: {text_color} !important;
    background-color: {bg_color} !important;
    border-radius: 8px !important; 
    line-height: {line_height} !important;
    padding-top: {padding_top} !important; 
    -webkit-font-smoothing: antialiased !important;
    text-rendering: optimizeLegibility !important;
}}
[class^="markup_"] img[class*="emoji"] {{
    vertical-align: text-bottom !important; 
    margin-bottom: 2px !important; 
}}
[class^="header_"] {{ margin-bottom: 0px !important; }}
[class^="username_"] {{ font-family: "Inter", sans-serif !important; font-weight: 600 !important; }}
"""

# --- 2. 默认多语言字典 (兜底用) ---
TRANSLATIONS = {
    "zh-CN": {
        "app_title": "Discord 审美实验室 v2.2",
        "panel_title": "⚙️ 视觉调色 (状态同步版)",
        "bg_label": "🎨 背景配色:",
        "text_ctrl_label": "🖋️ 文字颜色控制 (视觉调色):",
        "light_label": "亮度 (Lightness):",
        "preset_label": "常用预设:",
        "size_label": "字号大小: {}px",
        "height_label": "行高调节: {:.2f}",
        "btn_text": "🚀 实时同步到 Discord",
        "success_msg": "✅ 亮度同步 Bug 已修复！",
        "preview_title": "Dhik0  [v2.2 亮度 Bug 已修]",
        "preview_text": "文字颜色预览：\n1. 修复了亮度滑块在预览中不显示的 Bug。\n2. 现在的彩虹条点击位置更加精准。"
    },
    "en-US": {
        "app_title": "Discord Aesthetic Lab v2.2",
        "panel_title": "⚙️ Visual Tuning (Sync Mode)",
        "bg_label": "🎨 Background Color:",
        "text_ctrl_label": "🖋️ Text Color Control:",
        "light_label": "Lightness:",
        "preset_label": "Presets:",
        "size_label": "Font Size: {}px",
        "height_label": "Line Height: {:.2f}",
        "btn_text": "🚀 Sync to Discord",
        "success_msg": "✅ Brightness Sync Fixed!",
        "preview_title": "Dhik0 [v2.2 Bug Fixed]",
        "preview_text": "Preview Text:\n1. Fixed brightness slider bug.\n2. Rainbow bar is now precise."
    }
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_hue = 0.5
        self.lang = "zh-CN"
        
        self.bg_presets = [
            ("透明", "transparent"), ("暗岩", "#2B2D31"), ("墨黑", "#1E1F22"), 
            ("官方", "#313338"), ("气泡", "#3E4147"), ("Discord", "#5865F2")
        ]
        self.text_presets = [
            ("纯白", "#FFFFFF"), ("纸帛", "#F5F5F5"), ("护眼", "#CCE8CF"), 
            ("羊皮", "#E3DAC9"), ("淡金", "#FFF2CC"), ("荧光", "#39FF14")
        ]

        # 核心设置字典
        # 核心设置字典 (BETA 1.0 发行版内置配置)
        self.settings = {
            "font": "Georgia", 
            "size": 19.0, 
            "height": 1.7,
            "color": "#FFFFFF", 
            "bg": "transparent",
            "language": "en-US", 
            "ui_version": "BETA 1.0",
            
            # --- 以下是你自定义的 UI 文本，已全部注入内核 ---
            "ui_app_title_zh-CN": "Discord 审美实验室 BETA 1.0",
            "ui_app_title_en-US": "Discord Aesthetic Lab BETA 1.0",
            
            "ui_panel_title_zh-CN": "⚙️ 视觉调色 BETA 1.0",
            "ui_panel_title_en-US": "⚙️ Visual Tuning BETA 1.0",
            
            "ui_btn_text_zh-CN": "🚀 实时同步到 Discord",
            "ui_btn_text_en-US": "🚀 Sync to Discord",
            
            "ui_preview_title_zh-CN": "Dhik0 [BETA 1.0]",
            "ui_preview_title_en-US": "Dev by Dhik0",
            
            "ui_success_msg_zh-CN": "✅ 字体与文本已成功应用！",
            "ui_success_msg_en-US": "✅ Applied successfully!",
            
            "ui_preview_text_zh-CN": "文本预览: \n1. 你的 BETA 1.0 已就绪。\n2. 可以在 JSON 里随意修改这些文字。\n",
            "ui_preview_text_en-US": "Text Preview: \n1. Your BETA 1.0 is ready.\n2. Feel free to edit these lines in JSON.\n."
        }
        self.load_settings()
        self.lang = self.settings.get("language", "zh-CN")

        self.setup_ui()

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.settings.update(json.load(f))
            except: pass

    def save_settings(self):
        data = {
            "font": self.font_menu.get(), "size": self.size_slider.get(),
            "height": self.height_slider.get(), "color": self.color_entry.get(),
            "bg": self.bg_entry.get(), "language": self.lang,
            "ui_version": self.settings.get("ui_version", "2.2-Lab")
        }
        # 【关键】完整遍历并保留 config 中的所有 ui_ 自定义文本 (包括带语言后缀的)
        for key, value in self.settings.items():
            if key.startswith("ui_"):
                data[key] = value

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_text(self, key):
        # 【核心逻辑升级：三级查找制】
        # 1. 尝试找 config 里的“当前语言特定版”，如 ui_success_msg_en-US
        specific_key = f"ui_{key}_{self.lang}"
        if specific_key in self.settings:
            return self.settings[specific_key]
        
        # 2. 尝试找 config 里的“通用版”，如 ui_success_msg
        generic_key = f"ui_{key}"
        if generic_key in self.settings:
            return self.settings[generic_key]
            
        # 3. 如果 config 里都没有，读代码自带的翻译字典兜底
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["zh-CN"]).get(key, f"Missing_{key}")

    def setup_ui(self):
        self.geometry("850x850")
        ctk.set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1); self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_control_panel()
        self.create_preview_panel()
        
        # 初始化时执行一次全量文本刷新
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        # 统一刷新所有静态文本，配置优先
        self.title(self.get_text("app_title"))
        self.panel_label.configure(text=self.get_text("panel_title"))
        self.bg_label.configure(text=self.get_text("bg_label"))
        self.text_ctrl_label.configure(text=self.get_text("text_ctrl_label"))
        self.light_label.configure(text=self.get_text("light_label"))
        self.preset_label.configure(text=self.get_text("preset_label"))
        self.btn.configure(text=self.get_text("btn_text"))
        self.preview_header_label.configure(text=self.get_text("preview_title"))

        # 刷新大段的预览文本
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", self.get_text("preview_text"))
        
        # 触发一次动态预览渲染 (字号、行高等)
        self.update_preview()

    def change_language(self, new_lang_name):
        self.lang = "zh-CN" if new_lang_name == "简体中文" else "en-US"
        self.save_settings()
        self.refresh_ui_texts()

    def create_control_panel(self):
        control_frame = ctk.CTkScrollableFrame(self)
        control_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.lang_menu = ctk.CTkOptionMenu(control_frame, values=["简体中文", "English"], command=self.change_language)
        self.lang_menu.set("简体中文" if self.lang == "zh-CN" else "English")
        self.lang_menu.pack(anchor="ne", padx=20)

        self.panel_label = ctk.CTkLabel(control_frame, text="", font=("Inter", 20, "bold"))
        self.panel_label.pack(pady=15)

        self.font_menu = ctk.CTkOptionMenu(control_frame, values=["Charter", "Georgia", "Source Han Serif CN", "Microsoft YaHei"], command=self.update_preview)
        self.font_menu.set(self.settings.get("font", "Charter")); self.font_menu.pack(fill="x", padx=20, pady=10)

        self.bg_label = ctk.CTkLabel(control_frame, text="")
        self.bg_label.pack(anchor="w", padx=20, pady=(5, 0))
        self.create_palette(control_frame, self.bg_presets, "bg")
        
        self.bg_entry = ctk.CTkEntry(control_frame); self.bg_entry.insert(0, self.settings.get("bg", "transparent"))
        self.bg_entry.bind("<KeyRelease>", self.update_preview); self.bg_entry.pack(fill="x", padx=20, pady=10)

        self.text_ctrl_label = ctk.CTkLabel(control_frame, text="", font=("Inter", 13, "bold"))
        self.text_ctrl_label.pack(anchor="w", padx=20, pady=(15,5))
        
        self.hue_canvas = ctk.CTkCanvas(control_frame, width=240, height=20, highlightthickness=0, bg="#1E1F22")
        self.hue_canvas.pack(padx=20, pady=5); self.draw_hue_map()
        self.hue_canvas.bind("<Button-1>", self.on_hue_click); self.hue_canvas.bind("<B1-Motion>", self.on_hue_click)

        self.light_label = ctk.CTkLabel(control_frame, text="", font=("Inter", 11))
        self.light_label.pack(anchor="w", padx=20)
        self.light_slider = ctk.CTkSlider(control_frame, from_=0, to=1, command=self.update_from_light_slider)
        self.light_slider.set(0.9); self.light_slider.pack(fill="x", padx=20, pady=5)

        self.preset_label = ctk.CTkLabel(control_frame, text="")
        self.preset_label.pack(anchor="w", padx=20, pady=(5, 0))
        self.create_palette(control_frame, self.text_presets, "text")
        
        self.color_entry = ctk.CTkEntry(control_frame); self.color_entry.insert(0, self.settings.get("color", "#FFFFFF"))
        self.color_entry.bind("<KeyRelease>", self.update_preview); self.color_entry.pack(fill="x", padx=20, pady=10)

        self.size_label = ctk.CTkLabel(control_frame, text="--"); self.size_label.pack(anchor="w", padx=20)
        self.size_slider = ctk.CTkSlider(control_frame, from_=12, to=28, number_of_steps=16, command=self.update_preview)
        self.size_slider.set(self.settings.get("size", 16.0)); self.size_slider.pack(fill="x", padx=20, pady=10)

        self.height_label = ctk.CTkLabel(control_frame, text="--"); self.height_label.pack(anchor="w", padx=20)
        self.height_slider = ctk.CTkSlider(control_frame, from_=1.3, to=2.3, number_of_steps=20, command=self.update_preview)
        self.height_slider.set(self.settings.get("height", 1.75)); self.height_slider.pack(fill="x", padx=20, pady=10)

        self.btn = ctk.CTkButton(control_frame, text="", command=self.apply, fg_color="#5865F2", height=45)
        self.btn.pack(fill="x", padx=20, pady=20)

    def draw_hue_map(self):
        width = 240
        for i in range(width):
            hue = i / width
            r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
            color = "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
            self.hue_canvas.create_line(i, 0, i, 20, fill=color)
        self.hue_pointer = self.hue_canvas.create_line(120, 0, 120, 20, fill="white", width=3)

    def on_hue_click(self, event):
        x = max(0, min(event.x, 240))
        self.current_hue = x / 240
        self.hue_canvas.coords(self.hue_pointer, x, 0, x, 20)
        self.calculate_and_apply_color()

    def update_from_light_slider(self, _=None):
        self.calculate_and_apply_color()

    def calculate_and_apply_color(self):
        r, g, b = colorsys.hls_to_rgb(self.current_hue, self.light_slider.get(), 1.0)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
        self.color_entry.delete(0, "end"); self.color_entry.insert(0, hex_color)
        self.update_preview()

    def set_color_preset(self, target, hex_val):
        entry = self.bg_entry if target == "bg" else self.color_entry
        entry.delete(0, "end"); entry.insert(0, hex_val); self.update_preview()

    def create_palette(self, parent, presets, target):
        frame = ctk.CTkFrame(parent, fg_color="transparent"); frame.pack(fill="x", padx=15, pady=5)
        for i, (name, color) in enumerate(presets):
            is_t = (color.lower() == "transparent")
            btn = ctk.CTkButton(frame, text="", width=35, height=35, fg_color="#313338" if is_t else color, 
                border_width=2 if is_t else 0, border_color="#5865F2" if is_t else None, corner_radius=8, command=lambda c=color: self.set_color_preset(target, c))
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)

    def create_preview_panel(self):
        preview_frame = ctk.CTkFrame(self, fg_color="#313338")
        preview_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        header_box = ctk.CTkFrame(preview_frame, fg_color="transparent"); header_box.pack(fill="x", padx=20, pady=(10,0))
        ctk.CTkLabel(header_box, text="👤", font=("Inter", 24)).pack(side="left")
        self.preview_header_label = ctk.CTkLabel(header_box, text="", font=("Inter", 13, "bold"), text_color="#FFFFFF")
        self.preview_header_label.pack(side="left", padx=10)
        self.preview_text = ctk.CTkTextbox(preview_frame, wrap="word", width=300, height=450)
        self.preview_text.pack(padx=(50, 20), pady=10, fill="both", expand=True)

    def update_preview(self, event=None):
        try:
            f_size = int(self.size_slider.get()); l_height = self.height_slider.get()
            
            # 动态格式化字号和行高文本
            self.size_label.configure(text=self.get_text("size_label").format(f_size))
            self.height_label.configure(text=self.get_text("height_label").format(l_height))
            
            t_color = self.color_entry.get(); b_color = self.bg_entry.get()
            p_bg = "#313338" if b_color.lower() == "transparent" else b_color
            extra_s = int(f_size * (l_height - 1.0))
            
            self.preview_text.configure(font=(self.font_menu.get(), f_size), text_color=t_color if t_color.startswith("#") else "#FFFFFF", 
                spacing2=max(0, extra_s), spacing1=max(0, extra_s // 2), spacing3=max(0, extra_s // 2), fg_color=p_bg)
        except: pass 

    def apply(self):
        self.save_settings()
        themes_dir = os.path.join(os.getenv('APPDATA'), 'BetterDiscord', 'themes')
        target_path = os.path.join(themes_dir, 'Dhik0_Stable_Style.theme.css')
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(generate_css(self.font_menu.get(), self.height_slider.get(), int(self.size_slider.get()), self.color_entry.get(), self.bg_entry.get(), self.settings.get("ui_version", "2.2-Lab")))
            dialog = ctk.CTkLabel(self, text=self.get_text("success_msg"), text_color="#57F287")
            dialog.place(relx=0.5, rely=0.97, anchor="center")
            self.after(3000, dialog.destroy)
        except Exception as e: print(f"❌ 失败：{e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()