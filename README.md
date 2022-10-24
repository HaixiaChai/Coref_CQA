# Coref_CQA

# Evaluating Coreference Resolvers on Community-based Question Answering: From Rule-based to State of the Art

This repository contains the data and code to reproduce the results of our paper: https://aclanthology.org/2022.crac-1.7.pdf


Please use the following citation:

```
@inproceedings{chai-etal-2022-evaluating,
    title = "Evaluating Coreference Resolvers on Community-based Question Answering: From Rule-based to State of the Art",
    author = "Chai, Haixia  and
      Moosavi, Nafise Sadat  and
      Gurevych, Iryna  and
      Strube, Michael",
    booktitle = "Proceedings of the Fifth Workshop on Computational Models of Reference, Anaphora and Coreference",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.crac-1.7",
    pages = "61--73",
    abstract = "Coreference resolution is a key step in natural language understanding. Developments in coreference resolution are mainly focused on improving the performance on standard datasets annotated for coreference resolution. However, coreference resolution is an intermediate step for text understanding and it is not clear how these improvements translate into downstream task performance. In this paper, we perform a thorough investigation on the impact of coreference resolvers in multiple settings of community-based question answering task, i.e., answer selection with long answers. Our settings cover multiple text domains and encompass several answer selection methods. We first inspect extrinsic evaluation of coreference resolvers on answer selection by using coreference relations to decontextualize individual sentences of candidate answers, and then annotate a subset of answers with coreference information for intrinsic evaluation. The results of our extrinsic evaluation show that while there is a significant difference between the performance of the rule-based system vs. state-of-the-art neural model on coreference resolution datasets, we do not observe a considerable difference on their impact on downstream models. Our intrinsic evaluation shows that (i) resolving coreference relations on less-formal text genres is more difficult even for trained annotators, and (ii) the values of linguistic-agnostic coreference evaluation metrics do not correlate with the impact on downstream data.",
}
```

> **Abstract:** Coreference resolution is a key step in natural language understanding. Developments in coreference resolution are mainly focused on improving the performance on standard datasets annotated for coreference resolution. However, coreference resolution is an intermediate step for text understanding and it is not clear how these improvements translate into downstream task performance. In this paper, we perform a thorough investigation on the impact of coreference resolvers in multiple settings of community-based question answering task, i.e., answer selection with long answers. Our settings cover multiple text domains and encompass several answer selection methods. We first inspect extrinsic evaluation of coreference resolvers on answer selection by using coreference relations to decontextualize individual sentences of candidate answers, and then annotate a subset of answers with coreference information for intrinsic evaluation. The results of our extrinsic evaluation show that while there is a significant difference between the performance of the rule-based system vs. state-of-the-art neural model on coreference resolution datasets, we do not observe a considerable difference on their impact on downstream models. Our intrinsic evaluation shows that (i) resolving coreference relations on less-formal text genres is more difficult even for trained annotators, and (ii) the values of linguistic-agnostic coreference evaluation metrics do not correlate with the impact on downstream data.


## Usage

Download our [trained model](https://drive.google.com/file/d/1J1YFa2_vdaGyfpyQAZ_kOxNoOr2W-Vww/view?usp=sharing) and [data](https://drive.google.com/file/d/1wcood_TQUmADtsg7AJkz9f1Mmi6WnZcI/view?usp=sharing).

To run an experiment on original data:
```
python run_experiment.py configs/se_travel_cnn.yaml
```

To run an experiment on data incorporating coreference relations:
```
python run_experiment.py configs/se_travel_cnn.yaml test_travel_rule_CR
```

## Dependencies and Requirements

We used Python 3.6.9 for our experiments. 

Run (not all of the packages are strictly required):
```
pip install -r requirements.txt
pip install -U sentence-transformers

```
