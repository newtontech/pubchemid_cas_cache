import os
import csv
import pandas as pd
import requests
from urllib.parse import quote
cache_path = "./pubchemid_cas_cache.csv"
def get_pubchemid_by_cas(cas_number):
    """From CAS number query PubChem CID and cache the result"""
    cache = {}
    
    if os.path.exists(cache_path):
        df = pd.read_csv(cache_path)
        cache = dict(zip(df['cas_number'], df['pubchem_id'].astype(int)))
    
    if cas_number in cache:
        return cache[cas_number]
    
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{quote(cas_number)}/cids/JSON"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        cid_list = response.json().get('IdentifierList', {}).get('CID', [])
        
        if not cid_list:
            print(f"Cannot find PubChem ID for CAS number {cas_number}")
            return None
        
        pubchem_id = cid_list[0]
        new_data = pd.DataFrame({'pubchem_id': [pubchem_id], 'cas_number': [cas_number]})
        # Check if cache file exists and is not empty
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            new_data.to_csv(cache_path, mode='a', header=False, index=False)
        else:
            new_data.to_csv(cache_path, mode='w', header=True, index=False)
        return pubchem_id
        
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Query error: {e}")
        return None

def get_cas_by_pubchemid(pubchem_id):
    """From PubChem ID query CAS number and cache the result"""
    cache = {}
    
    if os.path.exists(cache_path):
        df = pd.read_csv(cache_path)
        # Build a mapping from pubchem_id to cas_number, note that pubchem_id is an integer
        cache = dict(zip(df['pubchem_id'].astype(int), df['cas_number']))
    
    if pubchem_id in cache:
        return cache[pubchem_id]
    
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{pubchem_id}/xrefs/CAS/JSON"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        data = response.json()
        info_list = data.get('InformationList', {}).get('Information', [])
        
        if not info_list or 'CAS' not in info_list[0]:
            print(f"Cannot find CAS number for PubChem ID {pubchem_id}")
            return None
        
        cas_number = info_list[0]['CAS']
        new_data = pd.DataFrame({'pubchem_id': [pubchem_id], 'cas_number': [cas_number]})
        # Check if cache file exists and is not empty
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            new_data.to_csv(cache_path, mode='a', header=False, index=False)
        else:
            new_data.to_csv(cache_path, mode='w', header=True, index=False)
        return cas_number
        
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Query error: {e}")
        return None

if __name__ == '__main__':
    print("Test get_pubchemid_by_cas('7732-18-5'):", get_pubchemid_by_cas('7732-18-5'))
    print("Test get_cas_by_pubchemid(962):", get_cas_by_pubchemid(962))
