import re
import itertools
import json
import numpy as np
from bert_serving.client import BertClient

TFX_FILE = 'tfx.json'
USER_COMMAND = 'insert'
bert_client = BertClient()


def normalized_correlation_coefficient(sequence, template):
    pad_size_0 = int(template.shape[0] / 2)
    padded_sequence = np.pad(sequence, (pad_size_0, pad_size_0), mode='constant')
    correlated_sequence = np.zeros_like(sequence).astype(float)
    for r in range(correlated_sequence.shape[0]):

        overlapping_padded_seq = padded_sequence[r:r + template.shape[0]]
        correlated_sequence[r] = np.corrcoef(overlapping_padded_seq, template)[0, 1]
    return correlated_sequence


def extract_terms(terms, string):
    complex_term_pattern = r"\{([A-Za-z0-9_]+)\}"
    complex_terms = list(map(lambda x: '{'+x+'}', re.findall(complex_term_pattern, string)))
    if not len(complex_terms):
        return string

    result = []
    for word in string.split():
        if not (word in complex_terms):
            result.append(word)
        else:
            m_result = [0]
            for pattern in terms[word]:
                m_result.append(extract_terms(terms, pattern))
            result.append(m_result)
    return result[0] if len(result) is 1 else result


def cartesian(templates):
    if type(templates) is list and templates[0] is 0:
        result = []
        for item in templates[1:]:
            result = result + cartesian(item)
        return result

    if type(templates) is str:
        return [templates]

    result = list(itertools.product(*list(map(cartesian, templates))))

    return result


def flatten(templates, result):
    if type(templates) is str:
        result.append(templates)
    elif type(templates) is tuple:
        for item in templates:
            flatten(item, result)

    return result


def extract_templates(terms, arg):
    extracted_terms = extract_terms(terms, arg)
    product = cartesian(extracted_terms)
    result = []
    for item in product:
        r = []
        result.append(flatten(item, r))
    return result


tfx = json.loads(open(TFX_FILE).read())
user_query = "i wanna sort second column ascending"
command_args = tfx["commands"][USER_COMMAND]["arguments"]
command_args_templates = {}
command_args_sequence = {}
for arg in command_args:
    templates = extract_templates(tfx["terms"], arg)
    command_args_sequence[arg] = list(map(lambda template: bert_client.encode(template).flatten(), templates))
    command_args_templates[arg] = templates

print(command_args_templates)

# user_query_word_by_word = user_query.split()
#
# user_query_sequence = bert_client.encode(user_query_word_by_word).flatten()
# res = []
# for template_seq in command_args_sequence['{selection}']:
#     corcoeff = normalized_correlation_coefficient(user_query_sequence, template_seq)
#     res.append(corcoeff)
#
# res = list(map(lambda x: np.max(x), res))
#
# print('sege')
