import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# API URL'leri
base_url = "https://www.tsb.org.tr/InsuranceData/"
year_url = f"{base_url}GetVehicleYearList?_=1719830908637"
brand_url = f"{base_url}GetVehicleBrandList?VehicleYear={{}}&_=1719830908639"
model_base_url = f"{base_url}GetVehicleModelList?vehicleYear={{}}&VehicleBrandId={{}}&_=1719830908640"
insurance_base_url = f"{base_url}GetInsuranceDatas?VehicleYear={{}}&VehicleModelId={{}}&_=1719830908641"

def fetch_years():
    response = requests.get(year_url)
    return response.json()['Result']

def fetch_brands(year):
    response = requests.get(brand_url.format(year))
    return response.json()['Result']

def fetch_models(year, brand_id):
    response = requests.get(model_base_url.format(year, brand_id))
    return response.json()['Result']

def fetch_insurance_data(year, model_id):
    response = requests.get(insurance_base_url.format(year, model_id))
    return response.json()['Result']

def fetch_all_data():
    start_time = time.time()
    
    years = fetch_years()
    all_data = []
    total_count = 0

    def process_model(year, brand, model):
        nonlocal total_count
        insurance_data = fetch_insurance_data(year, model['VehicleModelId'])
        total_count += 1
        return {
            'VehicleYear': year,
            'VehicleBrand': brand['Name'],
            'VehicleModelId': model['VehicleModelId'],
            'VehicleModelName': model['Name'],
            'Amount': insurance_data['Amount'],
            'VehicleBrandCode': insurance_data['VehicleBrandCode'],
            'VehicleModelCode': insurance_data['VehicleModelCode']
        }

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_model = {}

        for year in years:
            brands = fetch_brands(year)
            print(f"Year {year}: Found {len(brands)} brands")
            
            for brand in brands:
                models = fetch_models(year, brand['VehicleBrandId'])
                print(f"  Brand {brand['Name']}: Found {len(models)} models")
                
                for model in models:
                    future = executor.submit(process_model, year, brand, model)
                    future_to_model[future] = model

        for future in as_completed(future_to_model):
            model_data = future.result()
            all_data.append(model_data)

    elapsed_time = time.time() - start_time
    print(f"\nTotal data fetched: {total_count}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    with open('EBSinsurance_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

fetch_all_data()
