
import json
import os
import urllib.request
# Create a dictionary to store the transformed data
transformed_data = {"CategoryTitle": "", "Subcategories": []}



All_data=[]

data = []
# Load your data from the JSON Lines file
with open('data.jl', 'r') as jsonl_file:#creating base structre with respect to category title
    for line in jsonl_file:
        item = json.loads(line)
        category_title = item.get("CategoryTitle")
        


        if category_title not in data:
            data.append(category_title)
            transformed_data = {"CategoryTitle": category_title, "Subcategories": []}
            All_data.append(transformed_data)

data =[]

with open('data.jl', 'r') as jsonl_file:#creating base structre with respect to subcategory title
    for line in jsonl_file:
        item = json.loads(line)
        subcategory_title = item.get("SubcategoryTitle")
        category_title = item.get("CategoryTitle")
        


        if subcategory_title not in data:

            data.append(subcategory_title)
            for i in All_data:
                if i["CategoryTitle"]==category_title:
                    subcategory_map = {"SubcategoryTitle": subcategory_title,
                                        "Products": []
                            }

                    i["Subcategories"].append(subcategory_map)
data=[]
with open('data.jl', 'r') as jsonl_file:#Adding products
    for line in jsonl_file:
        item = json.loads(line)
        subcategory_title = item.get("SubcategoryTitle")
        category_title = item.get("CategoryTitle")
        products = item.get("Products")
       
        for i in products:

            if i not in data:
                data.append(i)
                for itr in All_data:

                    if itr["CategoryTitle"]==category_title:

                        subcategories = itr["Subcategories"]

                        for j in subcategories:

                            if j["SubcategoryTitle"] == subcategory_title:

                               if i not in j["Products"]:
                                    j["Products"].append(i)

#Downloading images
download_directory = '.\Images'

# the directory if it doesn't exist
os.makedirs(download_directory, exist_ok=True)

for i in All_data:
    subcategories = i["Subcategories"]

    for j in subcategories:

        for k in j["Products"]:
            if k["ItemImageURL"] != None:
                filename = os.path.join('.\Images', k["ItemImageURL"].split("/")[-1])

                try:
                    # Download the image to the specified directory
                    urllib.request.urlretrieve(k["ItemImageURL"], filename)

                    print(f'Successfully downloaded {filename}')
                except Exception as e:
                    print(f'Failed to download {k["ItemImageURL"]}: {e}')
                                

                
# Save the transformed data to a new JSON file
with open('transformed_data.json', 'w') as json_file:
    json.dump(All_data, json_file, indent=4)

