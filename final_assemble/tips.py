from comment import category as comment_categories
from comment import generate_comment, criteria

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


all_criteria = ""

for i in range(len(criteria)):
    all_criteria += f"{comment_categories[i]}\n{criteria[i]}\n"


def generate_tips(prompt, essay, feedbacks):
    input1 = f"Prompt: {prompt}\nEssay: {essay}"
    Prompt = (
        "Provide professional suggestions for improving IELTS Task 2 Writing."
        "Use the following 'Prompt' as the test question and the 'Essay' as the test taker's written response."
        "and include at least one example modification in your response to support your points. Ensure the response are detailed and concise (around 300 words)"
        "and tailored to the essay's quality, providing significantly distinct responses for different levels."
        "Your response should focus only on improvement suggestions without explicitly breaking down by 'Task Achievement', 'Coherence and Cohesion', 'Lexical Resource', or 'Grammatical Range and Accuracy'."
        "Avoid mentioning any band scores. Responses should be provided in a continuous paragraph format, not in bullet points or numbered lists."
        f"Consider the comments for the essay:\n{feedbacks}\n"
        f"Refer to this marking criteria for all aspects:\n{all_criteria}\n"
        f"{input1}"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": Prompt}
        ]
    )
    
    content = completion.choices[0].message.content
    return content


if __name__ == "__main__":
    prompt = "Today people are surrounded by advertising. This affects what people think is important and has a negative impact on people's lives. To what extent do you agree or disagree?"
    essay = """ In this digital world, people are encircled with various types of advertisements. It is omnipresent for all, TV adverts, Social Media Marketing, billboards, Personal advertisements and many more diverse ways. while this phenomenon is escalating to extremely new level, people are in influence of it. In my view, it has more positive effects than harmful.

Because of advertisements, people are aware of current products in market. At some extent, it educates the people and provides the knowledge. For an instance, In India serious disease like  polio is no more and the major success goes to awareness campaign help by famous personality with the use of digital marketing and TV advertisements. Moreover, to bind user with interest usually companies display various new idea and it add major value in entertainment world.

However, the critical impacts are also not avoidable.Firstly, it exposes kids and young generation towards the violence and  inappropriate content sometime. Secondly, Advertisements with various discounts and offers, make people lure to do impulsive shopping. Increasing obesity is also one of consequence of advertisement of junk food. In addition, few times people get influenced by various advertisings and tend to work more to achieve never ending desire of buying stuff, this approach add up to the stress and frustration. What more, kids might suffer from harmful psychological effects when their parents are unable to afford various products shown in advertisements.

To put this in a nutshell, I can say that advertisement is beneficial phenomenon with a number of insignificant drawbacks. In my view, negative advertising effects can be lowered with help of government using stringent approach and awareness campaigns.
"""

    feedbacks = """ 'The essay addresses the task by discussing both the positive and negative impacts of advertising, thereby responding to the prompt\'s request for a degree of agreement or disagreement. However, the position is somewhat unclear, as the author asserts it has "more positive effects" without thoroughly justifying this stance throughout the essay. For example, while the author provides a strong case for the benefits of advertising, such as awareness campaigns for health issues, the negatives mentioned, like violence exposure and consumerism, could be developed further to enhance balance and depth. The conclusion is present but feels rushed and repetitive. Overall, the essay demonstrates an understanding of the topic but lacks sufficient development and clarity in presenting a cohesive argument.\nThe essay exhibits some coherence, but it struggles with logical organization and clarity in paragraphing. Each paragraph presents a central idea; however, transitions between points can be confusing. For instance, in the first paragraph, the jump from discussing advertising\'s saturation to its positive impact lacks a clear link, reducing overall cohesion. While it uses some linking devices, they are sometimes improperly applied, as seen in the abrupt shift to negative impacts without a smooth transition. Additionally, referencing is present but not always clear, which can leave readers puzzled about connections. Enhanced structure and more precise linking could significantly improve the essay\'s clarity and flow.\nThe essay demonstrates an adequate range of vocabulary, effectively addressing the task with a mix of common and some less common words. Phrases like "encircled with various types of advertisements" and "bind user with interest" indicate an attempt to use descriptive language, which enhances clarity. However, there are notable spelling and word formation errors, such as "influence of it" (should be "influenced by it") and "experience of advertisement of junk food" (should be "advertisements for junk food"), which detract from overall comprehension. Additionally, inconsistent use of articles and plural forms creates minor confusion. Overall, while the vocabulary used serves the communication purpose, greater precision and fewer errors would enhance clarity significantly.\nThe essay demonstrates a reasonable variety of sentence structures, including both simple and complex sentences. However, it features several grammatical errors that hinder clarity. For instance, in the phrase "In my view, it has more positive effects than harmful," the use of "harmful" should be corrected to "harmful effects" for better grammatical accuracy. Additionally, punctuation errors, such as the lack of a comma after "However," affect readability. Although the essay presents clear communication of ideas, the frequent mistakes suggest a need for improved grammatical control. Overall, while the essay engages with the prompt effectively, greater accuracy and range in grammatical use would enhance its quality.\n'"""

    print(generate_tips(prompt, essay, feedbacks))