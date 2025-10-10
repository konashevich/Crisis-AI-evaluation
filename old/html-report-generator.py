import json
import os
import glob
import re
import argparse
from datetime import datetime

# --- Configuration ---
# Prefer timestamped files like 'gemini_evaluation_report_YYYY-MM-DD_HH-MM-SS.json';
# fallback to the legacy 'gemini_evaluation_report.json' if no timestamped file exists.
LEGACY_INPUT_FILE = 'gemini_evaluation_report.json'
TIMESTAMPED_PATTERN = 'gemini_evaluation_report_*.json'
OUTPUT_FILE = 'evaluation_report.html'

def _parse_score(score):
    """Try to convert a score to float; return None if not possible."""
    try:
        if score is None:
            return None
        return float(score)
    except (ValueError, TypeError):
        return None

def get_score_color(score):
    """Returns a Tailwind CSS color class based on the score."""
    if score is None:
        return "bg-gray-200 text-gray-700"
    try:
        s = int(score)
        if s >= 8:
            return "bg-green-100 text-green-800"
        elif s >= 5:
            return "bg-yellow-100 text-yellow-800"
        else:
            return "bg-red-100 text-red-800"
    except (ValueError, TypeError):
        return "bg-gray-200 text-gray-700"

def generate_summary_cards(report_data):
    """Calculates average scores and generates HTML for summary cards."""
    model_scores = {}
    
    # Aggregate scores for each model (skip Mistral-7B variants)
    for category in report_data.values():
        for subcategory in category.values():
            for entry in subcategory:
                if 'gemini_evaluation' in entry and 'evaluations' in entry['gemini_evaluation']:
                    evaluations = entry['gemini_evaluation']['evaluations']
                    # Handle cases where Gemini might return a non-list
                    if not isinstance(evaluations, list):
                        continue
                    for eval_item in evaluations:
                        model_name = eval_item.get('model_name')
                        if not model_name:
                            continue
                        # Exclude Mistral-7B family (case-insensitive)
                        if 'mistral-7b' in model_name.lower():
                            continue
                        score_num = _parse_score(eval_item.get('score'))
                        if score_num is not None:
                            if model_name not in model_scores:
                                model_scores[model_name] = []
                            model_scores[model_name].append(score_num)

    if not model_scores:
        return "<p>No model scores found to generate a summary.</p>"

    # Calculate averages and create cards sorted by average score (desc)
    ranking = []  # list of tuples: (name, avg_score, count)
    for name, scores in model_scores.items():
        avg_score = (sum(scores) / len(scores)) if scores else 0.0
        ranking.append((name, avg_score, len(scores)))

    # Sort: best to worst by avg_score desc; tie-breaker by name asc
    ranking.sort(key=lambda x: (-x[1], x[0].lower()))

    cards_html = ''
    for idx, (name, avg_score, count) in enumerate(ranking, start=1):
        card_color_class = get_score_color(avg_score).replace('100', '200')  # Slightly darker bg
        score_color = get_score_color(avg_score).split(' ')[1] if ' ' in get_score_color(avg_score) else 'text-gray-800'
        cards_html += f"""
        <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-700">{name}</h3>
                <span class="text-xs text-gray-500">#{idx}</span>
            </div>
            <p class="text-3xl font-bold mt-2 {score_color}">
                {avg_score:.2f}
            </p>
            <p class="text-sm text-gray-500 mt-1">Average Score ({count} questions)</p>
        </div>
        """
    return cards_html

