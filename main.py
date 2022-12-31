from excel import runExcel

def interface():
    print("--------------------------------------")
    print("Method for converting Student IDs:")
    print("-> Enter 1 for an already-made OCR")
    print("-> Enter 2 for features + classifier")
    codesChoice = 0
    while True:
        codesChoice = input("Choice: ")
        if (codesChoice == "1" or codesChoice == "2"):
            break
        else:
            print("Error! You can only choose between 1 and 2. Please try again")
    print("--------------------------------------")
    print("Method for converting Numbers:")
    print("-> Enter 1 for an already-made OCR")
    print("-> Enter 2 for features + classifier")
    digitsChoice = 0
    while True:
        digitsChoice = input("Choice: ")
        if (digitsChoice == "1" or digitsChoice == "2"):
            break
        else:
            print("Error! You can only choose between 1 and 2. Please try again")
    print("--------------------------------------")
    return int(codesChoice), int(digitsChoice)

def run():
    codesChoice, numbersChoice = interface()
    print("Processing...")
    runExcel(codesChoice, numbersChoice)
    print("--------------------------------------")
    print("DONE! Output written to 'autoFiller.xls'")

if __name__ == "__main__":
    run()