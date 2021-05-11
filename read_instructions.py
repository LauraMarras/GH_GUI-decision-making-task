def read_instructions(language):
    with open ('{} instructions.txt'.format(language), 'rt', encoding='UTF-8') as instructions_file:
        instructions_text = instructions_file.read()
        lines = instructions_text.split('\n')             
        instructions = {1: '', 2: '', 3: ''}
       
        for line in lines:
            instructions[int(line[0])] += line[1:] + '\n'

    return instructions

instructions = read_instructions('DUTCH')
    