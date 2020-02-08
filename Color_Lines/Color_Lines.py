# --------------------------------------------------------------
# Name:  Hao Xuan(1537913), Rain Wu(1586852).
# CMPUT 274,Fall 2018
# Final project : Color Lines
# --------------------------------------------------------------
import pygame
import math
import copy
import time
import random
from pygame.time import Clock
from pygame.event import get as get_events
from pygame import QUIT, Color, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from pygame.draw import circle as draw_circle

pygame.init()
# *************************************************************
# https://blog.csdn.net/jetmie/article/details/79252743
# We searched the method of check the voild point from internet.
# These two functions are used for check the route whether a ball can be moved
# to another position, if the way from one position to another postion are
# blocked, return False, otherwise return True.


def check_valid(mg, x, y):
    if x >= 0 and x < len(mg) and y >= 0 and y < len(mg[0]) and mg[x][y] == 1:
        return True
    else:
        return False


def process(step):
    # Checking the next point that cannot reach.
    change_records = []
    for i in range(len(step) - 1):
        if (abs(step[i][0] - step[i + 1][0]) == 0 and 
            abs(step[i][1] - step[i + 1][1]) == 1) or \
                        (abs(step[i][0] - step[i + 1][0]) == 1 
                        and abs(step[i][1] - step[i + 1][1]) == 0):
            pass
        else:
            change_records.append(i + 1)
    # print(change_records)
    # According to these points to find the farthest retreat point.
    clip_nums = []
    for i in change_records:
        for j in range(i):
            if (abs(step[j][0] - step[i][0]) == 0 and 
                abs(step[j][1] - step[i][1]) == 1) or \
                        (abs(step[j][0] - step[i][0]) == 1 and 
                        abs(step[j][1] - step[i][1]) == 0):
                break
        clip_nums.append((j, i))
    # print(clip_nums)
    # Reverse processing to prevent the mark move to below.
    record = []
    for i in clip_nums[::-1]:
        if not (i[0] in record or i[1] in record):
            step = step[:i[0] + 1] + step[i[1]:]
        record += list(range(i[0], i[1]))


step = []


def walk(mp, x, y, a, b):
    global step
    if x == a and y == b:
        step.append((x, y))
        process(step)
        return 1
    if check_valid(mp, x, y):
        step.append((x, y))
        mp[x][y] = 2
        switch = walk(mp, x, y + 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x, y - 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x - 1, y, a, b) 
        if switch == 1:
            return 1
        switch = walk(mp, x + 1, y, a, b)
        if switch == 1:
            return 1
# ***********************************************************
# The below 4 functions are used for check whether 5 or more same color balls
# connect in one line. we have a 9*9 map for our game, we use matrix to
# represent each point. The return of each function is a list with the balls'
# position if there are 5 or more same color balls connect in one line, if
# there are no more than 5 or more same color balls connect in one line, return
# an empty list.


def rowcheck(matrix):
    # rowcheck() is used for check all the rows of our game map, there are two
    # for loops to test, the secend for loop is in the first for loop. The
    # first for loop is used for determining the beginning point that we start
    # to check. The second for loop is used for check the balls. All the below
    # 4 funtions are using this method (the difference is how to determine the
    # begginng point that we start to check.
    newcolumnlist = []
    # The first for loop, used for stating the beginning point. We have a 9*9
    # matrix, which means we have 9 rows, so the first for loop will run 9
    # times.
    for row in range(9):
        column = 0
        rowcount = 0
        columncount = 0
        columnlist = []
        zu = (row, column)
        columnlist.append(zu)
        # Appending the first point of the row in columnlist, this step is uesd
        # make sure the first point of the row will be appending to the
        # columnlist when the five or more same color balls include the first
        # point.
        for i in range(8):
            # There are 9 columns in our matrix, so the second for loop will
            # run 9 times (because we just need to compare two points for 8
            # times.
            if matrix[row][column] == matrix[row][column + 1]:
                rowcount += 1
                zu = (row, column + 1)
                columnlist.append(zu)
            # If the left point equal to right point, append the right point
            # into columnlist. zu represent the right point. rowcount plus 1.
            if matrix[row][column] != matrix[row][column + 1] and rowcount < 4:
                rowcount = 0
                columnlist = []
                zu = (row, column + 1)
                columnlist.append(zu)
            # If the left point not equal to the right point and rowcount not
            # bigger than 4, which means there are not 5 balls connect in one
            # line, then flushing the columnlist to rewrite the columnlist.
            if matrix[row][column] != matrix[row][column + 1] and rowcount >= 4:
                break
            # If the left point not equal to the right point and rowcount
            # bigger than 4, which means we have at least 5 same color blls in
            # one line, then break the second for loop. (because it is not
            # possible to have another five same balls in one line)
            column += 1
        if rowcount >= 4:
            for i in columnlist:
                newcolumnlist.append(i)
        # Appending this line's columnlist in newcolumnlist(total list)
        row += 1
    return(newcolumnlist)
    # Returing the newcolumnlist which has all the balls' position if there are
    # 5 or more balls connect in one line on a row.


