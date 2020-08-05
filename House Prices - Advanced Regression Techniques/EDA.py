# %% markdown
# # EDA HOUSE PRICES
# %% codecell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import copy
import missingno as msno
from IPython.core import display as ICD
import json

os.chdir("/content/drive/My Drive/0. DATA SCIENCE/HOUSE PRICES/")
!ls
# %% codecell
def continous_grid(df, X , y ,n_rows, n_cols, bins=10, size = 10, size_ratio = 1,alpha=1,hue_col_name=None):


    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(size , size*size_ratio) )
    iter_variables = iter(X)
    counter = 0

    for i in range(n_rows):
            for j in range(n_cols):
                ax = axes[i][j]

                if counter < 2*len(X):
                    if j%2==0:
                        var_name = next(iter_variables)
                        sns.FacetGrid(df, hue=hue_col_name).map(sns.distplot, var_name ,bins=bins, ax=ax)
                        ax.set_title(var_name+" Distribution")
                        ax.legend(loc="best")
                    else:
                        sns.scatterplot(x=var_name, y=y, hue=hue_col_name, data =df, alpha=alpha, ax=ax)
                        ax.set_title(var_name + " Scatterplot")

                else:
                    ax.set_axis_off()

                counter += 1

    fig.tight_layout()
    sns.despine()
# %% codecell
def discrete_grid(df, X , y ,n_rows, n_cols, size = 4, size_ratio = 1,alpha=1,hue_col_name=None, s=10):

    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(size , size*size_ratio))

    iter_variables = iter(X)
    counter = 0

    for i in range(n_rows):
            for j in range(n_cols):
                ax = axes[i][j]

                if counter < 2*len(X):
                    if j%2==0:
                        var_name = next(iter_variables)
                        sns.countplot(x= var_name , hue = hue_col_name ,
                                      data = df , ax=ax, palette ="muted")
                        ax.set_title(var_name+" Countplot")
                        ax.legend(loc="best")
                    else:
                        sns.stripplot(x = var_name , y = y , hue = hue_col_name, s=s,
                                       data = df , #scale="count", scale_hue=False
                                       alpha = alpha, ax = ax, palette="muted")

                        # sns.violinplot( x = var_name , y = y , hue = hue_col_name,
                        #                data = df , #scale="count", scale_hue=False
                        #                alpha = alpha, ax = ax, palette="muted")

                        ax.legend().set_visible(False) # esto debido a que en test nunca tenemos y, solo X
                        ax.set_title(var_name + " Stripplot")

                else:
                    ax.set_axis_off()

                counter += 1

    fig.tight_layout()
    sns.despine()
# %% markdown
# ---
# ## Cargando e interpretando data
# %% codecell
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

df_train.drop("Id",axis=1,inplace=True)
df_test.drop("Id",axis=1,inplace=True)

# variables_categoricas = [x for x in df_test.columns if df_test[x].dtype=="object"]
# variables_numericas = [ x for x in df_test.columns if x not in variables_categoricas]

variables_continuas =[  'LotFrontage',
                        'LotArea',
                        'MasVnrArea',
                        'BsmtFinSF1',
                        'BsmtFinSF2',
                        'BsmtUnfSF',
                        'TotalBsmtSF',
                        '1stFlrSF',
                        '2ndFlrSF',
                        'GarageArea',
                        'GrLivArea',
                        'WoodDeckSF',
                        'OpenPorchSF',
                        'EnclosedPorch',
                        '3SsnPorch',
                        'ScreenPorch',
                        'PoolArea',
                        'MiscVal',
                        'LowQualFinSF',
                      ] #tmb están las discretas con muchos niveles

variables_discretas =['BsmtFullBath',
                      'BsmtHalfBath',
                      'FullBath',
                      'HalfBath',
                      'BedroomAbvGr',
                      'KitchenAbvGr',
                      'TotRmsAbvGrd',
                      'Fireplaces',
                      'GarageCars',
                      ]

