# WordPress to GitHub Blog Migration Tool

🚀 **Automatically migrate your entire WordPress blog to GitHub without needing XML exports!**

This powerful Python script discovers, scrapes, and converts your WordPress blog posts into individual Markdown files with all media assets, perfect for GitHub Pages, Jekyll, Hugo, or any static site generator.

## ✨ Features

- ✅ **No XML Export Required** - Works even when WordPress export is broken
- ✅ **Automatic Post Discovery** - Crawls sitemaps and archives to find all posts
- ✅ **Smart Content Extraction** - Intelligently extracts titles, dates, authors, categories, and tags
- ✅ **Media Downloads** - Automatically downloads all images and videos
- ✅ **Markdown Conversion** - Converts HTML to clean, readable Markdown
- ✅ **Original Dates Preserved** - Extracts actual publication dates, not modified dates
- ✅ **YAML Frontmatter** - Adds metadata for Jekyll/Hugo compatibility
- ✅ **Individual Files** - Creates one Markdown file per blog post
- ✅ **Archive Page Filtering** - Intelligently skips index/archive pages
- ✅ **Error Resilient** - Continues processing even if some downloads fail
- ✅ **Progress Logging** - Real-time console output of what's being processed
- ✅ **GitHub Pages Ready** - Output structure works perfectly with GitHub Pages

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Post Format](#post-format)
- [Deploying to GitHub Pages](#deploying-to-github-pages)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Requirements

- Python 3.7+
- pip (Python package manager)

## 📥 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/wordpress-to-github.git
   cd wordpress-to-github
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install requests beautifulsoup4 lxml html2text
   ```

## 🚀 Quick Start

Run the migration script with your WordPress URL:

```bash
python wordpress_to_github.py https://yourblog.com
```

That's it! The script will:
1. Discover all blog posts
2. Download content and media
3. Convert to Markdown
4. Save everything to `blog_backup/`

## 💻 Usage

### Basic Usage

```bash
python wordpress_to_github.py <your-wordpress-url>
```

**Example:**
```bash
python wordpress_to_github.py https://netjoints.com
```

### Custom Output Directory

```bash
python wordpress_to_github.py <your-wordpress-url> <output-directory>
```

**Example:**
```bash
python wordpress_to_github.py https://netjoints.com my-blog-backup
```

### What Happens During Migration

```
🔍 Discovering blog posts from https://yourblog.com...
   Checking sitemap: https://yourblog.com/sitemap.xml
   ✓ Found 150 posts from sitemap
   Checking archive: https://yourblog.com/
✓ Discovered 200 blog posts

📝 Processing 200 blog posts...

[1/200] Processing...
   📄 Scraping: https://yourblog.com/2024/01/15/my-post/
      ✓ Downloaded: my-post_image1.jpg
      ✓ Downloaded: my-post_image2.png
      ✓ Saved: 2024-01-15_my-post.md

[2/200] Processing...
...

============================================================
✓ Migration Complete!
============================================================
Successfully processed: 198 posts
Failed: 2 posts

Output directory: /path/to/blog_backup
  - Posts: /path/to/blog_backup/posts
  - Images: /path/to/blog_backup/media/images
  - Videos: /path/to/blog_backup/media/videos

Next steps:
  1. cd blog_backup
  2. git init
  3. git add .
  4. git commit -m 'Initial blog backup'
  5. Create a repo on GitHub and push
============================================================
```

## 📁 Output Structure

```
blog_backup/
├── README.md                          # Index of all posts with links
├── posts/                             # All blog posts as Markdown
│   ├── 2024-01-15_my-first-post.md
│   ├── 2024-02-20_another-post.md
│   ├── 2024-03-10_third-post.md
│   └── ...
└── media/
    ├── images/                        # All downloaded images
    │   ├── my-first-post_image1.jpg
    │   ├── my-first-post_image2.png
    │   ├── another-post_screenshot.png
    │   └── ...
    └── videos/                        # All downloaded videos
        ├── my-post_demo.mp4
        └── ...
```

## 📝 Post Format

Each Markdown file includes YAML frontmatter with metadata:

```markdown
---
title: "My Blog Post Title"
date: 2024-01-15
modified: 2024-03-10
author: John Doe
categories: ["Technology", "Web Development"]
tags: ["WordPress", "Migration", "GitHub"]
original_url: https://yourblog.com/2024/01/15/my-post
---

# Your Post Content Here

The HTML content is converted to clean Markdown with proper formatting.

Images are automatically linked to local files:

![Image description](../../media/images/my-post_image1.jpg)

Videos and other media are also handled automatically.
```

### Frontmatter Fields

- **title**: Post title (extracted from h1 or meta tags)
- **date**: Original publication date (when the blog was created)
- **modified**: Last modified date (only if different from publication date)
- **author**: Post author
- **categories**: Array of categories
- **tags**: Array of tags
- **original_url**: Original WordPress URL for reference

## 🌐 Deploying to GitHub Pages

### Step 1: Prepare Your Repository

```bash
cd blog_backup

# Rename posts folder for Jekyll
mv posts _posts

# Initialize git repository
git init
git add .
git commit -m "Initial blog migration from WordPress"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `your-blog` or `yourusername.github.io`
3. Don't initialize with README (we already have content)

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/yourusername/your-blog.git
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. Your blog will be live at `https://yourusername.github.io/your-blog/`

### Step 5: Configure Jekyll (Optional)

Create `_config.yml` in your repository root:

```yaml
title: My Blog
description: Migrated from WordPress
author: Your Name
email: your-email@example.com

# Use permalinks to match WordPress URLs
permalink: /:year/:month/:day/:title/

# Theme
theme: minima

# Plugins
plugins:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
```

### Popular Jekyll Themes

- `minima` - Clean, minimalist (default)
- `jekyll-theme-cayman` - Modern, professional
- `jekyll-theme-slate` - Dark theme
- `jekyll-theme-minimal` - Ultra-minimal

Browse more at [jekyllthemes.io](https://jekyllthemes.io)

## 🐛 Troubleshooting

### No Posts Found

**Issue:** Script reports 0 posts discovered

**Solutions:**
- Verify your WordPress URL is correct (with/without `www.`)
- Try with/without trailing slash
- Check if site is publicly accessible
- Some sites may have non-standard URL structures

### Import/Module Errors

**Issue:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
pip install requests beautifulsoup4 lxml html2text
```

If you get "externally-managed-environment" error:
```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Option 2: Install with flag
pip install --break-system-packages requests beautifulsoup4 lxml html2text
```

### Images Not Downloading

**Issue:** Some images fail to download

**Reasons:**
- Images hosted on external CDNs
- Old server no longer accessible
- Images behind authentication
- Network timeout

**Solution:** The script will continue and log failures. You can:
- Manually download missing images later
- Check your WordPress uploads folder for backups
- Accept that some old images may be missing

### Wrong Dates on Posts

**Issue:** Posts showing today's date instead of original date

**Causes:**
- Archive/index pages were scraped instead of actual posts
- Post doesn't have proper date metadata

**Solution:**
- The updated script filters out archive pages automatically
- For posts with wrong dates, manually check the URL structure
- Edit the `date:` field in the Markdown frontmatter

### Script Running Slow

**Issue:** Migration taking very long

**Reasons:**
- Normal for large sites (200+ posts can take 10-20 minutes)
- Old/unreachable servers causing timeouts
- Large media files

**Solutions:**
- Be patient - progress is logged in real-time
- Script now skips known unreachable servers
- Don't interrupt - each completed post is saved

### "Filename Too Long" Error

**Issue:** `OSError: [Errno 63] File name too long`

**Cause:** Script grabbed navigation/menu content as title

**Solution:** The updated script now:
- Limits filename length
- Validates title extraction
- Falls back to URL-based slugs

## 🎨 Customization

### Adjusting Content Selectors

If your WordPress theme uses unique HTML structure, you can customize the CSS selectors:

Edit `wordpress_to_github.py`:

```python
# Customize title selectors
selectors = [
    'h1.entry-title',
    'h1.post-title',
    '.your-custom-class',  # Add your theme's selector
]

# Customize content selectors
content_selectors = [
    'article .entry-content',
    '.post-content',
    '.your-content-class',  # Add your theme's selector
]
```

### Changing Sleep Delays

The script waits 1 second between requests to be polite:

```python
# In the run() method, change:
time.sleep(1)  # Change to 0.5 for faster (less polite)
```

### Skipping Specific URLs

Add patterns to exclude:

```python
def _is_blog_post(self, url):
    excluded = [
        '/feed/', '/category/', '/tag/',
        '/your-custom-exclude/',  # Add custom exclusions
    ]
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Areas for Improvement

- Support for more WordPress themes
- Better handling of custom post types
- WordPress API integration (for sites with REST API enabled)
- GUI version for non-technical users
- Docker container for easy deployment
- Support for WordPress multisite
- Better media optimization (image compression)

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Built with Python and love for the open-source community
- Uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Uses [html2text](https://github.com/Alir3z4/html2text) for Markdown conversion
- Inspired by the need to preserve content when WordPress exports fail

## 📞 Support

If you found this tool helpful, please:
- ⭐ Star this repository
- 🐛 Report bugs via Issues
- 💡 Suggest features via Issues
- 🔀 Submit Pull Requests

## 🎯 Use Cases

This tool is perfect for:

- **Blog Migration** - Moving from WordPress to static site generators
- **Backup** - Creating a complete, portable backup of your blog
- **Archival** - Preserving content in a simple, future-proof format
- **Multi-platform Publishing** - Maintaining content in Markdown for multiple platforms
- **Version Control** - Managing blog content with Git
- **Collaboration** - Enabling pull request-based editing workflows
- **Performance** - Switching from dynamic WordPress to fast static sites
- **Cost Reduction** - Moving from paid WordPress hosting to free GitHub Pages

## 📊 Success Stories

This tool has successfully migrated:
- ✅ 291 posts from netjoints.com
- ✅ Blogs with 600MB+ of media
- ✅ Sites with broken WordPress exports
- ✅ Multiple theme styles and layouts

## 🔮 Roadmap

Future enhancements planned:
- [ ] WordPress REST API support
- [ ] Comment export and conversion to Staticman/Disqus
- [ ] Automatic 301 redirect generation
- [ ] Custom taxonomy support
- [ ] WooCommerce product migration
- [ ] Multi-language site support
- [ ] Progress bar instead of text logging
- [ ] Resume from interruption
- [ ] Selective post migration (date ranges, categories)

---

**Made with ❤️ for the WordPress and GitHub communities**

If this tool saved you time, consider sharing it with others who might need it!
