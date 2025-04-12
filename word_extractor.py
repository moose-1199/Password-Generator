#!/usr/bin/env python3

import requests
import re
import click
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1) 

    return resp.content.decode()

def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        word = word.lower()
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1
    return word_count

def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)

def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

def generate_mutations(word):
    mutations = set()
    # Basic case mutations
    mutations.add(word.lower())
    mutations.add(word.upper())
    mutations.add(word.capitalize())
    
    # Common years and numbers
    years = [2023, 2024, 2025]
    numbers = ['123', '01', '1', '12']
    symbols = ['!', '@', '#', '$']
    
    base_words = [word.lower(), word.capitalize()]
    
    for base in base_words:
        # Add year variations
        for year in years:
            mutations.add(f"{base}{year}")
            mutations.add(f"{base}{year}!")
        
        # Add number variations
        for num in numbers:
            mutations.add(f"{base}{num}")
            
        # Add symbol variations
        for symbol in symbols:
            mutations.add(f"{base}{symbol}")
            mutations.add(f"{base}{symbol}{symbol}")
    
    return mutations

def is_valid_url(url, base_domain):
    # Check if URL is within the same domain scope
    try:
        parsed = urlparse(url)
        return parsed.netloc == base_domain
    except:
        return False

def get_urls_from(html, base_url):
    # Extract all URLs from HTML content
    soup = BeautifulSoup(html, 'html.parser')
    base_domain = urlparse(base_url).netloc
    urls = set()       
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            if is_valid_url(full_url, base_domain):
                urls.add(full_url)
    return urls

def crawl_and_extract(base_url, max_depth):
    # Crawl pages up to max_depth and collect words
    visited = set()
    to_visit = [(base_url, 0)]  # (url, depth)
    all_words = []
    base_domain = urlparse(base_url).netloc

    print(f"Starting crawl of {base_domain} with max depth {max_depth}")
    while to_visit:
        url, depth = to_visit.pop(0)
        
        if url in visited or depth > max_depth:
            continue
            
        try:
            print(f"Crawling {url} (depth {depth})")
            html = get_html_of(url)
            visited.add(url)
            
            # Extract words from current page
            soup = BeautifulSoup(html, 'html.parser')
            raw_text = soup.get_text()
            words = re.findall(r'\w+', raw_text)
            all_words.extend(words)
            print(f"Found {len(words)} words on page")
            
            if depth < max_depth:
                new_urls = get_urls_from(html, url)
                print(f"Found {len(new_urls)} new URLs to crawl")
                for new_url in new_urls:
                    if new_url not in visited:
                        to_visit.append((new_url, depth + 1))
                        
        except requests.RequestException as e:
            print(f"Network error crawling {url}: {e}")
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            
    return all_words

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract words from')
@click.option('--length', '-l', default=0, help='Minimum length of words to include')
@click.option('--depth', '-d', default=0, help='How many links deep to crawl the site')
@click.option('--limit', '-m', default=10, help='Maximum number of top words to process')
@click.option('--output', '-o', help='Output file for word list (prints to console if not specified)')
def main(url, length, depth, limit, output):
    
    the_words = crawl_and_extract(url, depth)
    top_words = get_top_words_from(the_words, length)
    
    word_count = min(limit, len(top_words))
    print(f"\nProcessing top {word_count} words...")

    if output:
        with open(output, 'w') as f:
            for i in range(word_count):
                word = top_words[i][0]
                f.write(f"{word}\n")
                mutations = generate_mutations(word)
                for mutation in mutations:
                    f.write(f"{mutation}\n")
                f.write("\n")
        print(f"Word list written to {output}")
    else:
        for i in range(word_count):
            word = top_words[i][0]
            print(f"\n{word}")
            for mutation in generate_mutations(word):
                print(mutation)

if __name__ == '__main__':
    main()