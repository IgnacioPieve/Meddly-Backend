import os.path
import pickle

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from whoosh import index
from whoosh.analysis import SimpleAnalyzer
from whoosh.fields import ID, TEXT, Schema


def get_umls_codes(code):
    """
    if code is 'UMLS:C0425251_bedridden^UMLS:C0741453_bedridden', this function will return ['C0425251', 'C0741453']
    if code is 'UMLS:C0425251_bedridden', this function will return ['C0425251']
    """
    codes = code.split('^')
    codes = [c.split('_')[0].replace('UMLS:', '') for c in codes]
    return codes


def generate_merged_dataframe():
    # Read and processing File 1
    all_diseases_file1 = set()
    all_symptoms_file1 = set()
    file_1_diseases = {}
    rows = pd.read_csv('base_files/symptom_x_diseases_dataset1.csv').to_numpy()
    actual_diseases = None
    for (disease, count, symptom) in rows:
        if symptom is np.nan:
            continue
        disease = get_umls_codes(disease) if type(disease) == str else None
        symptom = get_umls_codes(symptom)
        if disease is not None:
            actual_diseases = disease
            all_diseases_file1.update(disease)
            all_symptoms_file1.update(symptom)
            for actual_disease in actual_diseases:
                file_1_diseases[actual_disease] = {'count': count, 'symptoms': list(symptom)}
        else:
            for actual_disease in actual_diseases:
                file_1_diseases[actual_disease]['symptoms'] += symptom
                all_symptoms_file1.update(symptom)

    # Read and processing File 2
    all_diseases_file2 = set()
    all_symptoms_file2 = set()
    df = pd.read_csv('base_files/symptom_x_diseases_dataset2.csv')
    for column in df.columns:
        df.rename(columns={column: get_umls_codes(column)[0]}, inplace=True)
        all_symptoms_file2.add(get_umls_codes(column)[0])
    df.rename(columns={'prognosis': 'disease'}, inplace=True)
    for index in df.index:
        df.at[index, 'disease'] = get_umls_codes(df.at[index, 'disease'])[0]
        all_diseases_file2.add(df.at[index, 'disease'])

    # Merging
    all_symptoms = all_symptoms_file1.union(all_symptoms_file2)
    all_diseases = all_diseases_file1.union(all_diseases_file2)
    only_on_file_2_symptoms = all_symptoms_file2 - all_symptoms_file1

    # Generate new dataframe, with symptoms as columns and diseases as rows
    columns = {k: [] for k in ['disease'] + list(all_symptoms)}
    for disease, data in file_1_diseases.items():
        symptoms = data['symptoms']
        count = data['count']
        for _ in range(int(count / 42)):
            columns['disease'].append(disease)
            for symptom in all_symptoms:
                columns[symptom].append(1 if symptom in symptoms else 0)
    dataframe = pd.DataFrame().from_dict(columns)
    for symptom in only_on_file_2_symptoms:
        dataframe[symptom] = 0

    row_base = {k: 0 for k in all_symptoms}
    columns = {}
    for index in df.index:
        row = df.loc[index].to_dict()
        row = {**row_base, **row}
        for k, v in row.items():
            if k not in columns:
                columns[k] = []
            columns[k].append(v)
    new_dataframe = pd.DataFrame().from_dict(columns)
    dataframe = pd.concat([dataframe, new_dataframe], ignore_index=True)

    return dataframe, all_diseases, all_symptoms


def export_data(dataframe, all_diseases, all_symptoms):
    dataframe.to_csv('output/dataframe.csv', index=False)

    # Save all diseases and symptoms with pickle
    with open('output/diseases.pickle', 'wb') as f:
        pickle.dump(all_diseases, f)
    with open('output/symptoms.pickle', 'wb') as f:
        pickle.dump(all_symptoms, f)


    all_symptoms_column = {'symptom': list(all_symptoms)}
    all_symptoms_df = pd.DataFrame().from_dict(all_symptoms_column)
    all_symptoms_df.to_csv('output/symptoms.csv', index=False)
    all_diseases_column = {'disease': list(all_diseases)}
    all_diseases_df = pd.DataFrame().from_dict(all_diseases_column)
    all_diseases_df.to_csv('output/diseases.csv', index=False)


def train_model(dataframe):
    x = dataframe.drop('disease', axis=1)
    y = dataframe['disease']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)

    tree = RandomForestClassifier()
    tree.fit(x_train, y_train)

    # acc = tree.score(x_test, y_test) # Acc on test set: 96.88%

    if not os.path.exists('output'):
        os.mkdir('output')
    dump(tree, 'output/model.trained')


def generate_indexes(all_symptoms, all_diseases):
    def simplify_string(text):
        text = str(text)
        text = "".join(e for e in text if (e.isalnum() or e == " ")).capitalize()
        text = ' '.join(text.split())
        return text.strip()

    def generate_index(index_dataframe, index_name, must_be_in=None):
        # First we are going to create the symptoms index
        schema = Schema(code=ID(stored=True), description=TEXT(analyzer=SimpleAnalyzer(), stored=True))
        if not os.path.exists(f'output/{index_name}'):
            os.mkdir(f'output/{index_name}')
        writer = index.create_in(f'output/{index_name}', schema).writer()

        codes = index_dataframe.to_dict('records')
        for code in codes:
            if not must_be_in or (must_be_in and code['code'] in must_be_in):
                writer.add_document(
                    code=simplify_string(code['code']),
                    description=simplify_string(code['es'])
                )
        writer.commit()

    dataframe = pd.read_excel('base_files/codes_translated.xlsx')
    generate_index(dataframe, 'symptoms_index', all_symptoms)
    generate_index(dataframe, 'diseases_index', all_diseases)
    dataframe = pd.read_excel('base_files/medicine_names.xlsx')
    generate_index(dataframe, 'medicines_index')


if __name__ == '__main__':
    df, diseases, symptoms = generate_merged_dataframe()
    train_model(df)
    generate_indexes(symptoms, diseases)
    # export_data(df, diseases, symptoms) # Uncomment this line to export data, optional
