#!/usr/bin/env python3
"""
Fine-tune DistilBERT for AMKA transaction classification
"""

import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import os

# Load training data
print("Loading training data...")
with open('amka_training_data.json', 'r') as f:
    data = json.load(f)

# Create labels mapping
labels_to_ids = {
    "income": 0,
    "expense": 1,
    "query": 2,
    "report": 3,
    "help": 4
}

# Prepare data
texts = [item['text'] for item in data]
labels = [labels_to_ids[item['label']] for item in data]

print(f"Loaded {len(texts)} training examples")
print(f"Label distribution: {dict((k, labels.count(v)) for k, v in labels_to_ids.items())}")

# Create dataset
dataset = Dataset.from_dict({
    'text': texts,
    'labels': labels
})

# Split train/test (90/10)
split_dataset = dataset.train_test_split(test_size=0.1, seed=42)

print(f"Training set: {len(split_dataset['train'])} examples")
print(f"Test set: {len(split_dataset['test'])} examples")

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased"
print(f"Loading model: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(labels_to_ids)
)

# Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding="max_length",
        truncation=True,
        max_length=128
    )

print("Tokenizing dataset...")
tokenized_datasets = split_dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./amka_finetuned_model",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=5,
    eval_strategy="epoch",
)

# Trainer
print("Creating trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Train
print("Starting training...")
trainer.train()

# Save
print("Saving model...")
model.save_pretrained("./amka_finetuned_model")
tokenizer.save_pretrained("./amka_finetuned_model")

print("✅ Model fine-tuned and saved to ./amka_finetuned_model")

# Evaluate
print("Evaluating...")
results = trainer.evaluate()
print(f"Evaluation results: {results}")