variables_ordinales =['LotShape',
                      'LandSlope',
                      'HouseStyle',
                      'OverallQual',
                      'OverallCond',
                      'ExterQual',
                      'ExterCond',
                      'BsmtQual',
                      'BsmtCond',
                      'BsmtExposure',
                      'BsmtFinType1',
                      'BsmtFinType2',
                      'HeatingQC',
                      'CentralAir',#binaria
                      'KitchenQual',
                      'Functional',
                      'FireplaceQu',
                      'GarageFinish',
                      'GarageQual',
                      'GarageCond',
                      'PavedDrive',
                      'PoolQC',
                      'Fence',
                      ]

variables_nominales =['MSSubClass',
                      'MSZoning',
                      'Street', #binaria
                      'Alley',#puede ser ordinal,checkear
                      'LandContour',
                      'Utilities',
                      'LotConfig',
                      'Neighborhood',
                      'Condition1',
                      'Condition2',
                      'BldgType',
                      'RoofStyle',
                      'RoofMatl',
                      'Exterior1st',
                      'Exterior2nd',
                      'MasVnrType',
                      'Foundation',
                      'Heating',
                      'Electrical',
                      'GarageType',
                      'MiscFeature',
                      'SaleType',
                      'SaleCondition',
                      'MoSold',
                      ]

variables_temporales = ['YearBuilt',
                        'YearRemodAdd',
                        'GarageYrBlt',
                        'YrSold',
                        ]

variables_categoricas = variables_ordinales + variables_nominales
variables_numericas = variables_continuas + variables_discretas

target = ["SalePrice"]

#para plotear con hue
df_train["hue_col"] = "train"
df_test["hue_col"] = "test"
df_total = df_train.append(df_test, ignore_index=True)
# %% codecell
variables={"continuas":variables_continuas,
           "discretas":variables_discretas,
           "nominales":variables_nominales,
           "ordinales":variables_ordinales,
           "numericas":variables_numericas,
           "categoricas":variables_categoricas,
           "temporales":variables_temporales,
           }

# to json
with open('variables.json', 'w') as fp:
    json.dump(variables, fp)
# %% codecell
ordinal_mapper =  {

'LotShape':{"Reg":4,
            "IR1":3,
            "IR2":2,
            "IR3":1,
            np.nan:0},

'LandSlope':{"Gtl":1,
             "Mod":2,
             "Sev":3,
             np.nan:0},

'HouseStyle':{"1Story":1,
              "1.5Fin":2,
              "1.5Unf":3,
              "2Story":4,
              "2.5Fin":5,
              "2.5Unf":6,
              "SFoyer":7,
              "SLvl":8,
              np.nan:0},

#'OverallQual': ya está en números

# 'OverallCond': ya está en numeros

'ExterQual':{"Ex":1,
             "Gd":2,
             "TA":3,
             "Fa":4,
             "Po":5,
             np.nan:0},

'ExterCond':{"Ex":1,
             "Gd":2,
             "TA":3,
             "Fa":4,
             "Po":5,
             np.nan:0},

'BsmtQual':{"Ex":105,
            "Gd":95,
            "TA":85,
            "Fa":75,
            "Po":65,
            np.nan:0},

'BsmtCond':{"Ex":5,
            "Gd":4,
            "TA":3,
            "Fa":2,
            "Po":1,
            np.nan:0},

'BsmtExposure':{"Gd":5,
                "Av":4,
                "Mn":3,
                "No":2,
                "NA":1,
                np.nan:0},

'BsmtFinType1':{"GLQ":6,
                "ALQ":5,
                "BLQ":4,
                "Rec":3,
                "LwQ":2,
                "Unf":1,
                np.nan:0},

'BsmtFinType2':{"GLQ":6,
                "ALQ":5,
                "BLQ":4,
                "Rec":3,
                "LwQ":2,
                "Unf":1,
                np.nan:0},

'HeatingQC':{"Ex":5,
             "Gd":4,
             "TA":3,
             "Fa":2,
             "Po":1,
             np.nan:0},

'CentralAir':{"N":0,
              "Y":1,
              np.nan:-1},

'KitchenQual':{"Ex":5,
               "Gd":4,
               "TA":3,
               "Fa":2,
               "Po":1,
               np.nan:0},

'Functional':{"Typ":8,
              "Min1":7,
              "Min2":6,
              "Mod":5,
              "Maj1":4,
              "Maj2":3,
              "Sev":2,
              "Sal":1,
              np.nan:0},

'FireplaceQu':{"Ex":5,
               "Gd":4,
               "TA":3,
               "Fa":2,
               "Po":1,
               np.nan:0},

'GarageFinish':{"Fin":4,
                "RFn":3,
                "Unf":2,
                "NA":1,
                np.nan:0},

'GarageQual':{"Ex":5,
              "Gd":4,
              "TA":3,
              "Fa":2,
              "Po":1,
              np.nan:0},

'GarageCond':{"Ex":5,
              "Gd":4,
              "TA":3,
              "Fa":2,
              "Po":1,
              np.nan:0},

'PavedDrive':{"Y":3,
              "P":2,
              "N":1,
              np.nan:0},

'PoolQC':{"Ex":5,
          "Gd":4,
          "TA":3,
          "Fa":2,
          "NA":1,
          np.nan:0},

'Fence':{"GdPrv":4,
         "MnPrv":3,
         "GdWo":2,
         "MnWw":1,
         np.nan:0}

}

