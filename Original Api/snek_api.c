#include <string.h>
#include <time.h>
#include "snek_api.h"
#include <unistd.h>

int TIME_OUT = ((BOARD_SIZE * 4) - 4) * CYCLE_ALLOWANCE;

GameBoard* init_board(){
        GameBoard* gameBoard = (GameBoard*)(malloc(sizeof(GameBoard)));
        gameBoard-> CURR_FRAME = 0;
	gameBoard->SCORE = 0;
        gameBoard->MOOGLE_FLAG = 0;
        gameBoard-> MOOGLES_EATEN=0;
        for (int i = 0; i < BOARD_SIZE; i++){
                for (int j = 0; j < BOARD_SIZE; j++){
                        gameBoard->cell_value[i][j] = 0;
                        gameBoard->occupancy[i][j] = 0;
                }
        }
        gameBoard->occupancy[0][0] = 1; 
        gameBoard->snek = init_snek(0, 0);
        return gameBoard;
}

Snek* init_snek(int a, int b){
	Snek* snek = (Snek *)(malloc(sizeof(Snek)));

        snek->head = (SnekBlock *)malloc(sizeof(SnekBlock));
        snek->head->coord[x] = a;
        snek->head->coord[y] = b;

        snek->tail = (SnekBlock *)malloc(sizeof(SnekBlock));
        snek->tail->coord[x] = a;
        snek->tail->coord[y] = b;

        snek->tail->nextblock = NULL;
        snek->head->nextblock = snek->tail;

        snek->length = 1;

        return snek;
}

SnekBlock* init_block(int a, int b){
	SnekBlock* block = malloc(sizeof(SnekBlock));
	block->coord[x] = a;
	block->coord[y] = b;
	block->nextblock = NULL;
	return block;
}

int hits_edge(int axis, int direction, GameBoard* gameBoard){
	if (((axis == AXIS_Y) && ((direction == UP && gameBoard->snek->head->coord[y] + UP < 0) || (direction == DOWN && gameBoard->snek->head->coord[y] + DOWN > BOARD_SIZE - 1)))
           || (axis == AXIS_X && ((direction == LEFT && gameBoard->snek->head->coord[x] + LEFT < 0) || (direction == RIGHT && gameBoard->snek->head->coord[x] + RIGHT > BOARD_SIZE-1))))
        {
                return 1;
        } else {
                return 0;
	}
}

int hits_self(int axis, int direction, GameBoard *gameBoard){
	int new_x, new_y;
        if (axis == AXIS_X){
                new_x = gameBoard->snek->head->coord[x] + direction;
                new_y = gameBoard->snek->head->coord[y];
        } else if (axis == AXIS_Y){
                new_x = gameBoard->snek->head->coord[x];
                new_y = gameBoard->snek->head->coord[y] + direction;
        }
	return gameBoard->occupancy[new_y][new_x]; 
}

int time_out(GameBoard *gameBoard){
        return (gameBoard->MOOGLE_FLAG == 1 && gameBoard->CURR_FRAME > TIME_OUT);
}

int is_failure_state(int axis, int direction, GameBoard *gameBoard){
        return (hits_self(axis, direction, gameBoard) || hits_edge(axis, direction, gameBoard) || time_out(gameBoard));
}

void populate_moogles(GameBoard *gameBoard){
	if (gameBoard->MOOGLE_FLAG == 0){
                int r1 = rand() % BOARD_SIZE;
                int r2 = rand() % BOARD_SIZE;

                int r3 = rand() % (BOARD_SIZE * 10);
                if (r3 == 0){
                        gameBoard->cell_value[r1][r2] = MOOGLE_POINT * HARRY_MULTIPLIER;
                        gameBoard->MOOGLE_FLAG = 1;
                } else if (r3 < BOARD_SIZE){
                        gameBoard->cell_value[r1][r2] = MOOGLE_POINT;
                        gameBoard->MOOGLE_FLAG = 1;
                }
        }
}

void eat_moogle(GameBoard* gameBoard, int head_x, int head_y) {
        gameBoard->SCORE = gameBoard->SCORE + gameBoard->cell_value[head_y][head_x];
        gameBoard->cell_value[head_y][head_x] = 0;

        gameBoard->snek->length ++;
        gameBoard->MOOGLES_EATEN ++;
        gameBoard-> MOOGLE_FLAG = 0;
        gameBoard->CURR_FRAME = 0;
}

