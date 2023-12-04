<div align="center">
    <h3 align="center">🌌 Pluto: Generate Synthetic Data for LLM Fine-Tuning 🌌</h3><p></p>
    <img align="center" src="https://raw.githubusercontent.com/havenhq/pluto/main/images/pluto.png" height="300" alt="Oak" />
</div>

<div align="center">


<br>
<br>

[🌐 Website](https://haven.run/)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
[💬 Discord](https://discord.gg/JDjbfp6q2G)
<br>

</div>


## Welcome 💜

Pluto makes it easy to generate fine-tuning datasets for LLMs. Here's what you can do with it:

- Overcome repetitiveness and make your data highly diverse using topic trees
- Run multiple sampling requests in parallel to speed up data generation
- Use any model provider to generate data

<br>

## Quickstart 🚀

To get started, let's use GPT-4 to generate a dataset of coding questions about numpy. First install the pluto library:

```
pip install pluto-data
```

Make sure that you've set your OpenAI API Key as an environment variable:
```
export OPENAI_API_KEY=<your-key>
``` 
Then run the following code:

```python
from pluto import EngineArguments, DataEngine, Dataset, TopicTree, TopicTreeArguments

system_prompt = "You are a helpful AI coding assistant. You do not just give high level coding advice, but instead, you respond to coding questions with specific code examples."

tree = TopicTree(
    args=TopicTreeArguments(
        root_prompt="Functionalities of numpy",
        model_system_prompt=system_prompt,
        tree_degree=10,
        tree_depth=2
    )
)

tree.build_tree(model_name="gpt-3.5-turbo-1106")
tree.save("numpy_topictree.jsonl")

engine = DataEngine(
    args=EngineArguments(
        instructions="Please specifically provide training examples with questions about numpy. A training sample should consist of just one question and a response, and not a chat with multiple messages.",
        system_prompt=system_prompt,
    )
)

dataset = engine.create_data(
    model_name="gpt-4-1106-preview",
    num_steps=20,
    batch_size=5,
    topic_tree=tree
)

dataset.save("output_with_topictree.jsonl")
```

### What happened in this example? 🤔

In the example above, we did the following things:

**Generate Topic Tree:**
We first used GPT-3.5 to generate a "topic tree" with the root "Functionalities of numpy". A topic tree is simply a tree in which each child of a node needs to be a subtopic of its parent node and allows us to generate a list of aspects that should be covered in our training dataset. This is what paths from root to leaves within a topic tree look like (you can also find a full file [here]()):

```
Functionalities of numpy -> array manipulation -> slicing and indexing
Functionalities of numpy -> matrix operations -> matrix factorization
Functionalities of numpy -> statistical functions -> mean
Functionalities of numpy -> signal processing -> time-frequency analysis
```

**Generate Data from Topic Tree:**
After generating our topic tree, we feed it into the `create_data` function to ensure that our dataset touches upon a broad range of subjects and is not repetitive. Concretely, in this function, we iterate over all root-to-leaf paths in our topic tree and tell GPT-4 Turbo, which we use to generate our training data, to take the corresponding (sub)topic into account in its generated training sample. The parameter `batch_size=5` controls how many OpenAI requests we send simultaneously.
