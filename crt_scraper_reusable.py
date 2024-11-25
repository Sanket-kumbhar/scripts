import requests
import csv

def fetch_certificates(query, output_filename="certificates.csv"):
    # Construct the search URL (adjust as needed)
    url = f"https://crt.sh/?q={query}&output=json"
    
    try:
        print(f"Fetching certificate data for query '{query}'...")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Print response to inspect the data (for debugging)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text[:200])  # Print first 200 characters to inspect data
        
        # Check if the content is a JSON response
        if response.headers['Content-Type'] == 'application/json':
            data = response.json()  # If it's a JSON response
            if not data:
                print(f"No certificate data found for query: '{query}'")
                return
            
            # Write the data to CSV
            with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "Domain Name", "Common Name", "Certificate Transparency Logs", "Not Before", "Not After"])
                
                for cert in data:
                    common_name = cert.get("common_name", "")  # Extract the common name
                    issuer_name = cert.get("issuer_name", "")
                    not_before = cert.get("not_before", "")
                    not_after = cert.get("not_after", "")
                    
                    # Write the extracted information to the CSV file
                    writer.writerow([cert.get("id", ""), cert.get("name_value", ""), common_name, issuer_name, not_before, not_after])
            print(f"Data saved to {output_filename}")
        else:
            print("Unexpected content type. The page may not have returned JSON.")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return

def main():
    # Input query and output filename from the user
    query = input("Enter the domain or organization name to search for certificates: ")
    output_filename = input("Enter the desired output filename (default 'certificates.csv'): ") or "certificates.csv"
    
    fetch_certificates(query, output_filename)

if __name__ == "__main__":
    main()
