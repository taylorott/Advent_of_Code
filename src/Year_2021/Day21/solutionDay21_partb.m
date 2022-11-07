function solutionDay21_partb()

    p1 = 1;
    p2 = 3;
    
%     p1 = 4;
%     p2 = 8;

    dice_sum_possibilities = 3:9;
    dice_sum_counts = zeros(size(dice_sum_possibilities));
    
    for i = 1:3
        for j = 1:3
            for k = 1:3
                dice_sum_counts(i+j+k-2)=dice_sum_counts(i+j+k-2)+1;
            end
        end
    end
    
    [dice_sum_possibilities;dice_sum_counts];
    
    
    score_square_count_p1 = zeros(22,10,22); %(score+1,previous_square,turn+1)
    score_square_count_p2 = zeros(22,10,22); %(score+1,previous_square,turn+1)
    
    score_square_count_p1(1,p1,1) = 1;
    score_square_count_p2(1,p2,1) = 1;
    
    turn_number = 1;
    sub_21_score = 1;
    while sub_21_score
        sub_21_score = 0;
        for previous_square = 1:10
            for previous_score = 0:20
                for dice_index = 1:length(dice_sum_possibilities)
                    dice_roll_val = dice_sum_possibilities(dice_index);
                    dice_count = dice_sum_counts(dice_index);
                    
                    
                    next_square = mod(previous_square+dice_roll_val-1,10)+1;
                    next_score = min(previous_score+next_square,21);
                    
                    p1_count_increment = score_square_count_p1(previous_score+1,previous_square,turn_number)*dice_count;
                    score_square_count_p1(next_score+1,next_square,turn_number+1) = ...
                        score_square_count_p1(next_score+1,next_square,turn_number+1)+ p1_count_increment;
                        
                    p2_count_increment = score_square_count_p2(previous_score+1,previous_square,turn_number)*dice_count;    
                    score_square_count_p2(next_score+1,next_square,turn_number+1) = ...
                        score_square_count_p2(next_score+1,next_square,turn_number+1)+p2_count_increment;
                    
                    if next_score<21 && (p1_count_increment+p2_count_increment>0)
                        sub_21_score = 1;
                    end
                        
% 
% 
%                     score_square_count_p1(1 , next_square, turn_number+1)  
                end
            end
        end
        turn_number = turn_number+1;
    end
    
    final_turn_number = turn_number-1;
    
    score_turn_mat_p1 = zeros(22,final_turn_number+1); %(score+1,turn+1)
    score_turn_mat_p2 = zeros(22,final_turn_number+1); %(score+1,turn+1)
    
    for turn_number = 0:final_turn_number
        for score = 0:21
            score_turn_mat_p1(score+1,turn_number+1)  = sum(score_square_count_p1(score+1,:,turn_number+1));
            score_turn_mat_p2(score+1,turn_number+1)  = sum(score_square_count_p2(score+1,:,turn_number+1));
        end
    end
    
    
    format long g
    
    p1_reach21_mat = [sum(score_turn_mat_p1(1:21,:));score_turn_mat_p1(22,:)];
    p2_reach21_mat = [sum(score_turn_mat_p2(1:21,:));score_turn_mat_p2(22,:)];
    
    p1_world_count = sum(p1_reach21_mat(2,2:end).*p2_reach21_mat(1,1:(end-1)));
    p2_world_count = sum(p2_reach21_mat(2,:).*p1_reach21_mat(1,:));
    
    max(p1_world_count,p2_world_count)
end









% 
% 
% score1 = 0;
% score2 = 0;
% 
% triple_roll_mat = zeros(3,100);
% triple_roll_mat(1:300)=1:300;
% triple_roll_mat = mod(triple_roll_mat-1,100)+1;
% triple_roll_mat = sum(triple_roll_mat);
% 
% player1_triple_rolls = repmat(triple_roll_mat(1:2:(end-1)),[1,10]);
% player2_triple_rolls = repmat(triple_roll_mat(2:2:(end)),[1,10]);
% 
% player1_squares = mod(cumsum(player1_triple_rolls)+p1-1,10)+1;
% player1_scores = cumsum(player1_squares);
% 
% player2_squares = mod(cumsum(player2_triple_rolls)+p2-1,10)+1;
% player2_scores = cumsum(player2_squares);
% 
% 
% % [player1_scores(1:5)',player2_scores(1:5)']
% 
% 
% count = 1;
% while player1_scores(count)<1000 && player2_scores(count)<1000
%     count = count+1;
% end
% 
% if player1_scores(count)>=1000
% %     3*(2*count-1)
% %     player1_scores(count)
% %     player2_scores(count-1)
%     player2_scores(count-1)*3*(2*count-1)
% 
% else
% %     3*(2*count)
% %     player1_scores(count)
% %     player2_scores(count)
%     player1_scores(count)*3*(2*count)
% end
