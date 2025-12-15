#!/usr/bin/env python3
"""
WordPress to GitHub Blog Migration Script
Scrapes blog posts from WordPress site, downloads media, converts to Markdown
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import json
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
from datetime import datetime
import html2text

class WordPressToGitHub:
    def __init__(self, site_url, output_dir="blog_backup"):
        self.site_url = site_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.posts_dir = self.output_dir / "posts"
        self.media_dir = self.output_dir / "media"
        self.images_dir = self.media_dir / "images"
        self.videos_dir = self.media_dir / "videos"
        
        # Create directories
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0
        
    def discover_blog_posts(self):
        """Discover all blog post URLs from the site"""
        print(f"🔍 Discovering blog posts from {self.site_url}...")
        
        post_urls = set()
        
        # Try common WordPress archive pages
        pages_to_check = [
            f"{self.site_url}/",
            f"{self.site_url}/blog/",
            f"{self.site_url}/posts/",
            f"{self.site_url}/archives/",
        ]
        
        # Try sitemap
        sitemap_urls = [
            f"{self.site_url}/sitemap.xml",
            f"{self.site_url}/sitemap_index.xml",
            f"{self.site_url}/wp-sitemap.xml",
        ]
        
        for sitemap_url in sitemap_urls:
            try:
                print(f"   Checking sitemap: {sitemap_url}")
                response = self.session.get(sitemap_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    locs = soup.find_all('loc')
                    for loc in locs:
                        url = loc.text
                        if self._is_blog_post(url):
                            post_urls.add(url)
                    print(f"   ✓ Found {len(post_urls)} posts from sitemap")
            except Exception as e:
                print(f"   ✗ Sitemap not found: {sitemap_url}")
        
        # Crawl archive pages
        for page_url in pages_to_check:
            try:
                print(f"   Checking archive: {page_url}")
                response = self.session.get(page_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all links
                    for link in soup.find_all('a', href=True):
                        url = urljoin(self.site_url, link['href'])
                        if self._is_blog_post(url):
                            post_urls.add(url)
                            
                    # Try pagination
                    for i in range(2, 20):  # Check up to 20 pages
                        next_page = f"{page_url}page/{i}/"
                        try:
                            response = self.session.get(next_page, timeout=10)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.content, 'html.parser')
                                for link in soup.find_all('a', href=True):
                                    url = urljoin(self.site_url, link['href'])
                                    if self._is_blog_post(url):
                                        post_urls.add(url)
                            else:
                                break
                        except:
                            break
                        time.sleep(0.5)
                        
            except Exception as e:
                print(f"   ✗ Could not check {page_url}: {e}")
        
        print(f"✓ Discovered {len(post_urls)} blog posts")
        return list(post_urls)
    
    def _is_blog_post(self, url):
        """Determine if URL is likely a blog post"""
        # Exclude common non-post pages
        excluded = [
            '/feed/', '/category/', '/tag/', '/author/', 
            '/page/', '/wp-', '/login', '/admin',
            '.xml', '.jpg', '.png', '.gif', '.pdf',
            '/about', '/contact', '/privacy', '/terms',
            '/archives/', '/blog/', '/posts/'
        ]
        
        for excluded_term in excluded:
            if excluded_term in url.lower():
                return False
        
        # Must be from same domain
        if not url.startswith(self.site_url):
            return False
        
        # Parse URL
        parsed = urlparse(url)
        path = parsed.path.rstrip('/')
        
        # Exclude URLs that end with just a date (these are archive pages)
        # e.g., /2025/01/10/ or /2025/01/ or /2025/
        if re.match(r'^/\d{4}(/\d{2})?(/\d{2})?/?$', path):
            return False
        
        # Must have content after the date
        # Good: /2024/01/15/my-post-title/
        # Bad: /2024/01/15/
        if re.match(r'^/\d{4}/\d{2}/\d{2}/?$', path):
            return False
        
        # Typical WordPress post patterns - must have slug after date
        patterns = [
            r'/\d{4}/\d{2}/\d{2}/[a-z0-9-]+',  # /2024/01/15/post-title
            r'/\d{4}/\d{2}/[a-z0-9-]+',        # /2024/01/post-title
            r'/[a-z0-9-]{10,}',                # /my-post-title (longer slugs)
        ]
        
        for pattern in patterns:
            if re.search(pattern, path):
                return True
        
        return False
    
    def scrape_post(self, url):
        """Scrape a single blog post"""
        try:
            print(f"   📄 Scraping: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract post data
            post_data = {
                'url': url,
                'title': self._extract_title(soup),
                'date': self._extract_date(soup),
                'modified_date': self._extract_modified_date(soup),
                'content': self._extract_content(soup),
                'author': self._extract_author(soup),
                'categories': self._extract_categories(soup),
                'tags': self._extract_tags(soup),
                'media': []
            }
            
            return post_data
            
        except Exception as e:
            print(f"   ✗ Error scraping {url}: {e}")
            return None
    
    def _extract_title(self, soup):
        """Extract post title"""
        # Try multiple selectors
        selectors = [
            'h1.entry-title',
            'h1.post-title',
            'article h1',
            'h1[class*="title"]',
            '.entry-title',
            '.post-title',
        ]
        
        for selector in selectors:
            title = soup.select_one(selector)
            if title:
                text = title.get_text().strip()
                # Make sure it's not too long (likely grabbed wrong element)
                if len(text) < 200:
                    return text
        
        # Try h1 tags but filter out navigation
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            # Skip if h1 is inside nav or header
            if h1.find_parent(['nav', 'header']):
                continue
            text = h1.get_text().strip()
            if text and len(text) < 200:
                return text
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text().split('|')[0].split('-')[0].strip()
            if len(title_text) < 200:
                return title_text
        
        # Last resort: extract from URL
        parsed = urlparse(soup.find('link', rel='canonical')['href'] if soup.find('link', rel='canonical') else '')
        if parsed.path:
            parts = [p for p in parsed.path.split('/') if p and not p.isdigit()]
            if parts:
                return parts[-1].replace('-', ' ').title()
        
        return "Untitled Post"
    
    def _extract_date(self, soup):
        """Extract publication date (not modified date)"""
        # Priority 1: Meta tag for published time (most reliable)
        meta_published = soup.find('meta', property='article:published_time')
        if meta_published and meta_published.get('content'):
            return meta_published['content']
        
        # Priority 2: Meta tag for created time
        meta_created = soup.find('meta', property='article:created_time')
        if meta_created and meta_created.get('content'):
            return meta_created['content']
        
        # Priority 3: time tag with class "published" or "entry-date" (not "updated")
        time_published = soup.find('time', class_='published') or soup.find('time', class_='entry-date')
        if time_published and time_published.get('datetime'):
            return time_published['datetime']
        
        # Priority 4: First time tag with datetime (avoid "updated" class)
        time_tags = soup.find_all('time')
        for time_tag in time_tags:
            # Skip if it has "updated" or "modified" in the class
            classes = time_tag.get('class', [])
            if any('updated' in c.lower() or 'modified' in c.lower() for c in classes):
                continue
            if time_tag.get('datetime'):
                return time_tag['datetime']
        
        # Priority 5: JSON-LD structured data
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if isinstance(data, dict):
                    if 'datePublished' in data:
                        return data['datePublished']
                    if 'dateCreated' in data:
                        return data['dateCreated']
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            if 'datePublished' in item:
                                return item['datePublished']
                            if 'dateCreated' in item:
                                return item['dateCreated']
            except:
                pass
        
        # Priority 6: Common date classes (prefer "published" over "updated")
        date_selectors = [
            '.published',
            '.entry-date.published',
            '.post-date',
            '[itemprop="datePublished"]',
            '[itemprop="dateCreated"]',
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                # Check if it has datetime attribute
                if date_elem.get('datetime'):
                    return date_elem['datetime']
                # Otherwise get text
                text = date_elem.get_text().strip()
                if text:
                    return text
        
        # Priority 7: Try to extract from URL (WordPress date-based URLs)
        # e.g., /2024/01/15/post-title/
        # Try from canonical link first
        canonical = soup.find('link', rel='canonical')
        url_to_check = canonical['href'] if canonical and canonical.get('href') else ''
        
        url_date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url_to_check)
        if url_date_match:
            year, month, day = url_date_match.groups()
            return f"{year}-{month}-{day}"
        
        # Last resort: current date
        return datetime.now().isoformat()
    
    def _extract_modified_date(self, soup):
        """Extract last modified/updated date"""
        # Priority 1: Meta tag for modified time
        meta_modified = soup.find('meta', property='article:modified_time')
        if meta_modified and meta_modified.get('content'):
            return meta_modified['content']
        
        # Priority 2: time tag with "updated" or "modified" class
        time_updated = soup.find('time', class_='updated') or soup.find('time', class_='modified')
        if time_updated and time_updated.get('datetime'):
            return time_updated['datetime']
        
        # Priority 3: JSON-LD structured data
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if isinstance(data, dict):
                    if 'dateModified' in data:
                        return data['dateModified']
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and 'dateModified' in item:
                            return item['dateModified']
            except:
                pass
        
        # Priority 4: Common modified date selectors
        modified_selectors = [
            '.updated',
            '.modified',
            '[itemprop="dateModified"]',
        ]
        
        for selector in modified_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                if date_elem.get('datetime'):
                    return date_elem['datetime']
                text = date_elem.get_text().strip()
                if text:
                    return text
        
        # If no modified date found, return None
        return None
    
    def _extract_content(self, soup):
        """Extract main post content"""
        # Try multiple content selectors
        content_selectors = [
            'article .entry-content',
            '.post-content',
            'article .content',
            '[class*="post-content"]',
            'article',
            '.hentry'
        ]
        
        content = None
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        if not content:
            # Last resort: try to find main content
            content = soup.find('main') or soup.find('div', class_=re.compile('content|post'))
        
        if content:
            # Remove unwanted elements
            for unwanted in content.select('script, style, .comments, .related-posts, .share, nav'):
                unwanted.decompose()
            
            return content
        
        return None
    
    def _extract_author(self, soup):
        """Extract post author"""
        # Try meta tag
        meta_author = soup.find('meta', property='article:author')
        if meta_author and meta_author.get('content'):
            return meta_author['content']
        
        # Try common author selectors
        author_selectors = [
            '.author-name',
            '.entry-author',
            '[rel="author"]',
            '[class*="author"]'
        ]
        
        for selector in author_selectors:
            author = soup.select_one(selector)
            if author:
                return author.get_text().strip()
        
        return "Unknown"
    
    def _extract_categories(self, soup):
        """Extract post categories"""
        categories = []
        
        cat_links = soup.select('a[rel="category tag"], .cat-links a, [class*="categor"] a')
        for link in cat_links:
            cat = link.get_text().strip()
            if cat and cat not in categories:
                categories.append(cat)
        
        return categories
    
    def _extract_tags(self, soup):
        """Extract post tags"""
        tags = []
        
        tag_links = soup.select('a[rel="tag"], .tag-links a, [class*="tag"] a')
        for link in tag_links:
            tag = link.get_text().strip()
            if tag and tag not in tags:
                tags.append(tag)
        
        return tags
    
    def download_media(self, content_html, post_slug):
        """Download images and videos from post content"""
        if not content_html:
            return [], content_html
        
        soup = BeautifulSoup(str(content_html), 'html.parser')
        media_files = []
        
        # Download images
        for img in soup.find_all('img'):
            src = img.get('src')
            if not src:
                continue
            
            media_url = urljoin(self.site_url, src)
            local_path = self._download_file(media_url, self.images_dir, post_slug)
            
            if local_path:
                media_files.append({
                    'type': 'image',
                    'original_url': media_url,
                    'local_path': local_path
                })
                # Update img src to local path
                relative_path = f"../../media/images/{local_path.name}"
                img['src'] = relative_path
        
        # Download videos
        for video in soup.find_all(['video', 'source']):
            src = video.get('src')
            if not src:
                continue
            
            media_url = urljoin(self.site_url, src)
            local_path = self._download_file(media_url, self.videos_dir, post_slug)
            
            if local_path:
                media_files.append({
                    'type': 'video',
                    'original_url': media_url,
                    'local_path': local_path
                })
                # Update video src to local path
                relative_path = f"../../media/videos/{local_path.name}"
                if video.name == 'video':
                    video['src'] = relative_path
                else:
                    video['src'] = relative_path
        
        return media_files, str(soup)
    
    def _download_file(self, url, destination_dir, post_slug):
        """Download a single media file"""
        # Skip old unreachable server IPs
        if '107.23.205.221' in url:
            print(f"      ⊘ Skipping old server: {url}")
            return None
        
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Generate filename
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            
            # Clean filename
            filename = re.sub(r'[^\w\-.]', '_', filename)
            filename = f"{post_slug}_{filename}"
            
            filepath = destination_dir / filename
            
            # Download file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"      ✓ Downloaded: {filename}")
            return filepath
            
        except Exception as e:
            print(f"      ✗ Failed to download {url}: {e}")
            return None
    
    def convert_to_markdown(self, post_data):
        """Convert post to Markdown with frontmatter"""
        if not post_data or not post_data['content']:
            return None
        
        # Clean title - remove excessive whitespace and newlines
        title = post_data['title'].strip()
        title = ' '.join(title.split())  # Normalize whitespace
        title = title[:200]  # Limit title length
        
        # Generate slug from URL or title
        slug = self._generate_slug(post_data['url'], title)
        
        # Download media
        media_files, updated_html = self.download_media(post_data['content'], slug)
        post_data['media'] = media_files
        
        # Convert HTML to Markdown
        markdown_content = self.h2t.handle(updated_html)
        
        # Create frontmatter
        date_str = post_data['date']
        try:
            # Try to parse and format date
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
        except:
            # If date parsing fails, use current date
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Format modified date if available
        modified_str = ""
        if post_data.get('modified_date'):
            try:
                mod_date = post_data['modified_date']
                if 'T' in mod_date:
                    dt = datetime.fromisoformat(mod_date.replace('Z', '+00:00'))
                    modified_str = dt.strftime('%Y-%m-%d')
                else:
                    modified_str = mod_date
            except:
                pass
        
        frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
date: {date_str}"""
        
        if modified_str and modified_str != date_str:
            frontmatter += f"""
modified: {modified_str}"""
        
        frontmatter += f"""
author: {post_data['author']}
categories: {json.dumps(post_data['categories'])}
tags: {json.dumps(post_data['tags'])}
original_url: {post_data['url']}
---

"""
        
        full_markdown = frontmatter + markdown_content
        
        # Create safe filename with limited length
        # Format: YYYY-MM-DD_slug.md
        safe_slug = re.sub(r'[^\w\-]', '-', slug)[:50]
        safe_slug = re.sub(r'-+', '-', safe_slug).strip('-')
        
        if not safe_slug:
            # If slug is empty, use hash of URL
            import hashlib
            safe_slug = hashlib.md5(post_data['url'].encode()).hexdigest()[:12]
        
        filename = f"{date_str}_{safe_slug}.md"
        filepath = self.posts_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            print(f"      ✓ Saved: {filename}")
            return filepath
        except OSError as e:
            # If filename is still too long, truncate further
            print(f"      ⚠ Filename too long, truncating...")
            safe_slug = safe_slug[:20]
            filename = f"{date_str}_{safe_slug}.md"
            filepath = self.posts_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            print(f"      ✓ Saved: {filename}")
            return filepath
    
    def _generate_slug(self, url, title):
        """Generate a URL-safe slug"""
        # Try to extract slug from URL
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p and not p.isdigit()]
        
        if path_parts:
            slug = path_parts[-1]
            # Clean up the slug
            slug = re.sub(r'[^\w\s-]', '', slug)
            slug = re.sub(r'[-\s]+', '-', slug)
        else:
            # Generate from title
            slug = title.lower()
            # Remove non-alphanumeric characters except spaces and hyphens
            slug = re.sub(r'[^\w\s-]', '', slug)
            # Replace spaces and multiple hyphens with single hyphen
            slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        # If slug is still empty or too generic, generate from URL hash
        if not slug or len(slug) < 3:
            import hashlib
            slug = hashlib.md5(url.encode()).hexdigest()[:12]
        
        # Limit to 50 characters maximum
        return slug[:50]
    
    def create_index(self, post_files):
        """Create an index/README for the blog backup"""
        readme_content = f"""# Blog Backup from {self.site_url}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Statistics
- Total posts: {len(post_files)}
- Total media files: {len(list(self.images_dir.glob('*')))} images, {len(list(self.videos_dir.glob('*')))} videos

## Posts

"""
        
        # Sort posts by filename (which includes date)
        sorted_posts = sorted(post_files)
        
        for post_file in sorted_posts:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title from frontmatter
                title_match = re.search(r'title: "(.*?)"', content)
                date_match = re.search(r'date: (.*?)$', content, re.MULTILINE)
                
                title = title_match.group(1) if title_match else post_file.stem
                date = date_match.group(1) if date_match else ''
                
                readme_content += f"- [{title}](posts/{post_file.name}) - {date}\n"
        
        readme_path = self.output_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n✓ Created index: {readme_path}")
    
    def run(self):
        """Main execution method"""
        print(f"\n{'='*60}")
        print(f"WordPress to GitHub Migration")
        print(f"{'='*60}\n")
        
        # Discover posts
        post_urls = self.discover_blog_posts()
        
        if not post_urls:
            print("\n✗ No blog posts found. Please check your site URL.")
            return
        
        print(f"\n📝 Processing {len(post_urls)} blog posts...\n")
        
        processed = 0
        failed = 0
        post_files = []
        
        for i, url in enumerate(post_urls, 1):
            print(f"[{i}/{len(post_urls)}] Processing...")
            
            post_data = self.scrape_post(url)
            
            if post_data:
                markdown_file = self.convert_to_markdown(post_data)
                if markdown_file:
                    post_files.append(markdown_file)
                    processed += 1
                else:
                    failed += 1
            else:
                failed += 1
            
            # Be polite to the server
            time.sleep(1)
        
        # Create index
        if post_files:
            self.create_index(post_files)
        
        # Summary
        print(f"\n{'='*60}")
        print(f"✓ Migration Complete!")
        print(f"{'='*60}")
        print(f"Successfully processed: {processed} posts")
        print(f"Failed: {failed} posts")
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"  - Posts: {self.posts_dir.absolute()}")
        print(f"  - Images: {self.images_dir.absolute()}")
        print(f"  - Videos: {self.videos_dir.absolute()}")
        print(f"\n Next steps:")
        print(f"  1. cd {self.output_dir.absolute()}")
        print(f"  2. git init")
        print(f"  3. git add .")
        print(f"  4. git commit -m 'Initial blog backup'")
        print(f"  5. Create a repo on GitHub and push")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python wordpress_to_github.py <your-wordpress-site-url>")
        print("Example: python wordpress_to_github.py https://netjoints.com")
        sys.exit(1)
    
    site_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "blog_backup"
    
    migrator = WordPressToGitHub(site_url, output_dir)
    migrator.run()
