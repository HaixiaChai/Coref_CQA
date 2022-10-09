from experiment.qa.data.models import Token, TextItem
import collections

def flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x if len(x) > 0 for a in flatten(i)]
    else:
        return [x]
 
def update_tokens_with_coref(orginal_text_tokens, referent_pairs, idx):
    
    updated_tokens = [Token(item) for item in orginal_text_tokens]

    try:
        for pa in referent_pairs:
            
            if len(orginal_text_tokens) <= int(pa['index'][0]):
                pass
            
            anaphor_text_tokens = orginal_text_tokens[int(pa['index'][0]):int(pa['index'][-1])+1]
            anaphor_text = ' '.join(anaphor_text_tokens)
            
            if anaphor_text == pa['anaphor']:
                updated_tokens[int(pa['index'][0])] = [Token(item) for item in pa['antecedent']]
                for index in pa['index'][1:]:
                    updated_tokens[int(index)] = []
            else:
                raise Exception('Update tokens with coref error:'+str(idx))
    except:
        raise Exception('Update tokens with coref error: out of index!' + str(idx))

    return flatten(updated_tokens)

def build_text_item_with_coref(idx, coref_clusters, original_answer, resolver, domain, mmax_res):
    
    idx =  idx.split('ans_')[1] if 'ans_' in idx else idx
    referent_pairs = coref_clusters[idx] if idx in coref_clusters else None

    if not referent_pairs:
        return original_answer
    
    if resolver == 'human':
        original_answer_text_tokens = mmax_res['ans_'+idx]['tokens']
    else:
        original_answer_text_tokens = mmax_res['ans_'+idx]['sentences']
    answer_updated_tokens = update_tokens_with_coref(original_answer_text_tokens,
                                                     referent_pairs, idx)
    
    text = ' '.join([t.text for t in answer_updated_tokens])
    referent_answer = TextItem(text, answer_updated_tokens)
    referent_answer.metadata['id'] = original_answer.metadata['id']
    
    return referent_answer

def remove_missing_ground_truth(datapoints):
    result_datapoints = []
    count = False
    for p in datapoints:
        pooled_answers_indexs = [l.metadata['id'] for l in p.pooled_answers]
        gt_indexs = [gt.metadata['id'] for gt in p.ground_truth]

        for index in gt_indexs:
            if index in pooled_answers_indexs:
                count = True
                
        if (count):
            result_datapoints.append(p)
            count = False

    return result_datapoints