
def normalized_clusters(clusters):
    clusters = clusters.split(']')[0]
    pairs = clusters.split(';;')
    
    result = []
    for pair in pairs:
        token = pair.split('::::')[0]
        try:
            replacement =  pair.split('::::')[1].split('$$')[0]
            index = pair.split('::::')[1].split('$$')[1].split(' ')
        except:
            continue
        
        if len(index) ==0:
            continue

        if len(token.split()) < len(index):
            token = token.strip() + ' :'
            replacement = replacement.split(':')[1]
            
        result.append({
            'anaphor': token.strip(),
            'antecedent': replacement.strip().split(' '),
            'index': index
        })

    return result
 
def normalize(cluster_payload, delimiter):
    per_questions = cluster_payload.split(delimiter)[1:]
    final = dict()
    for per_question in per_questions:
        question_id = per_question.split('[')[0].strip() if delimiter == 'ans_' else cluster_payload.split('-')[0]
        clusters = per_question.split('[')[1]
        clusters = normalized_clusters(clusters)
        final.update({question_id:  clusters})

    return final
