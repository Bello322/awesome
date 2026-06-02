# Awesome

> 一个精心策划的 Python 工具和资源集合

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Bello322/awesome.svg?style=social)](https://github.com/Bello322/awesome)

---

## 📋 目录

- [介绍](#介绍)
- [项目内容](#项目内容)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 介绍

**Awesome** 是一个汇集了有用的 Python 工具、脚本和资源的仓库。无论你是初学者还是经验丰富的开发者，这里都能找到你需要的东西。

### 主要特性

✨ **精选工具** - 经过精心筛选的高质量 Python 脚本  
🚀 **即插即用** - 随时可用，易于集成  
📚 **详细文档** - 每个工具都配备使用指南  
🔧 **持续更新** - 定期添加新工具和改进  

---

## 项目内容

### 📦 当前工具

#### 1. **Web Scraper** (`web_scraper.py`)
一个功能完整的 Python 网络爬虫，支持分页处理和多种数据导出格式。

**功能特性：**
- 🕷️ 网页内容爬取
- 🔗 自动链接提取
- 📄 分页处理
- 💾 CSV/JSON 数据导出
- ⏱️ 请求延迟控制（礼貌爬虫）

**快速示例：**
```python
from web_scraper import WebScraper

scraper = WebScraper("https://example.com")
links = scraper.scrape_with_pagination(
    start_url="https://example.com/page/1",
    max_pages=5,
    delay=2
)
scraper.save_to_csv('output.csv')
```

---

## 快速开始

### 前置要求

- **Python** 3.6 或更高版本
- **pip** 包管理器

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/Bello322/awesome.git
cd awesome

# 安装依赖
pip install -r requirements.txt
```

### 依赖包

```
requests>=2.28.0
beautifulsoup4>=4.11.0
```

或手动安装：
```bash
pip install requests beautifulsoup4
```

---

## 使用指南

### Web Scraper 详细使用

#### 基础用法

```python
from web_scraper import WebScraper

# 创建爬虫实例
scraper = WebScraper(base_url="https://example.com")

# 爬取单页
soup = scraper.fetch_page("https://example.com")
links = scraper.extract_links(soup)
```

#### 分页爬取

```python
# 爬取多页并自动跟进分页
links = scraper.scrape_with_pagination(
    start_url="https://example.com/page/1",
    max_pages=10,              # 最多爬取10页
    link_selector='a',         # 链接CSS选择器
    next_page_selector='a.next', # 下一页按钮选择器
    delay=2                    # 每页延迟2秒
)
```

#### 数据导出

```python
# 导出为 CSV
scraper.save_to_csv('links.csv')

# 导出为 JSON
scraper.save_to_json('links.json')

# 打印链接
scraper.print_links(limit=10)
```

#### 完整示例

```python
from web_scraper import WebScraper

if __name__ == "__main__":
    scraper = WebScraper("https://example.com")
    
    # 爬取网站
    links = scraper.scrape_with_pagination(
        start_url="https://example.com/page/1",
        max_pages=5,
        delay=1.5
    )
    
    # 保存结果
    scraper.save_to_csv('scraped_links.csv')
    scraper.save_to_json('scraped_links.json')
    
    print(f"成功爬取 {len(links)} 个链接！")
```

### 选择器配置

网站结构不同，需要调整 CSS 选择器：

```python
# 查看网站 HTML 结构
# 右键 > 检查 > Elements
# 找到链接元素的 CSS 类名或 ID

# 示例选择器
link_selector = 'a.article-link'  # class 选择器
link_selector = 'a#main-link'      # ID 选择器
link_selector = 'div.content a'    # 后代选择器
link_selector = 'a[href^="http"]'  # 属性选择器
```

---

## 最佳实践

### 爬虫礼仪

✅ **务必遵守以下建议：**

1. **检查 robots.txt** - 尊重网站爬虫政策
   ```python
   # https://example.com/robots.txt
   ```

2. **设置请求延迟** - 避免过度请求
   ```python
   delay=2  # 每页延迟2秒
   ```

3. **使用合理的 User-Agent**
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
   }
   ```

4. **错误处理** - 优雅地处理异常
   ```python
   try:
       soup = scraper.fetch_page(url)
   except Exception as e:
       print(f"错误: {e}")
   ```

5. **查看网站服务条款** - 确保合法爬取

---

## 常见问题 (FAQ)

**Q: 爬虫超时怎么办？**
> A: 增加延迟时间或检查网络连接。

**Q: 如何处理动态加载的内容？**
> A: 使用 Selenium 或 Playwright（需额外配置）。

**Q: 如何避免被封IP？**
> A: 设置合理延迟、使用代理、轮换 User-Agent。

**Q: 支持哪些数据格式导出？**
> A: 目前支持 CSV 和 JSON，可扩展支持其他格式。

---

## 贡献

热烈欢迎贡献新工具、修复 bug 或改进文档！

### 贡献流程

1. **Fork** 本仓库
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启 Pull Request**

### 代码规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南
- 添加清晰的注释和文档字符串
- 包含必要的错误处理
- 更新 README.md 中的相关部分

---

## 许可证

本项目采用 **MIT License** 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 联系方式

- 💬 [提交 Issue](https://github.com/Bello322/awesome/issues)
- 💌 [讨论区](https://github.com/Bello322/awesome/discussions)
- 👤 [GitHub 主页](https://github.com/Bello322)

---

## 致谢

感谢所有为本项目做出贡献的开发者！

---

<div align="center">

⭐ 如果这个项目对你有帮助，请给个 Star！

Made with ❤️ by [Bello322](https://github.com/Bello322)

</div>
