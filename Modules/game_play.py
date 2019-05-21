class Game:
    def game_progress(self):
        f = open("./Modules/story.txt", 'r')
        story = f.readlines()
        return story
