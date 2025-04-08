import pandas as pd
import yaml

def generate_yaml_schema(csv_file, yaml_file):
   df = pd.read_csv(csv_file)

   schema = {"columns" : []}
   numerical_columns = []

   for column in df.columns:
       dataType = str(df[column].dtype)
       schema["columns"].append({column: dataType})

       if dataType.startswith("int") or dataType.startswith("float"):
           numerical_columns.append(column)
        
   schema["numerical_columns"] = numerical_columns

   with open (yaml_file, "w") as file:
       yaml.dump(schema, file, default_flow_style=False)



if __name__ == "__main__":
    csv_file = r"network_data\phisingData.csv"
    yaml_file = r"data_schema\schema.yaml"
    generate_yaml_schema(csv_file, yaml_file)
    print(f"Schema written to {yaml_file}")