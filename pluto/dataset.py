from typing import List, Dict
import json
from .utils import remove_linebreaks_and_spaces

class Dataset:
    def __init__(self):
        self.samples = []

    @classmethod
    def from_jsonl(cls, file_path):
        instance = cls()
        with open(file_path, 'r') as f:
            for line in f:
                sample = json.loads(line)
                assert cls.validate_sample(sample)
                instance.samples.append(sample)

        return instance

    @classmethod
    def from_list(cls, sample_list: List[Dict]):
        instance = cls()
        for sample in sample_list:
            assert self.validate_sample(sample)
            instance.samples.append(sample)

        return instance

    @classmethod
    def validate_sample(self, sample: Dict):
        if 'messages' not in sample:
            return False
        for message in sample['messages']:
            if 'role' not in message or 'content' not in message:
                return False
            if message['role'] not in ['user', 'assistant', 'system']:
                return False
        return True

    def save(self, save_path):
        with open(save_path, "w") as f:
            for sample in self.samples:
                f.write(remove_linebreaks_and_spaces(json.dumps(sample))+"\n")
    
    def add_samples(self, samples: List[Dict]):
        for sample in samples:
            if self.validate_sample(sample):
                self.samples.append(sample)
            else:
                print("Invalid sample, not added:", sample)



    