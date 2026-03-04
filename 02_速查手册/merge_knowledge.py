import yaml
import os

# 定义路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MKDOCS_YML_PATH = os.path.join(BASE_DIR, 'mkdocs.yml')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUTPUT_FILE = os.path.join(BASE_DIR, 'knowledge_base_full.md')

def read_mkdocs_nav():
    """读取 mkdocs.yml 中的 nav 配置"""
    if not os.path.exists(MKDOCS_YML_PATH):
        print(f"Error: {MKDOCS_YML_PATH} not found.")
        return None
    
    with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config.get('nav', [])
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return None

def process_nav_item(item, level=1):
    """递归处理导航条目，返回合并后的 Markdown 内容"""
    content = ""
    
    if isinstance(item, str):
        # 简单字串情况 (通常不会直接出现在 nav 顶层，除非是 'Page: path.md' 格式被解析错，但在 list 中通常是 dict)
        # 这里主要处理 list 中的项
        pass
        
    elif isinstance(item, dict):
        # 字典项，形如 { 'Title': 'path/to/file.md' } 或 { 'Title': [ ... ] }
        for title, value in item.items():
            # 添加章节标题
            header_prefix = "#" * level
            content += f"\n{header_prefix} {title}\n\n"
            
            if isinstance(value, str):
                # 是文件路径
                file_path = os.path.join(DOCS_DIR, value)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                            # 可选：降低引用件内部标题的层级，以保持结构清晰
                            # 但用户要求"不变更现在的知识库结构"，直接拼接可能更符合"汇总"直觉
                            # 为避免标题冲突，这里简单拼接，不做复杂的 AST 转换
                            content += file_content + "\n\n---\n\n"
                            print(f"Added: {title} ({value})")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        content += f"> Error reading file: {value}\n\n"
                else:
                    print(f"Warning: File not found: {file_path}")
                    content += f"> File not found: {value}\n\n"
            
            elif isinstance(value, list):
                # 是子目录列表
                for sub_item in value:
                    content += process_nav_item(sub_item, level + 1)
    
    return content

def main():
    print("Starting knowledge base aggregation...")
    nav = read_mkdocs_nav()
    if not nav:
        print("No navigation found or failed to read mkdocs.yml.")
        return

    full_content = "# 数据分析师 Python 终极知识库 (完整汇总版)\n\n"
    full_content += "> 本文档由脚本自动生成，汇总了 MkDocs 知识库的所有内容。\n\n---\n\n"
    
    for item in nav:
        full_content += process_nav_item(item, level=1)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"\nSuccessfully generated: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
