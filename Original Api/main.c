#include "snek_api.h"
#include <unistd.h>
#include "comp_moves.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

void computer_play(int moves[][2], int length){
   	 printf("starting\n");
        //board initialized, struct has pointer to snek
        GameBoard* board = init_board();
        show_board(board);

        int axis = AXIS_INIT;
        int direction = DIR_INIT;

        int play_on = 1;
        int coord[2];

        for (int i = 0; i < length && play_on; i++){
            play_on = advance_frame(moves[i][0], moves[i][1], board);
            show_board(board);
	    usleep (555550);
        }
	end_game(&board);
}

void computer_play2(Comp_moves *moves){
        GameBoard* board = init_board();
        show_board(board);

        int axis = AXIS_INIT;
        int direction = DIR_INIT;

        int play_on = 1;
        int coord[2];

        Comp_move *temp = moves->top;
        for (int i = 0; i <= moves->num_moves && play_on; i++){
	    show_board(board);
            printf("attempting to go in axis %d in direction %d\n", temp->axis, temp->direction);
	    if (hits_edge(temp->axis, temp->direction, board)) printf("huh");
	    if (hits_self(temp->axis, temp->direction, board)) printf("huhhhh"); 
	    play_on = advance_frame(temp->axis, temp->direction, board);
            if (temp->next_move) temp = temp->next_move;
            usleep(555550);
        }
	end_game(&board);
}

void play_game() {
        printf("starting\n");
        GameBoard* board = init_board();
        show_board(board);

        int axis = AXIS_INIT;
        int direction = DIR_INIT;

        int play_on = 1;
        int coord[2];

        while (play_on){
                coord[x] = board->snek->head->coord[x];
                coord[y] = board->snek->head->coord[y];
                unsigned short go_x = (axis == AXIS_Y && direction == 1 && coord[y] == (BOARD_SIZE - 1)) || (axis == AXIS_Y && direction == -1 && coord[y] == 0);
                unsigned short go_y = (axis == AXIS_X && direction == 1 && coord[x] == (BOARD_SIZE - 1)) || (axis == AXIS_X && direction == -1 && coord[x] == 0);
                if (go_x) {
                        axis = AXIS_X;
                        if (coord[x] < (int)(BOARD_SIZE / 2)){
                                direction = RIGHT;
                        } else {
                                direction = LEFT;
                        }
                } else if (go_y) {
                        axis =  AXIS_Y;
                        if (coord[y] < (int)(BOARD_SIZE / 2)){
                                direction = DOWN;
                        } else {
                                direction = UP;
                        }
                }
                show_board(board);
                play_on = advance_frame(axis, direction, board);
                printf("Going ");

                if (axis == AXIS_X){
                        if (direction == RIGHT){
                                printf("RIGHT");
                        } else {
                                printf("LEFT");
                        }
                } else {
                        if (direction == UP){
                                printf("UP");
                        } else {
                                printf("DOWN");
                        }
                } printf("\n");
                usleep(555550);
        }
        end_game(&board);

}

int main(){
	play_game();
	return(0);
}


