conversation_summary = ""


def get_summary():

    global conversation_summary

    return conversation_summary


def update_summary(new_summary):

    global conversation_summary

    conversation_summary = new_summary