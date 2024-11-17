### Datasets

#### Overview: 

This dataset is from online IELTS writing resource [ielts-blog.com](https://www.ielts-blog.com/ielts-writing-samples-essays-letters-reports/). More specifically, "Writing Samples" section, band score 5-9. ielts-blog.com had provide desire dataset sections that fit the purpose of our project, that is "score", "prompt", "essay", and "comment".

In Sprint 1, a complete dataset that include band 5-9 data points is collected. Time taken: 10h. 

Data points breakdown:

```python
score  count
9.0    53
8.5     2
8.0    34
7.5     1
7.0    17
6.5    12
6.0    10
5.5     3
5.0     5
```

#### The structure of the website:

1. For each band score sections, band score 5, 6, 7, 8, 9, has a lot of internal links, each points to one writing example. There is no distinction between integer band score and .5 band score, i.e. no band score 6.5 section.
2. For each band score sections, the comment may give a hint that the example essay is qualify for an extra of .5 score. E.g, one example under band 6 section suggest this is a 6.5 essay. This need manual recognition and adjustment.
3. Every example under same band score section is quite similar, but across different section is very different. This is probably due to each section is managed by different staff. Therefore, each section need to work on distinctly.

#### Stage of Work:

**Sprint 1:**

The process of retrieving data from ielts-blog.com involve a few stages:
1. Grep the URLs to individual examples and classfy them into different band scores (~ 1h)
2. Retrieve useful information from each URL by analyzing HTML structure of a number of examples. (~ 2h)
3. Problem 1 found: prompt, essay, and comment are all together, and there is no one-for-all ways to separate them like keyword matching or HTML section division
4. Band score 5, 6, 7 has fewer examples, each around 20-30, therefore manual separation is desirable. Recognition of extra .5 and adjustment was also done in this step. (~ 1h) 
5. Band 8 and 9 has more examples, therefore 
   1. Band 8: Using HTML pattern recognition is desirable (More complicated than expected. Only half is collected in Sprint 1. ~5h)
   2. Band 9: Since keyword consistent, using Regex to separate is desirable. (~ 1h)
6. Organize into a dataset file. (~ .5h)



**Sprint 2:**



#### Problem found:

1. Stage of Work part 3.

2. There are a few essay text wrapped with special `<div>`, which is ielts-blog.com special feature of suggesting probable typo, is not loaded upon starting of the webpage, but loaded shortly after by JavaScript. This wrapped text cannot be retrieved, leaving some sentences has a blanked in the middle. This problem is found more frequency among low score essays (band 5 and 6) but almost none in high score essays. This problem was found at very late stage of work, and the only solution seems to be completely move to another crawler package and abandon current work, the `beautifulsoup4` package that used so far is not able to solve this issue. 

#### Workload:
Zixi was assigned with this task and took him about 10-15 hours to do the work, due to multiple stages of work, the unorganized layout of the website, and various problems encountered during the crawling.