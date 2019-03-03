import lm
import corpus


def init(n):
    return lm.LanguageModel(n)


def generate():
    file_name = input("Please enter a training set's filename:")
    file = open(file_name)
    n = int(input("Please input a n-grams value 'n':"))
    model = init(n)
    sequences = []
    for line in file:
        tokens = corpus.tokenize(line)
        sequences.append(tokens)
        
    '''
    train_result = lm.train(sequences)
    print(lm.train(sequences))
    '''
    model.train(sequences)
    # print(model.counts)
    new_text_list = model.generate()
    # print(lm.generate())
    new_text = corpus.detokenize(new_text_list)
    return new_text


def generate_save():
    new_text = ''
    filename = input('Please input a filename:')
    number = int(input('Please input number of desire text:'))

    file_name = input("Please enter a training set's filename:")
    file = open(file_name)
    n = int(input("Please input a n-grams value 'n':"))
    model = init(n)
    sequences = []
    for line in file:
        tokens = (corpus.tokenize(line))
        sequences.append(tokens)
    model.train(sequences)

    for i in range(0, number):
        new_text_list = model.generate()
        new_text += corpus.detokenize(new_text_list)+'\n'
        
    file = open(filename, 'w')
    file.write(new_text)

    file.close()

    
print("This is a program which allow you to create a n-gram language model.\n"
      "What would you like to do with this program? Enter the number of functions you want.")
select = int(input("Test the function = 1\nGenerate and store the new text = 2\nexit = 3\nEnter:"))

if select == 1:
    print(generate())
    print("What would you like to do next?")
    next = int(input("Test again = 1\nGenerate and store a new text = 2\nExit = 3\nEnter:"))
    if next == 1:
        print(generate())
    elif next == 2:
        print(generate_save())
    elif next == 3:
        exit()
elif select == 2:
    generate_save()
    print("What would you like to do next?")
    next = int(input("Generate and store a new text = 1\nExit = 2\nEnter:"))
    if next == 1:
        print(generate_save())
    elif next == 2:
        exit()
elif select == 3:
    exit()

