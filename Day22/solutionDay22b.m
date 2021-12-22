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
    
    prism_list_current = [];
    
    for i = 1:length(command_list)
        size(prism_list_current,1)
%         i/length(command_list)
        prism_list_new = [];
        
        prism_to_check = coord_vec(i,:);
        
        for j = 1:size(prism_list_current,1)
            prism_list_new = [prism_list_new;prism_difference(prism_list_current(j,:),prism_to_check)];
        end
        
        
        if command_list(i)==1
            prism_list_new(end+1,:) = prism_to_check;
        end
        
        prism_list_current = prism_list_new;
    end

    volume_sum = 0;
    for i = 1:size(prism_list_current,1)
        volume_sum = volume_sum+compute_prism_volue(prism_list_current(i,:));
    end

    sprintf('%16.f',volume_sum)


end

function prism_volume = compute_prism_volue(coord_vec)
    dx = coord_vec(2)-coord_vec(1)+1;
    dy = coord_vec(4)-coord_vec(3)+1;
    dz = coord_vec(6)-coord_vec(5)+1;
    prism_volume = dx*dy*dz;
end


function prisms_remaining = prism_difference(prism_plus,prism_minus)
    prisms_remaining = [];
    
    [shared_interval_x,plus_x_only] = detect_overlap(prism_plus(1),prism_plus(2),prism_minus(1),prism_minus(2));
    [shared_interval_y,plus_y_only] = detect_overlap(prism_plus(3),prism_plus(4),prism_minus(3),prism_minus(4));
    [shared_interval_z,plus_z_only] = detect_overlap(prism_plus(5),prism_plus(6),prism_minus(5),prism_minus(6));
    
    
    % x_only  , y_only  , z_only
    prisms_remaining = [prisms_remaining;prism_cartesian_product(plus_x_only,plus_y_only,plus_z_only)];
 
    % x_shared, y_only  , z_only
    prisms_remaining = [prisms_remaining;prism_cartesian_product(shared_interval_x,plus_y_only,plus_z_only)];
    % x_only  , y_shared, z_only
    prisms_remaining = [prisms_remaining;prism_cartesian_product(plus_x_only,shared_interval_y,plus_z_only)];
    % x_only  , y_only  , z_shared
    prisms_remaining = [prisms_remaining;prism_cartesian_product(plus_x_only,plus_y_only,shared_interval_z)];

    % x_only  , y_shared, z_shared
    prisms_remaining = [prisms_remaining;prism_cartesian_product(plus_x_only,shared_interval_y,shared_interval_z)];
    % x_shared, y_only  , z_shared
    prisms_remaining = [prisms_remaining;prism_cartesian_product(shared_interval_x,plus_y_only,shared_interval_z)];
    % x_shared, y_shared, z_only
    prisms_remaining = [prisms_remaining;prism_cartesian_product(shared_interval_x,shared_interval_y,plus_z_only)];
end

function prisms_out = prism_cartesian_product(x_regions,y_regions,z_regions)
    prisms_out = [];

    for i = 1:length(x_regions)
       for j = 1:length(y_regions) 
            for k = 1:length(z_regions)
                prisms_out = [prisms_out;[x_regions{i},y_regions{j},z_regions{k}]];
            end
       end
    end
end



function [shared_interval,region1_only_intervals] = detect_overlap(q1_min,q1_max,q2_min,q2_max)
    shared_interval = {};
    region1_only_intervals = {};

    if q1_min<=q2_max && q2_min<=q1_max

        if q1_min < q2_min
            region1_only_intervals{end+1} = [q1_min,q2_min-1];
        end
        
        if q1_max > q2_max
            region1_only_intervals{end+1} = [q2_max+1,q1_max];
        end
        
        shared_interval{1} = [max(q1_min,q2_min),min(q1_max,q2_max)];
    else
        region1_only_intervals{1} = [q1_min,q1_max];
    end

end





