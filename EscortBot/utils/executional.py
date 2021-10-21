from customutils.models import EscortGirl


def get_escort_girls():  # id = 0
    return EscortGirl.select()
