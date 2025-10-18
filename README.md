# AI Model Update Tracker

**Stay updated on the latest changes from Anthropic, OpenAI, and Google AI.**

Automated tracking of Claude, GPT, and Gemini model releases, API updates, and feature launches. Delivered as curated weekly summaries with actionable insights.

---

## 📊 Latest Updates

> **Last Updated:** 2025-10-16
> **Status:** 🚀 Repository initialized, automation ready

*Weekly summaries will appear here once scraping begins*

---

## 🎯 What This Tracks

### Providers (Priority Order)
1. **Anthropic** - Claude models and API
2. **OpenAI** - GPT models and API
3. **Google** - Gemini models and API

### Update Categories
- ✅ **Model Releases** - New model families (e.g., Claude 3.5 → Claude 4)
- ✅ **Version Updates** - Model iterations (e.g., GPT-4 → GPT-4 Turbo)
- ✅ **API Features** - New capabilities (vision, streaming, function calling)
- ✅ **Pricing Changes** - Cost adjustments
- ✅ **Performance** - Speed/quality improvements
- ✅ **Breaking Changes** - Migration requirements

---

## 🔄 How It Works

### Automated (3x/week)
1. **GitHub Actions** scrapes provider sites (Mon/Wed/Fri @ 09:00 UTC)
2. Raw diffs saved to [`/raw/`](./raw/)
3. **Notification issue** created when changes detected

### Manual (~10 min/week)
1. Review `/raw/YYYY-MM-DD-summary.txt`
2. Paste relevant sections into **your AI assistant**
3. Ask for a summary: *"Summarize these AI model updates in our standard format"*
4. Commit summary to [`/updates/`](./updates/)

### Zero Cost
- **GitHub Actions:** Free tier (2,000 min/month, using ~60)
- **AI Summarization:** Use your existing LLM subscription
- **Total:** $0/month

---

## 📂 Repository Structure

```
/
├── providers/          # Provider tracking templates
│   ├── anthropic.md    # Anthropic changelog sources
│   ├── openai.md       # OpenAI changelog sources
│   └── google.md       # Google AI changelog sources
├── updates/            # Curated weekly summaries
│   └── 2025-10-16-summary.md
├── raw/                # Automated scrape output
│   ├── 2025-10-16-anthropic.json
│   ├── 2025-10-16-openai.json
│   ├── 2025-10-16-google.json
│   └── 2025-10-16-summary.txt
├── scripts/
│   └── scrape.py       # Python scraper
└── .github/workflows/
    └── scrape-updates.yml
```

---

## 🚀 Quick Start

### 1. Test the Scraper Locally
```bash
python scripts/scrape.py
```

This will:
- Scrape all three providers
- Save results to `/raw/`
- Output a summary file for review

### 2. Review Raw Output
```bash
cat raw/$(date +%Y-%m-%d)-summary.txt
```

### 3. Summarize with AI Assistant
1. Copy relevant sections from summary file
2. Paste into your preferred LLM (ChatGPT, Claude, Gemini, etc.)
3. Ask: *"Summarize these AI model updates. For each change, include: what changed, why it matters, and migration notes if applicable."*

### 4. Commit Your Summary
```bash
# Save the AI-generated summary to updates/
echo "AI summary here" > updates/2025-10-16-summary.md
git add updates/
git commit -m "Weekly summary: 2025-10-16"
git push
```

---

## 🤖 Automation Setup

The GitHub Action runs automatically, but you can:

### Trigger Manual Scrape
1. Go to **Actions** tab
2. Select **Scrape AI Model Updates**
3. Click **Run workflow**

### Adjust Frequency
Edit `.github/workflows/scrape-updates.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1,3,5'  # Mon/Wed/Fri at 09:00 UTC
```

### Disable Notifications
Remove or comment out the "Create notification issue" step in the workflow.

---

## 📖 Update Format

Each summary follows this template:

```markdown
# Weekly Summary: YYYY-MM-DD

## Anthropic
### [Date] Update Title
**What changed:** Brief description
**Why it matters:** Impact on use cases
**Migration notes:** Breaking changes or action items
**Link:** [Official announcement](URL)

## OpenAI
...

## Google
...
```

---

## 🔍 Provider Resources

### Anthropic
- [Changelog](https://docs.anthropic.com/en/docs/about-claude/changelog)
- [News](https://www.anthropic.com/news)
- [API Docs](https://docs.anthropic.com)

### OpenAI
- [API Changelog](https://platform.openai.com/docs/changelog)
- [Research Blog](https://openai.com/research)
- [API Docs](https://platform.openai.com/docs)

### Google
- [AI Blog](https://blog.google/technology/ai/)
- [Vertex AI Release Notes](https://cloud.google.com/vertex-ai/docs/release-notes)
- [Gemini API Docs](https://ai.google.dev/docs)

---

## 🛠️ Maintenance

### When Scraper Breaks
If a provider changes their site structure:

1. Check error in Actions logs
2. Update scraper in `scripts/scrape.py`
3. Test locally: `python scripts/scrape.py`
4. Commit fix

**Expected:** ~2x/year for maintenance

### Adding More Providers
1. Add provider template to `/providers/`
2. Add scraper function to `scripts/scrape.py`
3. Update README

---

## 📊 Stats

- **Scraping Frequency:** 3x/week
- **GitHub Actions Usage:** ~5 min/run = 60 min/month (3% of free tier)
- **Manual Effort:** ~10 min/week
- **Cost:** $0/month

---

## 🤝 Contributing

This is a personal tracking repo, but feel free to:
- **Fork** and customize for your own use
- **Open issues** for broken scrapers
- **Suggest** additional providers or categories

---

## 📄 License

MIT License - Use freely

---

## 💡 Why This Exists

AI models are evolving rapidly. Keeping up with Claude, GPT, and Gemini updates across blogs, changelogs, and release notes is time-consuming.

**This repo solves that by:**
- 🤖 Automating the scraping
- 📝 Surfacing only what changed
- 🧠 Using AI-assisted summarization
- 💰 Costing $0/month

---

**Questions?** Open an issue or check [provider docs](./providers/).
