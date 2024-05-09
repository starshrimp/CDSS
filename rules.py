from durable.lang import ruleset, when_all, post

# Define the rules
with ruleset('medical'):
    # Rule for disease type and condition
    @when_all((m.disease.is_in(['wounds', 'skin', 'respiratory_tract', 'gastrointestinal_tract',
                                'urinary_tract', 'genital_tract', 'nervous_system',
                                'cardiovascular_system', 'specific_infections', 'perinoperative_prophylaxis',
                                'foal', 'eyes'])),
              (m.condition.is_in(['contaminated_wounds_no_synovial', 'contaminated_wounds_synovial'])))
    def advice(c):
        # Action to take when conditions are met
        c.s.label = 'advice'
        c.s.advice = f"Provide treatment for {c.m.disease} with condition {c.m.condition}"

def get_advice(disease, condition):
    return post('medical', {'disease': disease, 'condition': condition})
