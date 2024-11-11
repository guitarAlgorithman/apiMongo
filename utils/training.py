from transformers import TrainingArguments, Trainer, AutoTokenizer, AutoModelForQuestionAnswering
from datasets import Dataset

def retrain_model(training_data):
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")
    model = AutoModelForQuestionAnswering.from_pretrained("mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")

    dataset = Dataset.from_dict({
        "question": [item["question"] for item in training_data],
        "context": [item["context"] for item in training_data],
        "answers": [item["answers"] for item in training_data]
    })

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )

    trainer.train()
