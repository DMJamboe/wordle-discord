def genFileOfLength(length: int):
    validwords = set()
    with open("popular.txt", "r+") as f:
        words = f.readlines()
        for word in words:
            word = word.strip()
            if len(word) == length:
                validwords.add(word.lower() + "\n")
    
    with open("words-five.txt", "w+") as f:
        f.writelines(validwords)

genFileOfLength(5)