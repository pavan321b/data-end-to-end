"""
Load ML FinBert Model
"""
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


def analyse(text):
    """
    # Let's load the model and the tokenizer
    """

    finbert = BertForSequenceClassification.from_pretrained(
        "yiyanghkust/finbert-tone", num_labels=3
    )
    tokenizer = BertTokenizer.from_pretrained(
        "yiyanghkust/finbert-tone",
        truncation=True,
        max_length=512,
        padding="max_length",
    )
    tokenizer.model_max_length = 512
    tokens = tokenizer(text, truncation=True, max_length=510)

    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

    output = nlp(tokenizer.decode(tokens["input_ids"]))

    print("Model Out: ", output)
    labels = ["Positive", "Neutral", "Negative"]
    final_output = {output[0]["label"]: output[0]["score"]}
    for label in labels:
        if label not in output[0].values():
            final_output[label] = (1 - list(output[0].values())[1]) / 2
    print("ML: ", final_output)
    return final_output
