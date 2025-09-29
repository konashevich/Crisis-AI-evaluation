import json
import os

# --- Configuration ---
INPUT_FILE = 'gemini_evaluation_report.json'
OUTPUT_FILE = 'evaluation_report.html'

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
    
    # Aggregate scores for each model
    for category in report_data.values():
        for subcategory in category.values():
            for entry in subcategory:
                if 'gemini_evaluation' in entry and 'evaluations' in entry['gemini_evaluation']:
                    evaluations = entry['gemini_evaluation']['evaluations']
                    # Handle cases where Gemini might return a non-list
                    if not isinstance(evaluations, list): continue
                    for eval_item in evaluations:
                        model_name = eval_item.get('model_name')
                        score = eval_item.get('score')
                        if model_name and score is not None:
                            if model_name not in model_scores:
                                model_scores[model_name] = []
                            model_scores[model_name].append(score)

    if not model_scores:
        return "<p>No model scores found to generate a summary.</p>"

    # Calculate averages and create cards
    cards_html = ''
    for name, scores in sorted(model_scores.items()):
        avg_score = sum(scores) / len(scores) if scores else 0
        card_color_class = get_score_color(avg_score).replace('100', '200') # Darker for card bg
        cards_html += f"""
        <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-700">{name}</h3>
            <p class="text-3xl font-bold mt-2 {get_score_color(avg_score).split(' ')[1]}">
                {avg_score:.2f}
            </p>
            <p class="text-sm text-gray-500 mt-1">Average Score ({len(scores)} questions)</p>
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
                        llm_answer = eval_item.get('llm_answer', 'Not provided.')
                        justification = eval_item.get('justification', 'Not provided.')
                        color_class = get_score_color(score)

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

def main():
    """Main function to generate the HTML report."""
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found. Please run the evaluation script first.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    # Discover all unique model names from the report
    model_names = sorted(list(set(
        eval_item['model_name']
        for category in report_data.values()
        for subcategory in category.values()
        for entry in subcategory
        if 'gemini_evaluation' in entry and 'evaluations' in entry['gemini_evaluation'] and isinstance(entry['gemini_evaluation'].get('evaluations'), list)
        for eval_item in entry['gemini_evaluation']['evaluations']
        if 'model_name' in eval_item
    )))

    if not model_names:
        print("Warning: No model evaluations found in the JSON report. The report will be empty.")

    summary_cards_html = generate_summary_cards(report_data)
    report_body_html = generate_report_body(report_data, model_names)

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
    <div class="container mx-auto p-4 sm:p-6 lg:p-8">
        <header class="mb-8">
            <h1 class="text-4xl font-extrabold text-gray-900">CrisisAI LLM Evaluation Report</h1>
            <p class="mt-2 text-lg text-gray-600">Comparative analysis of smaller LLMs for crisis response advice.</p>
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

        function toggleDetails(detailsId) {
            const detailsPane = document.getElementById(detailsId);
            if (!detailsPane) return;

            const parentRow = detailsPane.closest('.details-row');

            // If we are clicking the same element that is already open, close it.
            if (currentlyOpenDetailsId === detailsId) {
                detailsPane.classList.remove('active');
                parentRow.classList.remove('active');
                currentlyOpenDetailsId = null;
            } else {
                // First, close any currently open details pane
                if (currentlyOpenDetailsId) {
                    const oldPane = document.getElementById(currentlyOpenDetailsId);
                    if (oldPane) {
                         oldPane.classList.remove('active');
                         oldPane.closest('.details-row').classList.remove('active');
                    }
                }

                // Now, open the new one
                detailsPane.classList.add('active');
                parentRow.classList.add('active');
                currentlyOpenDetailsId = detailsId;
            }
        }
    </script>
</body>
</html>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Successfully generated HTML report: '{OUTPUT_FILE}'")

if __name__ == '__main__':
    main()
