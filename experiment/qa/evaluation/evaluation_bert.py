# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

from experiment.qa.evaluation import BasicQAEvaluation
from experiment.qa.model import sentBERT

class QAEvaluationBERT(BasicQAEvaluation):
    def __init__(self, config, config_global, logger):
        super(QAEvaluationBERT, self).__init__(config, config_global, logger)

    def score(self, qa_pairs, model, data, sess):
        questions, answers = zip(*qa_pairs)
        test_questions = [q.text for q in questions]
        test_answers = [a.text for a in answers]

        scores = sentBERT.predict(test_questions,test_answers)

        return scores

component = QAEvaluationBERT