# Web Word Extractor

A Python-based web crawler and word extraction tool designed for security research and wordlist generation. The tool crawls websites, extracts words, and generates common password mutations for security testing purposes.

## ⚠️ Security Disclaimer

This tool is intended for **educational and authorized security testing purposes only**.

- Only use on websites you own or have explicit written permission to test
- Unauthorized web crawling may be illegal and could violate:
  - Terms of Service
  - Computer Misuse laws
  - Website access policies
- The tool may cause heavy server load through rapid requests
- Always adhere to responsible security testing practices
- The authors accept no liability for misuse of this tool

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/moose-1199/Password-Generator.git

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

Basic usage:
```bash
python word_extractor.py -u https://example.com
```

### Command Line Options

- `-u, --url`: Target website URL (required)
- `-l, --length`: Minimum word length to include (default: 0)
- `-d, --depth`: Crawl depth for finding additional pages (default: 0)
- `-m, --limit`: Maximum number of top words to process (default: 10)
- `-o, --output`: Output file path (optional)

## 📝 Examples

1. Basic word extraction from homepage:
```bash
python word_extractor.py -u https://example.com
```

2. Deep crawl with word filtering:
```bash
python word_extractor.py -u https://example.com -d 2 -l 6 -m 50 -o wordlist.txt
```

3. Generate comprehensive wordlist:
```bash
python word_extractor.py -u https://example.com -d 3 -l 4 -m 100 -o comprehensive.txt
```

## 🛠️ Features

- Web crawling with configurable depth
- Word extraction and frequency analysis
- Common password mutation generation including:
  - Case variations
  - Number combinations
  - Common year appendixes
  - Special character mutations
- Domain-scoped crawling
- Progress reporting
- File export support

## 🚥 Rate Limiting

The tool does not implement rate limiting by default. For ethical usage:
- Add delays between requests
- Respect robots.txt
- Monitor server response times
- Implement appropriate timeouts
- Stop if encountering errors or blocks


## ⚖️ Legal

This tool should only be used in strict accordance with applicable laws and regulations. Users are responsible for ensuring they have proper authorization before using this tool against any web application or system.
