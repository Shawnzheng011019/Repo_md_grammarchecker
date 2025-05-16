# Markdown Docs Grammar Checker

A tool to automatically detect grammar errors and Chinglish expressions in Milvus documentation using OpenAI GPT-4 and create actionable GitHub issues for corrections.

## Features

- Automatically analyzes English documentation for grammar and style issues
- Uses OpenAI GPT-4 for high-quality language analysis
- Generates detailed reports in Markdown format
- Creates GitHub issues with specific correction suggestions
- Processes Markdown files while ignoring code blocks and HTML tags
- Skips specified files (e.g., release notes)
- Fully configurable through environment variables

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Shawnzheng011019/Repo_md_grammarchecker.git
   cd Repo_md_grammarchecker
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   - Copy `.env.example` to `.env`

   ```bash
   cp .env.example .env
   ```

   - Edit `.env` and add your API keys and configuration:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_APP_KEY_PATH=/path/to/your/private-key.pem
   REPO_URL=your_repo_url
   ```

## GitHub App Setup

To create and install a GitHub App:

1. **Create a new GitHub App**
   - Go to your GitHub account settings
   - Navigate to "Developer settings" > "GitHub Apps"
   - Click "New GitHub App"
   - Fill in the required fields:
     - **GitHub App name**: Choose a name (e.g., "Docs Grammar Checker")
     - **Homepage URL**: Your repository URL
     - **Webhook**: Disable (not required for this app)
   - Set Permissions:
     - Repository permissions:
       - Issues: Read & write
       - Contents: Read-only
   - **Where can this GitHub App be installed?**: Select "Only on this account"
   - Click "Create GitHub App"
2. **Generate a private key**
   - Scroll down to "Private keys"
   - Click "Generate a private key"
   - Save the downloaded `.pem` file securely
3. **Install the GitHub App**
   - On the GitHub App page, click "Install App"
   - Choose the repository where you want to create issues (e.g., `milvus-io/milvus-docs`)
   - Click "Install"
4. **Update your `.env` file**
   - Set `GITHUB_APP_KEY_PATH` to the path of the downloaded `.pem` file

## Usage

1. **Run the script**

   ```bash
   python main.py
   ```

2. **Review results**

   - The script will:
     - Clone or update the documentation repository
     - Analyze each Markdown file (except skipped ones)
     - Generate a detailed analysis report in `extracted_text/analysis_report.md`
     - Create GitHub issues for detected grammar issues

3. **Interpret the report**

   - The report includes:
     - Summary statistics
     - List of files with detected issues
     - Number of issues per file
     - Recommendations for improvement

## Configuration

All configuration is done through environment variables in the `.env` file:

| Variable              | Description                                     |
| --------------------- | ----------------------------------------------- |
| `OPENAI_API_KEY`      | Your OpenAI API key                             |
| `GITHUB_APP_KEY_PATH` | Path to your GitHub App private key (.pem file) |
| `REPO_URL`            | URL of the documentation repository to analyze  |
| `LOCAL_PATH`          | Local directory to clone the repository         |
| `TARGET_DIR`          | Directory within the repository to analyze      |
| `OUTPUT_DIR`          | Directory to store extracted text and reports   |
| `REPO_NAME`           | GitHub repository name                          |

## Customization

- **Skipping files**: Edit the `SKIP_FILES` set in `main.py` to exclude specific files
- **Adjusting analysis**: Modify the prompt in `analyze_text.py` to change how the LLM analyzes text
- **Report format**: Update `report_generator.py` to customize the output report
