function solutionDay22()

    %parse the input
    fid = fopen('InputDay22.txt');
    %extract text, splitting it by line
    data = textscan(fid,'%s','Delimiter','/');
    data = data{1};
    fclose(fid);

    %number of lines of text in the file
    file_length = length(data);
    
    for i = 1:file_length
        command_str_list = strsplit(data{i},' ');
        
        coord_str = command_str_list{2};
        coord_str = strrep(coord_str,'x=',' ');
        coord_str = strrep(coord_str,'y=',' ');
        coord_str = strrep(coord_str,'z=',' ');
        coord_str = strrep(coord_str,'..',' ');
        coord_str = strrep(coord_str,',',' ');
        coord_vec(i,:) = str2num(coord_str);

        
        command_list(i) = contains(command_str_list{1},'on');

        
    end
    
    interval_mat_x = generate_intervals(coord_vec(:,1)',coord_vec(:,2)');
    interval_mat_y = generate_intervals(coord_vec(:,3)',coord_vec(:,4)');
    interval_mat_z = generate_intervals(coord_vec(:,5)',coord_vec(:,6)');
    
    
    my_grid = zeros(size(interval_mat_x,2),size(interval_mat_y,2),size(interval_mat_z,2));
    
    function index_x = bin_search_x_interval(key_value)
        index1 = 1;
        index2 = size(interval_mat_x,2);
        while index2-index1>1
            index3 = round((index2+index1)/2);
            if key_value<interval_mat_x(1,index3)
                index2=index3;
            end
            if interval_mat_x(2,index3)<key_value
                index1=index3;
            end
            if interval_mat_x(1,index3)<=key_value && key_value <=interval_mat_x(2,index3)
                index1=index3;
                index2=index3;
            end
        end
        if interval_mat_x(1,index1)<=key_value && key_value <=interval_mat_x(2,index1)
            index_x = index1;
        end 
        if interval_mat_x(1,index2)<=key_value && key_value <=interval_mat_x(2,index2)
            index_x = index2;
        end 
    end
    function index_y = bin_search_y_interval(key_value)
        index1 = 1;
        index2 = size(interval_mat_y,2);
        while index2-index1>1
            index3 = round((index2+index1)/2);
            if key_value<interval_mat_y(1,index3)
                index2=index3;
            end
            if interval_mat_y(2,index3)<key_value
                index1=index3;
            end
            if interval_mat_y(1,index3)<=key_value && key_value <=interval_mat_y(2,index3)
                index1=index3;
                index2=index3;
            end
        end
        if interval_mat_y(1,index1)<=key_value && key_value <=interval_mat_y(2,index1)
            index_y = index1;
        end 
        if interval_mat_y(1,index2)<=key_value && key_value <=interval_mat_y(2,index2)
            index_y = index2;
        end 
    end
    function index_z = bin_search_z_interval(key_value)
        index1 = 1;
        index2 = size(interval_mat_z,2);
        while index2-index1>1
            index3 = round((index2+index1)/2);
            if key_value<interval_mat_z(1,index3)
                index2=index3;
            end
            if interval_mat_z(2,index3)<key_value
                index1=index3;
            end
            if interval_mat_z(1,index3)<=key_value && key_value <=interval_mat_z(2,index3)
                index1=index3;
                index2=index3;
            end
        end
        if interval_mat_z(1,index1)<=key_value && key_value <=interval_mat_z(2,index1)
            index_z = index1;
        end 
        if interval_mat_z(1,index2)<=key_value && key_value <=interval_mat_z(2,index2)
            index_z = index2;
        end 
    end
    

    for i = 1:file_length
        xmin_index = bin_search_x_interval(coord_vec(i,1));
        xmax_index = bin_search_x_interval(coord_vec(i,2));
        ymin_index = bin_search_y_interval(coord_vec(i,3));
        ymax_index = bin_search_y_interval(coord_vec(i,4));
        zmin_index = bin_search_z_interval(coord_vec(i,5));
        zmax_index = bin_search_z_interval(coord_vec(i,6));

        my_grid(xmin_index:xmax_index,ymin_index:ymax_index,zmin_index:zmax_index)=command_list(i);
    end

    my_width_x = interval_mat_x(2,:)-interval_mat_x(1,:)+1;
    my_width_y = interval_mat_y(2,:)-interval_mat_y(1,:)+1;
    my_width_z = interval_mat_z(2,:)-interval_mat_z(1,:)+1;
    

    total_volume = 0;
    
    for i = 1:size(my_grid,1)
        for j = 1:size(my_grid,2)
            for k = 1:size(my_grid,3)
                total_volume = total_volume+my_grid(i,j,k)*my_width_x(i)*my_width_y(j)*my_width_z(k);
            end
        end
    end
    
    sprintf('%16.f',total_volume)



end




function interval_mat = generate_intervals(min_coord_list,max_coord_list)
    min_coord_list = unique(min_coord_list);
    max_coord_list = unique(max_coord_list);
    
    
    min_coord_list2 = unique([min_coord_list,max_coord_list+1]);
    max_coord_list2 = unique([max_coord_list,min_coord_list-1]);
    

    my_coord_array = sort([min_coord_list2,max_coord_list2]);
    my_coord_array = my_coord_array(2:(end-1));
   	interval_mat = [my_coord_array(1:2:(end-1));my_coord_array(2:2:end)];
    

end






