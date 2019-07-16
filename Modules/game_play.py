class Game:
    def game_progress(self):
        f = open("./Modules/story.txt", 'r')
        story = f.readlines()
        return story

    def game_ending(self, num):
        if num == 1:
            f = open("./Modules/ending1.txt", 'r')
            ending_1 = f.readlines()
            return ending_1

        elif num == 2:
            f = open("./Modules/ending2.txt", 'r')
            ending_2 = f.readlines()
            return ending_2