def columncheck(matrix):
    # columncheck() using same way of rowcheck().
    newrowlist = []
    for column in range(9):
        row = 0
        columncount = 0
        rowlist = []
        zu = (row, column)
        rowlist.append(zu)
        # In the second for loop, the value of row will increase 1 each time,
        # to check the same column.
        for i in range(8):
            # Comparing the above point to under point.
            # row plus 1 to achieve this goal.
            if matrix[row][column] == matrix[row + 1][column]:
                columncount += 1
                zu = (row+1, column)
                rowlist.append(zu)
            elif matrix[row][column] != matrix[row + 1][column] and columncount < 4:
                columncount = 0
                rowlist = []
                zu = (row + 1, column)
                rowlist.append(zu)
            elif matrix[row][column] != matrix[row + 1][column] and columncount >= 4:
                break
            row += 1
        if columncount >= 4:
            for i in rowlist:
                newrowlist.append(i)
        column += 1
    return(newrowlist)
    # Returning all the balls' position that 5 or more than 5 same color balls
    # connect in columns.


def left_sloping(matrix):
    # Left_sloping(matrix) is used for checking the left diagnoals(from left
    # top to right bottom), because this is a 9*9 map, so we do not need to
    # check 4 left bottom and 4 right top diagnoals.
    column = 0
    newleftslop = []
    # Step 1.
    # The first for loop is still used to determine the beginning point that
    # we start to check. This for loop also determine the times that second
    # for loop run. checking from left top row ((0,0),(0,1),(0,2),(0,3),(0,4)).
    for column in range(5):
        row = 0
        count = 0
        leftslop = []
        a = 0
        zu = ()
        if row == 0 and column == 0:
            a = 9
            zu = (0, 0)
        elif row == 0 and column == 1:
            a = 8
            zu = (0, 1)
        elif row == 0 and column == 2:
            a = 7
            zu = (0, 2)
        elif row == 0 and column == 3:
            a = 6
            zu = (0, 3)
        elif row == 0 and column == 4:
            a = 5
            zu = (0, 4)
        leftslop.append(zu)
        # According to the first for loop, we get the beginning point and first
        # ball's position.
        for i in range(a - 1):
            # Comparing left top point to the right bottom point.
            # row and column plus one seprately each time to achieve this goal.
                if matrix[row][column] == matrix[row + 1][column + 1]:
                    count += 1
                    zu = (row+1, column+1)
                    leftslop.append(zu)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                    count = 0
                    leftslop = []
                    zu = (row + 1, column + 1)
                    leftslop.append(zu)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                    break
                row += 1
                column += 1
        if count >= 4:
            for i in leftslop:
                    newleftslop.append(i)
        column += 1
    column = 0
    row = 1
    a = 0
    leftslop = []
    # step 2.
    # Checking from the left top column ((1,0)(2,0)(3,0)(4,0))
    # same as first for loop.
    for row in range(5):
        column = 0
        count = 0
        leftslop = []
        a = 0
        if row == 1 and column == 0:
            a = 8
            zu = (1, 0)
        elif row == 2 and column == 0:
            a = 7
            zu = (2, 0)
        elif row == 3 and column == 0:
            a = 6
            zu = (3, 0)
        elif row == 4 and column == 0:
            a = 5
            zu = (4, 0)
        leftslop.append(zu)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column + 1]:
                count += 1
                zu = (row + 1, column + 1)
                leftslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                count = 0
                leftslop = []
                zu = (row + 1, column + 1)
                leftslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                break
            row += 1
            column += 1
        if count >= 4:
            for i in leftslop:
                newleftslop.append(i)
        row += 1
    return(newleftslop)


