import pandas as pd
import numpy as np
import sys
import os

def hamming_distance(s1, s2):
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))

def read_columns(file, cols):
    df = pd.read_csv(file)
    return df[cols]

def fill_placeholders(row, T_row, columns):
    # `*`の場所をTの対応する値で置き換え
    row_filled = row.copy()
    for col in columns:
        if row[col] == '*':
            return T_row[col]

def main(a_prefix, b_prefix, c_prefix):
    a_file = f'{a_prefix}.csv'
    b_file = f'{b_prefix}.csv'
    a = pd.read_csv(a_file)
    b = pd.read_csv(b_file)

    # a.csvのname列を削除
    if 'Name' in a.columns:
        a = a.drop(columns=['Name'])

    # 列の設定
    c_columns = [
        ['Gender', 'Age', '3877', '3889'],
        ['Occupation', 'ZIP-code', '653', '3489'],
        ['673', '1881', '2138'],
        ['2', '56', '1009', '1525', '1967', '2043', '2399', '3438', '3439', '3440'],
        ['810', '1126', '1702', '2253', '3393', '3466'],
        ['885', '1654', '2086'],
        ['2143', '2872', '3479'],
        ['1750', '2021', '2093'],
        ['247', '1920', '2017', '2087'],
        ['260', '1073', '1097', '2100', '2105', '2174', '2193', '2628', '2797', '2968']
    ]

    final_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '2', '56', '247', '260', '653', '673', '810', '885', 
                     '1009', '1073', '1097', '1126', '1525', '1654', '1702', '1750', '1881', '1920', '1967', '2017',
                     '2021', '2043', '2086', '2087', '2093', '2100', '2105', '2138', '2143', '2174', '2193', '2253',
                     '2399', '2628', '2797', '2872', '2968', '3393', '3438', '3439', '3440', '3466', '3479', '3489',
                     '3877', '3889']
    
    # T を作成
    T_parts = []
    column_names = []
    for i, cols in enumerate(c_columns):
        c_file = f'{c_prefix}_{i}.csv'
        if not os.path.exists(c_file):
            print(f'{c_file} does not exist')
            sys.exit(1)
        
        df = read_columns(c_file, cols)
        T_parts.append(df)
        column_names.extend(cols)
    
    T = pd.concat(T_parts, axis=1)

    # Tの列を指定された順に並べ替え
    T = T[final_columns]

    # Tをcsvファイルとして出力
#    T.to_csv('output_T.csv', index=False)
    
    # a.csv の各行を連結
    a_combined = a.apply(lambda row: ''.join(row.astype(str)), axis=1).values

    # 最小のハミング距離を持つ a.csv の行番号を格納するリスト
    min_indices = []
    filled_values = []
    
    # b.csv の各行について、最小のハミング距離を持つ a.csv の行番号を計算
    for b_index, b_row in b.iterrows():
        min_distance = float('inf')
        min_index = -1
        b_str = ''.join(b_row.astype(str))
        
        for a_index, a_str in enumerate(a_combined):
            combined_str = a_str + b_str
            
            i=0
            for t_row in T.itertuples(index=False, name=None):
                t_str = ''.join(map(str, t_row))
                distance = hamming_distance(combined_str, t_str)
                if distance < min_distance:
                    min_distance = distance
                    min_index = a_index
                    ii=i
                i=i+1

        # 最小のハミング距離だったTの行から*の位置の値を取得
#        T_row = T.iloc[min_index]
        T_row = T.iloc[ii]
        filled_row = fill_placeholders(b_row, T_row, b_row.index)
#        filled_row = fill_placeholders(b_row, best_t_row, b_row.index)
        filled_values.append(''.join(filled_row.astype(str)))
        min_indices.append(min_index)

        print(f'For b.csv row {b_index}, minimum Hamming distance is at a.csv row {min_index}')

    # 最小のハミング距離を持つ行番号をcsvファイルとして出力
    output_df = pd.DataFrame({
        'a_index': min_indices,
        'filled_values': filled_values
    })
    output_df.to_csv('E.csv', index=False, header=None)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <a_file> <b_file> <c_prefix>")
        sys.exit(1)

    a_prefix = sys.argv[1]
    b_prefix = sys.argv[2]
    c_prefix = sys.argv[3]

    main(a_prefix, b_prefix, c_prefix)
