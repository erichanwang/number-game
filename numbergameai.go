package main

import (
	"container/heap"
	"fmt"
)

type State struct {
	board   [][]int
	emptyX  int
	emptyY  int
	moves   []string
	g       int
	h       int
}

type PriorityQueue []*State

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].g+pq[i].h < pq[j].g+pq[j].h
}
func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}
func (pq *PriorityQueue) Push(x interface{}) {
	*pq = append(*pq, x.(*State))
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	x := old[n-1]
	*pq = old[0 : n-1]
	return x
}

var target = [3][3]int{
	{0, 1, 2},
	{3, 4, 5},
	{6, 7, 8},
}

func heuristic(board [][]int) int {
	h := 0
	for i := range board {
		for j := range board[i] {
			if board[i][j] != 0 {
				x, y := (board[i][j]-1)/3, (board[i][j]-1)%3
				h += abs(x-i) + abs(y-j)
			}
		}
	}
	return h
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func isSolved(board [][]int) bool {
	for i := range board {
		for j := range board[i] {
			if board[i][j] != target[i][j] {
				return false
			}
		}
	}
	return true
}

func getNeighbors(emptyX, emptyY int) [][2]int {
	return [][2]int{
		{emptyX - 1, emptyY}, // up
		{emptyX + 1, emptyY}, // down
		{emptyX, emptyY - 1}, // left
		{emptyX, emptyY + 1}, // right
	}
}

func moveTile(board [][]int, x1, y1, x2, y2 int) [][]int {
	newBoard := make([][]int, len(board))
	for i := range board {
		newBoard[i] = make([]int, len(board[i]))
		copy(newBoard[i], board[i])
	}
	newBoard[x1][y1], newBoard[x2][y2] = newBoard[x2][y2], newBoard[x1][y1]
	return newBoard
}

func main() {
	var k int
	fmt.Scan(&k)

	board := make([][]int, k)
	emptyX, emptyY := -1, -1
	for i := 0; i < k; i++ {
		board[i] = make([]int, k)
		for j := 0; j < k; j++ {
			fmt.Scan(&board[i][j])
			if board[i][j] == 0 {
				emptyX, emptyY = i, j
			}
		}
	}

	pq := &PriorityQueue{}
	initialState := &State{
		board:  board,
		emptyX: emptyX,
		emptyY: emptyY,
		moves:  []string{},
		g:      0,
		h:      heuristic(board),
	}
	heap.Push(pq, initialState)

	visited := make(map[string]bool)
	for pq.Len() > 0 {
		current := heap.Pop(pq).(*State)
		if isSolved(current.board) {
			fmt.Println(len(current.moves))
			for _, move := range current.moves {
				fmt.Println(move)
			}
			return
		}

		for _, neighbor := range getNeighbors(current.emptyX, current.emptyY) {
			x, y := neighbor[0], neighbor[1]
			if x < 0 || x >= k || y < 0 || y >= k {
				continue
			}
			newBoard := moveTile(current.board, current.emptyX, current.emptyY, x, y)
			boardKey := fmt.Sprintf("%v", newBoard)

			if visited[boardKey] {
				continue
			}
			visited[boardKey] = true

			move := ""
			switch {
			case x == current.emptyX-1:
				move = "DOWN"
			case x == current.emptyX+1:
				move = "UP"
			case y == current.emptyY-1:
				move = "RIGHT"
			case y == current.emptyY+1:
				move = "LEFT"
			}

			nextState := &State{
				board:  newBoard,
				emptyX: x,
				emptyY: y,
				moves:  append(current.moves, move),
				g:      current.g + 1,
				h:      heuristic(newBoard),
			}
			heap.Push(pq, nextState)
		}
	}
}
