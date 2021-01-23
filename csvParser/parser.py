import csv

file = open("raw.txt")

ingredients_set = set()
items_set = set()

for i, line in enumerate(file):

    ingredients = [item.strip() for item in line.split(';')[1].split(',')]
    item = line.split(';')[0].strip().replace(' ',r'_').lower()

    items_set.add(item)

    for ingredient in ingredients:
        ingredients_set.add(ingredient)

file.close()

print(ingredients_set)

filename = "ingredients.csv"
    
with open(filename, 'w+', newline='') as csvfile:  
    writer = csv.DictWriter(csvfile, fieldnames = ["item"] + list(items_set) + list(ingredients_set), restval=0)    
    writer.writeheader()

    for i,line in enumerate(open("dump2.txt")):
        ingredients = [item.strip() for item in line.split(';')[1].split(',')]

        ingredients_dict = {}

        for ingredient in ingredients:
            ingredients_dict[ingredient] = 1

        item = line.split(';')[0].strip().replace(' ',r'_').lower()

        row = {"item": item, item: 1,**ingredients_dict}

        print(row)

        writer.writerow(row)

file.close()
