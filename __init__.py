from mycroft import MycroftSkill, intent_file_handler


class SpaceIsAwesome(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('awesome.is.space.intent')
    def handle_awesome_is_space(self, message):
        self.speak_dialog('awesome.is.space')


def create_skill():
    return SpaceIsAwesome()