def generate_report_body(report_data, model_names):
    """Generates the main HTML table body for the report."""
    body_html = ""
    question_index = 0

    for cat_name, subcategories in report_data.items():
        body_html += f'<h2 class="text-2xl font-bold text-gray-800 mt-12 mb-4">{cat_name}</h2>'
        for sub_name, entries in subcategories.items():
            body_html += f'<h3 class="text-xl font-semibold text-gray-700 mt-6 mb-4">{sub_name}</h3>'
            
            # Start table
            body_html += '<div class="overflow-x-auto bg-white rounded-lg shadow border border-gray-200"><table class="min-w-full divide-y divide-gray-200">'
            
            # Table Header
            header_cols = "".join(f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{name}</th>' for name in model_names)
            body_html += f"""
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Question</th>
                    {header_cols}
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
            """

            # Table Rows
            for entry in entries:
                question = entry.get('question', 'N/A')
                eval_data = entry.get('gemini_evaluation', {})
                evaluations = eval_data.get('evaluations', [])
                
                # Handle cases where Gemini might return a non-list
                if not isinstance(evaluations, list): evaluations = []

                gemini_answer = eval_data.get('gemini_ideal_answer', 'Not provided.')
                
                # Create a map of model_name -> evaluation for easy lookup
                eval_map = {e.get('model_name'): e for e in evaluations}

                row_html = f'<tr><td class="px-6 py-4 align-top w-1/3"><div class="text-sm font-medium text-gray-900">{question}</div></td>'
                
                details_row_html = ''
                for i, model_name in enumerate(model_names):
                    eval_item = eval_map.get(model_name)
                    details_id = f"details-q{question_index}-m{i}"
                    
                    if eval_item:
                        score = eval_item.get('score')
                        score_num = _parse_score(score)
                        llm_answer = eval_item.get('llm_answer', 'Not provided.')
                        justification = eval_item.get('justification', 'Not provided.')
                        color_class = get_score_color(score_num)

                        row_html += f"""
                        <td class="px-6 py-4 whitespace-nowrap align-top text-center cursor-pointer hover:bg-gray-50" onclick="toggleDetails('{details_id}')">
                            <span class="px-3 py-1 inline-flex text-sm leading-5 font-bold rounded-full {color_class}">
                                {score if score is not None else 'N/A'}
                            </span>
                        </td>
                        """
                        details_row_html += f"""
                        <div id="{details_id}" class="details-pane hidden p-6 bg-gray-50 border-t border-gray-200">
                            <h4 class="font-bold text-md text-gray-800 mb-4">Evaluation Details for <span class="text-blue-600">{model_name}</span></h4>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h5 class="font-semibold text-gray-600 mb-2">Gemini's Ideal Answer (Score 10)</h5>
                                    <div class="prose prose-sm max-w-none p-4 bg-green-50 border border-green-200 rounded-md">{gemini_answer.replace('\\n', '<br>')}</div>
                                </div>
                                <div>
                                    <h5 class="font-semibold text-gray-600 mb-2">{model_name}'s Answer (Score {score})</h5>
                                    <div class="prose prose-sm max-w-none p-4 bg-white border border-gray-200 rounded-md">{llm_answer.replace('\\n', '<br>')}</div>
                                </div>
                            </div>
                            <div class="mt-4">
                                <h5 class="font-semibold text-gray-600 mb-2">Justification for Score</h5>
                                <div class="prose prose-sm max-w-none p-4 bg-yellow-50 border border-yellow-200 rounded-md">{justification.replace('\\n', '<br>')}</div>
                            </div>
                        </div>
                        """
                    else:
                        row_html += '<td class="px-6 py-4 whitespace-nowrap align-top text-center text-sm text-gray-400">Missing</td>'

                row_html += '</tr>'
                details_container_html = f'<tr class="details-row hidden"><td colspan="{len(model_names) + 1}">{details_row_html}</td></tr>'
                body_html += row_html + details_container_html
                question_index += 1

            body_html += "</tbody></table></div>" # Close table
    return body_html

def _find_latest_report_file():
    """Find the latest timestamped evaluation file, else return legacy if present, else None."""
    files = glob.glob(TIMESTAMPED_PATTERN)
    if files:
        # Sort by timestamp parsed from filename (falls back to mtime)
        def parse_ts(name):
            m = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', name)
            if m:
                try:
                    from datetime import datetime
                    return datetime.strptime(m.group(1), '%Y-%m-%d_%H-%M-%S')
                except Exception:
                    return None
            return None
        files.sort(key=lambda p: (parse_ts(os.path.basename(p)) or 0, os.path.getmtime(p)))
        return files[-1]
    if os.path.exists(LEGACY_INPUT_FILE):
        return LEGACY_INPUT_FILE
    return None

def _extract_date_from_filename(path):
    """Extract a human-friendly date string from a timestamped filename."""
    base = os.path.basename(path)
    m = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', base)
    if m:
        date_part, time_part = m.groups()
        return f"{date_part} {time_part.replace('-', ':')}"
    # Fallback: file modified time
    try:
        ts = datetime.fromtimestamp(os.path.getmtime(path))
        return ts.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return None

def main():
    """Main function to generate the HTML report."""
    parser = argparse.ArgumentParser(description='Generate CrisisAI HTML report from evaluation JSON')
    parser.add_argument('--input-file', '-i', dest='input_file', type=str, help='Path to a specific evaluation JSON to use')
    args = parser.parse_args()

    input_file = args.input_file if args.input_file and os.path.exists(args.input_file) else _find_latest_report_file()
    if not input_file:
        print(f"Error: No evaluation report found. Expected '{TIMESTAMPED_PATTERN}' or '{LEGACY_INPUT_FILE}'. Please run the evaluation script first.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    # Discover all unique model names from the report
    model_names = sorted(list(set(
        eval_item['model_name']
        for category in report_data.values()
        for subcategory in category.values()
        for entry in subcategory
        if 'gemini_evaluation' in entry and 'evaluations' in entry['gemini_evaluation'] and isinstance(entry['gemini_evaluation'].get('evaluations'), list)
        for eval_item in entry['gemini_evaluation']['evaluations']
        if 'model_name' in eval_item and 'mistral-7b' not in eval_item['model_name'].lower()
    )))

    if not model_names:
        print("Warning: No model evaluations found in the JSON report. The report will be empty.")

    summary_cards_html = generate_summary_cards(report_data)
    report_body_html = generate_report_body(report_data, model_names)

    # Derive a date label for the header from the filename, if possible
    evaluated_at = _extract_date_from_filename(input_file) or 'Unknown date'
    print(f"Generating HTML from: {input_file} (Evaluated at: {evaluated_at})")

    # Use a full-width container so the report stretches across the screen
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrisisAI LLM Evaluation Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .details-pane {{ display: none; }}
        .details-row.active {{ display: table-row; }}
        .details-pane.active {{ display: block; }}
        .prose {{ max-width: 100%; }}
    </style>
</head>
<body class="bg-gray-50 font-sans">
    <div class="w-full p-4 sm:p-6 lg:p-8">
        <header class="mb-8">
            <h1 class="text-4xl font-extrabold text-gray-900">CrisisAI LLM Evaluation Report</h1>
            <p class="mt-2 text-lg text-gray-600">Comparative analysis of smaller LLMs for crisis response advice.</p>
            <p class="mt-1 text-sm text-gray-500">Evaluated at: {evaluated_at}</p>
        </header>

        <section id="summary">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Performance Summary</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {summary_cards_html}
            </div>
        </section>

        <section id="detailed-report">
            {report_body_html}
        </section>
    </div>

    <script>
        let currentlyOpenDetailsId = null;

        function toggleDetails(detailsId) {{
            const detailsPane = document.getElementById(detailsId);
            if (!detailsPane) return;

            const parentRow = detailsPane.closest('.details-row');

            // If we are clicking the same element that is already open, close it.
            if (currentlyOpenDetailsId === detailsId) {{
                detailsPane.classList.remove('active');
                parentRow.classList.remove('active');
                currentlyOpenDetailsId = null;
            }} else {{
                // First, close any currently open details pane
                if (currentlyOpenDetailsId) {{
                    const oldPane = document.getElementById(currentlyOpenDetailsId);
                    if (oldPane) {{
                         oldPane.classList.remove('active');
                         oldPane.closest('.details-row').classList.remove('active');
                    }}
                }}

                // Now, open the new one
                detailsPane.classList.add('active');
                parentRow.classList.add('active');
                currentlyOpenDetailsId = detailsId;
            }}
        }}
    </script>
</body>
</html>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Successfully generated HTML report: '{OUTPUT_FILE}'")

if __name__ == '__main__':
    main()
