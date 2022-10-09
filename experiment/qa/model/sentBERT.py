# -*- coding: utf-8 -*-

from sentence_transformers import SentenceTransformer, util

embedder = SentenceTransformer('all-mpnet-base-v2')


def predict(questions, answers):
    
    cos_scores = []
    for i in range(len(questions)):
        query_embedding = embedder.encode(questions[i], convert_to_tensor=True)
        answer_embedding = embedder.encode(answers[i], convert_to_tensor=True)
    
        cos_scores.append(util.pytorch_cos_sim(query_embedding, answer_embedding)[0].item())
    
    return cos_scores