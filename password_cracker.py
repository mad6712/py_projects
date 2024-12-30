import hashlib
import os
import itertools
import random

def generate_hash(plaintext,algorithm):
    if(algorithm=='md5'):
        hash=hashlib.md5(plaintext.encode()).hexdigest()
    elif(algorithm=='sha1'):
        hash=hashlib.sha1(plaintext.encode()).hexdigest()
    elif(algorithm=='sha256'):
        hash=hashlib.sha256(plaintext.encode()).hexdigest()
    return hash    

# Function to apply character substitutions
def mutate_word(word):
    substitutions = {'a': '@', 'o': '0', 'i': '1', 's': '$', 'e': '3'}
    variations = set([word])  # Original word

    # Apply substitutions
    for char, sub in substitutions.items():
        if char in word:
            variations.add(word.replace(char, sub))
            variations.add(word.replace(char, sub).upper())

    # Add case variations
    variations.add(word.lower())
    variations.add(word.upper())
    variations.add(word.capitalize())

    return variations

def generate_wordlist(base_words,add_rand_num):
    # Remove duplicates and empty values
    base_words = list(set(word.strip() for word in base_words if word.strip()))

    # Mutate words for variations
    mutated_words = set()
    for word in base_words:
        mutated_words.update(mutate_word(word))

    # Generate combinations of words
    wordlist = set(mutated_words)  # Start with mutated words
    for r in range(2, 4):  # Create combinations of 2 and 3 words
        for combo in itertools.permutations(mutated_words, r):
            wordlist.add("".join(combo))  # Combined directly
            wordlist.add("_".join(combo))  # Combined with underscore
            wordlist.add("-".join(combo))  # Combined with hyphen

    # Add random numbers if selected
    if add_rand_num.lower() == 'y':
        for word in list(wordlist):
            for _ in range(5):  # Add up to 5 random variations per word
                random_num = random.randint(100, 9999)
                wordlist.add(f"{word}{random_num}")
                wordlist.add(f"{random_num}{word}")

    return wordlist

def main():
    algorithm=input("enter algorithm(md5/sha1/sha256):").lower()
    if algorithm not in ['md5', 'sha1', 'sha256']:
        print("Invalid algorithm! Please choose 'md5', 'sha1', or 'sha256'.")
        exit()

    user_hash=input("enter input hash:").strip()
    hash_set={user_hash}

    choice=input("Do you want to create a custom generated wordlist? Enter y or n:")

    if(choice=='y'):
        first_name=input("enter first name:").strip()
        sur_name=input("enter surname:").strip()
        nick_name=input("enter nickname:").strip()
        birthdate=input("enter birthdate (DDMMYYYY):").strip()
        pet_name=input("enter pet's name:").strip()
        company_name=input("enter company name:").strip()
        other_keyword=input("enter other keywords seperated by comma:").strip().split(",")
        add_rand_num=input("do you want to add random numbers at the end of words (y/n):").strip()
        base_words = [first_name, sur_name, nick_name, birthdate, pet_name, company_name] + other_keyword
        custom_wordlist = generate_wordlist(base_words, add_rand_num)
    
        # Save to file
        wordlist_file = f"G:/Coding/projects/python/password_cracker/{first_name}_custom_passlist.txt"
        with open(wordlist_file, "w", encoding="utf-8") as f:
            f.write("\n".join(custom_wordlist))

        print(f"Custom wordlist created with {len(custom_wordlist)} entries and saved to '{first_name}_custom_passlist.txt'.")
        
        passwords=custom_wordlist   
        
    elif(choice=='n'):
        with open("G:/Coding/projects/python/password_cracker/common_passwords.txt","r",encoding='utf-8') as f:
            passwords=f.read().splitlines()

    found=False
    for password in passwords:
        pass_hash=generate_hash(password,algorithm)
        if pass_hash in hash_set:
            print("password is:",password," hash is:",pass_hash)
            found=True
            
    if (found==False):
        print("No matching password found.")       
        
if __name__=="__main__":
    main()