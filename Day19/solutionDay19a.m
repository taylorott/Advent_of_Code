function solutionDay19a()
%parse the input
fid = fopen('InputDay19.txt');
data = textscan(fid,'%s','Delimiter','/');
fclose(fid);



num_input_lines = length(data{1});

scanner_coord_data = {};
num_scanners = 0;
input_line = 1;
coord_list = [];
num_coords = 0;
num_coords_list = [];
while input_line <=num_input_lines
    input_string = data{1}{input_line};
    if contains(input_string,'scanner')
        if num_scanners>0
            scanner_coord_data{num_scanners} = coord_list;
            num_coords_list(end+1) = num_coords;
        end
        num_scanners = num_scanners+1;
        coord_list = [];
        num_coords = 0;
    else
        if length(input_string)>2
            num_coords = num_coords+1;
            coord_string_list = strsplit(input_string,',');
            for i = 1:3
                coord_list(num_coords,i)=str2num(coord_string_list{i});
            end
        end
    end
    
    input_line = input_line+1;
end
num_coords_list(end+1) = num_coords;
scanner_coord_data{num_scanners} = coord_list;
distance_matrix_list = {};
for i = 1:num_scanners
     
    [distance_matrix,distance_list,vertex_index_list] = build_distance_matrix(scanner_coord_data{i});
    distance_matrix_list{i} = distance_matrix;
    distance_list_list{i} = distance_list;
    vertex_index_list_list{i} = vertex_index_list;
end

% distance_matrix_list{1}
% distance_list_list{1}


min_beacon_overlap = 12;
min_distance_list_overlap = min_beacon_overlap*(min_beacon_overlap-1)/2;

%note, they made it really easy for us in terms of resolving ambiguity in
%the problem input. my technique here exploits this

my_graph_indices_list = {};
my_graph_translations_list = {};
my_graph_rotations_list = {};

for i = 1:num_scanners
    my_graph_rotations = {};
    my_graph_translations = {};
    my_graph_indices = [];
    for j = 1:num_scanners
        if i~=j
            [num_overlap,index1_list,index2_list] = compute_list_overlap(distance_list_list{i},distance_list_list{j});
            if num_overlap>=min_distance_list_overlap
                reduced_index_list1 = reduce_sorted_list_of_repeat_elements(...
                sort([vertex_index_list_list{i}(1,index1_list),vertex_index_list_list{i}(2,index1_list)]));

                reduced_index_list2 = reduce_sorted_list_of_repeat_elements(...
                sort([vertex_index_list_list{j}(1,index2_list),vertex_index_list_list{j}(2,index2_list)]));

                reduced_distance_matrix1 = distance_matrix_list{i}(reduced_index_list1,reduced_index_list1);
                reduced_distance_matrix2 = distance_matrix_list{j}(reduced_index_list2,reduced_index_list2);

                sorted_reduced_distance_matrix1 = sort(reduced_distance_matrix1);
                sorted_reduced_distance_matrix2 = sort(reduced_distance_matrix2);

                matching_list = match_sorted_vectors(sorted_reduced_distance_matrix1,sorted_reduced_distance_matrix2);

                coord_set1 = scanner_coord_data{i}(reduced_index_list1,:);
                coord_set2 = scanner_coord_data{j}(reduced_index_list2(matching_list),:);

                my_rotation = round((diff(coord_set2)'*diff(coord_set1))/(diff(coord_set1)'*diff(coord_set1)));
                if det(my_rotation)>0
                    my_translation = my_rotation'*coord_set2'-coord_set1';
                    my_translation = my_translation(:,1);
                    
%                     coord_set2'-my_rotation*(coord_set1' + repmat(my_translation,[1,12]));
%                     (my_rotation'*coord_set2'-repmat(my_translation,[1,12]))-coord_set1'

                    my_graph_indices(end+1) = j;
                    my_graph_translations{end+1} = my_translation;
                    my_graph_rotations{end+1} = my_rotation;
                    
%                     my_graph_rotations{j,i} = my_rotation;
%                     my_graph_translation{j,i} = my_translation;
                end
            end
        else    
            my_graph_indices(end+1) = i;
            my_graph_translations{end+1} = zeros(3,1);
            my_graph_rotations{end+1} = eye(3);
        end
    end
    my_graph_indices_list{i} = my_graph_indices;
    my_graph_translations_list{i} = my_graph_translations;
    my_graph_rotations_list{i} = my_graph_rotations;
end

scanner_indices = my_graph_indices_list{1};
scanner_translations = my_graph_translations_list{1};
scanner_rotations = my_graph_rotations_list{1};