# %% codecell
print("TRAIN dtypes y sample:\n")
ICD.display(df_train.dtypes.to_frame().T)
print("\n")
ICD.display(df_train.sample(2))
# %% codecell
print("TEST dtypes y sample:\n")
ICD.display(df_test.dtypes.to_frame().T)
print("\n")
ICD.display(df_test.sample(2))
# %% markdown
# ---
# ## Vacíos
# %% codecell
sns.set_style("dark")
msno.matrix(df_train,labels=True , color=(0.2,0.2,0.2))
plt.xticks(rotation=90, horizontalalignment='center')
plt.show()
# %% codecell
g = msno.bar(df_train,sort="descending",color="gray",labels=True)
g.set_xticklabels(g.get_xticklabels(), rotation=90, horizontalalignment='center')

sns.set_style("darkgrid")
plt.xticks(rotation=90, horizontalalignment='center')
plt.show()
# %% codecell
g= msno.heatmap(df_train,n=df_train.shape[1])
plt.show()
# %% codecell
msno.dendrogram(df_train, )
plt.show()
# %% markdown
# ---
# # Multicolinearidad
# %% codecell
sns.set_
sns.set_context("talk")
fig, (ax) = plt.subplots(1,1,figsize=(40,40))

sns.heatmap(df_train.corr(),
            ax = ax,
            vmin = -1, vmax = 1,
            cmap ="coolwarm",
            annot = True,
            fmt = ".1f",
            linewidths=.05,
            )
    # fig.subplots_adjust(top=0.93)
# %% markdown
# ---
# # VARIABLES PREDICTORAS
# %% codecell
sns.set_style("darkgrid")
sns.set_context("poster")
continous_grid(df_total,variables_continuas, "SalePrice", 7, 6, 10 ,40,1,0.25, "hue_col")
plt.show()
# %% codecell
sns.set_style("darkgrid")
sns.set_context("talk")
discrete_grid(df_total ,variables_discretas,"SalePrice",5, 4 ,25 , 1,0.4, "hue_col" ,3)
plt.show()
# %% codecell
sns.set_style("darkgrid")
sns.set_context("talk")
discrete_grid(df_total ,variables_nominales,"SalePrice",6, 8 ,40 , 0.5,0.7, "hue_col",1.5 )
plt.show()
# %% codecell
sns.set_style("darkgrid")
sns.set_context("talk")
discrete_grid(df_total ,variables_ordinales,"SalePrice",6, 8 ,40 , 0.6,0.8, "hue_col",2 )
plt.show()
# %% markdown
# TARGET
# %% codecell

# %% markdown
# ---
# %% codecell
mapper={"Ex":5,"Gd":4,"TA":3,"Fa":2,np.nan:1}
foo = df_train[["PoolQC"]]
foo["PoolQC"].replace(mapper,inplace=True)
foo