def right_sloping(matrix):
    # right_sloping() is similar as left_sloping, this function will check all
    # the right diagonals (right top to left column).
    column = 8
    newrightslop = []
    columnlist = [8, 7, 6, 5, 4]
    for g in columnlist:
        # step 1.
        # Statement the beginning point to check.
        # Determining the times that we need to run in second loop.
        # checking from left top row ((0,8),(0,7),(0,6),(0,5),(0,4))
        row = 0
        count = 0
        rightslop = []
        a = 0
        zu = ()
        if row == 0 and g == 8:
            a = 9
            zu = (0, 8)
        elif row == 0 and g == 7:
            a = 8
            zu = (0, 7)
        elif row == 0 and g == 6:
            a = 7
            zu = (0, 6)
        elif row == 0 and g == 5:
            a = 6
            zu = (0, 5)
        elif row == 0 and g == 4:
            a = 5
            zu = (0, 4)
        rightslop.append(zu)
        column = g
        for i in range(a - 1):
            # Comparing right top point to the left bottom point.
            # row plus one and column minus one each time to achieve this goal.
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        column -= 1
    column = 8
    row = 1
    a = 0
    rightslop = []
    for row in range(5):
        # step 2.
        # checking from left top column ((1, 8),(2, 8),(3, 8),(4, 8)).
        column = 8
        count = 0
        rightslop = []
        a = 0
        if row == 1 and column == 8:
            a = 8
            zu = (1, 8)
        elif row == 2 and column == 8:
            a = 7
            zu = (2, 8)
        elif row == 3 and column == 8:
            a = 6
            zu = (3, 8)
        elif row == 4 and column == 8:
            a = 5
            zu = (4, 8)
        rightslop.append(zu)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                zu = (row+1, column-1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                zu = (row + 1, column - 1)
                rightslop.append(zu)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        row += 1
    return(newrightslop)
# After these four functions(rowcheck(), columncheck(), left_sloping() and
# right_sloping) we will return all the balls' positions if there are 5 or more
# than 5 balls connect in one line.


class Game:
    def __init__(self):
        # set for screen size
        self._height_ = 400
        self._width_ = 500
        # create window
        self._window_ = pygame.display.set_mode((self._width_, self._height_))
        self.create_window()
        # set up two matrix to represent ball position and each ball's color
        # for ballmap, 1 means empty and 0 means it contains a ball
        self._ballmap_ = [[1 for i in range(9)] for j in range(9)]
        self._colormap_ = [[[] for i in range(9)] for j in range(9)]
        # set for window close condition
        self._close_ = False
        # create clock to control frame rate
        self._clock_ = pygame.time.Clock()
        self._color_ = ['yellow', 'green', 'red', 'purple', 'brown', 'orange']
        # save for mouse position
        self._mouse_pos_ = [0, 0]
        # mouse condition, equals to one means a ball is selected
        self._mouse_cond_ = 0
        # save for the ball position before moving a ball
        self._last_ball_ = [0, 0]
        # record game score
        self._score_ = 0

    def create_window(self):
        # create_window() function set up the window including drawing the grid
        # and set the caption when the game started
        pygame.display.set_caption("game")
        # draw the basic grid for the gameplay
        self.draw_grid()
        pygame.display.flip()

    def play_game(self):
        # play_game() provide the basic loop for the game including all the
        # figures of the game
        # generate 3 random balls when the game started
        self.generate_ball()
        # update screen
        pygame.display.flip()
        # set for close window action
        # the condition for exiting loop is when the window is closed
        while not self._close_:
            # set for FPS
            self._clock_.tick(30)
            # deal with all kinds of user actions
            self.events()
            # check for end game condition
            if self.end_game():
                # clear the screen and print 'Game over' in the screen
                self._window_.fill((0, 0, 0))
                self.message_display("Game over", self._width_/2, self._height_/2, 50)
                time.sleep(2)
                break

    def events(self):
        # function events() contains a loop to detect all kinds of user action
        # and make reaction
        event_list = get_events()
        for event in event_list:
            self.single_event(event)

    def single_event(self, event):
        # single_event() handles every single event
        # for this program, we only need to consider two events
        # ---
        # QUIT means user close the window
        if event.type == QUIT:
            # set the _close_ to True, so it will break the main loop
            self._close_ = True
        # MOUSEBUTTONUP is returned when any mouse button goes up
        # in most cases this means a mouse click
        elif event.type == MOUSEBUTTONUP:
            # when detect a mouse click, record the mouse position
            self._mouse_pos_[0], self._mouse_pos_[1] = event.pos
            # do the move ball part
            self.move_ball()
            # check if there are 5 balls in line
            self.check_ball()

    def draw_grid(self):
        # draw_grid() is used to draw the basic grid for the game
        height = self._height_
        width = self._width_
        # calculate the size for each grid
        grid_h = height/11
        # set a list contains 4 pairs of coordinates of the outer 4 frames
        lines = [((grid_h, grid_h), (grid_h, height-grid_h)),
                 ((grid_h, grid_h), (height-grid_h, grid_h)),
                 ((grid_h, height-grid_h), (height-grid_h, height-grid_h)),
                 ((height-grid_h, grid_h), (height-grid_h, height-grid_h))]
        color = Color('white')
        # draw outer frames
        for i in lines:
            pygame.draw.line(self._window_, color, i[0], i[1], 2)
        # draw all the inner grids
        for i in range(8):
            pygame.draw.line(self._window_, color, 
                (grid_h*(i+2), grid_h), (grid_h*(i+2), height-grid_h))
            pygame.draw.line(self._window_, color, 
                (grid_h, grid_h*(i+2)), (height-grid_h, grid_h*(i+2)))

    def generate_ball(self):
        # generate_ball() generates 3 balls with random location and random
        # chosen colors in empty spaces
        # create an array to represent the blocks left empty
        array = [i for i in range(81)]
        for i in range(9):
            for j in range(9):
                # remove all the grids with balls already in them
                if self._ballmap_[i][j] == 0:
                    array.remove(i * 9 + j)
        random_ball = [0, 0, 0]
        # choose 3 random empty grids to generate balls
        for i in range(3):
            random_ball[i] = random.choice(array)
            # remove the chosen grid from the array and turn it to 0 in the
            # ballmap
            array.remove(random_ball[i])
            self._ballmap_[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = 0
        # choose 3 colors from the color list
        for i in range(3):
            c = random.choice(self._color_)
            self._colormap_[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = c
        # draw the new balls
        self.draw_ball()

    def draw_ball(self):
        # the function draw_ball is used for drawing all the balls according to
        # ballmap and with the corresponding color in colormap
        # clear the screen
        self._window_.fill((0, 0, 0))
        # draw the grid
        self.draw_grid()
        # calculate the size of each grid
        grid_h = self._height_/11
        for i in range(9):
            for j in range(9):
                # if ballmap[i][j]==0, it means there is a ball here,
                # draw it in this position
                if self._ballmap_[i][j] == 0:
                    draw_circle(self._window_, Color(self._colormap_[i][j]),
                                    (int((i+1.5) * grid_h), int((j+1.5) * grid_h)),
                                    int(grid_h/5 * 2))
        # draw score
        string = "Score: "+str(self._score_)
        width = self._height_ + (self._width_-self._height_) / 3
        self.message_display(string, width, grid_h, 25)
        # update the screen
        pygame.display.flip()

    def move_ball(self):
        # move_ball() function is able to move a ball to another position if
        # it's able to reach there with user mouse action(click)

        grid_h = self._height_ / 11
        # calculate for the mouse x and y position with respect to top left
        # corner of the grid
        x_pos = self._mouse_pos_[0] - grid_h
        y_pos = self._mouse_pos_[1] - grid_h
        # calculate the specific mouse position corresponding to 9*9
        # grid(matrix)
        mou_pos = [int(x_pos / grid_h), int(y_pos / grid_h)]
        # if mouse click outside the grid, no action would be taken
        if mou_pos[0] > 8 or mou_pos[1] > 8:
            return
        # if ballmap==0, it means mouse has click on to a ball,
        # change the mouse condition to 1(ball selected) and get that position
        if self._ballmap_[mou_pos[0]][mou_pos[1]] == 0:
            self._mouse_cond_ = 1
            self._last_ball_ = mou_pos
        # if ballmap==1, it means mouse clicks an empty block
        elif self._ballmap_[mou_pos[0]][mou_pos[1]] == 1:
            # check for the mouse condition to see whether it is in selected
            # mode if it is, go to move ball procedure
            if self._mouse_cond_ == 1:
                # make a copy of ballmap to make sure ballmap remain unchanged
                # in moving procedure
                m = copy.deepcopy(self._ballmap_)
                m[self._last_ball_[0]][self._last_ball_[1]] = 1
                # perform walk() to check whether a ball can be moved to the
                # position (no ball blocking the way)
                s = walk(m, self._last_ball_[0], self._last_ball_[1], 
                    mou_pos[0], mou_pos[1])
                if(s != 1):
                    # if the position can't be reached, finish moving ball
                    return
                # set the position after move to be 0 in ballmap because it
                # contains a ball
                self._ballmap_[mou_pos[0]][mou_pos[1]] = 0
                # set the position before move to be 1 because it's empty now
                self._ballmap_[self._last_ball_[0]][self._last_ball_[1]] = 1
                # make the color change
                self._colormap_[mou_pos[0]][mou_pos[1]] = self._colormap_[self._last_ball_[0]][self._last_ball_[1]]
                # remove the original color
                self._colormap_[self._last_ball_[0]][self._last_ball_[1]] = []
                # set the mouse condition back to 0 after move
                self._mouse_cond_ = 0
                # draw the new ballmap
                self.draw_ball()
                # wait 0.2 second and then check for 5 balls in line
                # take a pause before eliminate the ball will allow user to
                # see balls clearer
                time.sleep(0.2)
                if self.check_ball():
                    # if there is no ball removed, generate 3 random balls
                    time.sleep(0.2)
                    self.generate_ball()
            else:
                pass

    def check_ball(self):
        # this function is used to check whether there are 5 balls in line by
        # using columncheck(), rowcheck(), left_sloping(),right_sloping()
        s = 0
        # check columns
        c = columncheck(self._colormap_)
        # we only need to check for the colormap to see whether there are 5
        # same color in line, even though we could detect [](empty space), it's
        # ok since the elimination process is just ballmap[i][j]=1, if it's
        # already 1, there will be no effect on it
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        # check rows
        c = rowcheck(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        # check diagonals(left slope, right slope)
        c = left_sloping(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        c = right_sloping(self._colormap_)
        for i in c:
            if(self._ballmap_[i[0]][i[1]] == 0):
                s = 1
                self._score_ += 2
            self._ballmap_[i[0]][i[1]] = 1
        self.draw_ball()
        if s == 0:
            return True

    def end_game(self):
        # end_game() function checks for game over condition: less than 3 empty
        # gridss
        s = 0
        for i in range(9):
            for j in range(9):
                if self._ballmap_[i][j] == 1:
                    s += 1
        if s > 3:
            return False
        else:
            return True
# **************************************************************************
# https://blog.csdn.net/pianzang5201/article/details/78303954

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def message_display(self, text, width, height, size):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((width), (height))
        self._window_.blit(TextSurf, TextRect)
        pygame.display.update()
# **************************************************************************


def main():
    game = Game()
    game.play_game()
    pygame.display.quit()
main()
