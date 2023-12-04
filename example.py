from pluto import EngineArguments, DataEngine, Dataset, TopicTree, TopicTreeArguments

system_prompt = "You are a helpful AI coding assistant. You help software developers with their coding questions and write code for them. You do not just give high level coding advice, but instead, you tend to respond to coding questions with specific code examples."

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
