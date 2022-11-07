function solutionDay24()

    %parse the input
    fid = fopen('InputDay25.txt');
    %extract text, splitting it by line
    data = textscan(fid,'%s','Delimiter','/');
    data = data{1};
    fclose(fid);

    %number of lines of text in the file
    file_length = length(data);
    
    num_inputs = 0;
    state_vec = [];
    for i = 1:file_length
        state_vec(end+1,:)=1*(data{i}=='v')+2*(data{i}=='>');
    end
    state_vec
    
    my_width = size(state_vec,2);
    my_height = size(state_vec,1);
    
    new_state_vec = state_vec;
    
    count = 0;
    at_rest = 0;
    while at_rest == 0
        at_rest = 1;
        count = count+1;
        for i = 1:my_height
            for j = 1:my_width
                if state_vec(i,j)==2
                    i_new = i;
                    j_new = mod(j,my_width)+1;
                    if state_vec(i_new,j_new)==0
                        new_state_vec(i_new,j_new)=state_vec(i,j);
                        new_state_vec(i,j)=0;
                        at_rest = 0;
                    end
                end
            end
        end
        state_vec = new_state_vec;

        for i = 1:my_height
            for j = 1:my_width
                if state_vec(i,j)==1
                    i_new = mod(i,my_height)+1;
                    j_new = j;
                    if state_vec(i_new,j_new)==0
                        new_state_vec(i_new,j_new)=state_vec(i,j);
                        new_state_vec(i,j)=0;
                        at_rest = 0;
                    end
                end
            end
        end
        state_vec = new_state_vec;
    end
    count
end