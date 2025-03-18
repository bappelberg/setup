#!/usr/bin/python3
import requests
from requests.auth import HTTPBasicAuth
import argparse

# Hardcoded variables for Jenkins URL and API access
JENKINS_URL = 'http://localhost:8080'
USERNAME = 'beno'
API_TOKEN = '11eabb09e38d205bc80916407f7cdb9219'

# Configure argparse for command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Fetch and manage build information from Jenkins.')
    parser.add_argument('--all', action='store_true', help='List all jobs with all builds')
    parser.add_argument('--job-name', type=str, help='List build information for a specific job')
    parser.add_argument('--job-number', type=int, help='Show a specific build number for a job')
    parser.add_argument('--dryrun', action='store_true', help='Show which builds would be killed without actually killing them')
    parser.add_argument('--stop', action='store_true', help='Stop all ongoing builds')
    parser.add_argument('--term', action='store_true', help='Forcefully terminate all ongoing builds')
    parser.add_argument('--kill', action='store_true', help='Hard kill all ongoing builds')
    
    return parser.parse_args()

def stop_build(job_name, build_number, method="stop"):
    """Stop a specific build if it is ongoing"""
    stop_url = f'{JENKINS_URL}/job/{job_name}/{build_number}/{method}'
    response = requests.post(stop_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    if response.status_code == 200:
        print(f"Build number {build_number} for job {job_name} was successfully {method}ed.")
    else:
        print(f"Error {method}ing build number {build_number} for job {job_name}")

def format_duration(duration_ms):
    """Convert milliseconds to a readable format of d:h:m:s"""
    seconds = duration_ms // 1000
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{days}d:{hours}h:{minutes}m:{seconds}s"

def main():
    # Fetch command-line arguments
    args = parse_args()

    # Fetch all jobs if --all flag is set
    if args.all:
        all_jobs_url = f'{JENKINS_URL}/api/json?tree=jobs[name]'
        response = requests.get(all_jobs_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if response.status_code == 200:
            jobs = response.json()['jobs']
            for job in jobs:
                job_name = job['name']
                print(f"Job: {job_name}")
                # Fetch all builds for this job
                builds_url = f'{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,duration,result,url,building]'
                builds_response = requests.get(builds_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

                if builds_response.status_code == 200:
                    builds = builds_response.json()['builds']
                    for build in builds:
                        build_number = build['number']
                        build_url = build['url']
                        duration_ms = build.get('duration', 'N/A')
                        result = build.get('result', 'N/A')
                        building = build.get('building', False)  # Whether the build is ongoing

                        # Format the duration to d:h:m:s
                        formatted_duration = format_duration(duration_ms)

                        print(f"  Build number: {build_number}")
                        print(f"      URL: {build_url}")
                        print(f"      Duration: {formatted_duration}")
                        print(f"      Result: {result}")
                        print(f"      Ongoing: {'Yes' if building else 'No'}")

                        # If --dryrun is set and the build is ongoing, show which builds would be stopped
                        if args.dryrun and building:
                            print(f"        Would {args.stop and 'stop' or args.term and 'term' or args.kill and 'kill'} build number {build_number} (Job: {job_name})")

                        # If --stop, --term, or --kill is set, perform the appropriate action
                        if not args.dryrun and building:
                            if args.stop:
                                stop_build(job_name, build_number, method="stop")
                            elif args.term:
                                stop_build(job_name, build_number, method="term")
                            elif args.kill:
                                stop_build(job_name, build_number, method="kill")

                    print()
                else:
                    print(f"Error fetching build information for {job_name}")
        else:
            print("Error fetching job information.")

    # Fetch a specific job if --job-name is set
    elif args.job_name:
        job_name = args.job_name
        builds_url = f'{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,duration,result,url,building]'
        builds_response = requests.get(builds_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if builds_response.status_code == 200:
            builds = builds_response.json()['builds']
            print(f"Job: {job_name}")
            for build in builds:
                build_number = build['number']
                build_url = build['url']
                duration_ms = build.get('duration', 'N/A')
                result = build.get('result', 'N/A')
                building = build.get('building', False)

                # Format the duration to d:h:m:s
                formatted_duration = format_duration(duration_ms)

                print(f"  Build number: {build_number}")
                print(f"      URL: {build_url}")
                print(f"      Duration: {formatted_duration}")
                print(f"      Result: {result}")
                print(f"      Ongoing: {'Yes' if building else 'No'}")

                # If --dryrun is set and the build is ongoing, show which builds would be stopped
                if args.dryrun and building:
                    print(f"        Would {args.stop and 'stop' or args.term and 'term' or args.kill and 'kill'} build number {build_number} (Job: {job_name})")

                # If --stop, --term, or --kill is set, perform the appropriate action
                if not args.dryrun and building:
                    if args.stop:
                        stop_build(job_name, build_number, method="stop")
                    elif args.term:
                        stop_build(job_name, build_number, method="term")
                    elif args.kill:
                        stop_build(job_name, build_number, method="kill")
            print()
        else:
            print(f"Error fetching build information for {job_name}")
    
    # Fetch a specific job and build number if both --job-name and --job-number are set
    elif args.job_name and args.job_number:
        job_name = args.job_name
        build_number = args.job_number
        build_url = f'{JENKINS_URL}/job/{job_name}/{build_number}/api/json'
        build_response = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if build_response.status_code == 200:
            build = build_response.json()
            build_url = build['url']
            duration_ms = build.get('duration', 'N/A')
            result = build.get('result', 'N/A')
            building = build.get('building', False)

            # Format the duration to d:h:m:s
            formatted_duration = format_duration(duration_ms)

            print(f"Job: {job_name}")
            print(f"  Build number: {build_number}")
            print(f"      URL: {build_url}")
            print(f"      Duration: {formatted_duration}")
            print(f"      Result: {result}")
            print(f"      Ongoing: {'Yes' if building else 'No'}")

            # If --dryrun is set and the build is ongoing, show which builds would be stopped
            if args.dryrun and building:
                print(f"        Would {args.stop and 'stop' or args.term and 'term' or args.kill and 'kill'} build number {build_number} (Job: {job_name})")

            # If --stop, --term, or --kill is set, perform the appropriate action
            if not args.dryrun and building:
                if args.stop:
                    stop_build(job_name, build_number, method="stop")
                elif args.term:
                    stop_build(job_name, build_number, method="term")
                elif args.kill:
                    stop_build(job_name, build_number, method="kill")
        else:
            print(f"Error fetching build information for {job_name} build number {build_number}")
    else:
        print("""Jenkins Build Killer
Usage:
  --all           : Fetch information for all jobs
  --job-name      : Fetch build information for a specific job
  --job-name and --job-number : Fetch information for a specific build within a job
  --dryrun        : Show which builds would be affected without actually stopping, terminating, or killing them
  --stop          : Stop ongoing builds
  --term          : Forcefully terminate ongoing builds
  --kill          : Hard kill ongoing builds
""")
        

if __name__ == "__main__":
    main()
