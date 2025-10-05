from sentence_transformers import SentenceTransformer, util
import json
import os

class SemanticMatcher:
    def __init__(self, aliases_path):
        # Load alias dict and templates
        with open(aliases_path, 'r', encoding='utf-8') as f:
            self.alias_dict = json.load(f)
        self.templates = list(self.alias_dict.keys())

        # Load MiniLM model from HuggingFace
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Precompute template embeddings for faster matching
        self.template_embeddings = self.model.encode(self.templates, convert_to_tensor=True)

    def match(self, user_text):
        # Embed user input
        user_embedding = self.model.encode(user_text, convert_to_tensor=True)

        # Compute cosine similarity scores
        scores = util.cos_sim(user_embedding, self.template_embeddings)

        # Get best match index and score
        best_idx = scores.argmax().item()
        best_score = scores[0, best_idx].item()

        best_template = self.templates[best_idx]
        mapped_command = self.alias_dict[best_template]

        return best_template, mapped_command, best_score


# Example usage:
if __name__ == "__main__":
    matcher = SemanticMatcher("aliases.json")

    user_phrase = "show me all the files"
    template, command, score = matcher.match(user_phrase)
    print(f"User phrase: {user_phrase}")
    print(f"Best template: {template}")
    print(f"Mapped command: {command}")
    print(f"Similarity score: {score:.3f}")
