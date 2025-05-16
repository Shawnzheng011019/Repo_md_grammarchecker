import os
import time
from datetime import datetime
from update_repo import update_repo
from extract_text import extract_text_from_md
from analyze_text import analyze_with_llm, parse_analysis_results
from create_issue import create_github_issue
from report_generator import generate_analysis_report
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
REPO_URL = os.getenv('REPO_URL', "")
LOCAL_PATH = os.getenv('LOCAL_PATH', "")
TARGET_DIR = os.path.join(LOCAL_PATH, os.getenv('TARGET_DIR', ""))
OUTPUT_DIR = os.getenv('OUTPUT_DIR', "extracted_text")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GITHUB_APP_KEY_PATH = os.getenv('GITHUB_APP_KEY_PATH')
REPO_NAME = os.getenv('REPO_NAME', "")
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
GITHUB_APP_INSTALLATION_ID = os.getenv('GITHUB_APP_INSTALLATION_ID')

# Files to skip (filenames relative to TARGET_DIR)
SKIP_FILES = {"release_notes.md"}

def read_github_token_from_file(key_path):
    """Read GitHub App token from PEM file"""
    if not key_path:
        raise ValueError("GITHUB_APP_KEY_PATH environment variable not set")
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"GitHub App key file not found: {key_path}")
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Failed to read GitHub App key: {e}")

def main():
    """Main function"""
    if not OPENAI_API_KEY:
        raise ValueError("Required environment variable missing: OPENAI_API_KEY")
    
    try:
        GITHUB_APP_TOKEN = read_github_token_from_file(GITHUB_APP_KEY_PATH)
    except Exception as e:
        print(f"Error reading GitHub token: {e}")
        return
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    update_repo(REPO_URL, LOCAL_PATH)
    
    md_files = []
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                rel_file = os.path.relpath(file_path, TARGET_DIR)
                if os.path.basename(rel_file) in SKIP_FILES:
                    print(f"Skipping file: {rel_file}")
                    continue
                md_files.append(file_path)
    
    print(f"Found {len(md_files)} Markdown files to process")
    
    # Store analysis results for report
    analysis_results = {}
    
    for i, md_path in enumerate(md_files):
        print(f"\nProcessing file {i+1}/{len(md_files)}: {md_path}")
        
        rel_path = os.path.relpath(md_path, TARGET_DIR)
        txt_dir = os.path.join(OUTPUT_DIR, os.path.dirname(rel_path))
        os.makedirs(txt_dir, exist_ok=True)
        txt_path = os.path.join(txt_dir, os.path.basename(md_path).replace('.md', '.txt'))
        
        extract_text_from_md(md_path, txt_path)
        print(f"Text extracted to: {txt_path}")
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if len(text) > 15000:
                print("Text too long, truncating to first 15,000 characters")
                text = text[:15000]
            
            print("Analyzing text with LLM...")
            analysis_result = analyze_with_llm(text, md_path, OPENAI_API_KEY)
            
            # Parse analysis results
            issues = parse_analysis_results(analysis_result)
            analysis_results[md_path] = issues
            
            if not issues:
                print("No grammar issues found")
                continue
                
            print(f"Found {len(issues)} grammar issues")
            
            # Create GitHub issue if there are issues
            print("Creating GitHub issue...")
            create_github_issue(md_path, analysis_result, GITHUB_APP_TOKEN, REPO_NAME, LOCAL_PATH)
            
        except Exception as e:
            print(f"Error processing file: {e}")
            analysis_results[md_path] = [f"Processing error: {str(e)}"]
        finally:
            if os.path.exists(txt_path):
                os.remove(txt_path)
                print(f"Temporary file deleted: {txt_path}")
        
        time.sleep(20)  # Wait to avoid API rate limits

    # Generate final report
    report_path = os.path.join(OUTPUT_DIR, "analysis_report.md")
    generate_analysis_report(report_path, analysis_results)
    print(f"Analysis report generated: {report_path}")

    # Cleanup empty output directory
    if os.path.exists(OUTPUT_DIR) and not os.listdir(OUTPUT_DIR):
        os.rmdir(OUTPUT_DIR)
        print(f"Empty output directory deleted: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()    
