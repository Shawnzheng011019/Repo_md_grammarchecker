import os
from datetime import datetime
def generate_analysis_report(report_path, analysis_results):
    """Generate a Markdown report summarizing analysis results"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Grammar and Style Analysis Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n")
        f.write(f"Total files analyzed: {len(analysis_results)}\n\n")
        
        f.write("## Detailed Results\n")
        f.write("| File Path | Grammar Issues |\n")
        f.write("|-----------|----------------|\n")
        
        for file_path, issues in analysis_results.items():
            issue_count = len(issues) if isinstance(issues, list) else 0
            rel_path = os.path.relpath(file_path, os.getcwd())
            f.write(f"| {rel_path} | {issue_count} |\n")
        
        f.write("\n## Recommendations\n")
        f.write("1. Review files with the most grammar issues first\n")
        f.write("2. Address recurring issues across multiple files\n")
        f.write("3. Consider creating a style guide for technical documentation\n")    