from comment import category as comment_categories
from comment import generate_comment, criteria

from tips import generate_tips

import gradio as gr
import time

import math

from openai import OpenAI


model = "gpt-4o-mini"

try:
    with open("key.txt") as f:
        key = f.read().strip()
except (FileNotFoundError, IOError):
    key = ""

if key:
    client = OpenAI(api_key=key)
else:
    client = OpenAI()


def final_band_score(scores):
    try:
        real_score = [float(each[-3:]) for each in scores]
        avg = sum(real_score) / len(real_score)
        return round(avg * 2) / 2
    except Exception:
        return f"input does not follow format: 6.0 or 5.5 - 6.0: {scores}"


def process_input(prompt, essay):
    """
    Processes the given prompt and essay, checking word counts and returning feedback.
    """
    comments = []
    for each in comment_categories:
        yield f"Generating comments for {each} ..."
        comment = generate_comment(prompt, essay, each)
        # comment = 'debug'
        comments.append(comment)
        time.sleep(1)  # avoid OpenAI firewall

    yield "Generating comments complete ... Calculating suggested band score"
    
    scores = []
    for i, each in enumerate(comment_categories):
        yield f"Generating Band Score for {each} ..."
        Prompt = (
            f"Provide band score on the '{each}' aspect of an IELTS Task 2 Writing response. "
            f"For the input, 'Prompt' as the test question and the 'Essay' as the test taker's written response. A seperate agent had generated 'Comments' for '{each}' for the student response. "
            f"Consider the following criteria for '{each}': {criteria[i]} "
            "Only include the band score, or range of suggested band score in the response. If provide a range, the difference should not exceed 0.5 range."
            "Response in this format: 6.0, or 7.5 - 8.0 \n\n"
            "Here is the student response the comments for this category (that you should mark):\n"
            f"Prompt: {prompt}\n\nStudent Essay: {essay}\n\nComment: {comments[i]}"
        )
        # print(Prompt, end='\n\n\n\n')
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a IELTS Writing Task 2 grader"},
                {"role": "user", "content": Prompt}
            ]
        )

        content = completion.choices[0].message.content
        scores.append(content)

    output = ""
    for i, each in enumerate(comment_categories):
        output += (f"- {comment_categories[i]}:\n"
                   f"- {comments[i]}\n"
                   f"- Suggested Band Score ({each}): {scores[i]}\n\n")
    
    output += f"Suggested overall Band Score: {final_band_score(scores)}\n\n"

    yield "Band Score Calculation Complete. Generating Tips for Improvement."
    all_comments = '\n'.join(comments)
    output += f"Tips for improvement: \n{generate_tips(prompt, essay, all_comments)}"

    yield output



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