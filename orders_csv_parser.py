import sys
import pandas as pd
import collections


if len(sys.argv) < 2:
  print ("# Orders CSV Parser requires exactly 1 argument.")
  print ("# Usage:  orders_csv_parser path_to_input_file")
  quit()


path = sys.argv[1]
colnames=['Id', 'Area', 'Name', 'Quantity', 'Brand'] 

productQty = {}
brandCount = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
popularBrands = {}

rdf = pd.read_csv(path, names = colnames, usecols = ['Name', 'Quantity', 'Brand'], header = None)

for index, row in rdf.iterrows():
  name = row['Name']
  qty = row['Quantity']
  brand = row['Brand']
  # add name => qty
  if name in productQty:
    productQty[name] += qty
  else:
    productQty[name] = qty

  # add a pair of (name, brand) => count
  if name in brandCount:
      if brand in brandCount[name]:
        brandCount[name][brand] = brandCount.get(name).get(brand) + 1
      else:
        brandCount[name][brand] =  1

  else:
    brandCount[name][brand] = 1


for k in productQty.keys():
    productQty[k] /= len(rdf)


for k in brandCount.keys():
  popularBrands[k] = max(brandCount[k], key=brandCount[k].get)

index = path.rindex('/')
filename = path[index+1:]

wdf_0 = pd.DataFrame.from_dict(productQty, orient="index")
wdf_0.to_csv("0_"+ filename, columns=None, header=False, index=False)

wdf_1 = pd.DataFrame.from_dict(popularBrands, orient="index")
wdf_1.to_csv("1_"+ filename, columns=None, header=False, index=False)

print ("0_"+ filename + " and " "1_"+ filename + " created successfully!")
