import pandas as pd
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

category = ["Task Achievement", "Coherence and Cohesion", "Lexical Resource", "Grammatical Range and Accuracy"]
task = (
    "Band Score 5: - Does not completely address the task. - May follow the general topic but not the specific issue in the essay question. - There is a position but it is not always clear. - Any opinion given is unclear. - Possibly no conclusion. - Main ideas are not developed. - Some irrelevant detail."
    "Band Score 6: - Addresses the task – both the topic and issue are addressed. - Presents a relevant position. - Any opinion given is clear. - There is a conclusion – it may be repetitive or unclear. - Main ideas are relevant. - Ideas are not developed enough."
    "Band Score 7: - Addresses all parts of the task. - All issues in the question are answered. - Presents a clear position throughout the essay. - Any opinion given is supported in all paragraphs in the essay. - Main ideas are relevant. - Ideas are developed but there may be a lack of focus with supporting ideas or over generalisation."
    "Band Score 8: - Sufficiently addresses all parts of the task. - All issues in the essay question are answers well. - Presents a clear position throughout the essay. - Any opinion given is supported in all paragraphs in the essay. - Main ideas are relevant. - Ideas are developed, extended and well supported."
)

coherence = (
    "Band Score 5: - There is some organisation but may not use paragraphs. - Uses linking devices but with mistakes or inappropriate use. - May be repetitive due to lack of referencing.",
    "Band Score 6: - Organised information coherently. - Uses paragraphs but not always logically. - Uses linking devices effectively but there may be errors in linking between and within sentence. - Uses referencing but not always clearly.",
    "Band Score 7: - Logically organises information. - Good paragraphing. - Has one central topic for each paragraph. - Uses a range of linking devices. - May over or under use linking devices. - Good referencing.",
    "Band Score 8: - Information and ideas are organised logically. - Paragraphing is sufficient and appropriate. - Manages all aspects of linking and cohesion. - No problems with referencing."
)

lexical = (
    "Band Score 5: - Minimal range of vocabulary for the task. - Frequent errors with spelling or word formation. - Problems cause difficulty for the reader."
    "Band Score 6: - Adequate range of vocabulary for the task. - Uses some less common words but with errors. - Some errors in spelling and word formation. - Communication is clear."
    "Band Score 7: - A sufficient range of vocabulary for some precision. - Uses less common words. - Some awareness of style and collocations. - Occasional errors in spelling or word choice."
    "Band Score 8: - A wide range of vocabulary for precise meaning. - Skillfully uses less common words. - Rare errors in spelling or word formation."
)

grammar = (
    "Band Score 5: - Limited range of sentence structures. - Tries to use complex sentences with limited success. - Frequent errors in grammar. - Errors in punctuation. - Problems cause difficulty for the reader.",
    "Band Score 6: - Uses both simple and complex sentence structures. - Some errors in grammar. - Some errors in punctuation. - Communication is clear.",
    "Band Score 7: - Uses a variety of complex sentence structures. - Many error free sentences. - Good control over grammar. - Occasional errors in grammar or punctuation.",
    "Band Score 8: - Uses a wide range of complex structures. - Most sentences are free of errors."
)

criteria = [task, coherence, lexical, grammar]


def generate_comment(prompt, essay, category):
    input1 = f"Prompt: {prompt}\nEssay: {essay}"
    Prompt = (
        f"Provide comments on the '{category}' aspect of an IELTS Task 2 Writing response."
        "Use the following 'Prompt' as the test question and the 'Essay' as the test taker's written response."
        "Focus solely on how well the essay addresses the task, mentioning specific strengths or weaknesses,"
        "and include at least one example from the essay to support your points. Ensure your comments are concise (under 120 words)"
        "and tailored to the essay's quality, providing distinct feedback for varying levels of performance."
        "Only include the comments in the response."
        f"Consider the following criteria for '{category}': {criteria} "
        "Do not mention any band scores in your comments."
        f"{input1}"
    )

    completion = client.chat.completions.create(
        model=model,
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

    comment = generate_comment(prompt, essay, category[0])
    print(comment)