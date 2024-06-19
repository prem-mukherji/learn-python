import re
# import longResponses

def message_probability(user_message, recognized_words, single_response=False, required_words=[]):
    message_certainity = 0
    has_required_words = True
    for word in user_message:
        if word in recognized_words:
            message_certainity += 1
    
    percentage = float(message_certainity) / float(len(recognized_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0
    
def check_all_messages (message):
    highest_prob_list = {}

    def response (bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey'], single_response=True)
    response('I am doing fine, how about you?', ['how', 'are', 'you'], required_words=['how'])
    response('Weather seems to be fine, planning a picnic?', ['how', 'is', 'weather'], required_words=['weather'])
    response('sirius is an LLM tool', ['what', 'is', 'sirius', 'llm', 'genai'], required_words=['sirius', 'llm', 'genai'])
    response('sirius is an LLM tool', ['what', 'is', 'sirius', 'llm', 'genai'], required_words=['llm'])
    response('sirius is an LLM tool', ['what', 'is', 'sirius', 'llm', 'genai'], required_words=['genai'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    print(highest_prob_list)

    return best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


while True:
    print('Bot: ', get_response(input('You: ')))