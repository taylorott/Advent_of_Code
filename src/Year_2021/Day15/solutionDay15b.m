function res=submarine01()
    tic
    fid = fopen('InputDay15.txt');
    data = textscan(fid,'%s');
    fclose(fid);

    my_height = length(data{1});
    my_width = length(data{1}{1});

    my_mat=[];
    for i =1:my_height
        my_str = data{1}{i};
        for j = 1:length(my_str)
            my_mat(i,j) = str2num(my_str(j));
        end
    end

    my_height = my_height*5;
    my_width = my_width*5;

    my_mat_base = my_mat;

    for i = 1:4
        my_mat = [my_mat,my_mat_base+i];
    end

    my_mat_base = my_mat;
    for i = 1:4
        my_mat = [my_mat;my_mat_base+i];
    end

    my_mat = mod(my_mat-1,9)+1;
    cost_to_go = zeros(size(my_mat));

    cost_to_go(:,1) = cumsum(my_mat(:,1))-my_mat(1,1);
    cost_to_go(1,:) = cumsum(my_mat(1,:))-my_mat(1,1);


    for i = 2:my_height
        for j = 2:my_width
            cost_to_go(i,j)=my_mat(i,j)+ min(cost_to_go(i-1,j),cost_to_go(i,j-1));
        end
    end

    num_updates = 1;

    while num_updates>0

        num_updates = 0;
        for i = 1:my_height
            for j = 1:my_width
                term_list = [];
                if i>1 
                    term_list(end+1) = cost_to_go(i-1,j);
                end

                if i<my_height 
                    term_list(end+1) = cost_to_go(i+1,j);
                end

                if j>1 
                    term_list(end+1) = cost_to_go(i,j-1);
                end

                if j<my_width 
                    term_list(end+1) = cost_to_go(i,j+1);
                end

                if i~=1 || j~=1
                    new_cost_to_go_val = my_mat(i,j)+ min(term_list);
                    if new_cost_to_go_val~=cost_to_go(i,j)
                        cost_to_go(i,j)=new_cost_to_go_val;
    %                     updated_list(end+1,:) = [i,j];
                        num_updates = num_updates+1;
                    end
                end
            end 
        end

    %     num_updates
    end
    cost_to_go(end,end)
    toc
end

