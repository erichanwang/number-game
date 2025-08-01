#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <algorithm>

using namespace std;

// Structure to represent the state of the board
struct State {
    vector<vector<int>> board;
    int x, y; // position of the empty cell (0)
    string path; // path taken to get to this state
};

// Directions for moving the empty cell
const vector<pair<int, int>> directions = {
    {1, 0}, // DOWN
    {0, 1}, // RIGHT
    {-1, 0}, // UP
    {0, -1}  // LEFT
};

// Function to serialize the board state for the unordered_set
string serialize(const vector<vector<int>>& board) {
    string s;
    for (const auto& row : board) {
        for (int num : row) {
            s += to_string(num) + ",";
        }
    }
    return s;
}

// Function to check if the board is solved
bool isSolved(const vector<vector<int>>& board) {
    int k = board.size();
    int count = 0;
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < k; j++) {
            if (i == k - 1 && j == k - 1) {
                return board[i][j] == 0; // last cell should be zero
            }
            if (board[i][j] != count++) {
                return false;
            }
        }
    }
    return true;
}

// Function to solve the N-Puzzle using BFS
int solveNPuzzle(vector<vector<int>>& board) {
    int k = board.size();
    // Find the position of the empty space (0)
    int x, y;
    for (int i = 0; i < k; i++) {
        for (int j = 0; j < k; j++) {
            if (board[i][j] == 0) {
                x = i; y = j;
                break;
            }
        }
    }

    queue<State> q;
    unordered_set<string> visited;

    // Start BFS
    q.push({board, x, y, ""});
    visited.insert(serialize(board));

    while (!q.empty()) {
        State current = q.front();
        q.pop();

        if (isSolved(current.board)) {
            cout << current.path.size() << endl; // Number of moves
            for (char move : current.path) {
                if (move == 'U') cout << "UP" << endl;
                else if (move == 'D') cout << "DOWN" << endl;
                else if (move == 'L') cout << "LEFT" << endl;
                else if (move == 'R') cout << "RIGHT" << endl;
            }
            return true; // Puzzle solved
        }

        // Try all four possible moves
        for (int i = 0; i < 4; i++) {
            int newX = current.x + directions[i].first;
            int newY = current.y + directions[i].second;

            if (newX >= 0 && newX < k && newY >= 0 && newY < k) {
                // Make the move
                swap(current.board[current.x][current.y], current.board[newX][newY]);
                string newState = serialize(current.board);

                if (!visited.count(newState)) {
                    visited.insert(newState);
                    State nextState = {current.board, newX, newY, current.path + (i == 0 ? 'D' : i == 1 ? 'R' : i == 2 ? 'U' : 'L')}; // Move direction
                    q.push(nextState);
                }

                // Undo the move
                swap(current.board[current.x][current.y], current.board[newX][newY]);
            }
        }
    }
    return false; // Puzzle not solvable
}

int main() {
    int k;
    cin >> k;
    vector<vector<int>> board(k, vector<int>(k));
    for (int i = 0; i < k * k; i++) {
        cin >> board[i / k][i % k];
    }
    
    solveNPuzzle(board);
    return 0;
}
