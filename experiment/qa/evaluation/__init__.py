from __future__ import division

import os
from math import ceil

import numpy as np
from unidecode import unidecode

import experiment

class BasicQAEvaluation(experiment.Evaluation):
    def __init__(self, config, config_global, logger):
        super(BasicQAEvaluation, self).__init__(config, config_global, logger)
        self.primary_measure = self.config.get('primary_measure', 'accuracy')
        self.batchsize = self.config.get('batchsize', 512)

    def start(self, model, data, sess, valid_only=False):
        
        evaluation_data = [(data.archive.name, data.archive.valid)]
        
        if not valid_only:
            evaluation_data += [(data.archive.name, t) for t in data.archive.test]
            # transfer datasets
            evaluation_data += [(trans.name, t) for trans in data.transfer_archives for t in trans.test]
        
        output_path = self.config.get('output', None)
        if output_path and not os.path.exists(output_path):
            os.mkdir(output_path)

        results = dict()
        for dataset_name, split in evaluation_data:
            self.logger.info("Evaluating {} / {}".format(dataset_name, split.split_name))
            ranks = []
            average_precisions = []
            
            ##################################
            self.logger.info("pool size: {}".format(str(len(split.qa[0].pooled_answers))))
            ###################################
            
            # perform the scoring, used to calculate the measure values
            qa_pairs = [(qa.question, a) for qa in split.qa for a in qa.pooled_answers]
            n_batches = int(ceil(len(qa_pairs) / float(self.batchsize)))
            scores = []
            bar = self.create_progress_bar()
            for i in bar(range(n_batches)):
                batch_qa_pairs = qa_pairs[i * self.batchsize:(i + 1) * self.batchsize]
                result = self.score(batch_qa_pairs, model, data, sess)
                scores += result if type(result)==list else result.tolist()

            scores_used = 0
            
            if output_path:
                question_path = os.path.join(output_path, split.split_name+'.txt')
                
                with open(question_path, 'w') as f:
                    for pool in split.qa:
                        scores_pool = scores[scores_used:scores_used + len(pool.pooled_answers)]
                        scores_used += len(pool.pooled_answers)
        
                        sorted_answers = sorted(zip(scores_pool, pool.pooled_answers), key=lambda x: -x[0])
        
                        rank = 0
                        precisions = []
                        for i, (score, answer) in enumerate(sorted_answers, start=1):
                            for gt in pool.ground_truth:
                                if answer.metadata['id'] == gt.metadata['id']:
                                    if rank == 0:
                                        rank = i
                                    precisions.append((len(precisions) + 1) / float(i))
        
                        ranks.append(rank)
                        average_precisions.append(np.mean(precisions))
        
                        if not valid_only:
                            self.logger.debug('Rank: {}'.format(rank))
                        
                        q_id = pool.question.metadata['id']
                        gt_rank = rank
                        
                        cols = [str(q_id), str(gt_rank)]
                        f.write(' '.join(cols)+'\n')
                        
            correct_answers = len([a for a in ranks if a == 1])
            measures = {
                'accuracy': correct_answers / float(len(ranks)),
                'mrr': np.mean([1 / float(r) for r in ranks]),
                'map': np.mean(average_precisions)
            }

            results[split.split_name] = measures[self.primary_measure]

            self.logger.info("Evaluating {}".format(split.split_name))
            self.logger.info('Correct answers: {}/{}'.format(correct_answers, len(split.qa)))
            self.logger.info('Accuracy: {}'.format(measures['accuracy']))
            self.logger.info('MRR: {}'.format(measures['mrr']))
            self.logger.info('MAP: {}'.format(measures['map']))

        return results

    def score(self, question_answer_pairs, model, data, sess):
        raise NotImplementedError()


component = BasicQAEvaluation