count1 = 1;
while length(scanner_indices)<num_scanners
    neighbor_vertex = scanner_indices(count1);
    translation1 = scanner_translations{count1};
    rotation1 = scanner_rotations{count1};
    reachable_vertices = my_graph_indices_list{neighbor_vertex};
    for i = 1:length(reachable_vertices)
        reachable_vertex = reachable_vertices(i);
        %if vertex has not been seen yet...
        if sum(reachable_vertex==scanner_indices) == 0
            translation2 = my_graph_translations_list{neighbor_vertex}{i};
            rotation2 = my_graph_rotations_list{neighbor_vertex}{i};
            
            scanner_indices(end+1) = reachable_vertex;
            scanner_rotations{end+1} = rotation2*rotation1;
            scanner_translations{end+1} = translation1+rotation1'*translation2;
        end
    end
    
    count1=count1+1;
end




beacon_list = [];

for i = 1:length(scanner_indices)
    scanner_index = scanner_indices(i);
    beacon_update_list = scanner_coord_data{scanner_index}';
    beacon_list = [beacon_list,scanner_rotations{i}'*beacon_update_list-repmat(scanner_translations{i},[1,num_coords_list(scanner_index)])];
end


beacon_list = coord_lexicographic_sort(beacon_list');
num_individual_beacons(beacon_list);

max_manhattan_distance = 0;
for i = 1:num_scanners
    for j = 1:num_scanners
        manhattan_distance = sum(abs(scanner_translations{i}-scanner_translations{j}));
        if manhattan_distance>max_manhattan_distance
            max_manhattan_distance=manhattan_distance;
        end
    end
end
max_manhattan_distance
 
end

function num_individual_beacons(coord_list)
    s=size(coord_list);
    count=1;
    for i = 2:s(1)
        if sum(coord_list(i,:)==coord_list(i-1,:))<3
            count = count+1;
        end
    end
    count
end

function coord_list = coord_lexicographic_sort(coord_list)
    s=size(coord_list);

    [~,sorted_index_list] = sort(coord_list(:,1));
    coord_list = coord_list(sorted_index_list,:);
    
    for j=2:3
        count1=1;
        count2=2;
        while count2<=s(1)
            if coord_list(count2,j-1)~=coord_list(count1,j-1)

                [~,sorted_index_list] = sort(coord_list(count1:(count2-1),j));
                coord_list(count1:(count2-1),:)=coord_list(count1-1+sorted_index_list,:);
                count1=count2;
            end
            count2=count2+1;
                
        end
        [~,sorted_index_list] = sort(coord_list(count1:(count2-1),j));
        coord_list(count1:(count2-1),:)=coord_list(count1-1+sorted_index_list,:);
        count1=count2;
    end
%     coord_list
end


function matching_list = match_sorted_vectors(sorted_reduced_distance_matrix1,sorted_reduced_distance_matrix2)
    s = size(sorted_reduced_distance_matrix1);
    matching_list = zeros(1,s(1));
    for i=1:s(1)
        for j=1:s(1)
            if sum((sorted_reduced_distance_matrix1(:,i)-sorted_reduced_distance_matrix2(:,j)).^2)==0
                matching_list(i)=j;
            end
        end
    end
end

function reduced_list = reduce_sorted_list_of_repeat_elements(sorted_list)
    reduced_list(1) = sorted_list(1);
    for i = 2:length(sorted_list)
        if reduced_list(end)~=sorted_list(i)
            reduced_list(end+1)=sorted_list(i);
        end
    end
end

function [num_shared_elements,index1_list,index2_list] = compute_list_overlap(list1,list2)

count1=1;
count2=1;

index1_list = [];
index2_list = [];

numel1 = length(list1);
numel2 = length(list2);

num_shared_elements = 0;

while count1<=numel1 && count2<=numel2
    v1 = list1(count1);
    v2 = list2(count2);
    
    if v1 == v2
        num_shared_elements = num_shared_elements+1;
        index1_list(end+1) = count1;
        index2_list(end+1) = count2;
        count1 = count1+1;
        count2 = count2+1;
    else
        if v1<v2
            count1 = count1+1;
        else
            count2 = count2+1;
        end
    end
end




end


function [distance_matrix,distance_list,vertex_index_list] = build_distance_matrix(coord_data)
    s = size(coord_data);
    num_coords = s(1);
    
    distance_matrix = zeros(num_coords,num_coords);
    distance_list = zeros(1,num_coords*(num_coords-1)/2);
    vertex_index_list = zeros(2,num_coords*(num_coords-1)/2);
    
    distance_index = 0;
    for i = 1:num_coords
        for j = 1:num_coords
            distance_squared = sum((coord_data(i,:)-coord_data(j,:)).^2);
            distance_matrix(i,j) = distance_squared;
            if i<j
                distance_index = distance_index+1;
                
                distance_list(distance_index)=distance_squared;
                vertex_index_list(1,distance_index)=i;
                vertex_index_list(2,distance_index)=j;
            end
        end
    end
    [distance_list,sorted_indices] = sort(distance_list);
    vertex_index_list = vertex_index_list(:,sorted_indices);
end