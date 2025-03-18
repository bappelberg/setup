#!/usr/bin/python3
import requests
from requests.auth import HTTPBasicAuth
import argparse

# Hårdkodade variabler för Jenkins URL och API-åtkomst
JENKINS_URL = 'http://localhost:8080'
USERNAME = 'beno'
API_TOKEN = '11eabb09e38d205bc80916407f7cdb9219'

# Konfigurera argparse för kommandoradsargument
def parse_args():
    parser = argparse.ArgumentParser(description='Hämta bygginformation från Jenkins.')
    parser.add_argument('--all', action='store_true', help='Lista alla jobb med alla byggen')
    parser.add_argument('--job-name', type=str, help='Lista bygginformation för ett specifikt jobb')
    parser.add_argument('--job-number', type=int, help='Visa ett specifikt byggnummer för ett jobb')
    
    return parser.parse_args()

def main():
    # Hämta kommandoradsargument
    args = parse_args()
    
    # Hämta alla jobb om --all flaggan är satt
    if args.all:
        all_jobs_url = f'{JENKINS_URL}/api/json?tree=jobs[name]'
        response = requests.get(all_jobs_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if response.status_code == 200:
            jobs = response.json()['jobs']
            for job in jobs:
                job_name = job['name']
                print(f"Jobb: {job_name}")
                # Hämta alla byggen för detta jobb
                builds_url = f'{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,duration,result,url]'
                builds_response = requests.get(builds_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

                if builds_response.status_code == 200:
                    builds = builds_response.json()['builds']
                    for build in builds:
                        build_number = build['number']
                        build_url = build['url']
                        duration = build.get('duration', 'N/A')
                        result = build.get('result', 'N/A')

                        print(f"  Byggnummer: {build_number}")
                        print(f"  URL: {build_url}")
                        print(f"  Duration: {duration} ms")
                        print(f"  Resultat: {result}")
                    print()
                else:
                    print(f"Fel vid hämtning av bygginformation för {job_name}")
        else:
            print("Fel vid hämtning av jobbinformation.")

    # Hämta specifikt jobb om --job-name är satt
    elif args.job_name:
        job_name = args.job_name
        builds_url = f'{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,duration,result,url]'
        builds_response = requests.get(builds_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if builds_response.status_code == 200:
            builds = builds_response.json()['builds']
            print(f"Jobb: {job_name}")
            for build in builds:
                build_number = build['number']
                build_url = build['url']
                duration = build.get('duration', 'N/A')
                result = build.get('result', 'N/A')

                print(f"  Byggnummer: {build_number}")
                print(f"  URL: {build_url}")
                print(f"  Duration: {duration} ms")
                print(f"  Resultat: {result}")
            print()
        else:
            print(f"Fel vid hämtning av bygginformation för {job_name}")
    
    # Hämta specifikt jobb och byggnummer om både --job-name och --job-number är satt
    elif args.job_name and args.job_number:
        job_name = args.job_name
        build_number = args.job_number
        build_url = f'{JENKINS_URL}/job/{job_name}/{build_number}/api/json'
        build_response = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if build_response.status_code == 200:
            build = build_response.json()
            build_url = build['url']
            duration = build.get('duration', 'N/A')
            result = build.get('result', 'N/A')

            print(f"Jobb: {job_name}")
            print(f"  Byggnummer: {build_number}")
            print(f"  URL: {build_url}")
            print(f"  Duration: {duration} ms")
            print(f"  Resultat: {result}")
        else:
            print(f"Fel vid hämtning av bygginformation för {job_name} nummer {build_number}")
    else:
        print("Ingen giltig flagga angiven. Använd --all för alla jobb, --job-name för ett specifikt jobb, eller --job-name och --job-number för ett specifikt byggnummer.")

if __name__ == "__main__":
    main()
