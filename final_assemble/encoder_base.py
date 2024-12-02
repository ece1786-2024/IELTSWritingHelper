if __name__ == "__main__":
    print("The system is loading ... Will take less than 10 sec ...")

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW, get_scheduler
import torch
from torch.nn.functional import softmax
import datasets
from datasets import load_dataset, Dataset
import random
from torch.utils.data import DataLoader, Subset
import torch.nn.functional as F
import matplotlib.pyplot as plt
from tqdm import tqdm
from torchmetrics import F1Score
import pandas as pd
import numpy as np

from comment import category as comment_categories
from comment import generate_comment

from tips import generate_tips

import gradio as gr
import time

import math


pd.options.mode.copy_on_write = True


reverse_mapping_3 = {
    3.5: 0, 4.0: 0,
    4.5: 1, 5.0: 1,
    5.5: 2, 6.0: 2,
    6.5: 3, 7.0: 3,
    7.5: 4, 8.0: 4,
    8.5: 5, 9.0: 5
}

class_mapping = {
    0: "3.5 - 4.0",
    1: "4.5 - 5.0",
    2: "5.5 - 6.0",
    3: "6.5 - 7.0",
    4: "7.5 - 8.0",
    5: "8.5 - 9.0",
}

# if args.LLM:
#     print("Running in LLM mode")
# else:
#     print("Running in default mode")

def process_input(prompt, essay):
    """
    Processes the given prompt and essay, checking word counts and returning feedback.
    """
    comments = []
    for each in comment_categories:
        yield f"Generating comments for {each} ..."
        comment = generate_comment(prompt, essay, each)
        # comment = "debug"
        comments.append(comment)
        time.sleep(1)  # avoid OpenAI firewall

    yield "Generating comments complete ... Calculating suggested band score"
    
    classifier_output = []

    for i, model in enumerate(models):
        classifier_input = f"Prompt: {prompt}\n\nEssay:{essay}\n\nComment: {comments[i]}"
        inputs = tokenizer(classifier_input, return_tensors="pt").to(device)
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = logits.argmax(dim=1).item()
        classifier_output.append(predicted_class)

    avg = sum(classifier_output) / len(classifier_output)
    final_band_score = math.ceil(avg)
    final_band_score = class_mapping[final_band_score]

    output = ""
    for i in range(len(classifier_categories)):
        output += (f"- {comment_categories[i]}:\n"
                   f"- {comments[i]}\n"
                   f"- Suggested Band Score ({comment_categories[i]}): {class_mapping[classifier_output[i]]}\n\n")
    
    output += f"Suggested overall Band Score: {final_band_score}\n\n"

    yield "Band Score Calculation Complete. Generating Tips for Improvement."
    all_comments = '\n'.join(comments)
    output += f"Tips for improvement: \n{generate_tips(prompt, essay, all_comments)}"

    yield output




if __name__ == "__main__":
    classifier_categories = ['task_achievement', 
                            'grammatical',
                            'coherence',
                            'lexical'
                            ]
    models = []

    for category in classifier_categories:
        model = AutoModelForSequenceClassification.from_pretrained("mrm8488/deberta-v3-ft-financial-news-sentiment-analysis",num_labels=6, ignore_mismatched_sizes=True)
        # Load the saved state_dict into the model
        with open(f'models/{category}.pt', "rb") as f:
            model.load_state_dict(torch.load(f))

        # Move model to the device (GPU if available)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model.to(device)
        models.append(model)

    tokenizer = AutoTokenizer.from_pretrained("mrm8488/deberta-v3-ft-financial-news-sentiment-analysis")

    # Create the Gradio interface
    with gr.Blocks() as demo:
        gr.Markdown("""
        ### Prompt and Essay Input
        Please provide a **prompt** (about 100 words) and an **essay** (250-300 words).
        """)

        with gr.Row():
            prompt_input = gr.Textbox(
                label="Prompt (about 100 words)",
                placeholder="Enter your prompt here (approximately 100 words)...",
                lines=7  # Approximate height for 100 words
            )
            essay_input = gr.Textbox(
                label="Essay (250-300 words)",
                placeholder="Enter your essay here (approximately 250-300 words)...",
                lines=15  # Approximate height for 300 words
            )

        submit_button = gr.Button("Submit")
        output = gr.Textbox(label="Output", lines=25, interactive=False)

        submit_button.click(process_input, inputs=[prompt_input, essay_input], outputs=output)

    # Launch the Gradio app
    demo.launch()


