from sentence_transformers import SentenceTransformer
import numpy as np
import json

class SemanticMatcher:
    def __init__(self, alias_json_path):
        # Load MiniLM embedding model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # Load alias dictionary
        with open(alias_json_path, 'r', encoding='utf-8') as f:
            self.alias_dict = json.load(f)
        self.command_templates = list(self.alias_dict.keys())
        # Pre-compute embeddings of all alias phrases
        self.alias_embeddings = self.model.encode(self.command_templates)

    def match(self, user_text):
        # Embed user input text
        user_emb = self.model.encode([user_text])[0]
        # Compute cosine similarity against all alias embeddings
        similarities = np.dot(self.alias_embeddings, user_emb) / (
            np.linalg.norm(self.alias_embeddings, axis=1) * np.linalg.norm(user_emb) + 1e-10)
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])
        best_template = self.command_templates[best_idx]
        mapped_command = self.alias_dict[best_template]
        return best_template, mapped_command, best_score
