# 🚀 WordPress to GitHub Blog Migration Kit

**Complete toolkit to migrate your WordPress blog to GitHub with zero XML exports needed!**

Perfect for migrating **netjoints.com** (or any WordPress site) to GitHub Pages.

## 🎯 What This Does

- ✅ **Automatically discovers** all your blog posts (no XML export needed!)
- ✅ **Scrapes content** including titles, dates, authors, categories, tags
- ✅ **Downloads all media** (images and videos)
- ✅ **Converts to Markdown** with proper frontmatter
- ✅ **Creates individual files** for each post (perfect for GitHub)
- ✅ **Updates image paths** to local files
- ✅ **GitHub Pages ready** (Jekyll or Hugo compatible)
- ✅ **Includes GitHub Actions** for automatic deployment

## 📦 Files Included

```
wordpress_to_github.py      # Main migration script
migrate.sh                   # Quick-start script (easiest way!)
requirements.txt             # Python dependencies
SETUP_GUIDE.md              # Detailed documentation
_config.yml                 # Jekyll configuration for GitHub Pages
github-actions-deploy.yml   # GitHub Actions workflow
README.md                   # This file
```

## 🏃 Quick Start (3 Steps!)

### Step 1: Run the migration script

**Easiest way (interactive):**
```bash
chmod +x migrate.sh
./migrate.sh
```

The script will prompt you for:
- Your WordPress URL (e.g., https://netjoints.com)
- Output directory name (default: blog_backup)

**Or run directly:**
```bash
pip3 install requests beautifulsoup4 lxml html2text
python3 wordpress_to_github.py https://netjoints.com
```

### Step 2: Wait for migration to complete

The script will:
- Discover all blog posts (~200 posts should take 10-20 minutes)
- Download all media files
- Convert everything to Markdown
- Create organized directory structure

### Step 3: Push to GitHub

```bash
cd blog_backup

# Rename posts folder for Jekyll
mv posts _posts

# Copy Jekyll config
cp ../_config.yml .

# Edit _config.yml with your details
# (title, description, author, etc.)

# Initialize git
git init
git add .
git commit -m "Initial blog backup from WordPress"

# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/your-blog.git
git branch -M main
git push -u origin main
```

## 📁 Output Structure

After migration, you'll have:

```
blog_backup/
├── README.md                    # Index of all posts
├── _posts/                      # All blog posts (rename from posts/)
│   ├── 2024-01-15_my-post.md
│   ├── 2024-02-20_another-post.md
│   └── ... (200 posts)
└── media/
    ├── images/                  # All images (organized by post)
    │   ├── my-post_image1.jpg
    │   └── ...
    └── videos/                  # All videos
        └── ...
```

## 📝 Markdown Format

Each post will look like:

```markdown
---
title: "My Blog Post Title"
date: 2024-01-15
author: John Doe
categories: ["Technology", "Web Development"]
tags: ["WordPress", "GitHub"]
original_url: https://netjoints.com/2024/01/15/my-post
---

# Post Content

Your blog post content here, converted from HTML to Markdown.

Images are automatically linked to local files:
![Alt text](../media/images/my-post_image1.jpg)
```

## 🌐 Deploy to GitHub Pages

### Option A: Automatic Deployment (Recommended)

1. **Enable GitHub Pages:**
   - Go to your repo → Settings → Pages
   - Source: "GitHub Actions"

2. **Add the workflow file:**
   ```bash
   mkdir -p .github/workflows
   cp ../github-actions-deploy.yml .github/workflows/deploy.yml
   git add .github
   git commit -m "Add GitHub Actions deployment"
   git push
   ```

3. **That's it!** Your blog will auto-deploy on every push.

Your blog will be live at: `https://yourusername.github.io/your-blog/`

### Option B: Manual Jekyll Setup

If you want more control:

1. **Install Jekyll locally:**
   ```bash
   gem install bundler jekyll
   ```

2. **Create Gemfile:**
   ```ruby
   source "https://rubygems.org"
   gem "github-pages", group: :jekyll_plugins
   ```

3. **Install and test:**
   ```bash
   bundle install
   bundle exec jekyll serve
   ```

4. **Visit:** http://localhost:4000

## 🎨 Customize Your Blog

### Change Theme

Edit `_config.yml`:
```yaml
theme: minima  # or: jekyll-theme-cayman, jekyll-theme-minimal, etc.
```

Popular themes:
- `minima` (default, clean)
- `jekyll-theme-cayman`
- `jekyll-theme-minimal`
- `jekyll-theme-slate`

Or use a custom theme from https://jekyllthemes.io

### Add Features

Uncomment in `_config.yml`:
```yaml
# Google Analytics
google_analytics: UA-XXXXXXXX-X

# Disqus comments
disqus:
  shortname: your-shortname

# Social links
github_username: yourusername
twitter_username: yourusername
```

## 🛠️ Troubleshooting

### "No posts found"
- Verify your site URL is correct
- Try with/without `www.` or trailing slash
- Check if your site is accessible

### "Import errors"
```bash
pip3 install --upgrade requests beautifulsoup4 lxml html2text
```

### "Images not downloading"
- Some images might be on external CDNs
- Check if images require authentication
- Script will continue and log failures

### "Script is slow"
- Normal! 200 posts = 10-20 minutes
- Script waits 1 second between requests (polite crawling)
- Don't interrupt - progress is logged

### "Missing some content"
- Your WordPress theme might use custom HTML structure
- Check `SETUP_GUIDE.md` for customization options
- You may need to adjust CSS selectors in the script

## 💡 Pro Tips

1. **Test with a few posts first:**
   - Limit the script to process first 10 posts
   - Verify output quality before full migration

2. **Backup first:**
   - Even though XML export isn't working, try to backup via hosting control panel

3. **Check output quality:**
   - Review a few generated Markdown files
   - Check if images are downloading correctly
   - Verify frontmatter data

4. **Customize the theme:**
   - After migration, spend time on `_config.yml`
   - Try different Jekyll themes
   - Add custom CSS

5. **SEO:**
   - Keep same URL structure (permalink in `_config.yml`)
   - Add 301 redirects from old URLs if needed
   - Submit new sitemap to Google

## 🤔 Why GitHub Pages?

- **Free hosting** for your blog
- **Version control** for all posts
- **Markdown editing** is simpler than WordPress
- **No database** needed (static site)
- **Fast** and secure
- **No plugin updates** or security patches
- **Git-based** workflow

## 📚 Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [Jekyll Themes](https://jekyllthemes.io/)

## ⚠️ Important Notes

- Script respects robots.txt and crawls politely
- Downloads are logged to console
- Original URLs are preserved in frontmatter
- Script handles 404s and timeouts gracefully
- Media files are renamed to avoid conflicts

## 📧 Need Help?

If you run into issues:
1. Check `SETUP_GUIDE.md` for detailed troubleshooting
2. Review error messages in console
3. Verify site accessibility
4. Check if WordPress is blocking automated access

## 🎉 Success Checklist

- [ ] Ran migration script
- [ ] Verified posts and media downloaded
- [ ] Reviewed Markdown output quality
- [ ] Created GitHub repository
- [ ] Pushed files to GitHub
- [ ] Renamed `posts/` to `_posts/`
- [ ] Copied and edited `_config.yml`
- [ ] Enabled GitHub Pages in repo settings
- [ ] (Optional) Added GitHub Actions workflow
- [ ] Blog is live! 🚀

---

**Good luck with your migration!** 🎊

Your netjoints.com blog will look great on GitHub Pages.
