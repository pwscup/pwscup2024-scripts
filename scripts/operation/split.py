import pandas as pd
import sys

def create_output_files(inname):
    # Bi.csvファイルを読み込む
    input_filename = inname + '.csv'
    df = pd.read_csv(input_filename)

    # ヘッダ名を取得する
    headers = list(df.columns)

    # Bi_0.csvを作成する
    Bi_0_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '260', '653', '1525', '2105', '2193', '2253', '2628', '2872', '3438', '3439', '3440', '3877', '3889']
    df_Bi_0 = df[Bi_0_columns]
    out0 = inname + '_0.csv'
    df_Bi_0.to_csv(out0, index=False)

    # Bi_1.csvを作成する
    Bi_1_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '2', '56', '260', '653', '673', '1009', '1073', '1525', '1750', '1881', '1967', '2043', '2093', '2105', '2143', '2193', '2399', '2628', '2968', '3479', '3489', '3877', '3889']
    df_Bi_1 = df[Bi_1_columns]
    out1 = inname + '_1.csv'
    df_Bi_1.to_csv(out1, index=False)

    # Bi_2.csvを作成する
    Bi_2_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '673', '1881', '1920', '2087', '2138']
    df_Bi_2 = df[Bi_2_columns]
    out2 = inname + '_2.csv'
    df_Bi_2.to_csv(out2, index=False)

    # Bi_3.csvを作成する
    Bi_3_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '2', '56', '673', '810', '885', '1009', '1073', '1097', '1525', '1654', '1702', '1750', '1881', '1920', '1967', '2017', '2043', '2087', '2093', '2138', '2399', '3438', '3439', '3440']
    df_Bi_3 = df[Bi_3_columns]
    out3 = inname + '_3.csv'
    df_Bi_3.to_csv(out3, index=False)

    # Bi_4.csvを作成する
    Bi_4_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '673', '810', '1073', '1126', '1702', '2100', '2174', '2253', '2797', '3393', '3466']
    df_Bi_4 = df[Bi_4_columns]
    out4 = inname + '_4.csv'
    df_Bi_4.to_csv(out4, index=False)

    # Bi_5.csvを作成する
    Bi_5_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '247', '885', '1097', '1654', '2086', '2138', '2872']
    df_Bi_5 = df[Bi_5_columns]
    out5 = inname + '_5.csv'
    df_Bi_5.to_csv(out5, index=False)

    # Bi_6.csvを作成する
    Bi_6_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '247', '2100', '2143', '2872', '3479']
    df_Bi_6 = df[Bi_6_columns]
    out6 = inname + '_6.csv'
    df_Bi_6.to_csv(out6, index=False)

    # Bi_7.csvを作成する
    Bi_7_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '260', '1097', '1750', '2021', '2093', '2105', '2628', '2968']
    df_Bi_7 = df[Bi_7_columns]
    out7 = inname + '_7.csv'
    df_Bi_7.to_csv(out7, index=False)

    # Bi_8.csvを作成する
    Bi_8_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '247', '1920', '2017', '2087']
    df_Bi_8 = df[Bi_8_columns]
    out8 = inname + '_8.csv'
    df_Bi_8.to_csv(out8, index=False)

    # Bi_9.csvを作成する
    Bi_9_columns = ['Gender', 'Age', 'Occupation', 'ZIP-code', '260', '1097', '2628', '2174', '2797', '1073', '2100', '2968', '2105', '2193']
    df_Bi_9 = df[Bi_9_columns]
    out9 = inname + '_9.csv'
    df_Bi_9.to_csv(out9, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 split.py Bi00")
    else:
        inname = sys.argv[1]
        create_output_files(inname)
