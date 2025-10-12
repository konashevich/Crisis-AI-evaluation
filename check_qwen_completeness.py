import json
import os
from pathlib import Path

base_dir = Path('test_results/2025-10-10_11')

print("=" * 70)
print("CHECKING ALL QWEN MODELS FOR COMPLETENESS")
print("=" * 70)

# Get all qwen result files
qwen_files = sorted([f for f in base_dir.glob('*.json') if 'qwen' in f.name.lower() and '_runinfo' not in f.name])

incomplete_models = []
complete_models = []

for result_file in qwen_files:
    # Extract model name
    import re
    model_name = result_file.name.replace('.json', '')
    model_name = re.sub(r'_2025-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', '', model_name)
    
    # Load the results
    try:
        results = json.load(open(result_file, encoding='utf-8'))
        
        total_q = 0
        answered_q = 0
        error_q = 0
        
        for category, subcats in results.items():
            for subcat_name, qa_list in subcats.items():
                total_q += len(qa_list)
                for qa in qa_list:
                    answer = qa.get('answer', '')
                    if answer and answer.strip():
                        answered_q += 1
                        if answer.startswith('ERROR') or answer.startswith('API Call Error'):
                            error_q += 1
        
        # Check if complete (should have 32 questions)
        expected_questions = 32
        
        status = "✅"
        status_text = f"COMPLETE ({answered_q}/{expected_questions})"
        
        if total_q < expected_questions:
            status = "⚠️"
            status_text = f"INCOMPLETE - Only {total_q} questions"
            incomplete_models.append({
                'name': model_name,
                'total': total_q,
                'expected': expected_questions,
                'answered': answered_q,
                'errors': error_q
            })
        elif answered_q < total_q:
            status = "⚠️"
            status_text = f"INCOMPLETE - {answered_q}/{total_q} answered"
            incomplete_models.append({
                'name': model_name,
                'total': total_q,
                'expected': expected_questions,
                'answered': answered_q,
                'errors': error_q
            })
        elif error_q > 0:
            status = "❌"
            status_text = f"HAS ERRORS ({error_q} errors)"
            incomplete_models.append({
                'name': model_name,
                'total': total_q,
                'expected': expected_questions,
                'answered': answered_q,
                'errors': error_q
            })
        else:
            complete_models.append(model_name)
        
        print(f"\n{status} {model_name}")
        print(f"   Status: {status_text}")
        print(f"   Questions: {total_q} total, {answered_q} answered, {error_q} errors")
        
    except Exception as e:
        print(f"\n❌ {model_name}")
        print(f"   ERROR reading file: {e}")
        incomplete_models.append({
            'name': model_name,
            'total': 0,
            'expected': 32,
            'answered': 0,
            'errors': 0,
            'file_error': str(e)
        })

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total Qwen models found: {len(qwen_files)}")
print(f"✅ Complete: {len(complete_models)}")
print(f"⚠️  Incomplete/Errors: {len(incomplete_models)}")

if incomplete_models:
    print("\n" + "=" * 70)
    print("MODELS THAT NEED TO BE RERUN:")
    print("=" * 70)
    for model in incomplete_models:
        print(f"  • {model['name']}")
        if 'file_error' in model:
            print(f"    Reason: File read error - {model['file_error']}")
        elif model['total'] < model['expected']:
            print(f"    Reason: Only {model['total']}/{model['expected']} questions in file")
        elif model['answered'] < model['total']:
            print(f"    Reason: Only {model['answered']}/{model['total']} questions answered")
        elif model['errors'] > 0:
            print(f"    Reason: {model['errors']} timeout/API errors")
else:
    print("\n🎉 All Qwen models completed successfully!")
