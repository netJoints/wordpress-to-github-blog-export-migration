# WordPress to GitHub Migration Tool

This script automatically scrapes your WordPress blog, downloads all posts and media files, converts them to Markdown, and organizes everything for GitHub.

## Features

- ✅ Automatically discovers all blog posts (no XML export needed!)
- ✅ Downloads all images and videos from posts
- ✅ Converts HTML content to Markdown
- ✅ Creates individual Markdown files for each post
- ✅ Adds YAML frontmatter with metadata (title, date, categories, tags, etc.)
- ✅ Updates image/video paths to local files
- ✅ Generates a README index of all posts
- ✅ Ready for GitHub Pages (Jekyll/Hugo compatible)

## Installation

### 1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4 lxml html2text
```

## Usage

### Basic usage:
```bash
python wordpress_to_github.py https://netjoints.com
```

### Custom output directory:
```bash
python wordpress_to_github.py https://netjoints.com my-blog-backup
```

## What It Does

1. **Discovers Posts**: Checks sitemaps and crawls archive pages to find all blog posts
2. **Scrapes Content**: Extracts title, date, author, categories, tags, and content
3. **Downloads Media**: Saves all images and videos locally
4. **Converts to Markdown**: Transforms HTML to clean Markdown with frontmatter
5. **Organizes Files**: Creates structured directories for posts and media
6. **Creates Index**: Generates README.md with links to all posts

## Output Structure

```
blog_backup/
├── README.md                 # Index of all posts
├── posts/                    # All blog posts as Markdown
│   ├── 2024-01-15_my-first-post.md
│   ├── 2024-02-20_another-post.md
│   └── ...
└── media/
    ├── images/              # All downloaded images
    │   ├── my-first-post_image1.jpg
    │   └── ...
    └── videos/              # All downloaded videos
        └── ...
```

## Example Post Format

Each Markdown file includes frontmatter:

```markdown
---
title: "My Blog Post Title"
date: 2024-01-15
author: John Doe
categories: ["Technology", "Web Development"]
tags: ["WordPress", "Migration", "GitHub"]
original_url: https://netjoints.com/2024/01/15/my-post
---

# Post content here

Images and videos are automatically linked to local files.

![Alt text](../../media/images/my-first-post_image1.jpg)
```

## After Migration - Push to GitHub

```bash
cd blog_backup

# Initialize git repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial blog backup from WordPress"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/yourusername/your-blog.git
git branch -M main
git push -u origin main
```

## Using with GitHub Pages

### Option 1: Jekyll (GitHub's default)

1. Rename `posts/` to `_posts/`
2. Create a `_config.yml`:
```yaml
title: My Blog
description: Migrated from WordPress
theme: minima
```
3. Enable GitHub Pages in repo settings

### Option 2: Hugo

1. Install Hugo: `brew install hugo`
2. Create new site: `hugo new site myblog`
3. Copy `posts/` to `myblog/content/posts/`
4. Copy `media/` to `myblog/static/media/`
5. Choose a theme and configure

## Troubleshooting

### No posts found?
- Check if your site URL is correct
- Try with/without trailing slash
- Your site might have non-standard URL structure

### Images not downloading?
- Check if images are hosted externally (CDN)
- Some images might be behind authentication
- Script may need adjustment for specific image patterns

### Script running slow?
- Normal for large sites (200 posts ~10-20 minutes)
- Script sleeps 1 second between requests to be polite
- You can reduce `time.sleep(1)` to `time.sleep(0.5)` if needed

### Missing content?
- Some WordPress themes use non-standard HTML structure
- Script tries multiple selectors but may need customization
- Check generated files and adjust selectors if needed

## Customization

The script includes multiple fallback selectors for:
- Post titles
- Content areas
- Dates
- Authors
- Categories/tags

If your WordPress theme uses unique class names, you can edit the selector lists in the script:

```python
content_selectors = [
    'article .entry-content',
    '.post-content',
    # Add your theme's selector here
    '.your-custom-class'
]
```

## Notes

- Script respects robots.txt and includes polite delays
- Downloads are logged to console
- Failed downloads are reported but don't stop the process
- Original URLs are preserved in frontmatter
- Media file paths are automatically updated in Markdown

## License

Free to use and modify for your needs.

## Support

For issues specific to netjoints.com migration, check:
1. Site accessibility
2. WordPress version and theme
3. Any authentication requirements