int advance_frame(int axis, int direction, GameBoard *gameBoard){
	if (is_failure_state(axis, direction, gameBoard)){
		return 0;
        } else {
                int head_x, head_y;
                if (axis == AXIS_X) {
                        head_x = gameBoard->snek->head->coord[x] + direction;
                        head_y = gameBoard->snek->head->coord[y];
                } else if (axis == AXIS_Y){
                        head_x = gameBoard->snek->head->coord[x];
                        head_y = gameBoard->snek->head->coord[y] + direction;
                }
                int tail_x = gameBoard->snek->tail->coord[x];
                int tail_y = gameBoard->snek->tail->coord[y];

                gameBoard->occupancy[head_y][head_x] = 1;
                if (gameBoard->snek->length > 1) { 
                        SnekBlock *newBlock = (SnekBlock *)malloc(sizeof(SnekBlock));
                        newBlock->coord[x] = gameBoard->snek->head->coord[x];
                        newBlock->coord[y] = gameBoard->snek->head->coord[y];
                        newBlock->nextblock = gameBoard->snek->head->nextblock;

                        gameBoard->snek->head->coord[x] = head_x;
                        gameBoard->snek->head->coord[y] = head_y;
                        gameBoard->snek->head->nextblock = newBlock;

                        if (gameBoard->cell_value[head_y][head_x] > 0){  
                                eat_moogle(gameBoard, head_x, head_y);
                        } else { 
                                gameBoard->occupancy[tail_y][tail_x] = 0;
                                SnekBlock *currBlock = gameBoard->snek->head;
                                while (currBlock->nextblock != gameBoard->snek->tail){
                                        currBlock = currBlock->nextblock;
                                } 

                                currBlock->nextblock = NULL;
                                free(gameBoard->snek->tail);
                                gameBoard->snek->tail = currBlock;
                        }

                } else if ((gameBoard->snek->length == 1) && gameBoard->cell_value[head_y][head_x] == 0){ // change both head and tail coords, head is tail
                        gameBoard->occupancy[tail_y][tail_x] = 0;
                        gameBoard->snek->head->coord[x] = head_x;
                        gameBoard->snek->head->coord[y] = head_y;
                        gameBoard->snek->tail->coord[x] = head_x;
                        gameBoard->snek->tail->coord[y] = head_y;

                } else { 
                        eat_moogle(gameBoard, head_x, head_y);
                        gameBoard->snek->head->coord[x] = head_x;
                        gameBoard->snek->head->coord[y] = head_y;
                }
                gameBoard->SCORE = gameBoard->SCORE + LIFE_SCORE;
                if (gameBoard->MOOGLE_FLAG == 1){
                        gameBoard->CURR_FRAME ++;
                }

                populate_moogles(gameBoard);
                return 1;
        }
}

void show_board(GameBoard* gameBoard) {
        fprintf(stdout, "\033[2J"); 
        fprintf(stdout, "\033[0;0H"); 

        char blank =    43;
        char snek =     83;
        char moogle =   88;

        for (int i = 0; i < BOARD_SIZE; i++){
                for (int j = 0; j < BOARD_SIZE; j++){
                        if (gameBoard->occupancy[i][j] == 1){
                                fprintf(stdout, "%c", snek);
                        } else if (gameBoard->cell_value[i][j] > 0) {
                                fprintf(stdout, "%c", moogle);
                        } else {
                                fprintf(stdout, "%c", blank);
                        }
                }
                fprintf(stdout, "\n");

        }

        fprintf(stdout, "\n\n");

        if (gameBoard->MOOGLE_FLAG == 1){
                fprintf(stdout, "!..ALERT, MOOGLE IN VICINITY..!\n\n");
        }
        fprintf(stdout, "SCORE: %d\n", gameBoard->SCORE);
        fprintf(stdout, "YOU HAVE EATEN %d MOOGLES\n\n", gameBoard->MOOGLES_EATEN);

        fprintf(stdout, "SNEK HEAD\t(%d, %d)\n", gameBoard->snek->head->coord[x], gameBoard->snek->head->coord[y]);
        fprintf(stdout, "SNEK TAIL\t(%d, %d)\n", gameBoard->snek->tail->coord[x], gameBoard->snek->tail->coord[y]);
        fprintf(stdout, "LENGTH \t%d\n", gameBoard->snek->length);
        fprintf(stdout, "CURR FRAME %d vs TIME OUT %d\n", gameBoard->CURR_FRAME, TIME_OUT);


        fflush(stdout);
}

int get_score(GameBoard *gameBoard) {
        return gameBoard->SCORE;
}

void end_game(GameBoard **board){
        fprintf(stdout, "\n\n\n--!!---GAME OVER---!!--\n\nYour score: %d\n\n\n\n", (*board)->SCORE);
        fflush(stdout);
        SnekBlock **snekHead = &((*board)->snek->head);
        SnekBlock *curr;
        SnekBlock *prev;
        while ((*snekHead)->nextblock != NULL) {
                curr = *snekHead;
                while (curr->nextblock != NULL){
                        prev = curr;
                        curr = curr->nextblock;
                }
                prev->nextblock = NULL;
                free(curr);
        }
        free(*snekHead);
        free((*board)->snek);
        free(*board);
}

void sleeep(){
	srand(time(NULL));
}
