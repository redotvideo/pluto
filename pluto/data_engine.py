import litellm
from typing import List, Dict
from tqdm import tqdm
import random
import re
import ast  # Abstract Syntax Trees module for safe evaluation of literals
import json
import math
from tqdm import tqdm
from dataclasses import dataclass
from .prompts import SAMPLE_GENERATION_PROMPT
from .topic_tree import TopicTree
from .dataset import Dataset
from .utils import remove_linebreaks_and_spaces, extract_list, replace_linebreaks


@dataclass
class EngineArguments:
    instructions: str
    system_prompt: str
    example_data: Dataset = None


class DataEngine:
    def __init__(self, args: EngineArguments):
        self.args = args
        self.dataset = Dataset()

    def create_data(self, model_name: str, num_steps: int = None, num_example_demonstrations: int = 3, batch_size: int = 10, topic_tree : TopicTree = None):
        data_creation_prompt = SAMPLE_GENERATION_PROMPT

        if self.args.example_data is None:
            num_example_demonstrations = None
        
        if num_steps is None:
            raise Exception("no number of steps was specified")

        if topic_tree is not None:
            tree_paths = topic_tree.tree_paths

        if topic_tree is not None and num_steps is not None:
            if num_steps*batch_size >  len(tree_paths):
                raise Exception("num_steps * batch_size cannot be bigger than number of tree paths")
            else:
                tree_paths = random.sample(tree_paths, num_steps*batch_size)

        if topic_tree is not None:
            num_steps = math.ceil(len(tree_paths)/batch_size)           

        print(f"Generating dataset in {num_steps} steps, with batch size {batch_size}.")
        for step in tqdm(range(num_steps)):
            prompts = []
            for i in range(batch_size):
                if topic_tree is not None:
                    try:
                        path = tree_paths[step*batch_size+i]
                    except Exception as e:
                        break
                else:
                    path = None

                sample_prompt = self.build_prompt(
                    data_creation_prompt=data_creation_prompt,
                    model_name=model_name,
                    num_example_demonstrations=num_example_demonstrations,
                    subtopics_list=path
                )
                prompts.append(sample_prompt)
            
            for j in range(3):
                try:
                    responses = litellm.batch_completion(
                        model=model_name,
                        messages=[[{"role": "user", "content": p}] for p in prompts],
                        temperature=1.0,
                        response_format={"type": "json_object"},
                        max_retries=10
                    )
                    
                    samples = [json.loads(r.choices[0].message.content) for r in responses]
                    for sample in samples:
                        new_message = {"role": "system", "content": self.args.system_prompt}
                        sample["messages"].insert(0, new_message)

                    self.dataset.add_samples(samples)
                    print("Example of a generated sample: ", samples[0])
                    break

                except Exception as e:
                    print(e)
                    print("error generating example, retrying...")
                    if j == 2:
                        raise Exception(f"{j} consecutive errors generating training examples. Something's probably wrong.")

        return self.dataset


    def build_prompt(self, data_creation_prompt: str, model_name: str, num_example_demonstrations: int, subtopics_list: List[List[str]] = None):

        prompt = data_creation_prompt.replace("{{{{system_prompt}}}}", self.build_system_prompt())
        prompt = prompt.replace("{{{{instructions}}}}", self.build_custom_instructions_text())
        prompt = prompt.replace("{{{{examples}}}}", self.build_examples_text(num_example_demonstrations))
        prompt = prompt.replace("{{{{subtopics}}}}", self.build_subtopics_text(subtopics_list))

        return prompt


    def save_dataset(self, save_path):
        self.dataset.save(save_path)


    def build_custom_instructions_text(self) -> str:    
        if self.args.instructions is None:
            return ""
        else:
            return f"\nHere are additional instructions:\n<instructions>\n{self.args.instructions}\n</instructions>\n"


    def build_system_prompt(self):
        return self.args.system_prompt


    def build_examples_text(self, num_example_demonstrations: int ):
        if self.args.example_data is None:
            return ""

        else:
            examples_text = ""
            if num_example_demonstrations != 0:
                examples_text += "Here are output examples:\n\n"
                examples = random.sample(self.args.example_data.samples, num_example_demonstrations)

                for i, ex in enumerate(examples):
                    examples_text += f"Example {i+1}: \n\n{ex}\n"

            return f"\nHere are output examples:\n<examples>\n{examples_text}\n</examples>\n"
        

    def build_subtopics_text(self, subtopic_list: List[str]):
        if subtopic_list is None:
            return ""
        else:
            return f"\nLastly, the topic of the training data should be related to the following subtopics: {' -> '.join(subtopic_list)}"



