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
    cost_to_go = inf(size(my_mat));
    cost_to_go(1,1) = 0;

    final_set_matrix = zeros(size(my_mat));

    neighbor_set_matrix = zeros(size(my_mat));
    neighbor_set_matrix(1,1) = 1;

    total_elements = my_height*my_width;
    my_priority_queue = zeros(total_elements,1);
    my_priority_queue(1)=1;
    num_elements = 1;

    priority_queue_index_list = zeros(total_elements,1);
    priority_queue_index_list(1) = 1;


    function element_out = pop()
        element_out = my_priority_queue(1);
        priority_queue_index_list(element_out)=0;
        
        my_priority_queue(1) = my_priority_queue(num_elements);
        priority_queue_index_list(my_priority_queue(1))=1;
        
        num_elements = num_elements -1;
        current_index = 1;
        while (current_index-1)*2+2 <= num_elements
            index_left = (current_index-1)*2+2;
            index_right = (current_index-1)*2+3;
            switch_index = -1;
            
            if index_right <= num_elements
                if cost_to_go(my_priority_queue(current_index))<cost_to_go(my_priority_queue(index_left))&&...
                   cost_to_go(my_priority_queue(current_index))<cost_to_go(my_priority_queue(index_right))
                    break
                else
                    if cost_to_go(my_priority_queue(index_left))<cost_to_go(my_priority_queue(index_right))
                        switch_index = index_left;
                    else
                        switch_index = index_right;
                    end
                end
            else
                if cost_to_go(my_priority_queue(current_index))<cost_to_go(my_priority_queue(index_left))
                    break
                else
                    switch_index = index_left;
                end
            end
            temp = my_priority_queue(switch_index);
            my_priority_queue(switch_index) = my_priority_queue(current_index);
            my_priority_queue(current_index) = temp;
            
            priority_queue_index_list(my_priority_queue(switch_index))=switch_index;
            priority_queue_index_list(my_priority_queue(current_index))=current_index;
            
            current_index = switch_index;
        end 
    end

    function push(element_in)
        num_elements = num_elements + 1;
        my_priority_queue(num_elements) = element_in;
        
        current_index  = num_elements;
        priority_queue_index_list(my_priority_queue(current_index))=current_index;
      
        while current_index>1 && cost_to_go(my_priority_queue(current_index))<cost_to_go(my_priority_queue(floor((current_index-2)/2)+1))
            temp = my_priority_queue(current_index);
            my_priority_queue(current_index) = my_priority_queue(floor((current_index-2)/2)+1);
            my_priority_queue(floor((current_index-2)/2)+1) = temp;
            
            priority_queue_index_list(my_priority_queue(current_index))=current_index;
            current_index = floor((current_index-2)/2)+1;
            priority_queue_index_list(my_priority_queue(current_index))=current_index;
            
        end
    end

    function sift_up(index_to_fix)
        current_index  = index_to_fix;
      
        while current_index>1 && cost_to_go(my_priority_queue(current_index))<cost_to_go(my_priority_queue(floor((current_index-2)/2)+1))
            temp = my_priority_queue(current_index);
            my_priority_queue(current_index) = my_priority_queue(floor((current_index-2)/2)+1);
            my_priority_queue(floor((current_index-2)/2)+1) = temp;
            
            priority_queue_index_list(my_priority_queue(current_index))=current_index;
            current_index = floor((current_index-2)/2)+1;
            priority_queue_index_list(my_priority_queue(current_index))=current_index;
        end
    end

    while num_elements>0
        my_index =  pop();
        final_set_matrix(my_index)=1;
        i = mod(my_index-1,my_height)+1;
        j = 1+(my_index-i)/my_height;

        update_list = [];
        if 1<i
            update_list(end+1) = (j-1)*my_height+(i-1);
        end

        if i<my_height
            update_list(end+1) = (j-1)*my_height+(i+1);
        end

        if 1<j
            update_list(end+1) = (j-2)*my_height+(i);
        end

        if j<my_width
            update_list(end+1) = (j)*my_height+(i);
        end


        for update_index = update_list
            if final_set_matrix(update_index)~=1
                cost_to_go(update_index)=min(my_mat(update_index)+cost_to_go(my_index),cost_to_go(update_index));
                if neighbor_set_matrix(update_index)==0
                    neighbor_set_matrix(update_index)=1;
                    push(update_index)
                else
                    sift_up(priority_queue_index_list(update_index));
                end
            end
        end
    end

    cost_to_go(end)
    toc
end

