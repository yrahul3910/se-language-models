import pickle
import traceback
import os
import torch
from datasets import load_dataset
from transformers import BertTokenizerFast
from transformers import AutoModelForMaskedLM
from transformers import TrainingArguments
from transformers import Trainer
from transformers import DataCollatorForLanguageModeling


base_path = '../se-language-models/data/'
model_name = 'bert-large-uncased'
max_length = 512
checkpoints_dir = 'checkpoints'
dataset_used = 'full'

print('Training on GPU:', torch.cuda.is_available())

# Does the checkpoints dir exist?
if not os.path.exists(checkpoints_dir):
    os.mkdir(checkpoints_dir)

# Initiaize a tokenizer. We are training on English text, so the pretrained one is fine.
tokenizer = BertTokenizerFast.from_pretrained(model_name, do_lower_case=True)

# Get the pretrained model for masked language modeling.
model = AutoModelForMaskedLM.from_pretrained(model_name)

# Pad to max length and truncate.


def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=max_length)


# Load the text dataset.
dataset = load_dataset('text',
                       data_files={
                           'train': f'{base_path}train.txt',
                           'test': f'{base_path}test.txt',
                           'validation': f'{base_path}valid.txt'
                       }
                       )

# If we've saved the tokenized dataset before, load it. Otherwise, tokenize the data.
if os.path.exists(f'tokenized-{dataset_used}.pkl'):
    print('Loading tokenized dataset.')
    with open(f'tokenized-{dataset_used}.pkl', 'rb') as f:
        tokenized_dataset = pickle.load(f)
else:
    print('Tokenizing data. This may take a while...')
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Save the tokenized dataset.
try:
    if not os.path.exists(f'tokenized-{dataset_used}.pkl'):
        with open(f'tokenized-{dataset_used}.pkl', 'wb') as f:
            pickle.dump(tokenized_dataset, f)
except:
    print('Failed to pickle tokenized dataset.')
    try:
        traceback.print_exc()
    except:
        print('Failed to print error.')

train_dataset = tokenized_dataset['train']
eval_dataset = tokenized_dataset['test']


# Get a data collator for MLM.
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# Define training args.
training_args = TrainingArguments(
    output_dir=checkpoints_dir,
    num_train_epochs=1,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    save_steps=10000,
    prediction_loss_only=True
)

print('Training the model...')
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)
trainer.train()
trainer.save_model(f'./final-model')
