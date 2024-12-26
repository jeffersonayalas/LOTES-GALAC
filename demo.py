import pandas as pd 

input_cols = [0, 1, 2]

df = pd.read_excel("plantilla.xlsx", header=0, sheet_name="PLANTILLA DE FACTURAS GALAC", )

#print(pd.__version__)
#df.shape()
#print(df.columns[0])

df_cols = df.columns

#Archivo txt
#f = open("prueba.txt", "x")
#f = open("myfile.txt", "w")

for col in df_cols:
    #print(col)
    #var = df[col].head(12)
    print(df[col].head(12)) # DAR FORMATO A LA SALIDA# 
    #f.write(var)



df.to_csv("export.csv", sep="', ", header=True, index=False)

# --- condiciones --- #


