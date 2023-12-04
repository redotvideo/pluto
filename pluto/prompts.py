SAMPLE_GENERATION_PROMPT ="""I want to train a large language model and you should help me generate training data for it. Here is the system prompt of the model that tells it what it should be able to do:

<system_prompt>
{{{{system_prompt}}}}
</system_prompt>

You should now generate three training samples for the model. A training sample consists of a json object with the field "messages" being a list of messages, alternating between user messages, which represent the user of the language model, and assistant messages, which represent the language model itself. The first message should be a user message, the last one an assistant message. Depending on the use case of the system prompt, you might need one user and assistant messages each, or more. The format of a sample looks like this:

{
    "messages": [
        {
            "role": "user",
            "content": "<user_content>"
        },
        {
            "role": "assistant",
            "content": "<assistant_content>"
        }
        # more messages if neccessary
    ]
}
{{{{instructions}}}}
{{{{examples}}}}
{{{{subtopics}}}}

Now write a training sample and return it as a json, as seen above."""



TREE_GENERATION_PROMPT = """I want to train a large language model and I am using another, bigger large language model to generate training data for this. However, if we always ask the bigger model to generate training data with the same prompt, it will end up generating very repetitive training samples. Therefore, we will slightly modify our prompt for each sampling procedure according to some aspects. For instance, when asking the model to generate news articles, we could modify the prompt to let the model tell news articles about particular topics, such as business or politics. To further generate training data, we will do this recursively, and generate submodifications to the prompt. For instance, within the domain of business, we could adapt the prompt to generate news about the stock market or business scandals, and within politics, we could ask the model to generate articles for subtopics like elections or climate policy. We do this recursively, and therefore, we get a tree-like structure of topics.
Your job is the following: I will give you a path of nodes down the topic tree - you should then come up with a list of new subtopics for this given node and return it as a python list. Here are a few examples of what your outputs should look like, related to the news example I just gave you:

Example 1:
node path: "News Topics" -> "Sports" -> "Football"
desired number of subtopics: 5
subtopics: ["college football", "football stadiums", "health consequences football", "Seattle Seahawks", "football sponsorships"]


Example 2:
node path: "News Topics" -> "Entertainment" -> "Movies" -> "Star Portraits"
desired number of subtopics: 8
subtopics: ["Tom Hanks", "Meryl Streep", "Leonardo DiCaprio", "Jennifer Lawrence", "Denzel Washington", "Charlize Theron", "Robert Downey Jr.", "Emma Stone"]


Here are three new examples, this time for generating smalltalk topics for a friendly chat assistant:

Example 1:
node path: "Small Talk Topics"
desired number of subtopics: 7
subtopics: ["weather", "weekend plans", "hobbies", "family", "books", "food", "music"]

Example 2:
node path: "Small Talk Topics" -> "Family"
desired number of subtopics: 5
subtopics: ["parents", "grandparents", "siblings", "family traditions", "family vacations"]

Example 3:
node path: "Small Talk Topics" -> "Hobbies" -> "Cooking"
desired number of subtopics: 6
subtopics: ["recipes", "asian food", "favourite dishes", "cookbooks", "kitchen gadgets", "vegan cooking"]


Here is a description / the system prompt for the model we want to train:

<system_prompt>
{{{{system_prompt}}}}
</system_prompt>


Here is your topic input. When generating subtopics, remain somewhat vague. Things can only be tangentially related and they don't have to be interpreted in a single way. Importantly, make sure that the subtopics fit the system prompt, if one was supplied:
node path: {{{{subtopics_list}}}}
desired number of subtopics: {{{{num_subtopics}}}}

Now return the subtopics as a python list, and return it in just one line, not multiple ones. Don't return anything else."""