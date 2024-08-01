from utils import *

df_csv = read_file("cand.csv", "csv")
print(type_casting(df_csv, {"2": "str"}))

# print(df_csv.fill_nan(None).null_count())
# print(fill_interpolation(df_csv))
# df_csv = rename_columns(df_csv, {"read_val": "val"})
# # print(df_csv)

# df_filtered = filter_data(df_csv, "tag_id == BIO_FT_MAP.FT_2803.TOTAL")

# df_filtered = filter_data(df_filtered, "val < 1")
# # print(df_filtered_str2)

# datetime_format = "%Y/%m/%d %H:%M"
# type_casting(df_filtered, {df_filtered.columns[1]: "datetime"}, datetime_format=datetime_format)
# # print(slice_data(df_filtered, 0, 1000))

# # 컬럼 이름으로 선택
# selected_by_name = select_col(df_filtered, ['val'])
# print(selected_by_name)

# # 데이터 타입으로 선택
# selected_by_type = select_col(df_filtered, pl.Float64)
# print(selected_by_type)


# # 데이터 슬라이싱
# df_sliced = slice_data(df_csv, 0, 10)
# print(df_sliced)

# # 컬럼명 변경
# df_renamed = rename_columns(df_csv, {"0": "test"})
# print(df_renamed)

# # 피봇
# df_pivoted = pivot_data(df_csv, values=["value_col"], index=["index_col"], columns=["column_col"])
# print(df_pivoted)

# # 멜트
# df_melted = melt_data(df_csv, id_vars=["id_col"], value_vars=["value_col1", "value_col2"])
# print(df_melted)


# # 필터링
# df_filtered_str = filter_data(df_csv, "column_name > 10")
# print(df_filtered_str)

# # 필터링 - 커스텀 함수
# def custom_filter(df: pl.DataFrame) -> pl.DataFrame:
#     return df.filter(pl.col("asdf") < 5)

# df_filtered_func = filter_data(df_csv, custom_filter)
# print(df_filtered_func)