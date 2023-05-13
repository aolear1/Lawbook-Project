import pygame as pg
import random as r
import time as t


class Wordlist():
    def __init__(self, file_name):
        self.list = []
        self.dict = {}
        self.file = open(file_name, "r", encoding="utf-8")
        for x in self.file:
            a = x.index(":")
            self.list.append(x[:a])
            self.dict.update({str(x[:a]): str(x[a + 1:]).replace("\n", "")})
        r.shuffle(self.list)
        self.word = ""
        self.hidden = ""
        self.definition = ""
        self.offset = 0
        self.font = 0

    def randomize_word(self):
        r.shuffle(self.list)
        self.word = self.list[0]
        self.hidden = ""

        for i in range(len(self.word)):
            if self.word[i] == " ":
                self.hidden += " "
            else:
                self.hidden += "_ "

        self.definition = self.dict[self.word]

    def check_text(self, input):

        if self.word.lower().replace(" ","") == input.lower().replace(" ",""):
            return True
        else:
            return False

    def update_font(self):
        if len(self.definition)<27:
            self.font = 50

        elif 27<len(self.definition)<35:
            self.font = 35

        else:
            self.font = 20

    def mrd(self,character):
        if character.score == 54:
            self.word = "Mr D"
            self.definition = 'The coolest teacher'
            self.hidden = "_ _   _"
        else:
            pass


class Screen():

    def __init__(self):
        self.screen = pg.display.set_mode((700, 370))
        self.screen.fill((10, 10, 10))
        self.color = 'black'

    def blittext(self, word, y, font):
        font = pg.font.Font(None, font)
        text3 = font.render(word, True, self.color)
        text_rect = text3.get_rect(center=(700 / 2, 370 / 2))
        self.screen.blit(text3, (text_rect[0],y))

    def blitletters(self,word,x,y,font):
        font = pg.font.Font(None, font)
        text3 = font.render(word, True, self.color)
        self.screen.blit(text3, (x, y))

    def background(self,image_file):
        background = pg.image.load(image_file)
        self.screen.blit(background,(-34.5,0))

    def blit(self,image,pos):
        self.screen.blit(image,pos)





class Character():

    def __init__(self, list):
        self.lives = 3
        self.score = 0
        self.hearts = []

        for i in list:

            picture = pg.image.load(i).convert_alpha()
            self.hearts.append(pg.transform.scale(picture, (100, 110)))

    def givelife(self,Background):
        for x in range(self.lives):
            for i in self.hearts:
                image = i
                Background.blit(image, (570, 10 + 110 * x))
                pg.display.flip()
                t.sleep(.08)


    def isalive(self):
        if self.lives > 0:
            return True
        else:
            return False

    def print_lives(self, Background):

        for x in range(self.lives):
            image = self.hearts[-1]
            Background.blit(image, (570, 10 + 110 * x))


    def loselife(self):
        self.lives = self.lives-1

    def scoreup(self):
        self.score +=1

    def restart(self):
        self.score = 0
        self.lives = 3



def main():

    heart_pics = [
        #"C:/Users/aiden/Downloads/frame_00_delay-0.png",
        "heart images/frame_01_delay-0.png",
        "heart images/frame_02_delay-0.png",
        "heart images/frame_03_delay-0.png",
        "heart images/frame_04_delay-0.png",
        "heart images/frame_05_delay-0.png",
        "heart images/frame_06_delay-0.png",
        "heart images/frame_07_delay-0.png",
        "heart images/frame_08_delay-0.png",
        "heart images/frame_09_delay-0.png",
        "heart images/frame_10_delay-0.png",
        "heart images/frame_11_delay-0.png",
        "heart images/frame_12_delay-0.png"
    ]

    screen = Screen()

    GAMEOVER = False

    character = Character(heart_pics)



    clock = pg.time.Clock()

    wordlist = Wordlist("Law Dictionairy.txt")
    wordlist.randomize_word()
    wordlist.update_font()
    x = 0
    text = ""


    while True:

        if x == 0:
            screen.screen.fill((10, 10, 10))
            screen.background("lawroom.png")
            character.givelife(screen)
            x = 1

        if x == 1:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if wordlist.check_text(text) == True:
                            wordlist.randomize_word()
                            wordlist.mrd(character)
                            wordlist.update_font()
                            character.scoreup()
                            text = ""
                        else:
                            text = ""
                            character.loselife()
                            if character.isalive() == False:
                                x = -2
                            else:
                                x = -1
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-2]

                    else:
                        text += event.unicode
                        text += " "



            screen.screen.fill((10, 10, 10))
            screen.background("lawroom.png")
            character.print_lives(screen)

            screen.blittext("Score: "+str(character.score),10, 45)

            screen.blittext(text, 305, 45)

            screen.blittext(wordlist.hidden, 310, 44)
            screen.blittext(wordlist.definition, 80, wordlist.font)

            pg.display.flip()


        elif x == -1 or x ==-2:

            if GAMEOVER == False:

                for photo in character.hearts:
                    t.sleep(.1)
                    position = character.hearts.index(photo)
                    screen.screen.fill((10, 10, 10))
                    screen.background("lawroom.png")

                    screen.blittext("You Lost A Life!", 30, 60)
                    screen.blittext(f"{wordlist.word}:{wordlist.definition}",90,15)
                    character.print_lives(screen)

                    screen.blit(character.hearts[-position-1],(570, 10 + 110 * character.lives+1))

                    pg.display.flip()


                t.sleep(1)
                wordlist.randomize_word()
                wordlist.mrd(character)
                wordlist.update_font()

                if x == -1:
                    x = 1

                else:
                    GAMEOVER = True



            elif GAMEOVER == True:

                screen.screen.fill((10, 10, 10))
                screen.background("lawroom.png")

                screen.blittext("GUILTY!", 30, 80)
                screen.blittext("Click r for a retrial or q to accept your sentance",90,30)

                pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                            character.restart()
                            x = 0
                        elif event.key == pg.K_q:
                            return

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()