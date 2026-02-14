import evaluate
from tqdm import tqdm
import fire
import json

def batch_evaluates(path):
    import json
    from tqdm import tqdm
    import evaluate

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bleu = evaluate.load("sacrebleu")
    rouge = evaluate.load("rouge")
    meteor = evaluate.load("meteor")

    preds = []
    multi_references = []

    for item in tqdm(data):
        preds.append(item['predicted_answer'])
        multi_references.append([item['answer1'], item['answer2']])

    bleu_score = bleu.compute(predictions=preds, references=multi_references)
    rouge_score = rouge.compute(predictions=preds, references=multi_references)
    meteor_score = meteor.compute(predictions=preds, references=multi_references)

    print(f"BLEU: {bleu_score}")
    print(f"ROUGE-Lsum: {rouge_score}")
    print(f"METEOR: {meteor_score}")

if __name__ == "__main__":
    fire.Fire(batch_evaluates)
