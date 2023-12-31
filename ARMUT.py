import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules


df_ = pd.read_csv("armut_data.csv")
df = df_.copy()
df.head()
df.dtypes


df["Hizmet"] = [str(row[1]) + "_" + str(row[2]) for row in df.values]
df.head()

# Alternatif
df["ServiceId_1"] = df["ServiceId"].astype(str)
df["CategoryId_1"] = df["CategoryId"].astype(str)

df["SC_Id"] = ["_".join(i) for i in (df[["ServiceId_1","CategoryId_1"]].values)]


df["CreateDate"] = pd.to_datetime(df["CreateDate"])
df["NEW_DATE"] = df["CreateDate"].dt.strftime("%Y-%m")
df["SepetID"] = [str(row[0]) + "_" + str(row[5]) for row in df.values]
df.head()

#df["New_Date"]=df["CreateDate"].dt.to_period('M')


# Hizmet         0_8  10_9  11_11  12_7  13_11  14_7  15_1  16_8  17_5  18_4..
# SepetID
# 0_2017-08        0     0      0     0      0     0     0     0     0     0..
# 0_2017-09        0     0      0     0      0     0     0     0     0     0..
# 0_2018-01        0     0      0     0      0     0     0     0     0     0..
# 0_2018-04        0     0      0     0      0     1     0     0     0     0..
# 10000_2017-08    0     0      0     0      0     0     0     0     0     0..

invoice_product_df = df.groupby(['SepetID', 'Hizmet'])['Hizmet'].count().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)
df_t=invoice_product_df
df_t.head()
invoice_product_df.loc[["10591_2018-08"]]


frequent_itemsets = apriori(invoice_product_df, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules.head()

rules.sort_values(by="lift",ascending=False)

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate (sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"]))
    #recommendation_list = list({item for item_list in recommendation_list for item in item_list})
    return recommendation_list[:rec_count]

arl_recommender(rules, "2_0", 2)

# Alternatif
def arl_recommender1(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []

    for i, product in sorted_rules["antecedents"].items():
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"]))
    recommendation_list = list({item for item_list in recommendation_list for item in item_list})
    return recommendation_list[:rec_count]


arl_recommender1(rules,"2_0", 2)


df.loc[df["Hizmet"] == "2_0"].sort_values("CreateDate", ascending=False)

invoice_product_df.loc[["21857_2017-08"]]

