import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import csv
from datetime import datetime

class WebScraper:
    def __init__(self, base_url, headers=None):
        """
        初始化网络爬虫
        
        Args:
            base_url: 目标网站的基础URL
            headers: 请求头（可选）
        """
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.links = []
        self.session = requests.Session()
        
    def fetch_page(self, url):
        """
        获取页面内容
        
        Args:
            url: 要获取的URL
            
        Returns:
            BeautifulSoup对象或None
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"请求失败 {url}: {e}")
            return None
    
    def extract_links(self, soup, link_selector='a'):
        """
        从页面中提取链接
        
        Args:
            soup: BeautifulSoup对象
            link_selector: CSS选择器（默认提取所有<a>标签）
            
        Returns:
            链接列表
        """
        page_links = []
        link_elements = soup.select(link_selector)
        
        for link in link_elements:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if href:
                # 转换相对URL为绝对URL
                absolute_url = urljoin(self.base_url, href)
                page_links.append({
                    'url': absolute_url,
                    'text': text,
                    'scraped_at': datetime.now().isoformat()
                })
        
        return page_links
    
    def get_next_page_url(self, soup, next_page_selector=None):
        """
        获取下一页URL
        
        Args:
            soup: BeautifulSoup对象
            next_page_selector: 下一页按钮的CSS选择器
            
        Returns:
            下一页URL或None
        """
        if not next_page_selector:
            # 默认查找常见的"下一页"按钮
            next_button = soup.select_one('a[rel="next"], .next, .pagination a:last-child')
        else:
            next_button = soup.select_one(next_page_selector)
        
        if next_button and next_button.get('href'):
            return urljoin(self.base_url, next_button.get('href'))
        
        return None
    
    def scrape_with_pagination(self, start_url, max_pages=None, 
                               link_selector='a', next_page_selector=None, 
                               delay=1):
        """
        带分页处理的爬虫
        
        Args:
            start_url: 起始URL
            max_pages: 最大页数（None表示无限制）
            link_selector: 链接CSS选择器
            next_page_selector: 下一页选择器
            delay: 页面之间的延迟时间（秒）
        """
        current_url = start_url
        page_count = 0
        
        print(f"开始爬取: {start_url}\n")
        
        while current_url and (max_pages is None or page_count < max_pages):
            page_count += 1
            print(f"正在爬取第 {page_count} 页: {current_url}")
            
            # 获取页面
            soup = self.fetch_page(current_url)
            if not soup:
                break
            
            # 提取链接
            page_links = self.extract_links(soup, link_selector)
            self.links.extend(page_links)
            print(f"  找到 {len(page_links)} 个链接")
            
            # 获取下一页URL
            current_url = self.get_next_page_url(soup, next_page_selector)
            
            # 延迟（礼貌爬虫）
            if current_url:
                time.sleep(delay)
        
        print(f"\n爬取完成! 总共获得 {len(self.links)} 个链接")
        return self.links
    
    def save_to_csv(self, filename='scraped_links.csv'):
        """
        将爬取的链接保存到CSV文件
        
        Args:
            filename: 输出文件名
        """
        if not self.links:
            print("没有链接可保存")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['url', 'text', 'scraped_at'])
                writer.writeheader()
                writer.writerows(self.links)
            print(f"链接已保存到 {filename}")
        except Exception as e:
            print(f"保存失败: {e}")
    
    def save_to_json(self, filename='scraped_links.json'):
        """
        将爬取的链接保存到JSON文件
        
        Args:
            filename: 输出文件名
        """
        import json
        
        if not self.links:
            print("没有链接可保存")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.links, f, ensure_ascii=False, indent=2)
            print(f"链接已保存到 {filename}")
        except Exception as e:
            print(f"保存失败: {e}")
    
    def print_links(self, limit=None):
        """
        打印爬取的链接
        
        Args:
            limit: 限制打印数量
        """
        display_links = self.links[:limit] if limit else self.links
        
        for i, link in enumerate(display_links, 1):
            print(f"{i}. {link['text']}")
            print(f"   URL: {link['url']}\n")


# 使用示例
if __name__ == "__main__":
    # 示例1: 爬取网站（请根据实际需求修改URL和选择器）
    base_url = "https://example.com"  # 修改为目标网站
    start_url = "https://example.com/page/1"  # 修改为起始页面
    
    # 创建爬虫实例
    scraper = WebScraper(base_url)
    
    # 执行爬取（带分页处理）
    links = scraper.scrape_with_pagination(
        start_url=start_url,
        max_pages=5,  # 爬取最多5页
        link_selector='a',  # CSS选择器：所有链接
        next_page_selector='a.next',  # 下一页按钮选择器（根据网站调整）
        delay=2  # 每页之间延迟2秒
    )
    
    # 保存结果
    scraper.save_to_csv('links.csv')
    scraper.save_to_json('links.json')
    
    # 打印前10个链接
    scraper.print_links(limit=10)
