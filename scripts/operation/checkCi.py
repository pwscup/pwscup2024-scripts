import pandas as pd
import os
import sys
from tqdm import tqdm

def check_csv_file(file1, file2):
    # CSVファイルの存在確認
    if not os.path.exists(file1):
        print(f"エラー: ファイル '{file1}' が存在しません")
        return False, [f"ファイル '{file1}' が存在しません"]
    if not os.path.exists(file2):
        print(f"エラー: ファイル '{file2}' が存在しません")
        return False, [f"ファイル '{file2}' が存在しません"]
    
    # CSVファイルを読み込む
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # "Name"列を削除して比較用のデータを作成
    B = df1.drop(columns=["Name"], errors='ignore')
    C = df2.drop(columns=["Name"], errors='ignore')
    
    # チェックNGの箇所を記録するリスト
    errors = []
    
    # 進捗表示用のtqdmの設定
    total_checks = len(C.columns) + 2  # 行数・列数チェック + 列ごとのチェック
    progress_bar = tqdm(total=total_checks, desc="チェック進行中", ncols=100)

    # 1. 行数と列数が同じであることを確認
    if B.shape != C.shape:
        errors.append("行数または列数が一致しません")
        progress_bar.update(1)
        progress_bar.close()
        return False, errors
    progress_bar.update(1)
    
    # 2. 列名が一致していることを確認
    if not all(B.columns == C.columns):
        errors.append("列名が一致しません")
        progress_bar.update(1)
        progress_bar.close()
        return False, errors
    progress_bar.update(1)
    
    # 3. 列ごとのチェック
    for col in C.columns:
        if col.isdigit():
            if not C[col].isin([0, 1, 2, 3, 4, 5]).all():
                errors.append(f"列 {col} に0から5の整数以外の値が含まれています")
                if len(errors) >= 20:
                    break
        else:
            if not C[col].isin(B[col]).all():
                errors.append(f"列 {col} にBの当該列に含まれる値以外の値が含まれています")
                if len(errors) >= 20:
                    break
        progress_bar.update(1)
    
    progress_bar.close()

    if errors:
        return False, errors

    return True, []

def main():
    if len(sys.argv) != 3:
        print("使い方: python3 checkCi.py input_file1.csv input_file2.csv")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    result, error_list = check_csv_file(file1, file2)
    
    if not result:
        print("チェックがNGの箇所(20箇所まで表示します)：")
        for error in error_list:
            print(error)
    else:
        print("すべてのチェックをクリアしました")

if __name__ == "__main__":
    main()

