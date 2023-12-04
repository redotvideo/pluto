import litellm
import json
from dataclasses import dataclass
from typing import List, Dict
from .utils import extract_list
from .prompts import TREE_GENERATION_PROMPT

@dataclass
class TopicTreeArguments:
    root_prompt: str
    model_system_prompt: str = None
    tree_degree: int = 10
    tree_depth: int = 3

class TopicTree:
    def __init__(self, args: TopicTreeArguments):
        self.args = args
        self.tree_paths = []

    def build_tree(self, model_name: str = "gpt-3.5-turbo-1106"):
        self.tree_paths = self.build_subtree(model_name, [self.args.root_prompt], self.args.model_system_prompt, self.args.tree_degree, self.args.tree_depth)

    def build_subtree(self, model_name: str, node_path: List[str], system_prompt: str, tree_degree: int, subtree_depth: int):
        print(f"building subtree for path: {' -> '.join(node_path)}")
        if subtree_depth == 0:
            return [node_path]

        else:
            subnodes = self.get_subtopics(system_prompt=system_prompt, node_path=node_path, num_subtopics=tree_degree, model_name=model_name)
            updated_node_paths = [node_path + [sub] for sub in subnodes]
            result = []
            for path in updated_node_paths:
                result.extend(self.build_subtree(model_name, path, system_prompt, tree_degree, subtree_depth-1))
            return result


    def get_subtopics(self, system_prompt: str, node_path: List[str], num_subtopics: int, model_name: str):
        prompt = TREE_GENERATION_PROMPT

        prompt = prompt.replace("{{{{system_prompt}}}}", system_prompt)
        prompt = prompt.replace("{{{{subtopics_list}}}}", ' -> '.join(node_path))
        prompt = prompt.replace("{{{{num_subtopics}}}}", str(num_subtopics))

        response = litellm.completion(
            model=model_name,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return extract_list(response.choices[0].message.content)


    def save(self, save_path: str):
        with open(save_path, "w") as f:
            for path in self.tree_paths:
                f.write(json.dumps(dict(path=path))+"\n")


