function res=submarine01()

fid = fopen('InputDay10.txt');
data = textscan(fid,'%s');
fclose(fid);

num_lines = length(data{1});

score_list = [];

for i = 1:num_lines
    my_string = data{1}{i};

    is_correct = 1;
    my_stack = [];
    my_index = 0;
    for j = 1:length(my_string)
        if my_string(j)=='{' || my_string(j)=='[' || my_string(j)=='(' || my_string(j)=='<'
            my_index = my_index+1;
            my_stack(my_index) = my_string(j);
        end
        
        if my_string(j)=='}' || my_string(j)==']' || my_string(j)==')' || my_string(j)=='>'
            if pair_char(my_string(j)) == my_stack(my_index)
                my_index = my_index-1;
            else
                is_correct = 0;
%                 score = score+score_val(my_string(j));
                break
            end
        end
        
    end
    
    if my_index>0 && is_correct==1
        temp_score = 0;
        while my_index>0
            temp_score = temp_score*5;
            temp_score = temp_score + score_val(my_stack(my_index));
            my_index = my_index - 1;
        end
        score_list(end+1) = temp_score;
    end
    
    
end

score_list = sort(score_list);

score_list(ceil(length(score_list)/2))
% length(score_list)
% ceil(length(score_list)/2)
% length(score_list)

% num_linesr
% q = importdata('InputDay10.dat');


end

function char_out =  pair_char(char_in)
    char_out = '';
    
    if char_in == '}'
       char_out = '{';
    end
       
    if char_in == ']'
       char_out = '[';
    end

    if char_in == ')'
       char_out = '(';
    end
    
    if char_in == '>'
       char_out = '<';
    end
    
    if char_in == '{'
       char_out = '}';
    end
       
    if char_in == '['
       char_out = ']';
    end

    if char_in == '('
       char_out = ')';
    end
    
    if char_in == '<'
       char_out = '>';
    end
end

function score =  score_val(char_in)
    score = 0;
    
    if char_in == '}'
       score = 1197;
    end
       
    if char_in == ']'
       score = 57;
    end

    if char_in == ')'
       score = 3;
    end
    
    if char_in == '>'
       score = 25137;
    end
    
    if char_in == '{'
       score = 3;
    end
       
    if char_in == '['
       score = 2;
    end

    if char_in == '('
       score = 1;
    end
    
    if char_in == '<'
       score = 4;
    end
end