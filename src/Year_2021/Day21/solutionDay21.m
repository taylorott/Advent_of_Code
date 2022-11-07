function solutionDay20()


p1 = 1;
p2 = 3;

% p1 = 4;
% p2 = 8;


score1 = 0;
score2 = 0;

triple_roll_mat = zeros(3,100);
triple_roll_mat(1:300)=1:300;
triple_roll_mat = mod(triple_roll_mat-1,100)+1;
triple_roll_mat = sum(triple_roll_mat);

player1_triple_rolls = repmat(triple_roll_mat(1:2:(end-1)),[1,10]);
player2_triple_rolls = repmat(triple_roll_mat(2:2:(end)),[1,10]);

player1_squares = mod(cumsum(player1_triple_rolls)+p1-1,10)+1;
player1_scores = cumsum(player1_squares);

player2_squares = mod(cumsum(player2_triple_rolls)+p2-1,10)+1;
player2_scores = cumsum(player2_squares);


% [player1_scores(1:5)',player2_scores(1:5)']


count = 1;
while player1_scores(count)<1000 && player2_scores(count)<1000
    count = count+1;
end

if player1_scores(count)>=1000
%     3*(2*count-1)
%     player1_scores(count)
%     player2_scores(count-1)
    player2_scores(count-1)*3*(2*count-1)

else
%     3*(2*count)
%     player1_scores(count)
%     player2_scores(count)
    player1_scores(count)*3*(2*count)
end

end


