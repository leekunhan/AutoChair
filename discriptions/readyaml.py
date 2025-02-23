import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

if __name__ == "__main__":
    file_path = '/home/kh/AutoChair/discriptions/corsa.yaml'
    yaml_data = read_yaml(file_path)
    print(yaml_data)