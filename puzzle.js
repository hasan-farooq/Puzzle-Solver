

var w, h;
var rows = 3;
var cols = 3;
var start = [[' ', '1', '3'], ['4', '2', '5'], ['7', '8', '6']];
var goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']];
// var start = [['1', '2', '3'], ['4', '5', '6'], ['7', ' ', '8']];

function puzzle_box(state,parent = null, move = null) {
    this.state = state;
    this.parent = parent;
    this.move = move;
}


function show(puzzle,color,x,y) {
    // createCanvas(600,600);
    textSize(60);
    x_diff = x;
    y_diff = y;
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            noFill()
            rect(x_diff + 2, y_diff + 2, 75, 56);
            fill(color);
            text(puzzle[i][j], 20 + x_diff, 5 + y_diff, 20 + x_diff, 60);
            x_diff = x_diff + 60
        }
        x_diff = x;
        y_diff = y_diff + 60
    }
}

function copy_puzzle(puzzle) {
    temp = [['', '', ''], ['', '', ''], ['', '', '']];

    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            temp[i][j] = puzzle[i][j];
        }
    }
    return temp;
}

function is_goal(puzzle) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            if (!(puzzle[i][j] == goal[i][j])) {
                return false
            }
        }
    }
    return true
}

function is_out_of_boundary(row, col) {
    if (row > 2 || col > 2 || row < 0 || col < 0) {
        return true
    }
    else {
        return false
    }
}


function is_left(puzzle) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            if (puzzle[i][j] == ' ' && (!is_out_of_boundary(i, j + 1))) {
                temp = copy_puzzle(puzzle);
                temp[i][j] = puzzle[i][j + 1];
                temp[i][j + 1] = ' ';
                return temp;
            }
        }
    }
    return false
}

function is_right(puzzle) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            if (puzzle[i][j] == ' ' && (!is_out_of_boundary(i, j - 1))) {
                temp = copy_puzzle(puzzle);
                temp[i][j] = puzzle[i][j - 1];
                temp[i][j - 1] = ' ';
                return temp;
            }
        }
    }
    return false
}

function is_up(puzzle) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            if (puzzle[i][j] == ' ' && (!is_out_of_boundary(i + 1, j))) {
                temp = copy_puzzle(puzzle);
                temp[i][j] = puzzle[i+1][j];
                temp[i+1][j] = ' ';
                return temp;
            }
        }
    }
    return false
}

function is_down(puzzle) {
    for (var i = 0; i < rows; i++) {
        for (var j = 0; j < cols; j++) {
            if (puzzle[i][j] == ' ' && (!is_out_of_boundary(i - 1, j))) {
                temp = copy_puzzle(puzzle);
                temp[i][j] = puzzle[i-1][j];
                temp[i-1][j] = ' ';
                return temp;
            }
        }
    }
    return false;
}

function track_path(puzzle){
    var moves = [];
    var current = puzzle;
    var parent = current.parent;

    while(parent != 'Root'){
        moves.push(current.move);
        current = parent;
        parent = current.parent;
    }
    return (moves.reverse())
}


function BFS(puzzle) {
    queue = [];
    queue.push(puzzle);
    while (true) {
        parent = queue.pop();
        current = parent.state;
        // console.log('Current State',current);
        // show(current,'red',250,50);
        if (is_goal(current)) {
            console.log('Solved !!!');
            show(current,'red',350,50);
            return parent;
        }
        else {
            temp = is_left(current);
            if(temp != false){
                queue.unshift(new puzzle_box(temp,parent,'Left'));
                // console.log('Left');
            }
            temp = is_right(current);
            if(temp != false){
                queue.unshift(new puzzle_box(temp,parent,'Right'));
                // console.log('Right');
            }
            temp = is_up(current);
            if(temp != false){
                queue.unshift(new puzzle_box(temp,parent,'Up'));
                // console.log('Up');
            }
            temp = is_down(current);
            if(temp != false){
                queue.unshift(new puzzle_box(temp,parent,'Down'));
                // console.log('Down');
            }
        }
    }


}


function setup() {
    createCanvas(600, 600);
    w = width / cols;
    h = height / rows;
    // noFill()
    // background(color('green'))

    initialize = new puzzle_box(start,'Root')

    show(start,'black',100,50);

    // is_goal(start);

    result = BFS(initialize);
    moves = track_path(result);

    console.log('Moves : ', moves);         // prints moves for the puzzle

}

function draw() {

}




