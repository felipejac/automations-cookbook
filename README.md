# Automations Cookbook

The Living Repository: Self-evolving automation &amp; AI hub with n8n, Zapier &amp; API integrations. Auto-generated tutorials, downloadable templates, and LLM-friendly documentation.

## 🚀 Features

- **Automated Web Scraping**: Scrapes templates from n8n and Zapier with rate limiting and error handling
- **LLM Tutorial Generation**: Uses OpenAI API to generate comprehensive tutorials from templates
- **SEO Optimization**: Generates YAML metadata for improved search engine visibility
- **Weekly Updates**: GitHub Actions CI/CD pipeline runs weekly to keep content fresh
- **API Endpoints**: RESTful API for accessing templates programmatically
- **Netlify Deployment**: Ready for serverless deployment

## 📁 Project Structure

```
automations-cookbook/
├── scripts/              # Python automation framework
│   ├── __init__.py      # Package initialization
│   ├── config.py        # Configuration management
│   ├── logger.py        # Logging utilities
│   ├── scraper.py       # Web scraping for n8n & Zapier
│   ├── tutorial_generator.py  # LLM-based tutorial generation
│   ├── metadata_generator.py  # SEO metadata generation
│   └── main.py          # Main orchestration script
├── api/                 # Netlify serverless functions
│   └── templates.py     # Template download endpoint
├── .github/workflows/   # CI/CD pipelines
│   └── automation.yml   # Weekly scraping workflow
├── data/                # Generated data (created at runtime)
├── requirements.txt     # Python dependencies
├── netlify.toml        # Netlify configuration
└── .env.example        # Environment variables template
```

## 🛠️ Setup

### Prerequisites

- Python 3.11 or higher
- OpenAI API key (for tutorial generation)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/felipejac/automations-cookbook.git
cd automations-cookbook
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## 💻 Usage

### Run the Full Pipeline

```bash
# Scrape templates, generate tutorials, and create metadata
python -m scripts.main
```

### Scraping Only

```bash
# Scrape templates without LLM generation
python -m scripts.main --scrape-only --n8n-limit 20 --zapier-limit 20
```

### Skip Tutorial Generation

```bash
# Scrape and generate metadata only (no LLM calls)
python -m scripts.main --no-tutorials
```

### Custom Limits

```bash
# Specify how many templates to scrape from each source
python -m scripts.main --n8n-limit 50 --zapier-limit 30
```

## 🔌 API Endpoints

### Get All Templates

```bash
curl https://your-site.netlify.app/api/templates
```

### Filter by Source

```bash
curl https://your-site.netlify.app/api/templates?source=n8n
curl https://your-site.netlify.app/api/templates?source=zapier
```

### Limit Results

```bash
curl https://your-site.netlify.app/api/templates?limit=10
```

## 🤖 Automation

The GitHub Actions workflow runs weekly (every Monday at 9:00 AM UTC) to:

1. Scrape latest templates from n8n and Zapier
2. Generate tutorials using OpenAI API (if configured)
3. Create SEO-optimized metadata
4. Commit and push changes automatically

### Manual Trigger

You can manually trigger the workflow from the GitHub Actions tab.

## 📝 Features Details

### Web Scraping

- **Rate Limiting**: Configurable rate limits to respect website policies
- **Error Handling**: Robust error handling with retry logic
- **Exponential Backoff**: Automatic retry with exponential backoff
- **Logging**: Comprehensive logging for debugging

### Tutorial Generation

- Uses OpenAI GPT models for high-quality content
- Structured output with consistent sections:
  - Overview
  - Prerequisites
  - Setup Steps
  - Configuration
  - Testing
  - Troubleshooting
  - Best Practices

### SEO Metadata

- Automatic keyword extraction
- Open Graph tags for social sharing
- Twitter Card metadata
- Schema-friendly YAML format

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for tutorial generation | Required for LLM |
| `RATE_LIMIT_CALLS` | Max requests per period | 10 |
| `RATE_LIMIT_PERIOD` | Rate limit period (seconds) | 60 |
| `USER_AGENT` | User agent for web requests | AutomationsCookbook/1.0 |
| `REQUEST_TIMEOUT` | Request timeout (seconds) | 30 |
| `RETRY_ATTEMPTS` | Number of retry attempts | 3 |
| `OUTPUT_DIR` | Directory for generated data | data |
| `LLM_MODEL` | OpenAI model to use | gpt-3.5-turbo |
| `LLM_MAX_TOKENS` | Max tokens for generation | 2000 |
| `LLM_TEMPERATURE` | Temperature for generation | 0.7 |

## 🚀 Deployment

### Netlify

The repository is configured for automatic deployment to Netlify:

1. Connect your repository to Netlify
2. Add `OPENAI_API_KEY` to Netlify environment variables
3. Deploy will happen automatically on push to main

### GitHub Actions Secrets

Add the following secrets to your GitHub repository:

- `OPENAI_API_KEY`: Your OpenAI API key

## 📄 License

MIT License - feel free to use this project for your own automation needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
