import requests
import argparse

# Function to fetch results from Google Custom Search API
def google_search(api_key, cse_id, query, num_results=10):
    base_url = "https://www.googleapis.com/customsearch/v1"
    results = []
    start_index = 1  # Google API starts indexing at 1

    while len(results) < num_results:
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query,
            "start": start_index,
        }
        response = requests.get(base_url, params=params)

        # Check for HTTP errors
        if not response.ok:  # Equivalent to `response.status_code` >= 400
            print(f"HTTP Error {response.status_code}: {response.reason}")
            break

        data = response.json()

        # Handle API-specific errors
        if "error" in data:
            print(f"API Error: {data['error']['message']}")
            break

        # Parse and collect results
        items = data.get("items", [])
        for item in items:
            results.append(item.get("link"))

        # Update starting index for pagination
        start_index += 10
        if len(items) < 10:  # Stop if fewer results are returned
            break

    return results[:num_results]


# Main function for CLI
def main():
    parser = argparse.ArgumentParser(description="CLI tool to scrape domains using Google Dorking.")
    parser.add_argument("-q", "--query", required=True, help="Google Dork query")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of results to fetch (default: 10)")
    parser.add_argument("-o", "--output", help="Output file to save results (optional)")
    parser.add_argument("-k", "--api_key", required=True, help="Google API key")
    parser.add_argument("-c", "--cse_id", required=True, help="Google Custom Search Engine ID")
    args = parser.parse_args()

    # Validate API key and CSE ID
    if not args.api_key or not args.cse_id:
        print("Error: API key and CSE ID must be provided.")
        return

    # Perform search
    print(f"Searching for: {args.query}")
    results = google_search(args.api_key, args.cse_id, args.query, args.num)

    # Display results
    if results:
        print("\nResults:")
        for result in results:
            print(result)

        # Save to file if specified
        if args.output:
            with open(args.output, "w") as file:
                for result in results:
                    file.write(result + "\n")
            print(f"\nResults saved to {args.output}")
    else:
        print("No results found or an error occurred.")


if __name__ == "__main__":
    main()
